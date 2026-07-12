# Inference Log

## Mục đích

Tài liệu này mô tả schema của log inference runtime cho backend AI face surveillance.
Nó giúp giữ traceability giữa request `/detect`, metric benchmark và kết quả inference.

## File log

Inference log được ghi vào:

- `logs/inference/inference.log`

Mỗi dòng là một JSON object mô tả một event inference hoặc một request `/detect` hoàn thành.

## Schema record

Mỗi record có các trường tối thiểu sau:

- `timestamp`: thời điểm event được ghi (UTC ISO format)
- `level`: log level (`INFO` cho các inference event bình thường)
- `message`: giá trị cố định `inference_event`
- `event`: loại event, ví dụ `detect_completed`
- `request_id`: định danh request duy nhất
- `model`: backbone đang sử dụng (`mobile0.25` hoặc `resnet50`)
- `stage`: tầng pipeline, ví dụ `pipeline`
- `face_count`: số face được phát hiện
- `latency_ms`: tổng độ trễ xử lý request
- `fps`: tốc độ quy đổi từ latency
- `status`: trạng thái xử lý (`ok` hoặc lỗi)
- `extra`: đối tượng bổ sung chứa những tham số đầu vào và flags

## Mô tả trường

- `timestamp`: định dạng ISO 8601 UTC, dùng để đồng bộ với logs khác.
- `request_id`: key chính để liên kết logs với response frontend và report.
- `model`: thể hiện backbone detector được dùng trong lần inference.
- `stage`: chỉ ra tầng xử lý. Hiện backend dùng giá trị `pipeline` cho request `/detect`.
- `face_count`: số face candidate cuối cùng trong response.
- `latency_ms`: tổng thời gian backend dùng cho request, tính từ khi nhận ảnh đến khi trả response.
- `fps`: tốc độ tương đương, tính bằng `1000 / max(latency_ms, 1)`.
- `extra`: chứa các tham số đầu vào như `threshold`, `draw_mask`, `upscale`, `save_report`.

## Ví dụ record

```json
{
  "timestamp": "2026-07-13T10:30:00Z",
  "level": "INFO",
  "message": "inference_event",
  "event": "detect_completed",
  "request_id": "e9a7d19f-8c3d-4f62-ab78-0c1e2f3d4b5a",
  "model": "mobile0.25",
  "stage": "pipeline",
  "face_count": 2,
  "latency_ms": 132,
  "fps": 7.58,
  "status": "ok",
  "extra": {
    "threshold": 0.5,
    "draw_mask": false,
    "upscale": false,
    "save_report": false
  }
}
```

## Quan hệ với response `/detect`

Backend `/detect` trả về đồng thời trường `request_id`, `latency_ms`, `fps`, `face_count`, `network`, và `status`.
Điều này cho phép frontend hoặc hệ thống kiểm thử đối chiếu trực tiếp response với log entry tương ứng.

## Cách sử dụng

- Dùng `request_id` để tra ngược event log tương ứng.
- Dùng `latency_ms` cùng `fps` để xác định bottleneck trên request.
- Dùng `face_count` để kiểm tra bất thường trong pipeline phát hiện.
- Dùng `extra` để hiểu cấu hình request khi đánh giá chất lượng kết quả.
