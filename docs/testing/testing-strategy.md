# Chiến lược kiểm thử

Tài liệu này mô tả cách kiểm thử phù hợp với repository hiện tại.

## Mục tiêu

- Kiểm tra các tính năng cốt lõi đã triển khai: nhận diện khuôn mặt, phân đoạn khuôn mặt, đánh giá chất lượng và luồng xử lý media.
- Đảm bảo các script huấn luyện và đánh giá mô hình vẫn có thể chạy đúng với dữ liệu và model hiện có.
- Duy trì khả năng kiểm tra regression khi thay đổi logic phát hiện hoặc quality assessment.

## Phạm vi kiểm thử hiện tại

Repository hiện có các thư mục test nhưng chưa triển khai đầy đủ các test case thực thi bằng pytest. Các script kiểm thử hiện hữu chủ yếu là các script đánh giá mô hình như:

- [backend/test_widerface.py](../../backend/test_widerface.py)
- [backend/test_fddb.py](../../backend/test_fddb.py)

Do đó, chiến lược kiểm thử nên được chia thành các tầng:

1. Unit test cho các hàm logic nhỏ và helper.
2. Model test cho detector và segmenter.
3. Integration test cho endpoint /detect và luồng backend-frontend cơ bản.
4. Pipeline test cho các quy trình từ input ảnh đến output kết quả.
5. Regression test cho các trường hợp đã biết và cần bảo vệ.
6. Benchmark test để đánh giá thời gian và hiệu năng.

## Khuyến nghị triển khai

- Bắt đầu bằng unit test cho các hàm độc lập như face quality và mask encoding.
- Sau đó bổ sung integration test cho FastAPI endpoint bằng file ảnh mẫu.
- Cuối cùng mới mở rộng sang benchmark và regression khi có dữ liệu mẫu ổn định.
