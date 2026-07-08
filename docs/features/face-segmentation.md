# Phân đoạn khuôn mặt

## Mục đích
Tách vùng khuôn mặt khỏi ảnh xung quanh để tạo mặt nạ có thể dùng cho phân tích chi tiết và hiển thị.

## Đầu vào
- Một vùng cắt khuôn mặt được phát hiện từ ảnh hoặc khung hình đầu vào
- Vùng khuôn mặt được xác định bởi mô hình phát hiện

## Đầu ra
- Mặt nạ phân đoạn nhị phân cho vùng khuôn mặt
- Mặt nạ có thể được chồng lên ảnh
- Mặt nạ phù hợp cho phân tích chất lượng và xuất bằng chứng tiếp theo

## Phụ thuộc
- Kết quả phát hiện khuôn mặt
- Mô hình phân đoạn U-Net
- Các bước thay đổi kích thước và chuẩn hóa ảnh

## API liên quan
- POST /detect

## Mô hình liên quan
- Mô hình phân đoạn khuôn mặt U-Net
