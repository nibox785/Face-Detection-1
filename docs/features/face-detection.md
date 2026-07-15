# Nhận Diện & Theo Dõi Khuôn Mặt

## Mục Đích

Module này kết hợp hai bài toán:
1. **Phát hiện (Detection):** Xác định vị trí khuôn mặt trong ảnh/frame bằng RetinaFace.
2. **Theo dõi (Tracking):** Duy trì ID ổn định cho từng khuôn mặt qua nhiều frame liên tiếp bằng SORT-like Tracker.

---

## Đầu Vào

- Tệp ảnh JPEG/PNG tải lên từ người dùng
- Khung hình webcam hoặc video được gửi từ vòng lặp xử lý frontend
- Ngưỡng độ tin cậy (`threshold`, mặc định `0.60`)
- Kích thước mặt tối thiểu (`min_face_px`, mặc định `36px`)

---

## Đầu Ra

- Danh sách các track đã xác nhận, mỗi track bao gồm:
  - `id`: Track ID ổn định, không thay đổi khi khuôn mặt di chuyển
  - `box`: Tọa độ bounding box `[x1, y1, x2, y2]`
  - `confidence`: Điểm tin cậy của detection gần nhất
  - `landmarks`: 5 điểm mốc khuôn mặt `[10 float]`
  - `binary_mask`: Ma trận nhị phân `(H, W)` từ U-Net hoặc ellipse fallback
  - `face_png_alpha`: Ảnh chân dung cắt nền PNG base64 (có kênh Alpha)

---

## Kiến Trúc & Thuật Toán

### 2.1 RetinaFace Detector

**File:** `backend/models/face_detector.py`

- Hỗ trợ 2 backbone ONNX:
  - **MobileNet0.25** (`mobilenet0.25_Final.onnx`): ~24ms/frame, ưu tiên tốc độ
  - **ResNet50** (`Resnet50_Final.onnx`): chính xác cao hơn cho đám đông dày đặc
- PriorBox được cache theo kích thước ảnh để tránh tính lại mỗi frame.
- NMS threshold mặc định: `0.4`.

### 2.2 SORT-like FaceTracker

**File:** `backend/utils/tracker.py`

Tracker sử dụng 5 cơ chế kết hợp:

#### A. Skip-frame Detection
- RetinaFace chạy mỗi `DETECTOR_INTERVAL` (mặc định 4) frame.
- 3 frame trung gian dùng Constant Velocity Predictor để cập nhật vị trí bbox và landmarks.

#### B. Geometric Filter (`is_valid_face_box`)
Loại bỏ detection không phải khuôn mặt thật:
- Kích thước `w < min_face_px` hoặc `h < min_face_px` → Loại bỏ
- Tỉ lệ `w/h > 2.5` hoặc `w/h < 0.4` → Loại bỏ

Hiệu quả: Loại bỏ lỗ thông gió, bảng hiệu, hoa văn trên tường.

#### C. Hungarian Algorithm Matching
1. Tính IoU Cost Matrix giữa detections (đã lọc) và vị trí dự báo của tracked faces.
2. `scipy.optimize.linear_sum_assignment` tìm phân công tối ưu toàn cục.
3. Cặp (detection, track) chỉ được chấp nhận khi `IoU ≥ 0.10`.

So với Euclidean greedy cũ: **Không còn ID swap** khi 2 người đi gần hoặc qua nhau.

#### D. Hit-streak Gate
- Track mới → Tentative (chưa hiển thị).
- Sau `N_HIT_CONFIRM = 2` lần ghép thành công liên tiếp → Confirmed (bắt đầu hiển thị).
- Ngăn box flash từ false positive trong 1 frame.

#### E. last_match_time Eviction
- `last_match_time` chỉ được cập nhật bởi detector (không bởi velocity predictor).
- Track bị thu hồi sau `MAX_MISS_SECS = 1.0s` không có detector match.
- Loại bỏ hoàn toàn hiện tượng "ghost box" (box ma bị kẹt).

---

## Hằng Số Cấu Hình Quan Trọng

| Hằng số | Giá trị mặc định | Ý nghĩa |
|---|---|---|
| `N_HIT_CONFIRM` | `2` | Số frame liên tiếp để xác nhận track |
| `MAX_MISS_SECS` | `1.0` | Giây tối đa chờ detector match trước khi evict |
| `MIN_IOU_MATCH` | `0.10` | IoU tối thiểu để chấp nhận Hungarian match |
| `MIN_FACE_PX` | `36` | Kích thước pixel tối thiểu (có thể override qua API) |
| `MAX_ASPECT_RATIO` | `2.5` | Tỉ lệ w/h tối đa |

---

## Phụ Thuộc Kỹ Thuật

- `onnxruntime`: Chạy RetinaFace inference ONNX trên CPU
- `scipy.optimize.linear_sum_assignment`: Hungarian Algorithm assignment
- `opencv-python`: Xử lý ảnh, vẽ ellipse fallback, resize mask
- `numpy`: Tính IoU matrix, xử lý ma trận nhị phân

---

## API Liên Quan

- `POST /detect` — Tham số `threshold`, `min_face_px`, `network`, `upscale`

---

## Mô Hình Liên Quan

- `mobilenet0.25_Final.onnx` — RetinaFace backbone tốc độ cao
- `Resnet50_Final.onnx` — RetinaFace backbone độ chính xác cao
- `unet_face_celeb.onnx` — U-Net phân vùng khuôn mặt (xem thêm `face-segmentation.md`)
