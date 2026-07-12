# Kiến trúc kiểm thử

Tài liệu này mô tả cách tổ chức kiểm thử cho hệ thống phát hiện và phân đoạn khuôn mặt trong repository này.

## Mục tiêu kiến trúc

- Bảo vệ luồng xử lý chính từ ảnh đầu vào đến kết quả trả về.
- Tách rõ các lớp kiểm thử theo mức độ độ phức tạp và mức độ phụ thuộc.
- Giảm rủi ro khi thay đổi detector, segmenter, quality assessment hoặc API.

## Các lớp kiểm thử

### 1. Unit test

Kiểm tra các thành phần logic độc lập, không cần chạy full pipeline.

Các vùng ưu tiên:
- logic đánh giá chất lượng khuôn mặt trong [backend/quality/face_quality.py](../../backend/quality/face_quality.py)
- logic chuyển đổi mask sang dạng binary trong [backend/segmentation/postprocess.py](../../backend/segmentation/postprocess.py)
- logic mã hóa mask RLE trong [backend/main.py](../../backend/main.py)
- các helper xử lý box, landmark và NMS nếu có trong thư mục [backend/utils](../../backend/utils)

### 2. Component test

Kiểm tra giao diện giữa các module và các wrapper chạy mô hình.

Các thành phần chính:
- [backend/models/face_detector.py](../../backend/models/face_detector.py)
- [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)

Mục tiêu là xác nhận các wrapper mô hình:
- nhận đầu vào đúng định dạng
- trả về output đúng shape và kiểu dữ liệu
- xử lý fallback khi inference không thành công

### 3. Integration test

Kiểm tra tương tác giữa API, backend service và các thành phần AI.

Đối tượng chính:
- endpoint /detect trong [backend/main.py](../../backend/main.py)
- luồng nhận file ảnh, chạy detector, segmenter, quality assessment và trả response

### 4. Pipeline test

Kiểm tra toàn bộ quy trình từ đầu vào ảnh đến kết quả phân tích cuối cùng.

Luồng cần bảo vệ:
1. Nhận ảnh đầu vào.
2. Chạy detector.
3. Chạy segmenter nếu phát hiện face hợp lệ.
4. Tính quality metrics.
5. Trả về response cho frontend.

### 5. Regression test

Bảo vệ các trường hợp đã từng gặp lỗi hoặc dễ bị tái diễn trong quá trình phát triển.

Ví dụ:
- ảnh không có khuôn mặt
- box quá nhỏ
- segmenter thất bại
- input không hợp lệ
- model không tồn tại hoặc load lỗi

### 6. Benchmark test

Đánh giá hiệu năng và độ ổn định về thời gian xử lý.

Các chỉ số cần quan sát:
- latency trung bình
- thời gian xử lý detector
- thời gian xử lý segmenter
- mức tiêu thụ bộ nhớ

## Vai trò trách nhiệm

- Backend team: chịu trách nhiệm cho unit, component và integration test.
- AI/ML team: đảm bảo các expectation về output model và giới hạn của mô hình.
- DevOps/Platform: đảm bảo môi trường CI, dependency và dữ liệu test sẵn sàng.
- QA/release owner: giám sát regression và benchmark ở mức release.

## Luồng kiểm thử đề xuất

```text
Input ảnh
→ Validate request
→ Detector wrapper
→ Segmentation wrapper
→ Quality assessment
→ Response formatting
→ Verification / report
```

## Phụ thuộc kiểm thử

- FastAPI và Uvicorn cho API
- OpenCV, NumPy, Pillow cho preprocessing
- PyTorch và ONNX Runtime cho inference
- Dữ liệu hình ảnh mẫu và model weights
- pytest và các thư viện hỗ trợ test HTTP

## Sản phẩm kiểm thử

- test suite theo từng lớp
- fixture ảnh mẫu
- báo cáo kết quả
- baseline benchmark cho performance
- danh sách regression case đã bảo vệ
