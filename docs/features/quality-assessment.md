# Đánh giá chất lượng

## Mục đích
Đánh giá các khuôn mặt phát hiện được để hỗ trợ xem xét chất lượng, cảnh báo và quyết định giám sát.

## Đầu vào
- Hộp giới hạn của khuôn mặt được phát hiện
- Điểm độ tin cậy từ kết quả phát hiện
- Điểm mốc khuôn mặt từ kết quả phát hiện
- Mặt nạ phân đoạn của khuôn mặt được phát hiện

## Đầu ra
- Tỷ lệ hiển thị vùng khuôn mặt
- Chỉ báo về tình trạng che khuất
- Phân loại tư thế như bình thường, trái, phải, ngửa hoặc cúi
- Điểm chất lượng tổng hợp
- Xếp hạng chất lượng và nhãn trạng thái

## Phụ thuộc
- Kết quả phát hiện khuôn mặt
- Kết quả phân đoạn khuôn mặt
- Logic đánh giá chất lượng theo quy tắc

## API liên quan
- POST /detect

## Mô hình liên quan
- Mô hình RetinaFace
- Mô hình phân đoạn khuôn mặt U-Net
