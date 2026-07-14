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

## Response metric và logging đồng bộ

Khi `/detect` trả về, backend hiện bao gồm các trường benchmark cơ bản:

- `latency_ms`: tổng độ trễ của request
- `fps`: tốc độ quy đổi từ latency
- `face_count`: số face phát hiện
- `request_id`: định danh request duy nhất
- `network`: backbone detector đang sử dụng
- `status`: trạng thái xử lý

Đồng thời backend ghi structured log event cho mỗi request vào `logs/inference/inference.log` theo schema JSON.

### Lệnh benchmark runner

Một cách đo benchmark tự động là dùng module runner:

```bash
python -m backend.benchmark.runner --mode pipeline --repeat 10 --network mobile0.25 --image path/to/sample.jpg
```

Kết quả benchmark sẽ được ghi vào `logs/benchmark/benchmark.log` và tổng hợp báo cáo vào `reports/benchmark/`.
