# Assumptions

Các giả định dưới đây được rút ra từ bằng chứng triển khai hiện có.

1. Người dùng có thể cung cấp ảnh hoặc file video hợp lệ để hệ thống xử lý.
2. Khi sử dụng webcam, trình duyệt sẽ cho phép truy cập camera.
3. Các file mô hình ONNX sẽ có sẵn tại [backend/weights](../../backend/weights) hoặc có thể tải về từ GitHub Releases.
4. Backend sẽ chạy trong môi trường có cài đặt đầy đủ các dependency được liệt kê trong [requirements.txt](../../requirements.txt).
5. Mô hình U-Net và RetinaFace được coi là các mô hình runtime chính trong luồng inference hiện tại.
6. Frontend sẽ được phục vụ bởi backend qua các static files và route /static.
