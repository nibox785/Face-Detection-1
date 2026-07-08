# Tổng quan hệ thống

Hệ thống được triển khai như một ứng dụng web giám sát khuôn mặt bằng trí tuệ nhân tạo, chạy trên một backend FastAPI và một frontend tĩnh. Người dùng tương tác qua trình duyệt, gửi ảnh hoặc khung hình video vào backend, backend gọi mô hình phát hiện và phân đoạn, sau đó trả lại kết quả đã annotate để frontend hiển thị và lưu trữ bằng chứng.

## Cấu trúc triển khai

- Backend chính nằm ở [backend/main.py](backend/main.py). File này tạo FastAPI app, phục vụ route gốc, route /detect và mount tài nguyên tĩnh frontend.
- Logic phát hiện khuôn mặt nằm ở [backend/models/face_detector.py](backend/models/face_detector.py).
- Logic phân đoạn khuôn mặt nằm ở [backend/models/face_segmenter.py](backend/models/face_segmenter.py).
- Logic đánh giá chất lượng nằm ở [backend/quality/face_quality.py](backend/quality/face_quality.py).
- Frontend UI và vòng lặp xử lý media nằm ở [frontend/index.html](frontend/index.html) và [frontend/js/app.js](frontend/js/app.js).
- Khởi chạy hệ thống được thực hiện bởi [run.py](run.py), nơi kiểm tra và tải model ONNX nếu thiếu.

## Vai trò của từng lớp

- Presentation layer: frontend hiển thị viewport, overlay, biểu đồ và nút xuất bằng chứng.
- API layer: backend nhận request, chuẩn hóa input và trả về kết quả JSON plus hình ảnh annotate.
- AI layer: RetinaFace phát hiện khuôn mặt, U-Net phân đoạn mặt nạ, logic chất lượng đánh giá face quality.
- Supporting layer: file export, telemetry, cảnh báo âm thanh, cache mô hình.

## Luồng vận hành tổng thể

1. Frontend thu thập frame từ ảnh, video hoặc webcam.
2. Frontend gửi frame tới endpoint /detect.
3. Backend giải mã ảnh, gọi detector, tạo mask và đánh giá chất lượng.
4. Backend trả về ảnh đã annotate và danh sách thông tin khuôn mặt.
5. Frontend vẽ overlay, cập nhật biểu đồ và cung cấp chức năng lưu trữ bằng chứng.

## Mô tả sơ đồ thành phần

Các thành phần chính có thể được hiểu như sau:

- Client UI: quản lý nguồn media và hiển thị kết quả.
- API Server: nhận request và điều phối xử lý.
- Detector Service: thực hiện phát hiện khuôn mặt.
- Segmenter Service: thực hiện phân vùng khuôn mặt.
- Quality Analyzer: đánh giá độ visibility, occlusion, pose và quality score.
- Export/Telemetry: lưu frame, crop, mask và ghi log cảnh báo.
