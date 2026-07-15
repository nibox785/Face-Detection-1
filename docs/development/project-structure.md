# Cấu Trúc Dự Án (Project Structure)

Cấu trúc thư mục phản ánh sự phân chia rõ ràng giữa backend AI, frontend dashboard, tests và tài liệu.

---

## Cấu Trúc Tổng Quan

```text
/ (Thư mục gốc)
├── backend/                  # Toàn bộ logic phía server (FastAPI + AI Pipeline)
│   ├── main.py               # FastAPI app chính: route /detect, /health, /
│   ├── app_logging/          # Hệ thống logging có cấu trúc
│   │   └── structured_logger.py  # Logger ghi JSON event (timestamp, type, latency)
│   ├── data/                 # Cấu hình RetinaFace
│   │   └── config.py         # cfg_mnet (MobileNet) và cfg_re50 (ResNet50)
│   ├── layers/               # Các lớp neural network (PriorBox, decode)
│   │   └── functions/
│   │       └── prior_box.py  # Tính toán anchor boxes
│   ├── models/               # ONNX model wrappers
│   │   ├── face_detector.py  # RetinaFace ONNX wrapper (detect + NMS + hậu xử lý)
│   │   └── face_segmenter.py # U-Net ONNX wrapper (batch predict, resize)
│   ├── quality/              # Đánh giá chất lượng khuôn mặt
│   │   ├── face_quality.py   # Visibility, Occlusion, Head Pose, Score, Rating
│   │   ├── alert.py          # Logic cảnh báo
│   │   └── logger.py         # Trích xuất lịch sử hoạt động
│   ├── segmentation/         # Mã nguồn PyTorch U-Net (huấn luyện)
│   │   ├── config.py         # Mapping 19 lớp CelebAMask-HQ
│   │   ├── model.py          # Kiến trúc U-Net PyTorch
│   │   └── postprocess.py    # Logits → Binary Mask
│   ├── utils/
│   │   ├── tracker.py        # ★ SORT-like FaceTracker (core tracking module)
│   │   │                     #   - is_valid_face_box() geometric filter
│   │   │                     #   - compute_iou_matrix() + Hungarian matching
│   │   │                     #   - Velocity EMA + Constant Velocity Predictor
│   │   │                     #   - Hit-streak gate (tentative → confirmed)
│   │   │                     #   - last_match_time eviction
│   │   ├── box_utils.py      # Decode bbox từ RetinaFace output
│   │   └── nms/
│   │       └── py_cpu_nms.py # Non-Maximum Suppression thuần Python
│   └── weights/              # File mô hình ONNX (không commit lên git)
│       ├── mobilenet0.25_Final.onnx
│       ├── Resnet50_Final.onnx
│       └── unet_face_celeb.onnx
│
├── frontend/                 # Giao diện web tĩnh (serve bởi FastAPI /static)
│   ├── index.html            # Dashboard layout (Glassmorphism CCTV style)
│   │                         #   - Slider: Ngưỡng tin cậy (0.1–0.9, mặc định 0.60)
│   │                         #   - Slider: Kích thước mặt tối thiểu (20–200px, mặc định 36px)
│   │                         #   - Checkboxes: HUD options (Bbox, Mask, Landmarks...)
│   │                         #   - Preset buttons: Normal / Detect / Segment mode
│   │                         #   - Backbone selector: MobileNet / ResNet50
│   ├── css/
│   │   └── style.css         # Dark glassmorphism CSS + Neon HUD effects
│   └── js/
│       └── app.js            # ★ Frontend logic chính
│                             #   - Webcam/Video/Image stream loop
│                             #   - sessionFaceDatabase (Session Face Gallery)
│                             #   - State-Transition Alert Logger
│                             #   - ApexCharts: Quality Donut + Pose Bar + History Line
│                             #   - Audio HUD beeps
│                             #   - Evidence export (frame, crops, snapshot)
│
├── tests/                    # Bộ kiểm thử (21 test cases, pytest)
│   ├── benchmark/
│   │   └── test_performance_benchmark.py  # Latency & FPS benchmark
│   ├── integration/
│   │   └── test_api_detect.py             # API /detect integration tests
│   ├── model/
│   │   ├── test_face_detector.py          # RetinaFace detector tests
│   │   └── test_segmentation.py           # U-Net segmenter tests
│   └── unit/
│       └── test_face_quality.py           # Face quality unit tests
│
├── docs/                     # Tài liệu đầy đủ của dự án
│   ├── api/                  # API Reference
│   ├── architecture/         # Kiến trúc hệ thống và pipeline AI
│   ├── features/             # Mô tả các tính năng chính
│   ├── development/          # Hướng dẫn phát triển
│   └── ...                   # Các tài liệu khác
│
├── export_onnx.py            # Script chuyển đổi .pth → .onnx
├── requirements.txt          # Dependencies (fastapi, onnxruntime, scipy, torch...)
├── pytest.ini                # Cấu hình pytest
└── run.py                    # Entrypoint: tự động tải weights + khởi động uvicorn
```

---

## Các File Quan Trọng Nhất

| File | Vai trò |
|---|---|
| `backend/main.py` | API gateway, điều phối toàn bộ pipeline |
| `backend/utils/tracker.py` | **Core AI**: SORT-like tracker, Hungarian matching, geometric filter |
| `backend/models/face_detector.py` | RetinaFace ONNX inference wrapper |
| `backend/models/face_segmenter.py` | U-Net ONNX inference wrapper |
| `backend/quality/face_quality.py` | Face Quality analytics |
| `frontend/js/app.js` | **Core Frontend**: stream loop, gallery, alert logger |
| `frontend/index.html` | Dashboard UI layout |

---

## Hướng Dẫn Mở Rộng

- **Thêm backend route mới** → Chỉnh sửa `backend/main.py`
- **Thay đổi logic tracking** → `backend/utils/tracker.py` (class `FaceTracker`)
- **Thêm tham số API mới** → Thêm `Form(...)` vào hàm `detect()` trong `main.py`, cập nhật `formData.append()` trong `app.js`
- **Thêm chỉ số chất lượng mới** → `backend/quality/face_quality.py` → `analyze_face_quality()`
- **Thêm UI component** → `frontend/index.html` + `frontend/css/style.css` + `frontend/js/app.js`
- **Thêm test** → `tests/unit/`, `tests/integration/` hoặc `tests/model/`
