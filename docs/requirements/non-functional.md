# Non-Functional Requirements

Các yêu cầu phi chức năng dưới đây được suy ra từ cách triển khai hiện tại.

## 1. Công nghệ và môi trường
1. Hệ thống phải chạy trên nền tảng Python với các thư viện được liệt kê trong [requirements.txt](../../requirements.txt).
2. Backend phải sử dụng FastAPI và Uvicorn để phục vụ API.
3. Mô hình inference phải sử dụng ONNX Runtime trong luồng runtime hiện tại.
4. Frontend phải chạy trên trình duyệt hỗ trợ HTML, Canvas và WebRTC.

## 2. Hiệu suất và vòng đời xử lý
1. Hệ thống phải cung cấp phản hồi thời gian thực hoặc gần thời gian thực cho image/video/webcam input thông qua vòng lặp xử lý trên frontend.
2. Backend phải trả về latency_ms cho mỗi lần xử lý ảnh.
3. Frontend phải hiển thị FPS và latency để người dùng theo dõi.

## 3. Dễ bảo trì
1. Backend phải được tổ chức theo các module rõ ràng: models, quality, segmentation, utils, data.
2. Frontend phải được tách thành file HTML, CSS và JavaScript riêng biệt.

## 4. Khả năng mở rộng và tái sử dụng
1. Backend phải hỗ trợ cache các instance detector và segmenter để tránh tải lại mô hình cho mỗi request.
2. Mô hình detector phải có thể chọn giữa hai cấu hình backbone khác nhau.
