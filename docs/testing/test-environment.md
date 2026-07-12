# Môi trường kiểm thử

Tài liệu này mô tả môi trường cần thiết để thực hiện các lớp kiểm thử cho hệ thống.

## Môi trường phát triển

- Python 3.9+ hoặc phiên bản tương thích với requirements hiện tại
- Cài đặt các dependency từ [requirements.txt](../../requirements.txt)
- Môi trường local có thể chạy CPU cho hầu hết test

## Môi trường CI

- Runner Linux hoặc Windows phù hợp với repository
- Cài đặt đầy đủ các package backend
- Có thể chạy test không cần GPU

## Thành phần cần có

- FastAPI và Uvicorn
- OpenCV, NumPy, Pillow
- PyTorch và ONNX Runtime
- pytest và các plugin hỗ trợ HTTP test

## Dữ liệu môi trường

- Ảnh mẫu nhỏ dùng cho unit và integration test
- Ảnh có và không có khuôn mặt
- Ảnh có face nhỏ, occluded, nhiều khuôn mặt để kiểm tra edge case
- Model weights cần có sẵn hoặc fixture mock phù hợp

## Yêu cầu vận hành

- Test nên chạy nhanh và ổn định trên môi trường sạch.
- Môi trường phải có thể reproduce lỗi một cách nhất quán.
- Nên phân biệt giữa môi trường unit test và môi trường benchmark/performance.
