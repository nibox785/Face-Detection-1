# Integration Testing

Integration test nên kiểm tra luồng end-to-end giữa frontend, API và backend inference.

## Scope

- Kiểm tra endpoint /detect có thể nhận file ảnh và trả về response hợp lệ.
- Kiểm tra backend có thể tạo ảnh annotate, face_count và danh sách faces.
- Kiểm tra kết quả trả về có đủ trường cần thiết cho frontend hiển thị.

## Các thành phần cần kiểm tra

- FastAPI route /detect trong [backend/main.py](../../backend/main.py)
- Mô hình detector và segmenter được load đúng
- Response chứa ít nhất:
  - image
  - face_count
  - faces
  - latency_ms

## Test case đề xuất

1. Gửi một ảnh hợp lệ tới /detect.
2. Xác nhận response status code là 200.
3. Xác nhận face_count là số nguyên.
4. Xác nhận faces là danh sách.
5. Xác nhận mỗi face có box, confidence và landmarks.

## Ghi chú

Hiện tại thư mục [tests/integration](../../tests/integration) còn trống. Đây là nơi thích hợp để triển khai các test HTTP đầu tiên.
