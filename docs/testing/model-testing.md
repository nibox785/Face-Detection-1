# Model Testing

Model testing liên quan đến việc kiểm tra detector và segmenter bằng dữ liệu mẫu hoặc các script hiện có.

## Scope

- Kiểm tra detector RetinaFace bằng các script đánh giá trên WIDER Face và FDDB.
- Kiểm tra segmenter U-Net bằng các script training/evaluation.

## Các script hiện có

- [backend/test_widerface.py](../../backend/test_widerface.py): chạy đánh giá detector trên tập WIDER Face.
- [backend/test_fddb.py](../../backend/test_fddb.py): chạy đánh giá detector trên tập FDDB.
- [backend/segmentation/evaluate.py](../../backend/segmentation/evaluate.py): đánh giá mô hình U-Net.

## Mục tiêu kiểm thử

- Đảm bảo model có thể load đúng từ file weights.
- Đảm bảo inference chạy trên input mẫu mà không lỗi.
- Đảm bảo đầu ra có dạng phù hợp với các consumer tiếp theo.

## Gợi ý dữ liệu

- Nên dùng ảnh mẫu có mặt rõ ràng để kiểm tra phát hiện.
- Nên có một bộ dữ liệu nhỏ dùng cho smoke test trước khi chạy toàn bộ benchmark.
