# Unit Testing

Unit test nên tập trung vào các phần logic có thể kiểm tra độc lập mà không cần chạy toàn bộ mô hình.

## Các khu vực nên test

- Logic đánh giá chất lượng khuôn mặt trong [backend/quality/face_quality.py](../../backend/quality/face_quality.py)
  - kiểm tra visibility computation
  - kiểm tra occlusion logic
  - kiểm tra pose classification
  - kiểm tra quality score và rating
- Logic mã hóa mask RLE trong [backend/main.py](../../backend/main.py)
- Logic chuẩn hóa và xử lý box trong các helper nếu có.

## Ví dụ test case đề xuất

- Với mask rỗng, visibility phải bằng 0.
- Với box có kích thước rất nhỏ, quality status phải là Face Too Small.
- Với landmarks không đủ dài, head pose phải trả về Normal.
- Với một mask có diện tích lớn trong box, visibility tính ra phải gần 100%.

## Ghi chú

Hiện tại thư mục [tests/unit](../../tests/unit) còn trống, nên đây là nơi phù hợp để bắt đầu xây dựng test suite thực tế.
