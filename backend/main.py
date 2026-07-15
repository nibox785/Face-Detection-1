import os
import sys
import io
import base64
import time
import numpy as np
import cv2
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Add backend directory to sys.path so inner imports work
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from .models.face_detector import RetinaFaceDetector
from .models.face_segmenter import UNetFaceSegmenter
from .quality.face_quality import analyze_face_quality
from .utils.reporting import save_detection_report, sanitize_name, DEFAULT_REPORT_ROOT
from .app_logging import log_inference_event, generate_request_id

app = FastAPI(title="AI Crowd Face Surveillance API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .utils.tracker import FaceTracker

# Cache detectors, segmenter and tracker
detectors = {}
segmenter = None
tracker = FaceTracker(unet_interval=6)

def get_detector(network_name: str):
    if network_name not in detectors:
        detectors[network_name] = RetinaFaceDetector(network_name=network_name)
    return detectors[network_name]

def get_segmenter():
    global segmenter
    if segmenter is None:
        segmenter = UNetFaceSegmenter()
    return segmenter

def rle_encode(mask):
    flat = (mask > 0).astype(np.uint8).flatten()
    changes = np.diff(flat)
    idxs = np.where(changes != 0)[0] + 1
    idxs = np.concatenate(([0], idxs, [len(flat)]))
    runs = np.diff(idxs)
    return {
        'size': list(mask.shape),
        'counts': runs.tolist(),
        'start_val': int(flat[0])
    }

def segment_face(img_raw, box, landmarks):
    h, w = img_raw.shape[:2]
    x1, y1, x2, y2 = map(int, box[:4])
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)
    
    rect_w = x2 - x1
    rect_h = y2 - y1
    
    binary_mask = np.zeros((h, w), dtype=np.uint8)
    
    if rect_w * rect_h < 400 or rect_w <= 4 or rect_h <= 4:
        center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        axes = (int(rect_w / 2), int(rect_h / 2))
        cv2.ellipse(binary_mask, center, axes, 0, 0, 360, 255, -1)
    else:
        try:
            face_crop = img_raw[y1:y2, x1:x2]
            seg = get_segmenter()
            crop_mask = seg.predict(face_crop)
            binary_mask[y1:y2, x1:x2] = crop_mask
        except Exception as e:
            print("U-Net segmentation failed, falling back to ellipse:", e)
            center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
            axes = (int(rect_w / 2), int(rect_h / 2))
            cv2.ellipse(binary_mask, center, axes, 0, 0, 360, 255, -1)
            
    pad = min(15, int(max(rect_w, rect_h) * 0.1))
    px1 = max(0, x1 - pad)
    py1 = max(0, y1 - pad)
    px2 = min(w, x2 + pad)
    py2 = min(h, y2 + pad)
    
    crop_w = px2 - px1
    crop_h = py2 - py1
    
    if crop_w > 0 and crop_h > 0:
        face_crop = img_raw[py1:py2, px1:px2]
        mask_crop = binary_mask[py1:py2, px1:px2]
        mask_crop_soft = cv2.GaussianBlur(mask_crop, (5, 5), 0)
        
        b_ch, g_ch, r_ch = cv2.split(face_crop)
        rgba_crop = cv2.merge([b_ch, g_ch, r_ch, mask_crop_soft])
        
        _, png_buffer = cv2.imencode('.png', rgba_crop)
        png_base64 = base64.b64encode(png_buffer).decode('utf-8')
        face_png_alpha = f"data:image/png;base64,{png_base64}"
    else:
        face_png_alpha = ""
        
    return binary_mask, face_png_alpha

@app.get("/", response_class=HTMLResponse)
def get_index():
    index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/index.html"))
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Giao diện Frontend không tìm thấy.")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/detect")
async def detect(
    image: UploadFile = File(...),
    network: str = Form("mobile0.25"),
    threshold: float = Form(0.6),
    draw_mask: bool = Form(False),
    upscale: bool = Form(False),
    save_report: bool = Form(False),
    report_name: str = Form(None),
    min_face_px: int = Form(36),
    background_tasks: BackgroundTasks = None,
):
    try:
        contents = await image.read()
        request_id = generate_request_id()
        nparr = np.frombuffer(contents, np.uint8)
        img_raw = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_raw is None:
            raise HTTPException(status_code=400, detail="File ảnh không hợp lệ")
            
        t_start = time.time()
        
        # Determine if we need to run the heavy face detector on this frame
        if tracker.needs_detector_run():
            detector = get_detector(network)
            faces_list = detector.detect(img_raw, confidence_threshold=threshold, upscale=upscale)
        else:
            faces_list = None
        
        h, w = img_raw.shape[:2]
        
        # 1. Update the tracker with detections
        segmenter = get_segmenter()
        tracked_faces = tracker.update(
            detected_faces=faces_list,
            img_raw=img_raw,
            draw_mask=draw_mask,
            segmenter=segmenter,
            threshold=threshold,
            min_face_px=min_face_px
        )
        
        # 2. Draw annotations and assemble payload
        annotated_img = img_raw.copy()
        overlay_color = [246, 92, 139] # BGR purple (139, 92, 246)
        
        faces_data = []
        face_count = len(tracked_faces)
        
        for face in tracked_faces:
            box_coords = face['box']
            confidence = face['confidence']
            landmarks_coords = face['landmarks']
            binary_mask = face['binary_mask']
            face_png_alpha = face['face_png_alpha']
            track_id = face['id']
            
            # Quality assessment
            q_results = analyze_face_quality(box_coords, confidence, landmarks_coords, binary_mask)
            mask_rle = rle_encode(binary_mask)
            
            # Draw mask overlay
            if draw_mask:
                idx_pts = (binary_mask > 0)
                if np.any(idx_pts):
                    mask_color_img = np.zeros_like(annotated_img)
                    mask_color_img[idx_pts] = overlay_color
                    cv2.addWeighted(annotated_img, 0.7, mask_color_img, 0.3, 0, dst=annotated_img)
                    
            # Draw bounding box and landmarks
            box_ints = list(map(int, box_coords))
            cv2.rectangle(annotated_img, (box_ints[0], box_ints[1]), (box_ints[2], box_ints[3]), (0, 255, 0), 2)
            
            # Label box
            text = f"ID:{track_id} {confidence:.2f}"
            cx = box_ints[0]
            cy = box_ints[1] - 5 if box_ints[1] - 5 > 15 else box_ints[1] + 15
            label_size, base_line = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.4, 1)
            cv2.rectangle(annotated_img, (box_ints[0], cy - label_size[1] - 2), (box_ints[0] + label_size[0], cy + base_line - 2), (0, 255, 0), cv2.FILLED)
            cv2.putText(annotated_img, text, (box_ints[0], cy),
                        cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
            
            # Draw 5 landmarks
            for j in range(5):
                cv2.circle(annotated_img, (int(landmarks_coords[2*j]), int(landmarks_coords[2*j+1])), 3, (0, 0, 255), -1)
                
            faces_data.append({
                'id': track_id,
                'box': box_coords,
                'confidence': confidence,
                'landmarks': landmarks_coords,
                'mask_rle': mask_rle,
                'face_png_alpha': face_png_alpha,
                'visibility': q_results['visibility'],
                'quality_score': q_results['quality_score'],
                'pose': q_results['pose'],
                'status': q_results['status'],
                'rating': q_results['rating']
            })
            
        t_latency = int((time.time() - t_start) * 1000)
        fps = round(1000.0 / max(t_latency, 1), 2)
        
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        payload = {
            'image': f"data:image/jpeg;base64,{img_base64}",
            'face_count': face_count,
            'faces': faces_data,
            'latency_ms': t_latency,
            'fps': fps,
            'request_id': request_id,
            'network': network,
            'status': 'ok'
        }

        if save_report:
            report_dir_name = sanitize_name(report_name or image.filename)
            report_dir = DEFAULT_REPORT_ROOT / report_dir_name
            
            if background_tasks is not None:
                background_tasks.add_task(
                    save_detection_report,
                    image_input=contents,
                    payload=payload.copy(),
                    annotated_image=annotated_img.copy() if annotated_img is not None else None,
                    report_name=report_dir_name
                )
            else:
                save_detection_report(
                    image_input=contents,
                    payload=payload,
                    annotated_image=annotated_img,
                    report_name=report_dir_name
                )
                
            payload['report_dir'] = str(report_dir)
            payload['report_url'] = f"/reports/inference/{report_dir.name}"

        log_inference_event(
            "detect_completed",
            request_id,
            network,
            "pipeline",
            face_count,
            t_latency,
            extra={
                "threshold": threshold,
                "draw_mask": draw_mask,
                "upscale": upscale,
                "save_report": bool(save_report),
            }
        )

        return payload
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files under /static
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    # Disable Uvicorn's HTTP access logs by default to prevent flooding the terminal
    access_log = os.getenv("ACCESS_LOG", "False").lower() == "true"
    
    uvicorn.run(app, host=host, port=port, access_log=access_log)
