# AI Pipeline — Luồng Xử Lý Trí Tuệ Nhân Tạo

Tài liệu này mô tả toàn bộ pipeline AI của hệ thống từ khi nhận frame camera đến khi phản hồi kết quả về Frontend.

---

## Tổng Quan

Pipeline được thiết kế theo nguyên tắc **Skip-frame Inference** — detector nặng chỉ chạy mỗi N frame (mặc định N=4), các frame trung gian dùng thuật toán nhẹ hơn để duy trì hiển thị mượt mà.

```
Frame input
    │
    ├─ [Detector Frame: N mod 4 == 0]─── RetinaFace ONNX ──▶ Geometric Filter ──▶ Hungarian Matching
    │                                                                                       │
    └─ [Skip Frame]──────────────────── Constant Velocity Predictor ──────────────────────▶┘
                                                                                            │
                                                                                  FaceTracker State
                                                                                            │
                                                                          Hit-streak Gate (N≥2 → Confirmed)
                                                                                            │
                                                                                U-Net Segmentation (mỗi 6 frame)
                                                                                            │
                                                                                Face Quality Analysis
                                                                                            │
                                                                              JSON + Base64 Response
```

---

## Bước 1: Skip-frame Decision

File: `backend/utils/tracker.py` → `FaceTracker.needs_detector_run()`

- `self.frame_counter` tăng mỗi request.
- Nếu `frame_counter % DETECTOR_INTERVAL == 0` hoặc không có track nào → Chạy RetinaFace.
- Ngược lại → Trả về `None` cho `detected_faces` → Bộ theo dõi chuyển sang chế độ dự báo vận tốc.

**Biến môi trường:** `DETECTOR_INTERVAL` (mặc định `4`).

---

## Bước 2A: RetinaFace Inference (Detector Frames)

File: `backend/models/face_detector.py` → `RetinaFaceDetector.detect()`

- **Input:** Frame BGR `(H, W, 3)`.
- **Tiền xử lý:** Trừ mean `(104, 117, 123)`, transpose sang `(1, 3, H, W)`.
- **ONNX Inference:** Chạy session trên CPU (ONNX Runtime). Trả về `loc`, `conf`, `landms`.
- **Hậu xử lý:** Decode box từ PriorBox anchor, scale về tọa độ pixel gốc, lọc NMS (threshold mặc định `0.4`).
- **Output:** Danh sách `{box, confidence, landmarks}` với `confidence ≥ threshold`.
- **Cache PriorBox:** `cached_size` lưu cache PriorBox theo kích thước ảnh, tránh tính lại mỗi frame.

---

## Bước 2B: Constant Velocity Predictor (Skip Frames)

File: `backend/utils/tracker.py` → `FaceTracker._predict_step()`

Trên mỗi frame skip, với mỗi confirmed track:
1. Đọc vector vận tốc `(vx, vy)` đã tính sẵn từ frame detector trước.
2. Dịch chuyển `bbox` và `landmarks` theo `(vx, vy)`.
3. Giảm vận tốc bằng hệ số decay `0.85` để tránh drift xa.
4. Cập nhật `last_seen` (nhưng **không** cập nhật `last_match_time` — chỉ detector mới được cập nhật).

---

## Bước 3: Geometric Filter (chỉ trên Detector Frames)

File: `backend/utils/tracker.py` → `is_valid_face_box()`

Mỗi detection từ RetinaFace được kiểm tra:
- **Kích thước tối thiểu:** `box_width ≥ min_face_px` VÀ `box_height ≥ min_face_px` (mặc định 36px).
- **Tỉ lệ hình dạng:** `0.4 ≤ w/h ≤ 2.5`.

Detection không hợp lệ bị loại bỏ ngay lập tức, tránh false positive từ lỗ thông gió, bảng hiệu, hoa văn.

---

## Bước 4: Hungarian Algorithm Matching

File: `backend/utils/tracker.py` → `compute_iou_matrix()` + `scipy.optimize.linear_sum_assignment`

1. **Dự báo vị trí track:** Áp dụng velocity prediction lên tất cả confirmed tracks → `track_pred_boxes`.
2. **IoU Cost Matrix:** `C[i][j] = 1 - IoU(detection[i], track_pred[j])`, kích thước `(N_dets, N_tracks)`.
3. **Hungarian Assignment:** `scipy.optimize.linear_sum_assignment(cost_matrix)` tìm phân công chi phí tối thiểu.
4. **Gate threshold:** Chỉ chấp nhận cặp (detection, track) khi `IoU ≥ MIN_IOU_MATCH = 0.10`.

**Ưu điểm so với Euclidean greedy:**
- Phân công tối ưu toàn cục → không bị ID swap khi nhiều người đi gần nhau.
- IoU-based → immune với sự thay đổi kích thước mặt theo khoảng cách camera.

---

## Bước 5: Hit-streak Gate (Chống False Positive)

File: `backend/utils/tracker.py` → tentative tracks logic

- Detection chưa khớp với track nào → Tạo **tentative track** (chưa hiển thị).
- Mỗi lần detector tiếp theo ghép thành công → `hit_streak += 1`.
- Khi `hit_streak ≥ N_HIT_CONFIRM = 2` → **Promote** lên confirmed track → Bắt đầu hiển thị.
- Tentative track không được xác nhận trong `MAX_MISS_SECS = 1.0s` → Bị xóa.

---

## Bước 6: Velocity EMA Update

Mỗi khi detector cập nhật một confirmed track:
```python
vx_raw = (x1_new - x1_old) / DETECTOR_INTERVAL  # vận tốc pixel/frame
vx = 0.4 * vx_raw + 0.6 * vx_prev               # EMA smoothing
```
Vector vận tốc được cập nhật bằng EMA (α=0.4) để lọc nhiễu rung camera.

---

## Bước 7: U-Net Segmentation (Throttled)

File: `backend/models/face_segmenter.py` + `backend/utils/tracker.py`

- U-Net chỉ chạy khi `unet_counter ≥ unet_interval (=6)` hoặc `crop_mask is None`.
- **Batch inference:** Tất cả các track cần U-Net được gom lại và chạy `predict_batch()` một lần.
- **Cache mask:** Mask được lưu trong `track['crop_mask']` và resize cho các frame trung gian.
- **Fallback:** Khi U-Net tắt hoặc thất bại → vẽ ellipse nội tiếp bbox.

---

## Bước 8: Face Quality Analysis

File: `backend/quality/face_quality.py` → `analyze_face_quality()`

| Chỉ số | Phương pháp |
|---|---|
| **Visibility (%)** | `mask_pixels_in_bbox / bbox_area × 100` |
| **Occlusion** | Visibility < 40% → Bị che khuất |
| **Head Pose** | Tỉ lệ hình học giữa landmarks (mắt, mũi, miệng) |
| **Quality Score** | Tổng hợp: `0.4×confidence + 0.3×visibility + 0.15×size_score + 0.15×pose_score` |
| **Rating** | Excellent (≥85) / Good (≥70) / Acceptable (≥50) / Poor (≥30) / Unusable (<30) |

---

## Bước 9: Track Eviction

Track bị thu hồi khi:
- `current_time - last_match_time > MAX_MISS_SECS (1.0s)` trên **cả** detector frames và skip frames.

`last_match_time` **chỉ** được cập nhật khi detector chạy và ghép thành công — không bị làm mới bởi velocity prediction.

---

## Hiệu Năng Tham Khảo

| Cấu hình | Latency/frame | FPS lý thuyết |
|---|---|---|
| MobileNet, skip=4, U-Net tắt | ~8–28ms | 35–120 FPS |
| MobileNet, skip=4, U-Net bật | ~28–60ms | 15–35 FPS |
| ResNet50, skip=4, U-Net tắt | ~180–250ms | 4–5 FPS |
| ResNet50, skip=4, U-Net bật | ~250–400ms | 2–4 FPS |

> [!TIP]
> Để đạt FPS cao nhất trên máy CPU yếu: Dùng MobileNet, tắt U-Net Mask, giảm độ phân giải webcam xuống 640×480.
