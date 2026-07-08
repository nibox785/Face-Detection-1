# Nhận diện khuôn mặt

## Mục đích
Xác định các khuôn mặt người có trong ảnh đầu vào hoặc khung hình video để có thể được đánh dấu, đếm và phân tích tiếp.

## Đầu vào
- Tệp ảnh được tải lên
- Khung hình video được cung cấp bởi vòng lặp xử lý ở frontend
- Khung hình webcam được chụp từ trình duyệt
- Ngưỡng độ tin cậy do người dùng cấu hình

## Đầu ra
- Danh sách các khuôn mặt được phát hiện
- Hộp giới hạn cho từng khuôn mặt
- Điểm độ tin cậy cho mỗi phát hiện
- Năm điểm mốc khuôn mặt cho mỗi phát hiện
- Tổng số khuôn mặt phát hiện trong phản hồi hiện tại

## Phụ thuộc
- Xử lý giải mã và tiền xử lý ảnh ở backend
- Quy trình phát hiện dựa trên RetinaFace
- Loại bỏ hộp trùng bằng thuật toán non-maximum suppression

## API liên quan
- POST /detect

## Mô hình liên quan
- Mô hình RetinaFace
- Phiên bản dựa trên MobileNet
- Phiên bản dựa trên ResNet50
