# Benchmark Testing

Benchmark test dùng để theo dõi hiệu năng xử lý của detector và toàn bộ pipeline.

## Mục tiêu

- Đo thời gian xử lý cho ảnh đơn lẻ.
- Đo thời gian cho video/webcam frame loop.
- Theo dõi mức độ tải CPU và độ trễ trung bình.

## Khu vực phù hợp

- Thời gian inference detector.
- Thời gian chạy segmenter.
- Tổng latency_ms trả về từ /detect.

## Gợi ý triển khai

- Dùng một tập ảnh mẫu nhỏ và lặp lại nhiều lần.
- Ghi nhận latency trung bình và p95 nếu cần.
- Đánh giá riêng cho từng backbone MobileNet và ResNet50.
