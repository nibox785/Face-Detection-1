# Đánh Giá Chất Lượng Khuôn Mặt (Face Quality Assessment)

## Mục Đích

Module này tự động tính toán các chỉ số chất lượng khuôn mặt nhằm hỗ trợ:
- Lọc và cảnh báo khuôn mặt bị che khuất hoặc chất lượng thấp.
- Cung cấp dữ liệu cho biểu đồ thống kê thời gian thực (Quality Donut Chart, Head Pose Bar Chart).
- Hỗ trợ quyết định lưu evidence cho các đối tượng nghi vấn.

---

## Đầu Vào

| Tham số | Nguồn | Mô tả |
|---|---|---|
| `box` | FaceTracker | Tọa độ `[x1, y1, x2, y2]` của bounding box |
| `confidence` | RetinaFace | Điểm tin cậy (0.0–1.0) |
| `landmarks` | RetinaFace | 5 điểm mốc `[10 float]` |
| `binary_mask` | U-Net / Ellipse | Ma trận nhị phân `(H, W)` biểu diễn vùng khuôn mặt |

---

## Đầu Ra

| Trường | Kiểu | Mô tả |
|---|---|---|
| `visibility` | `int` (0–100) | % vùng mask che phủ trong bounding box |
| `is_occluded` | `bool` | True nếu visibility < 40% |
| `pose` | `string` | Hướng quay đầu: `Normal`, `Head Left`, `Head Right`, `Head Up`, `Head Down` |
| `quality_score` | `int` (0–100) | Điểm chất lượng tổng hợp |
| `status` | `string` | `Normal` hoặc `Face Occluded` |
| `rating` | `string` | `Excellent`, `Good`, `Acceptable`, `Poor`, `Unusable` |

---

## Thuật Toán

### 1. Tính Visibility

**File:** `backend/quality/face_quality.py` → `check_visibility()`

```python
visibility = (mask_pixels_inside_bbox / bbox_area) × 100
```

Chỉ đếm pixel mask trong vùng bounding box (không tính vùng ngoài box).

### 2. Phát Hiện Che Khuất (Occlusion)

**File:** `check_occlusion()`

```python
is_occluded = (visibility < 40)
```

### 3. Ước Lượng Góc Xoay Đầu (Head Pose)

**File:** `check_head_pose()`

Dùng hình học từ 5 landmarks `[eye_L, eye_R, nose, mouth_L, mouth_R]`:

| Chỉ số | Công thức | Ngưỡng |
|---|---|---|
| **Pitch** (Up/Down) | `nose_y_ratio = (nose_y - eye_y) / (mouth_y - eye_y)` | `> 0.82` → Head Down; `< 0.28` → Head Up |
| **Yaw** (Left/Right) | `nose_x_ratio = (nose_x - left_eye_x) / (right_eye_x - left_eye_x)` | `< 0.33` → Head Left; `> 0.67` → Head Right |

### 4. Điểm Chất Lượng Tổng Hợp (Quality Score)

**File:** `analyze_face_quality()`

```
quality_score = 0.40 × (confidence × 100)
              + 0.30 × visibility
              + 0.15 × size_score     # Too Small=40, Large=95, Normal=100
              + 0.15 × pose_score     # Normal=100, khác=75
```

### 5. Phân Loại Rating

| Rating | Quality Score |
|---|---|
| `Excellent` | ≥ 85 |
| `Good` | 70–84 |
| `Acceptable` | 50–69 |
| `Poor` | 30–49 |
| `Unusable` | < 30 |

---

## Phụ Thuộc

- `backend/models/face_detector.py` → Cung cấp `confidence` và `landmarks`
- `backend/utils/tracker.py` → Cung cấp `binary_mask` từ U-Net hoặc ellipse fallback
- `backend/models/face_segmenter.py` → U-Net ONNX tạo segmentation mask chính xác

---

## Kết Nối API

- `POST /detect` → Mỗi face trong `faces[]` bao gồm đầy đủ các trường quality
- Frontend đọc `rating`, `quality_score`, `pose`, `status` để hiển thị HUD và cập nhật biểu đồ
