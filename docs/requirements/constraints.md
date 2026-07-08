# Constraints

Các ràng buộc sau được suy ra từ hiện trạng triển khai.

## 1. Ràng buộc công nghệ
1. Backend hiện tại phụ thuộc vào Python và các thư viện trong [requirements.txt](../../requirements.txt).
2. Runtime inference sử dụng ONNX Runtime cho các mô hình ONNX.
3. Frontend hiện tại là giao diện tĩnh bằng HTML/CSS/JavaScript, không dùng framework frontend.

## 2. Ràng buộc model
1. Backend hiện tại phụ thuộc vào các file model ONNX có tên: mobilenet0.25_Final.onnx, Resnet50_Final.onnx và unet_face_celeb.onnx.
2. Nếu model chưa có trong [backend/weights](../../backend/weights), hệ thống sẽ cố gắng tải từ GitHub Releases khi chạy [run.py](../../run.py).

## 3. Ràng buộc input
1. Endpoint /detect hiện tại nhận một file ảnh duy nhất trong mỗi request.
2. Webcam mode phụ thuộc vào quyền truy cập camera của trình duyệt.
3. Video mode phụ thuộc vào file video cục bộ được tải lên bởi người dùng.

## 4. Ràng buộc dữ liệu huấn luyện
1. Pipeline huấn luyện hiện tại dựa trên dữ liệu WIDER Face và FDDB như thể hiện trong các script đánh giá.
2. Pipeline segmentation có liên quan tới dữ liệu CelebAMask-HQ theo mô tả trong README.
