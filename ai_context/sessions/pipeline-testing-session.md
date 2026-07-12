# AI Context Log

## Files read
- [README.md](../../README.md)
- [docs/testing/README.md](../../docs/testing/README.md)
- [docs/testing/pipeline-testing.md](../../docs/testing/pipeline-testing.md)
- [backend/main.py](../../backend/main.py)
- [backend/models/face_detector.py](../../backend/models/face_detector.py)
- [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)
- [backend/quality/face_quality.py](../../backend/quality/face_quality.py)

## Decisions
- Tài liệu pipeline testing nên tập trung vào endpoint /detect vì đây là luồng orchestration chính giữa detector, segmenter và quality assessment.
- Nội dung cần phản ánh đúng các nhánh fallback và điều kiện bỏ qua box nhỏ như đã được triển khai trong code.
- Không nên thêm các kịch bản giả lập vượt quá implementation hiện có.

## Assumptions
- Pipeline testing dựa trên cách backend hiện tại xử lý request và tạo response, không giả định thêm service layer khác.
- Các mô hình ONNX và weights có thể được sử dụng trong môi trường test khi cần chạy pipeline thực tế.

## Missing information
- Chưa có test suite pipeline thực tế trong thư mục tests/pipeline.
- Chưa có fixture ảnh mẫu được ghi nhận rõ ràng trong docs.

## TODO
- Bổ sung các case pipeline khi có fixture ảnh mẫu và dữ liệu response chuẩn.
- Cập nhật tài liệu khi endpoint /detect thay đổi contract response.