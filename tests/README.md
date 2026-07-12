# Test Suite

## Purpose

Thư mục này chứa toàn bộ mã nguồn kiểm thử cho hệ thống phát hiện và phân đoạn khuôn mặt.

Chiến lược kiểm thử được mô tả rõ hơn tại [docs/testing](../docs/testing/README.md).

---

## Nguyên tắc triển khai

Các test nên được tổ chức theo từng lớp và mỗi lớp có mục tiêu rõ ràng:

- Unit test: kiểm tra logic thuần túy, không phụ thuộc mô hình đầy đủ.
- Model test: kiểm tra wrapper mô hình và giao diện đầu vào/đầu ra.
- Integration test: kiểm tra API và luồng giữa các module.
- Pipeline test: kiểm tra luồng end-to-end từ ảnh đầu vào đến response cuối cùng.
- Regression test: bảo vệ các tình huống lỗi đã từng gặp hoặc dễ tái diễn.
- Benchmark test: đo hiệu năng khi cần, không phải là bước đầu tiên.

Không nên dùng mock cho toàn bộ hệ thống. Mock chỉ nên dùng ở rìa, ví dụ khi cần thay thế model session hoặc IO boundary.

---

## Cấu trúc đề xuất

```text
tests/
├── unit/              # Logic độc lập: quality scoring, mask logic, box utils
├── model/             # Wrapper detector/segmenter, model load, inference contract
├── integration/       # API /detect, request/response, FastAPI interaction
├── pipeline/          # Luồng đầy đủ từ ảnh -> detector -> segmenter -> quality -> response
├── regression/        # Các trường hợp lỗi trước đây, fallback, empty input, tiny box
├── benchmark/         # Optional performance / latency checks
├── fixtures/          # Ảnh mẫu, dữ liệu giả lập, file nhỏ dùng chung
└── conftest.py        # Fixtures và setup chung (nếu có)
```

---

## Mức ưu tiên triển khai

### Giai đoạn 1: nền tảng
- Thiết lập pytest, pytest-cov, pytest-html.
- Tạo cấu trúc thư mục và fixture chung.
- Bắt đầu với unit test cho các hàm logic cốt lõi.

### Giai đoạn 2: bảo vệ luồng chính
- Viết model test cho detector và segmenter.
- Viết integration test cho endpoint /detect.

### Giai đoạn 3: bảo vệ rủi ro
- Thêm regression test cho các trường hợp không có face, box quá nhỏ, segmentation lỗi, input không hợp lệ.

### Giai đoạn 4: hiệu năng
- Thêm benchmark test khi hệ thống đã ổn định.

---

## Các file test nên có tên như thế nào

- Tên file nên phản ánh module hoặc luồng đang test.
- Ví dụ:
  - test_face_quality.py
  - test_postprocess.py
  - test_face_detector.py
  - test_api_detect.py
  - test_pipeline_detect.py

---

## Dữ liệu test

- Nên dùng ảnh mẫu nhỏ và ổn định trong [tests/fixtures](fixtures/).
- Có thể dùng ảnh thật và ảnh synthetic.
- Nên phân biệt giữa dữ liệu dùng cho unit test và dữ liệu dùng cho integration/pipeline test.

---

## Chạy test

```bash
pytest
```

Chạy từng nhóm:

```bash
pytest tests/unit
```

```bash
pytest tests/model
```

```bash
pytest tests/integration
```

```bash
pytest tests/pipeline
```

```bash
pytest tests/regression
```

```bash
pytest tests/benchmark
```

---

## Khuyến nghị thực tế cho dự án này

Vì hệ thống có cả AI inference và API, cách test hợp lý nhất là:

1. Đầu tiên test các logic thuần túy.
2. Sau đó test các wrapper mô hình.
3. Tiếp đến test endpoint /detect.
4. Cuối cùng mới mở rộng sang regression và benchmark.

Điều này giúp giảm rủi ro sớm, giữ test chạy nhanh và dễ debug hơn.