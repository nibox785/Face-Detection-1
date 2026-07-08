# Project Structure

Cấu trúc thư mục hiện tại phản ánh việc chia tách rõ ràng giữa backend, frontend, scripts và tài liệu.

## Root-level structure

- [run.py](../../run.py): entrypoint để khởi chạy hệ thống và tự động tải weights nếu cần.
- [requirements.txt](../../requirements.txt): dependency manifest.
- [backend](../../backend): mã nguồn backend và pipeline training/inference.
- [frontend](../../frontend): giao diện web tĩnh.
- [docs](../../docs): tài liệu phân tích, kiến trúc, phát triển và yêu cầu.
- [tests](../../tests): thư mục test hiện có nhưng chưa triển khai đầy đủ.

## Backend structure

- [backend/main.py](../../backend/main.py): FastAPI entrypoint, route / và /detect.
- [backend/models](../../backend/models): wrapper cho detector và segmenter.
- [backend/quality](../../backend/quality): logic đánh giá chất lượng và cảnh báo.
- [backend/data](../../backend/data): cấu hình RetinaFace và data utilities.
- [backend/segmentation](../../backend/segmentation): training, evaluation và cấu hình cho U-Net.
- [backend/utils](../../backend/utils): các helper liên quan box decoding và NMS.
- [backend/weights](../../backend/weights): lưu trọng số và model ONNX.

## Frontend structure

- [frontend/index.html](../../frontend/index.html): layout và các thành phần UI.
- [frontend/css](../../frontend/css): stylesheet cho dashboard.
- [frontend/js/app.js](../../frontend/js/app.js): logic xử lý media, API gọi và canvas overlay.

## Script and training structure

- [backend/train.py](../../backend/train.py): training RetinaFace.
- [backend/convert_to_onnx.py](../../backend/convert_to_onnx.py): export model sang ONNX.
- [backend/segmentation/train.py](../../backend/segmentation/train.py): training U-Net.
- [backend/segmentation/evaluate.py](../../backend/segmentation/evaluate.py): đánh giá U-Net.

## Guidance for contributors

Khi mở rộng project, nên giữ logic theo module hiện có: backend route ở main.py, model wrappers ở models/, quality logic ở quality/, và training scripts ở các thư mục riêng tương ứng.
