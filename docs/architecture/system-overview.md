# Tổng Quan Hệ Thống (System Overview)

Hệ thống là một ứng dụng web giám sát khuôn mặt đám đông bằng trí tuệ nhân tạo, chạy trên một backend FastAPI và một frontend tĩnh. Người dùng tương tác qua trình duyệt, gửi frame ảnh/video vào backend, backend chạy pipeline AI và trả về kết quả JSON + ảnh annotate để frontend hiển thị.

---

## Cấu Trúc Triển Khai

```
Trình duyệt (Client)
    │
    │   POST /detect (multipart/form-data)
    ▼
FastAPI Backend (uvicorn, port 5000)
    │
    ├── FaceTracker (SORT-like)         ← Quản lý track ID qua nhiều frame
    │       ├── RetinaFace ONNX         ← Phát hiện khuôn mặt (mỗi 4 frame)
    │       ├── Geometric Filter        ← Lọc false positive (size, aspect ratio)
    │       ├── Hungarian Matching      ← Gán detection ↔ track tối ưu
    │       ├── Hit-streak Gate         ← Xác nhận track sau N≥2 lần
    │       └── Velocity Predictor      ← Dự báo vị trí frame skip
    │
    ├── U-Net ONNX                      ← Phân vùng khuôn mặt (mỗi 6 frame/track)
    │
    ├── Face Quality Analyzer           ← Visibility, Pose, Score, Rating
    │
    └── JSON + Base64 Response
            │
            ▼
    Frontend Dashboard
        ├── Canvas Overlay              ← Bbox, Mask, Landmarks
        ├── Session Face Gallery        ← Tất cả track trong phiên (ONLINE/OFFLINE)
        ├── State-Transition Alerts     ← Log chỉ khi có thay đổi trạng thái
        └── ApexCharts                  ← Quality Donut, Pose Bar, History Line
```

---

## Các Lớp Hệ Thống

| Lớp | Mô tả | Files chính |
|---|---|---|
| **Presentation** | Hiển thị viewport, overlay, gallery, biểu đồ | `frontend/index.html`, `frontend/js/app.js` |
| **API** | Nhận request, điều phối pipeline, trả JSON | `backend/main.py` |
| **Tracking** | SORT-like tracker, Hungarian matching, eviction | `backend/utils/tracker.py` |
| **Detection** | RetinaFace ONNX inference | `backend/models/face_detector.py` |
| **Segmentation** | U-Net ONNX inference (throttled) | `backend/models/face_segmenter.py` |
| **Quality** | Face quality analytics | `backend/quality/face_quality.py` |
| **Logging** | Structured JSON event logger | `backend/app_logging/structured_logger.py` |

---

## Luồng Vận Hành Tổng Thể

### Phía Backend (mỗi request `/detect`)

1. Giải mã ảnh từ `UploadFile` → `img_raw (BGR ndarray)`.
2. **Skip-frame check**: `tracker.needs_detector_run()` → Chạy RetinaFace hoặc dùng velocity.
3. **FaceTracker.update()**:
   - Detector frames: Geometric Filter → Hungarian Matching → Hit-streak Gate → Update velocity.
   - Skip frames: Constant Velocity Predictor → Update bbox & landmarks.
4. **U-Net Segmentation** (throttled per track): Batch predict, cache mask.
5. **Face Quality Analysis**: Visibility, Occlusion, Head Pose, Quality Score.
6. **Annotate & Response**: Vẽ bbox/landmarks/mask overlay → encode Base64 JPEG → return JSON.

### Phía Frontend (mỗi frame)

1. Capture frame từ webcam/video.
2. POST lên `/detect` với `threshold`, `min_face_px`, `network`, `draw_mask`.
3. Nhận JSON → Cập nhật canvas overlay và `sessionFaceDatabase`.
4. Cập nhật gallery (ONLINE/OFFLINE badge dựa trên track IDs hiện tại).
5. Kiểm tra state transition → Ghi Alert Log nếu có thay đổi.
6. Cập nhật ApexCharts theo dữ liệu mới nhất.

---

## Hiệu Năng Hệ Thống

### Thiết kế tối ưu tốc độ

- **Skip-frame Inference**: Chỉ chạy RetinaFace mỗi 4 frame (~75% tiết kiệm CPU).
- **U-Net Throttling**: Chỉ chạy U-Net mỗi 6 frame/track.
- **ONNX Runtime**: Nhanh hơn PyTorch 2–3× trên CPU.
- **PriorBox Cache**: Tránh tính lại anchor boxes mỗi frame.
- **Batch U-Net**: Tất cả crops được gom và predict một lần.

### Benchmark (CPU, single-thread)

| Cấu hình | Latency ước tính | FPS thực tế |
|---|---|---|
| MobileNet + skip=4 + U-Net tắt | 8–24ms | 40–120 FPS |
| MobileNet + skip=4 + U-Net bật | 24–55ms | 18–40 FPS |
| ResNet50 + skip=4 + U-Net tắt | 150–250ms | 4–7 FPS |

---

## Các Cải Tiến Lớn (Changelog)

| Phiên bản | Nội dung |
|---|---|
| v1.0 | RetinaFace ONNX + U-Net ONNX cơ bản |
| v1.1 | Skip-frame Inference + ONNX intra-op threading |
| v1.2 | Constant Velocity Predictor + Template Matching (đã thay thế) |
| v1.3 | **SORT-like Tracker** (Hungarian IoU + Geometric Filter + Hit-streak Gate) |
| v1.4 | `last_match_time` eviction — loại bỏ ghost box hoàn toàn |
| v1.5 | State-Transition Alert Logger + Session Face Gallery |
| v1.6 | `min_face_px` slider (người dùng điều chỉnh bộ lọc hình học) |
