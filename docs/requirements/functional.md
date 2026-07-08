# Functional Requirements

Các yêu cầu chức năng dưới đây được suy ra từ các file hiện có trong repository.

## 1. Khởi chạy hệ thống
1. Hệ thống phải có thể khởi chạy từ [run.py](../../run.py) để bắt đầu backend và phục vụ giao diện web.
2. Khi khởi chạy, hệ thống phải kiểm tra sự tồn tại của các file model ONNX và tự động tải nếu thiếu.

## 2. Xử lý ảnh đầu vào
1. Backend phải nhận file ảnh qua endpoint POST /detect trong [backend/main.py](../../backend/main.py).
2. Backend phải đọc và giải mã ảnh đầu vào bằng OpenCV.
3. Backend phải xử lý ảnh đầu vào thành dữ liệu có thể đưa vào mô hình phát hiện khuôn mặt.

## 3. Phát hiện khuôn mặt
1. Backend phải sử dụng mô hình RetinaFace để phát hiện khuôn mặt từ ảnh đầu vào.
2. Backend phải trả về bounding box cho mỗi khuôn mặt phát hiện được.
3. Backend phải trả về confidence score cho mỗi phát hiện.
4. Backend phải trả về 5 landmarks cho mỗi phát hiện.
5. Backend phải áp dụng NMS để loại bỏ các hộp chồng lặp.
6. Backend phải hỗ trợ chọn backbone detector là MobileNet hoặc ResNet50.

## 4. Phân đoạn khuôn mặt
1. Backend phải sử dụng mô hình U-Net để tạo mặt nạ phân vùng cho từng khuôn mặt phát hiện được.
2. Backend phải tạo binary mask có giá trị 0/255 từ đầu ra logits của mô hình segmenter.
3. Backend phải có thể tạo mask cho nhiều face crop trong một batch.

## 5. Đánh giá chất lượng khuôn mặt
1. Backend phải tính toán độ visibility của mặt nạ trong bounding box.
2. Backend phải xác định trạng thái có bị che khuất hay không.
3. Backend phải ước lượng pose dựa trên landmarks.
4. Backend phải tính quality score và rating từ các chỉ số trên.

## 6. Trả kết quả cho frontend
1. Backend phải trả về một ảnh đã được annotate dưới dạng base64.
2. Backend phải trả về số lượng khuôn mặt phát hiện được.
3. Backend phải trả về danh sách thông tin từng khuôn mặt, bao gồm box, confidence, landmarks, mask, quality metrics và face crop alpha image.

## 7. Giao diện người dùng
1. Frontend phải cho phép người dùng chọn nguồn dữ liệu là ảnh tĩnh, video hoặc webcam.
2. Frontend phải hiển thị hình ảnh/video/webcam trong viewport chính.
3. Frontend phải vẽ overlay gồm bounding box, landmarks và mask trên canvas.
4. Frontend phải hỗ trợ bật/tắt các loại overlay qua checkbox.
5. Frontend phải hiển thị các chỉ số như số khuôn mặt, latency, FPS và mật độ đám đông.
6. Frontend phải hiển thị biểu đồ chất lượng khuôn mặt, pose và lịch sử phát hiện.
7. Frontend phải hiển thị nhật ký cảnh báo và phát âm thanh cảnh báo khi có điều kiện phù hợp.

## 8. Xuất bằng chứng
1. Frontend phải cho phép lưu khung hình đã annotate.
2. Frontend phải cho phép lưu các face crop có alpha.
3. Frontend phải cho phép tạo snapshot gồm frame, crop, mask và metadata JSON.
4. Frontend phải cho phép xuất dữ liệu JSON và toàn bộ mask.
