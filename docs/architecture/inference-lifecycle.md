# Sequence

## Chuỗi hoạt động chính

1. Người dùng chọn nguồn media trên frontend.
2. Frontend thu thập frame và gửi tới endpoint /detect.
3. Backend đọc và giải mã frame.
4. Backend chọn detector và thực hiện phát hiện khuôn mặt.
5. Backend chuẩn bị crop và chạy segmenter.
6. Backend tính quality metrics.
7. Backend trả về ảnh annotate và dữ liệu khuôn mặt.
8. Frontend vẽ overlay và cập nhật giao diện.

## Mô tả theo dạng câu chuyện

- Khi xử lý ảnh tĩnh, flow bắt đầu từ file upload và kết thúc bằng response hiển thị trên canvas.
- Khi xử lý webcam hoặc video, flow lặp liên tục trên nhiều frame, cho phép giám sát thời gian thực.
- Khi người dùng bấm export, frontend dùng dữ liệu hiện có để tạo frame, crop, mask và metadata JSON.
