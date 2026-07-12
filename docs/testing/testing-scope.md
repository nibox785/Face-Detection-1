# Phạm vi kiểm thử

Tài liệu này xác định phạm vi kiểm thử cho dự án phát hiện và phân đoạn khuôn mặt.

## Phạm vi trong

### 1. API và service layer
- Kiểm tra endpoint /detect trong [backend/main.py](../../backend/main.py)
- Xác nhận request và response đúng cấu trúc
- Xử lý lỗi khi upload ảnh không hợp lệ

### 2. AI inference layer
- Kiểm tra detector wrapper trong [backend/models/face_detector.py](../../backend/models/face_detector.py)
- Kiểm tra segmenter wrapper trong [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)
- Đảm bảo các output có thể dùng tiếp cho bước phân tích tiếp theo

### 3. Logic xử lý hậu kỳ
- Kiểm tra logic mask postprocessing trong [backend/segmentation/postprocess.py](../../backend/segmentation/postprocess.py)
- Kiểm tra logic đánh giá chất lượng trong [backend/quality/face_quality.py](../../backend/quality/face_quality.py)

### 4. Luồng pipeline tổng thể
- Kiểm tra từ ảnh đầu vào đến result trả về cho frontend
- Đảm bảo fallback hoạt động đúng khi segmenter hoặc detector gặp lỗi

## Phạm vi ngoài

- Huấn luyện mô hình
- Đánh giá độ chính xác trên dataset lớn như FDDB hoặc WIDER FACE
- Giao diện frontend
- Tuning hiệu năng thấp mức kernel hoặc ONNX runtime

## Nguyên tắc phạm vi

- Kiểm thử tập trung vào “độ tin cậy hệ thống” hơn là “độ chính xác mô hình” ở mức nghiên cứu.
- Các bài kiểm thử nên phản ánh những rủi ro thực tế của service production.
- Mỗi mức test cần có mục tiêu rõ ràng và không chồng chéo quá mức.
