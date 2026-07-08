# AI Pipeline

Pipeline AI của hệ thống được tổ chức theo ba bước chính: phát hiện, phân đoạn và đánh giá chất lượng.

## 1. Phát hiện khuôn mặt

- Input: ảnh đầu vào hoặc frame từ frontend.
- Mô hình: RetinaFace.
- Output: bounding box, confidence score và landmarks cho mỗi khuôn mặt phát hiện được.

## 2. Phân đoạn khuôn mặt

- Input: crop khuôn mặt từ ảnh gốc.
- Mô hình: U-Net.
- Output: binary mask biểu diễn khuôn mặt.

## 3. Đánh giá chất lượng

- Input: box, confidence, landmarks và mask.
- Logic: tính visibility, occlusion, pose, quality score và status.
- Output: kết quả đánh giá dùng để hiển thị và cảnh báo.

## Mối liên hệ giữa các bước

- Kết quả phát hiện là đầu vào cho phân đoạn.
- Kết quả phân đoạn và phát hiện cùng nhau tạo dữ liệu cho quality assessment.
- Tất cả kết quả được kết hợp trong một response JSON và image annotate để frontend dùng.
