# Acceptance Criteria

Các tiêu chí chấp nhận dưới đây dựa trên hành vi hiện có của hệ thống.

## 1. Khởi động
1. Chạy [run.py](../../run.py) phải khởi động backend và phục vụ giao diện web trên cổng 5000.
2. Truy cập root endpoint phải trả về giao diện frontend.

## 2. Phát hiện khuôn mặt
1. Gửi một file ảnh hợp lệ tới endpoint /detect phải trả về JSON chứa field face_count.
2. Phản hồi phải chứa danh sách faces với thông tin box, confidence, landmarks và các metrics chất lượng.
3. Khi không phát hiện khuôn mặt, phản hồi phải báo face_count bằng 0 và danh sách faces rỗng.

## 3. Chọn backbone
1. Khi chọn network mobile0.25 hoặc resnet50, hệ thống phải sử dụng đúng mô hình detector tương ứng.

## 4. Frontend
1. Frontend phải cho phép chuyển đổi giữa ảnh tĩnh, video và webcam.
2. Frontend phải vẽ overlay và cập nhật dữ liệu trên bảng điều khiển sau khi nhận phản hồi từ backend.
3. Frontend phải cho phép người dùng bật/tắt các overlay và thay đổi ngưỡng tin cậy.

## 5. Export và evidence
1. Frontend phải cho phép lưu frame, face crop và snapshot evidence.
2. Frontend phải cho phép xuất dữ liệu JSON và mask.

## 6. Model loading
1. Nếu các file model ONNX đã có, hệ thống phải load chúng từ [backend/weights](../../backend/weights).
2. Nếu thiếu model, hệ thống phải cố gắng tải chúng trước khi khởi động inference.
