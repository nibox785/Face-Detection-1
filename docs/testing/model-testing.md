# Model Testing

Tài liệu này tập trung vào kiểm thử các thành phần AI cốt lõi của hệ thống: detector RetinaFace và segmenter U-Net.

## Scope

Model testing nên kiểm tra các phần sau:
- khả năng load và khởi tạo mô hình từ file weights
- khả năng chạy inference trên input mẫu
- tính nhất quán của đầu ra với các thành phần tiếp theo trong pipeline

Chi tiết này được xây dựng dựa trên các module hiện có trong [backend/models/face_detector.py](../../backend/models/face_detector.py), [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py), [backend/segmentation/evaluate.py](../../backend/segmentation/evaluate.py) và [backend/segmentation/model.py](../../backend/segmentation/model.py).

## Các thành phần cần kiểm thử

### 1. RetinaFace detector

#### Mục đích
Kiểm tra wrapper chạy mô hình RetinaFace ONNX và các bước hậu xử lý liên quan.

#### Nội dung cần xem xét
- mô hình có thể được khởi tạo từ file ONNX trong [backend/weights](../../backend/weights)
- inference có thể chạy trên ảnh đầu vào hợp lệ
- đầu ra phải có dạng phù hợp cho bước decode box, decode landmark và NMS
- trường hợp ảnh nhỏ với upscale bật hoặc tắt cần được xử lý đúng luồng

#### Reference implementation
- [backend/models/face_detector.py](../../backend/models/face_detector.py)

### 2. U-Net segmenter

#### Mục đích
Kiểm tra wrapper chạy mô hình U-Net ONNX và quá trình postprocess mask.

#### Nội dung cần xem xét
- mô hình có thể load từ file weights
- preprocessing và normalization cho crop ảnh phải đúng định dạng
- output mask phải có kích thước tương ứng với crop đầu vào
- luồng batch prediction cần xử lý đúng danh sách crop

#### Reference implementation
- [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)
- [backend/segmentation/postprocess.py](../../backend/segmentation/postprocess.py)

### 3. Model evaluation scripts hiện có

Repository đã có các script đánh giá mô hình dùng cho mục đích kiểm thử thủ công hoặc offline:
- [backend/test_widerface.py](../../backend/test_widerface.py): chạy đánh giá detector trên tập WIDER Face
- [backend/test_fddb.py](../../backend/test_fddb.py): chạy đánh giá detector trên tập FDDB
- [backend/segmentation/evaluate.py](../../backend/segmentation/evaluate.py): đánh giá mô hình U-Net

Những script này phù hợp để kiểm tra khả năng chạy inference và xuất output, nhưng chưa thay thế cho một suite test tự động.

## Mục tiêu kiểm thử

- Đảm bảo mô hình có thể load đúng từ file weights.
- Đảm bảo inference chạy trên input mẫu mà không lỗi.
- Đảm bảo đầu ra có định dạng phù hợp cho các module tiếp theo.
- Đảm bảo các class và cấu trúc mô hình được giữ ổn định khi thay đổi implementation.

## Hạn chế và ràng buộc

- Không nên coi các script đánh giá hiện có là full replacement cho automated model test.
- Model testing nên tập trung vào khả năng chạy và tương thích đầu ra, không tự ý đưa thêm metric không có trong code hiện tại.

## Gợi ý dữ liệu cho model testing

- Ảnh mẫu đơn giản có khuôn mặt rõ để kiểm tra detector.
- Các crop khuôn mặt mẫu để kiểm tra segmenter.
- Một tập nhỏ dùng cho smoke test trước khi chạy đánh giá lớn hơn.

## Liên hệ với tài liệu khác

Thông tin chi tiết về phạm vi và kiến trúc kiểm thử có thể xem thêm tại:
- [docs/testing/testing-architecture.md](../../docs/testing/testing-architecture.md)
- [docs/testing/testing-scope.md](../../docs/testing/testing-scope.md)
- [docs/testing/test-environment.md](../../docs/testing/test-environment.md)
