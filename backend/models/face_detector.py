import os
import cv2
import numpy as np
import torch
import onnxruntime as ort

from ..data.config import cfg_mnet, cfg_re50
from ..layers.functions.prior_box import PriorBox
from ..utils.box_utils import decode, decode_landm
from ..utils.nms.py_cpu_nms import py_cpu_nms

class RetinaFaceDetector:
    def __init__(self, network_name="mobile0.25", weights_dir=None):
        self.network_name = network_name
        if weights_dir is None:
            weights_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../weights"))
            
        if network_name == "mobile0.25":
            self.cfg = cfg_mnet
            self.weights_path = os.path.join(weights_dir, "mobilenet0.25_Final.onnx")
        else:
            self.cfg = cfg_re50
            self.weights_path = os.path.join(weights_dir, "Resnet50_Final.onnx")
            
        print(f"Loading RetinaFace ONNX model from {self.weights_path}...")
        opts = ort.SessionOptions()
        intra_threads = int(os.environ.get("ONNX_INTRA_OP_THREADS", "0"))
        opts.intra_op_num_threads = intra_threads
        opts.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = ort.InferenceSession(self.weights_path, sess_options=opts, providers=ort.get_available_providers())
        print("RetinaFace ONNX model loaded successfully.")
        # PriorBox and scale cache for speed optimization
        self.cached_size = None
        self.cached_priors_np = None
        self.cached_scale_np = None
        self.cached_scale1_np = None

    def detect(self, img_raw, confidence_threshold=0.5, nms_threshold=0.4, upscale=False):
        im_height, im_width, _ = img_raw.shape
        # Crowd detection optimization: upscale image if it's small and upscale=True to detect tiny/distant faces
        target_width = 1280
        scale_factor = 1.0
        if upscale and im_width < target_width:
            scale_factor = target_width / im_width
            new_width = int(im_width * scale_factor)
            new_height = int(im_height * scale_factor)
            img_processed = cv2.resize(img_raw, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        else:
            img_processed = img_raw
            
        proc_height, proc_width, _ = img_processed.shape
        
        # Preprocessing
        img = np.float32(img_processed)
        img -= (104, 117, 123)
        img = img.transpose(2, 0, 1)
        img = np.expand_dims(img, axis=0) # shape (1, 3, H, W)
        
        # Run ONNX inference
        input_name = self.session.get_inputs()[0].name
        loc, conf, landms = self.session.run(None, {input_name: img})
        
        # Check cached priors and scale factors
        if self.cached_size == (proc_height, proc_width):
            priors_np = self.cached_priors_np
            scale_np = self.cached_scale_np
            scale1_np = self.cached_scale1_np
        else:
            priorbox = PriorBox(self.cfg, image_size=(proc_height, proc_width))
            priors = priorbox.forward()
            priors_np = priors.data.cpu().numpy()
            scale_np = np.array([proc_width, proc_height, proc_width, proc_height], dtype=np.float32)
            scale1_np = np.array([proc_width, proc_height, proc_width, proc_height,
                                  proc_width, proc_height, proc_width, proc_height,
                                  proc_width, proc_height], dtype=np.float32)
            self.cached_size = (proc_height, proc_width)
            self.cached_priors_np = priors_np
            self.cached_scale_np = scale_np
            self.cached_scale1_np = scale1_np
            
        loc_np = loc.squeeze(0)
        conf_np = conf.squeeze(0)
        landms_np = landms.squeeze(0)
        
        # Decode boxes in NumPy
        variance = self.cfg['variance']
        boxes = np.concatenate((
            priors_np[:, :2] + loc_np[:, :2] * variance[0] * priors_np[:, 2:],
            priors_np[:, 2:] * np.exp(loc_np[:, 2:] * variance[1])
        ), axis=1)
        boxes[:, :2] -= boxes[:, 2:] / 2
        boxes[:, 2:] += boxes[:, :2]
        
        # Scale back to original resolution
        boxes = (boxes * scale_np) / scale_factor
        
        # Decode scores
        scores = conf_np[:, 1]
        
        # Decode landmarks in NumPy
        landms_decoded = np.concatenate((
            priors_np[:, :2] + landms_np[:, :2] * variance[0] * priors_np[:, 2:],
            priors_np[:, :2] + landms_np[:, 2:4] * variance[0] * priors_np[:, 2:],
            priors_np[:, :2] + landms_np[:, 4:6] * variance[0] * priors_np[:, 2:],
            priors_np[:, :2] + landms_np[:, 6:8] * variance[0] * priors_np[:, 2:],
            priors_np[:, :2] + landms_np[:, 8:10] * variance[0] * priors_np[:, 2:]
        ), axis=1)
        landms_decoded = (landms_decoded * scale1_np) / scale_factor
        
        # Filter low scores
        inds = np.where(scores > confidence_threshold)[0]
        boxes = boxes[inds]
        landms = landms_decoded[inds]
        scores = scores[inds]
        
        # Keep top-K before NMS
        top_k = 5000
        order = scores.argsort()[::-1][:top_k]
        boxes = boxes[order]
        landms = landms[order]
        scores = scores[order]
        
        # Do NMS
        dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
        keep = py_cpu_nms(dets, nms_threshold)
        dets = dets[keep, :]
        landms = landms[keep]
        
        # Keep top-K after NMS
        keep_top_k = 750
        dets = dets[:keep_top_k, :]
        landms = landms[:keep_top_k, :]
        
        # Format outputs as a list of bounding boxes and landmarks
        faces = []
        for i, b in enumerate(dets):
            confidence = float(b[4])
            if confidence < confidence_threshold:
                continue
            box_coords = [float(b[0]), float(b[1]), float(b[2]), float(b[3])]
            landmarks_coords = [float(landms[i][j]) for j in range(10)]
            faces.append({
                'box': box_coords,
                'confidence': confidence,
                'landmarks': landmarks_coords
            })
            
        return faces
