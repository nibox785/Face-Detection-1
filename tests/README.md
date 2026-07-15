# Test Suite

## Mục Đích

Thư mục này chứa toàn bộ mã nguồn kiểm thử cho hệ thống phát hiện, theo dõi và phân đoạn khuôn mặt AI.

Bộ test hiện tại: **21 test cases**, chạy bằng `pytest`.

---

## Cấu Trúc Hiện Tại

```text
tests/
├── benchmark/
│   └── test_performance_benchmark.py  # Đo latency và FPS (3 tests)
├── integration/
│   └── test_api_detect.py             # API /detect integration tests (5 tests)
├── model/
│   ├── test_face_detector.py          # RetinaFace wrapper tests (2 tests)
│   └── test_segmentation.py           # U-Net segmenter wrapper tests (5 tests)
└── unit/
    └── test_face_quality.py           # Face quality logic unit tests (6 tests)
```

---

## Chi Tiết Từng Nhóm Test

### `tests/unit/` — Unit Tests (6 tests)

Kiểm tra logic thuần túy của `backend/quality/face_quality.py`:
- `check_face_size()`: Kích thước "Too Small" / "Normal" / "Large"
- `check_visibility()`: Tính % visibility từ binary mask
- `check_occlusion()`: Occlusion dựa trên visibility threshold
- `check_head_pose()`: Ước lượng Head Pose từ landmarks hình học
- `analyze_face_quality()`: Composite quality score và rating

### `tests/model/` — Model Tests (7 tests)

- **`test_face_detector.py`** (2 tests): Kiểm tra RetinaFace wrapper ONNX
  - Load model không throw exception
  - `detect()` trả về đúng cấu trúc `{box, confidence, landmarks}`
- **`test_segmentation.py`** (5 tests): Kiểm tra U-Net segmenter
  - `predict_batch()` với batch đơn/nhiều crops
  - Output mask shape và dtype

### `tests/integration/` — Integration Tests (5 tests)

Dùng `FastAPI TestClient` với `DummyDetector` (box 80×80px) và `DummySegmenter`:
- `test_root_endpoint_returns_html`: GET `/` trả về HTML
- `test_detect_with_invalid_image_returns_400`: Ảnh binary không hợp lệ → 400
- `test_detect_response_has_required_fields`: Kiểm tra JSON schema của response
- `test_detect_with_valid_image_returns_expected_structure`: 320×320px image → face_count ≥ 0
- `test_health_check`: GET `/health` → `{"status": "healthy"}`

> [!IMPORTANT]
> **Ghi chú SORT Tracker**: Với hit-streak gate (N≥2 confirmations), track mới chỉ hiện ra từ lần thứ 2 được detect. Do đó integration test chỉ assert `face_count >= 0`, không assert `>= 1` cho request đơn lẻ.

> [!NOTE]
> `DummyDetector` trả về box `[0, 0, 80, 80]` (80×80px) để đảm bảo vượt qua Geometric Filter (`MIN_FACE_PX = 36px`). Box cũ `[0, 0, 20, 20]` sẽ bị lọc bỏ bởi `is_valid_face_box()`.

### `tests/benchmark/` — Benchmark Tests (3 tests)

Đo hiệu năng end-to-end với ảnh thật hoặc ảnh synthetic:
- Latency < 500ms/frame với MobileNet
- FPS đạt ≥ 5 trong điều kiện CPU-only

---

## Chạy Test

```bash
# Chạy toàn bộ 21 tests
pytest

# Chạy từng nhóm riêng
pytest tests/unit
pytest tests/model
pytest tests/integration
pytest tests/benchmark

# Với verbose output
pytest -v

# Với coverage report
pytest --cov=backend --cov-report=term-missing
```

---

## Nguyên Tắc Test

- **Unit tests**: Không phụ thuộc model ONNX, chỉ test logic thuần Python.
- **Model tests**: Sử dụng model ONNX thật từ `backend/weights/`.
- **Integration tests**: Dùng `monkeypatch` để mock detector và segmenter, chỉ test API schema và routing.
- **DummyDetector box size**: Phải `>= MIN_FACE_PX (36px)` để vượt qua Geometric Filter của FaceTracker.
- **False positive behavior**: Bộ lọc hình học đang hoạt động đúng — không bao giờ assert `face_count >= 1` với ảnh đen trống.