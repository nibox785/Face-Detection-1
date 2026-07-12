# AI Context Log

## Files read
- [README.md](../../README.md)
- [docs/testing/README.md](../../docs/testing/README.md)
- [docs/testing/model-testing.md](../../docs/testing/model-testing.md)
- [backend/models/face_detector.py](../../backend/models/face_detector.py)
- [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)
- [backend/segmentation/evaluate.py](../../backend/segmentation/evaluate.py)
- [backend/segmentation/config.py](../../backend/segmentation/config.py)
- [backend/segmentation/model.py](../../backend/segmentation/model.py)
- [backend/weights](../../backend/weights)
- [docs/ai/ai-context.md](../../docs/ai/ai-context.md)

## Decisions
- Tài liệu model testing nên tập trung vào detector RetinaFace và segmenter U-Net vì đây là hai thành phần AI cốt lõi trong hệ thống.
- Nội dung nên dựa trên implementation hiện tại, không invent thêm metric hoặc behavior chưa có trong code.
- Nên liên kết tới các tài liệu testing khác thay vì lặp lại đầy đủ chiến lược tổng thể.

## Assumptions
- Các file weights ONNX có sẵn trong thư mục backend/weights cho mục đích tham khảo.
- Các script đánh giá hiện có là nguồn tham chiếu cho model testing, nhưng không thay thế cho test suite tự động.

## Missing information
- Không có test suite hiện tại cho mô hình trong thư mục tests/model.
- Không có tài liệu chi tiết về dataset dùng cho validation ngoài các script hiện có.

## TODO
- Cập nhật thêm model-testing.md khi có dataset hoặc fixture cụ thể.
- Bổ sung các case kiểm thử nếu repository có thêm model variants hoặc export format mới.