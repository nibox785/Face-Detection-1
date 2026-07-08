# Pipeline Testing

Pipeline testing tập trung vào toàn bộ quy trình xử lý từ đầu vào hình ảnh đến output phân tích.

## Quy trình cần bảo vệ

1. Nhận ảnh đầu vào.
2. Chạy detector để tìm khuôn mặt.
3. Nếu có face hợp lệ, chạy segmenter.
4. Tính quality metrics.
5. Trả về response gồm image annotate và dữ liệu face.

## Mục tiêu kiểm thử

- Đảm bảo nếu detector không phát hiện face thì không xảy ra lỗi trong bước segmenter.
- Đảm bảo nếu segmenter thất bại thì hệ thống vẫn có fallback và trả về response.
- Đảm bảo output có cấu trúc nhất quán cho frontend.

## Test case đề xuất

- Với ảnh không có mặt, response phải có face_count = 0.
- Với ảnh có một khuôn mặt rõ, response phải có ít nhất một face entry.
- Với ảnh có nhiều khuôn mặt, response phải phản ánh đúng số lượng.
