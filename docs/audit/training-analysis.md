# Training Analysis

Tài liệu tạm thời này mô tả tổng quan về pipeline huấn luyện và đánh giá mô hình trong dự án.

## Dataset

Pipeline huấn luyện chủ yếu dùng cho mô hình RetinaFace và đọc dữ liệu từ WIDER Face thông qua [backend/data/wider_face.py](../../backend/data/wider_face.py).

Mỗi sample bao gồm:
- ảnh đầu vào
- bounding box khuôn mặt
- các landmark của khuôn mặt
- nhãn đối tượng

## Luồng huấn luyện

1. Khởi tạo tham số huấn luyện trong [backend/train.py](../../backend/train.py).
2. Chọn backbone là MobileNet hoặc ResNet50 theo cấu hình trong [backend/data/config.py](../../backend/data/config.py).
3. Dùng pipeline augmentations từ [backend/data/data_augment.py](../../backend/data/data_augment.py):
   - crop ngẫu nhiên
   - distort màu sắc và độ sáng
   - mirror
   - resize và normalize
4. Tạo prior boxes bằng PriorBox.
5. Chạy forward/backward và cập nhật optimizer.
6. Lưu checkpoint sau mỗi epoch hoặc khi cần.

## Luồng đánh giá

Dự án có các script đánh giá riêng cho detector và segmenter:
- [backend/test_widerface.py](../../backend/test_widerface.py): đánh giá RetinaFace trên WIDER Face
- [backend/test_fddb.py](../../backend/test_fddb.py): đánh giá RetinaFace trên FDDB
- [backend/segmentation/evaluate.py](../../backend/segmentation/evaluate.py): đánh giá U-Net bằng pixel accuracy và IoU

## Luồng export

Sau khi huấn luyện, mô hình PyTorch có thể được xuất sang ONNX bằng [backend/convert_to_onnx.py](../../backend/convert_to_onnx.py). Đây là bước quan trọng để backend runtime có thể chạy inference bằng ONNX Runtime.

## Nhận xét

Pipeline huấn luyện có cấu trúc khá rõ ràng cho mục đích nghiên cứu và phát triển mô hình. Tuy nhiên, việc tách biệt giữa training, evaluation và runtime inference vẫn cần được làm rõ hơn nếu muốn hệ thống được chuẩn hóa cho production.
