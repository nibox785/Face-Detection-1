"""
FaceTracker - SORT-like IoU Hungarian Algorithm Tracker
========================================================
Improvements over the previous greedy Euclidean distance tracker:
  1. Geometric filter (is_valid_face_box): rejects background FP with bad aspect ratio / too small
  2. IoU cost matrix computed on velocity-predicted box positions
  3. Hungarian optimal assignment (scipy.optimize.linear_sum_assignment) replaces greedy nearest-neighbor
  4. Hit-streak gate: tentative tracks are only confirmed after N_HIT_CONFIRM=2 consecutive detections
  5. Eviction based on last_match_time (not last_seen) to avoid ghost/stuck boxes
"""

import time
import numpy as np
import cv2
import base64
import os
from scipy.optimize import linear_sum_assignment

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────
N_HIT_CONFIRM   = 2       # Consecutive detections before a track is shown
MAX_MISS_SECS   = 1.0     # Seconds without a detector match before eviction
MIN_IOU_MATCH   = 0.10    # Minimum IoU to accept a Hungarian assignment
MIN_FACE_PX     = 36      # Minimum face side length in pixels (geometric filter)
MAX_ASPECT_RATIO = 2.5    # Max w/h or h/w allowed (geometric filter)


# ─────────────────────────────────────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────────────────────────────────────

def generate_face_thumbnail(img_raw, bbox, crop_mask=None):
    """Generate a base64-encoded face thumbnail (PNG with alpha or JPEG)."""
    h, w = img_raw.shape[:2]
    tx1, ty1, tx2, ty2 = map(int, bbox[:4])
    tw, th = tx2 - tx1, ty2 - ty1
    pad = min(15, int(max(tw, th) * 0.1))
    px1 = max(0, tx1 - pad)
    py1 = max(0, ty1 - pad)
    px2 = min(w, tx2 + pad)
    py2 = min(h, ty2 + pad)

    crop_w, crop_h = px2 - px1, py2 - py1
    if crop_w <= 0 or crop_h <= 0:
        return ""

    face_crop_region = img_raw[py1:py2, px1:px2]

    if crop_mask is not None:
        full_mask = np.zeros((h, w), dtype=np.uint8)
        mh, mw = crop_mask.shape[:2]
        if mh != (ty2 - ty1) or mw != (tx2 - tx1):
            try:
                crop_mask = cv2.resize(crop_mask, (tx2 - tx1, ty2 - ty1), interpolation=cv2.INTER_NEAREST)
            except Exception:
                pass
        full_mask[ty1:ty2, tx1:tx2] = crop_mask
        mask_crop = full_mask[py1:py2, px1:px2]
        mask_crop_soft = cv2.GaussianBlur(mask_crop, (5, 5), 0)
        b_ch, g_ch, r_ch = cv2.split(face_crop_region)
        rgba_crop = cv2.merge([b_ch, g_ch, r_ch, mask_crop_soft])
        _, png_buffer = cv2.imencode('.png', rgba_crop)
        png_base64 = base64.b64encode(png_buffer).decode('utf-8')
        return f"data:image/png;base64,{png_base64}"
    else:
        _, jpg_buffer = cv2.imencode('.jpg', face_crop_region, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        jpg_base64 = base64.b64encode(jpg_buffer).decode('utf-8')
        return f"data:image/jpeg;base64,{jpg_base64}"


def is_valid_face_box(box, min_px=MIN_FACE_PX, max_aspect=MAX_ASPECT_RATIO):
    """
    Geometric sanity check: reject detections that cannot be a human face.
    - Too small (ventilation holes, distant objects)
    - Bad aspect ratio (wide signs, tall narrow objects)
    """
    x1, y1, x2, y2 = box[:4]
    bw = x2 - x1
    bh = y2 - y1
    if bw < min_px or bh < min_px:
        return False
    aspect = bw / max(bh, 1.0)
    if aspect > max_aspect or aspect < (1.0 / max_aspect):
        return False
    return True


def compute_iou(boxA, boxB):
    """Compute Intersection over Union between two boxes [x1,y1,x2,y2]."""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    inter_w = max(0.0, xB - xA)
    inter_h = max(0.0, yB - yA)
    inter_area = inter_w * inter_h
    if inter_area == 0:
        return 0.0
    areaA = max(0.0, (boxA[2] - boxA[0])) * max(0.0, (boxA[3] - boxA[1]))
    areaB = max(0.0, (boxB[2] - boxB[0])) * max(0.0, (boxB[3] - boxB[1]))
    union_area = areaA + areaB - inter_area
    return inter_area / max(union_area, 1e-6)


def compute_iou_matrix(det_boxes, track_pred_boxes):
    """
    Compute IoU matrix of shape (N_dets, N_tracks).
    det_boxes:        list of [x1,y1,x2,y2]
    track_pred_boxes: list of [x1,y1,x2,y2] (velocity-predicted positions)
    """
    n_d = len(det_boxes)
    n_t = len(track_pred_boxes)
    iou_mat = np.zeros((n_d, n_t), dtype=np.float32)
    for i, db in enumerate(det_boxes):
        for j, tb in enumerate(track_pred_boxes):
            iou_mat[i, j] = compute_iou(db, tb)
    return iou_mat


def predict_box(bbox, velocity):
    """Apply constant-velocity prediction to a bounding box."""
    vx, vy = velocity
    x1, y1, x2, y2 = bbox
    return [x1 + vx, y1 + vy, x2 + vx, y2 + vy]


# ─────────────────────────────────────────────────────────────────────────────
# SORT-like Face Tracker
# ─────────────────────────────────────────────────────────────────────────────

class FaceTracker:
    """
    SORT-like face tracker using:
      - Velocity-predicted IoU cost matrix
      - Hungarian optimal assignment
      - Geometric sanity filter
      - Hit-streak confirmation gate (prevents FP tracks from showing)
      - last_match_time eviction (prevents ghost boxes)
    """

    def __init__(self, unet_interval=6):
        self.tracks = {}          # track_id -> track dict
        self.tentative = {}       # track_id -> tentative track dict (unconfirmed)
        self.next_track_id = 1
        self.unet_interval = unet_interval
        self.detector_interval = int(os.environ.get("DETECTOR_INTERVAL", "4"))
        self.frame_counter = 0
        self.last_update_time = 0.0

    # ── Public API ────────────────────────────────────────────────────────────

    def needs_detector_run(self):
        if not self.tracks and not self.tentative:
            return True
        return self.frame_counter % self.detector_interval == 0

    def update(self, detected_faces, img_raw, draw_mask, segmenter, threshold,
               min_face_px=None):
        """
        Update tracker. Returns list of confirmed face track dicts.

        Args:
            detected_faces: list of detection dicts (from RetinaFace), or None on skipped frames
            img_raw:        raw BGR frame
            draw_mask:      whether to run U-Net segmentation
            segmenter:      UNetFaceSegmenter instance
            threshold:      confidence threshold (informational)
            min_face_px:    override MIN_FACE_PX for geometric filter
        """
        current_time = time.time()

        # Reset on long idle
        if current_time - self.last_update_time > 2.0:
            self.tracks.clear()
            self.tentative.clear()
            self.next_track_id = 1
            self.frame_counter = 0
        self.last_update_time = current_time

        h, w = img_raw.shape[:2]
        self.frame_counter += 1

        min_px = min_face_px if min_face_px is not None else MIN_FACE_PX

        # ── Skipped frames: constant-velocity prediction ───────────────────
        if detected_faces is None:
            return self._predict_step(current_time, img_raw, draw_mask, segmenter, w, h)

        # ── Detector frame: filter → Hungarian match → update/create/evict ──
        # 1. Geometric filter on raw detections
        valid_dets = [f for f in detected_faces if is_valid_face_box(f['box'], min_px=min_px)]

        # 2. Build velocity-predicted boxes for all confirmed tracks
        track_ids   = list(self.tracks.keys())
        track_pred  = [predict_box(self.tracks[tid]['bbox'], self.tracks[tid].get('velocity', (0.0, 0.0)))
                       for tid in track_ids]

        det_boxes = [f['box'] for f in valid_dets]

        # 3. Hungarian assignment
        matched_det_to_track = {}   # det_idx -> track_id
        unmatched_det_indices = set(range(len(valid_dets)))
        used_track_ids = set()

        if det_boxes and track_pred:
            iou_mat = compute_iou_matrix(det_boxes, track_pred)
            cost_mat = 1.0 - iou_mat
            row_ind, col_ind = linear_sum_assignment(cost_mat)

            for r, c in zip(row_ind, col_ind):
                iou_val = iou_mat[r, c]
                if iou_val >= MIN_IOU_MATCH:
                    matched_det_to_track[r] = track_ids[c]
                    used_track_ids.add(track_ids[c])
                    unmatched_det_indices.discard(r)

        # 4. Update matched confirmed tracks
        crops_to_segment = []
        crops_info = []   # (det_idx, track_id)

        for det_idx, face in enumerate(valid_dets):
            x1, y1, x2, y2 = map(int, face['box'])
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            rect_w, rect_h = x2 - x1, y2 - y1

            track_id = matched_det_to_track.get(det_idx)

            if track_id is not None:
                track = self.tracks[track_id]
                old_x1, old_y1 = track['bbox'][:2]

                # Velocity EMA update
                vx_raw = (x1 - old_x1) / float(self.detector_interval)
                vy_raw = (y1 - old_y1) / float(self.detector_interval)
                pv_x, pv_y = track.get('velocity', (0.0, 0.0))
                track['velocity'] = (0.4 * vx_raw + 0.6 * pv_x, 0.4 * vy_raw + 0.6 * pv_y)

                track['bbox']           = [x1, y1, x2, y2]
                track['landmarks']      = face['landmarks']
                track['confidence']     = face['confidence']
                track['unet_counter']  += 1
                track['last_seen']      = current_time
                track['last_match_time'] = current_time
                track['hit_streak']    += 1
                if rect_w > 10 and rect_h > 10:
                    track['last_crop'] = img_raw[y1:y2, x1:x2]

                if draw_mask:
                    if (track['unet_counter'] >= self.unet_interval) or (track['crop_mask'] is None):
                        if rect_w > 10 and rect_h > 10:
                            crops_to_segment.append(img_raw[y1:y2, x1:x2])
                            crops_info.append((det_idx, track_id))
                        else:
                            track['crop_mask'] = None
                            track['unet_counter'] = 0
                else:
                    track['crop_mask'] = None
                    track['unet_counter'] = 0
                    track['face_png_alpha'] = generate_face_thumbnail(img_raw, [x1, y1, x2, y2], None)

            else:
                # Unmatched detection → check tentative pool or create new tentative
                # Try to match with tentative tracks using IoU too
                tent_ids   = list(self.tentative.keys())
                tent_preds = [predict_box(self.tentative[tid]['bbox'], self.tentative[tid].get('velocity', (0.0, 0.0)))
                              for tid in tent_ids]

                matched_tent = None
                if tent_preds:
                    best_iou = MIN_IOU_MATCH
                    for j, tp in enumerate(tent_preds):
                        iou_v = compute_iou([x1, y1, x2, y2], tp)
                        if iou_v > best_iou and tent_ids[j] not in used_track_ids:
                            best_iou = iou_v
                            matched_tent = tent_ids[j]

                if matched_tent is not None:
                    tent = self.tentative[matched_tent]
                    tent['bbox']           = [x1, y1, x2, y2]
                    tent['landmarks']      = face['landmarks']
                    tent['confidence']     = face['confidence']
                    tent['hit_streak']    += 1
                    tent['last_match_time'] = current_time
                    tent['last_seen']      = current_time
                    used_track_ids.add(matched_tent)

                    # Promote to confirmed track if hit_streak >= N_HIT_CONFIRM
                    if tent['hit_streak'] >= N_HIT_CONFIRM:
                        new_id = self.next_track_id
                        self.next_track_id += 1
                        confirmed_track = dict(tent)
                        confirmed_track['track_id']      = new_id
                        confirmed_track['face_png_alpha'] = generate_face_thumbnail(img_raw, [x1, y1, x2, y2], None)
                        confirmed_track['crop_mask']     = None
                        confirmed_track['unet_counter']  = 0
                        if rect_w > 10 and rect_h > 10:
                            confirmed_track['last_crop']  = img_raw[y1:y2, x1:x2]
                        self.tracks[new_id] = confirmed_track
                        del self.tentative[matched_tent]

                        if draw_mask and rect_w > 10 and rect_h > 10:
                            crops_to_segment.append(img_raw[y1:y2, x1:x2])
                            crops_info.append((det_idx, new_id))
                else:
                    # Brand new tentative track
                    tent_id = self.next_track_id
                    self.next_track_id += 1
                    self.tentative[tent_id] = {
                        'track_id':       tent_id,
                        'bbox':           [x1, y1, x2, y2],
                        'landmarks':      face['landmarks'],
                        'confidence':     face['confidence'],
                        'velocity':       (0.0, 0.0),
                        'hit_streak':     1,
                        'last_seen':      current_time,
                        'last_match_time': current_time,
                    }

        # 5. Batch U-Net prediction
        if crops_to_segment:
            try:
                unet_masks = segmenter.predict_batch(crops_to_segment)
            except Exception as e:
                print("U-Net batch prediction failed:", e)
                unet_masks = [np.zeros((c.shape[0], c.shape[1]), dtype=np.uint8) for c in crops_to_segment]

            for i, (det_idx, track_id) in enumerate(crops_info):
                if track_id not in self.tracks:
                    continue
                track = self.tracks[track_id]
                if i < len(unet_masks):
                    track['crop_mask']   = unet_masks[i]
                    track['unet_counter'] = 0
                    tx1, ty1, tx2, ty2 = map(int, track['bbox'])
                    tx1, ty1 = max(0, tx1), max(0, ty1)
                    tx2, ty2 = min(w, tx2), min(h, ty2)
                    tw, th = tx2 - tx1, ty2 - ty1
                    if tw > 0 and th > 0:
                        pad_png = min(15, int(max(tw, th) * 0.1))
                        px1 = max(0, tx1 - pad_png)
                        py1 = max(0, ty1 - pad_png)
                        px2 = min(w, tx2 + pad_png)
                        py2 = min(h, ty2 + pad_png)
                        cw, ch = px2 - px1, py2 - py1
                        if cw > 0 and ch > 0:
                            full_mask = np.zeros((h, w), dtype=np.uint8)
                            unet_mask_resized = cv2.resize(unet_masks[i], (tw, th), interpolation=cv2.INTER_NEAREST)
                            full_mask[ty1:ty2, tx1:tx2] = unet_mask_resized
                            face_crop_region = img_raw[py1:py2, px1:px2]
                            mask_crop = full_mask[py1:py2, px1:px2]
                            mask_crop_soft = cv2.GaussianBlur(mask_crop, (5, 5), 0)
                            b_ch, g_ch, r_ch = cv2.split(face_crop_region)
                            rgba_crop = cv2.merge([b_ch, g_ch, r_ch, mask_crop_soft])
                            _, png_buffer = cv2.imencode('.png', rgba_crop)
                            track['face_png_alpha'] = f"data:image/png;base64,{base64.b64encode(png_buffer).decode('utf-8')}"

        # 6. Evict unmatched confirmed tracks (last_match_time expired)
        self.tracks = {tid: t for tid, t in self.tracks.items()
                       if current_time - t.get('last_match_time', current_time) < MAX_MISS_SECS}

        # 7. Evict expired tentative tracks
        self.tentative = {tid: t for tid, t in self.tentative.items()
                          if current_time - t.get('last_match_time', current_time) < MAX_MISS_SECS}

        # 8. Build response from confirmed tracks
        return self._build_response(img_raw, draw_mask, w, h)

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _predict_step(self, current_time, img_raw, draw_mask, segmenter, w, h):
        """Constant-velocity prediction for skipped detector frames."""
        response_faces = []

        for track_id, track in list(self.tracks.items()):
            if current_time - track.get('last_match_time', current_time) > MAX_MISS_SECS:
                continue

            vx, vy = track.get('velocity', (0.0, 0.0))
            tx1, ty1, tx2, ty2 = track['bbox']
            new_box = [tx1 + vx, ty1 + vy, tx2 + vx, ty2 + vy]

            new_landmarks = None
            if track.get('landmarks') is not None:
                new_landmarks = []
                for idx in range(5):
                    new_landmarks.append(track['landmarks'][2 * idx] + vx)
                    new_landmarks.append(track['landmarks'][2 * idx + 1] + vy)

            # Decay velocity to prevent runaway drift
            track['velocity'] = (vx * 0.85, vy * 0.85)
            track['bbox'] = new_box
            track['landmarks'] = new_landmarks
            track['last_seen'] = current_time
            track['unet_counter'] += 1

            # U-Net on skipped frames if needed
            nx1, ny1, nx2, ny2 = map(int, new_box)
            nx1, ny1 = max(0, nx1), max(0, ny1)
            nx2, ny2 = min(w, nx2), min(h, ny2)
            rect_w, rect_h = nx2 - nx1, ny2 - ny1

            if draw_mask:
                if (track['unet_counter'] >= self.unet_interval) or (track['crop_mask'] is None):
                    if rect_w > 10 and rect_h > 10:
                        crop = img_raw[ny1:ny2, nx1:nx2]
                        if crop.size > 0:
                            try:
                                unet_mask = segmenter.predict_batch([crop])[0]
                                track['crop_mask'] = unet_mask
                                track['unet_counter'] = 0
                                pad_png = min(15, int(max(rect_w, rect_h) * 0.1))
                                px1 = max(0, nx1 - pad_png)
                                py1 = max(0, ny1 - pad_png)
                                px2 = min(w, nx2 + pad_png)
                                py2 = min(h, ny2 + pad_png)
                                cw, ch = px2 - px1, py2 - py1
                                if cw > 0 and ch > 0:
                                    full_mask = np.zeros((h, w), dtype=np.uint8)
                                    rw2, rh2 = nx2 - nx1, ny2 - ny1
                                    if rw2 > 0 and rh2 > 0:
                                        unet_resized = cv2.resize(unet_mask, (rw2, rh2), interpolation=cv2.INTER_NEAREST)
                                        full_mask[ny1:ny2, nx1:nx2] = unet_resized
                                    face_crop_region = img_raw[py1:py2, px1:px2]
                                    mask_crop = full_mask[py1:py2, px1:px2]
                                    mask_crop_soft = cv2.GaussianBlur(mask_crop, (5, 5), 0)
                                    b_ch, g_ch, r_ch = cv2.split(face_crop_region)
                                    rgba_crop = cv2.merge([b_ch, g_ch, r_ch, mask_crop_soft])
                                    _, png_buffer = cv2.imencode('.png', rgba_crop)
                                    track['face_png_alpha'] = f"data:image/png;base64,{base64.b64encode(png_buffer).decode('utf-8')}"
                            except Exception as e:
                                print("U-Net on skipped frame failed:", e)

            # Build binary mask
            binary_mask = np.zeros((h, w), dtype=np.uint8)
            if track['crop_mask'] is not None and rect_w > 0 and rect_h > 0:
                try:
                    resized_mask = cv2.resize(track['crop_mask'], (rect_w, rect_h), interpolation=cv2.INTER_NEAREST)
                    binary_mask[ny1:ny2, nx1:nx2] = resized_mask
                except Exception:
                    _draw_ellipse_fallback(binary_mask, new_box, w, h)
            else:
                _draw_ellipse_fallback(binary_mask, new_box, w, h)

            response_faces.append({
                'id':            track_id,
                'box':           new_box,
                'confidence':    track['confidence'],
                'landmarks':     new_landmarks,
                'binary_mask':   binary_mask,
                'face_png_alpha': track['face_png_alpha']
            })

        # Evict expired tracks
        self.tracks = {tid: t for tid, t in self.tracks.items()
                       if current_time - t.get('last_match_time', current_time) < MAX_MISS_SECS}
        self.tentative = {tid: t for tid, t in self.tentative.items()
                          if current_time - t.get('last_match_time', current_time) < MAX_MISS_SECS}
        return response_faces

    def _build_response(self, img_raw, draw_mask, w, h):
        """Assemble the response list from all confirmed tracks."""
        response_faces = []

        for track_id, track in self.tracks.items():
            x1, y1, x2, y2 = map(int, track['bbox'])
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            rect_w, rect_h = x2 - x1, y2 - y1

            binary_mask = np.zeros((h, w), dtype=np.uint8)
            if track.get('crop_mask') is not None and rect_w > 0 and rect_h > 0:
                try:
                    resized_mask = cv2.resize(track['crop_mask'], (rect_w, rect_h), interpolation=cv2.INTER_NEAREST)
                    binary_mask[y1:y2, x1:x2] = resized_mask
                except Exception:
                    _draw_ellipse_fallback(binary_mask, track['bbox'], w, h)
            else:
                _draw_ellipse_fallback(binary_mask, track['bbox'], w, h)

            # Ensure face_png_alpha is populated
            if not track.get('face_png_alpha'):
                track['face_png_alpha'] = generate_face_thumbnail(img_raw, [x1, y1, x2, y2], None)

            response_faces.append({
                'id':            track_id,
                'box':           track['bbox'],
                'confidence':    track['confidence'],
                'landmarks':     track.get('landmarks'),
                'binary_mask':   binary_mask,
                'face_png_alpha': track['face_png_alpha']
            })

        return response_faces


# ─────────────────────────────────────────────────────────────────────────────
# Private helper
# ─────────────────────────────────────────────────────────────────────────────

def _draw_ellipse_fallback(binary_mask, box, w, h):
    """Draw an inscribed ellipse as fallback when no U-Net mask is available."""
    rx1, ry1, rx2, ry2 = map(int, box[:4])
    rx1, ry1 = max(0, rx1), max(0, ry1)
    rx2, ry2 = min(w, rx2), min(h, ry2)
    rw, rh = rx2 - rx1, ry2 - ry1
    if rw > 0 and rh > 0:
        center = (int((rx1 + rx2) / 2), int((ry1 + ry2) / 2))
        axes   = (int(rw / 2), int(rh / 2))
        cv2.ellipse(binary_mask, center, axes, 0, 0, 360, 255, -1)
