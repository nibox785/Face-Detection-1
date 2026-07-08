# Frontend Analysis

Tài liệu tạm thời này mô tả tổng quan về frontend của dự án Face Detection.

## Tổng quan

Frontend là một dashboard giám sát khuôn mặt chạy trên trình duyệt. Nó cho phép người dùng:
- chọn nguồn dữ liệu ảnh/video/webcam
- xem luồng hình ảnh trực tiếp
- xem các kết quả nhận diện trực quan trên canvas
- theo dõi thống kê và cảnh báo

## Luồng ứng dụng

1. Trang web được load từ [frontend/index.html](../../frontend/index.html).
2. Script [frontend/js/app.js](../../frontend/js/app.js) khởi tạo UI, charts, clock và các event listener.
3. Người dùng chọn một nguồn dữ liệu.
4. Frontend thu thập frame từ source đang chọn và gửi tới backend qua endpoint /detect.
5. Kết quả nhận diện được dùng để vẽ overlay, cập nhật bảng mục tiêu và biểu đồ.

## Luồng camera

### Ảnh tĩnh
- Người dùng chọn một file ảnh.
- Ảnh được gửi một lần tới backend.
- Kết quả được hiển thị trên ảnh.

### Webcam
- Frontend yêu cầu quyền truy cập camera.
- Frame được chụp liên tục và gửi tới backend theo vòng lặp.

### Video
- Người dùng tải file video cục bộ.
- Frontend phát video và lấy frame theo thời gian thực.
- Các frame được xử lý liên tiếp.

## Giao tiếp API

Frontend giao tiếp bằng fetch với endpoint /detect, dùng multipart FormData với các trường:
- image
- network
- threshold
- draw_mask
- upscale

Phản hồi từ backend chứa thông tin về các face detected, confidence, landmarks và chất lượng.

## Các module UI chính

- Header và telemetry: FPS, độ trễ, thời gian, trạng thái hệ thống
- Viewport: hiển thị media và overlay annotations
- Face gallery: danh sách các mục tiêu phát hiện
- Alert log panel: nhật ký cảnh báo
- Control panel: nguồn dữ liệu, ngưỡng tin cậy, lựa chọn backbone, chế độ hiển thị
- Charts: chất lượng khuôn mặt, head pose, lịch sử phát hiện
- Evidence tools: lưu frame, lưu face crops, snapshot và export dữ liệu

## Ghi chú

Giao diện được xây dựng thủ công bằng HTML/CSS/JavaScript thuần, không dùng framework frontend như React.
