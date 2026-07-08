# Backend Flow

Backend được triển khai bằng FastAPI và đóng vai trò là điểm trung tâm xử lý yêu cầu từ frontend.

## Luồng xử lý request

1. Khi nhận request POST /detect, backend đọc file ảnh được upload từ client.
2. Backend giải mã ảnh bằng OpenCV và chuyển đổi thành dữ liệu hình ảnh hợp lệ.
3. Backend chọn detector phù hợp theo tham số network.
4. Backend gọi detector để phát hiện các khuôn mặt và trả về box, confidence và landmarks.
5. Với từng face detection hợp lệ, backend chuẩn bị crop khuôn mặt và gửi vào segmenter để tạo binary mask.
6. Backend dùng kết quả mask và landmarks để tính toán chất lượng khuôn mặt.
7. Backend vẽ overlay lên ảnh gốc, tạo image đã annotate và trả về JSON chứa kết quả và ảnh base64.

## Thành phần chính

- FastAPI app: định nghĩa route / và /detect, mount /static.
- Detector cache: lưu instance RetinaFace theo network để giảm thời gian tải model.
- Segmenter cache: lưu instance U-Net để tái sử dụng giữa các request.
- Quality analyzer: chạy các hàm đánh giá visibility, occlusion, pose và quality score.

## Output chính của backend

- Ảnh đã annotate dưới dạng base64
- Số lượng khuôn mặt phát hiện
- Danh sách thông tin từng khuôn mặt
- Thời gian xử lý latency_ms

## Điểm cần lưu ý

Backend không thực hiện toàn bộ luồng qua một pipeline class riêng; thay vào đó, logic được tổ chức theo các module riêng biệt và phối hợp trong route /detect.
