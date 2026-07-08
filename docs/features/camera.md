# Nhận dữ liệu từ camera và phương tiện

## Mục đích
Hỗ trợ quy trình giám sát từ nhiều nguồn phương tiện bằng cách chấp nhận ảnh tĩnh, video tải lên và đầu vào camera trực tiếp.

## Đầu vào
- Tệp ảnh được tải lên
- Tệp video được tải lên
- Luồng webcam trực tiếp từ trình duyệt
- Tùy chọn xử lý do người dùng chọn như backbone mạng và ngưỡng phát hiện

## Đầu ra
- Khung hiển thị với media trực tiếp hoặc được tải lên
- Chú thích chồng lên khung hình đang hiển thị
- Số liệu theo thời gian như số khuôn mặt phát hiện, độ trễ và FPS
- Tài liệu xuất bằng chứng như khung hình hoặc crop đã lưu

## Phụ thuộc
- Xử lý media ở frontend trong trình duyệt
- Endpoint phát hiện ở backend để phân tích khung hình
- Hỗ trợ truy cập camera và video từ trình duyệt

## API liên quan
- POST /detect

## Mô hình liên quan
- Mô hình RetinaFace
- Mô hình phân đoạn khuôn mặt U-Net
