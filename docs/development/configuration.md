# Configuration

Tài liệu này tổng hợp các cấu hình quan trọng mà developer cần biết khi làm việc với project.

## Backend runtime configuration

- Backend app được cấu hình trong [backend/main.py](../../backend/main.py).
- FastAPI app có title, version và CORS middleware mở rộng cho tất cả origins.
- Endpoint /detect nhận các tham số form: network, threshold, draw_mask, upscale.

## Detector configuration

- Cấu hình RetinaFace được lưu trong [backend/data/config.py](../../backend/data/config.py).
- Có hai cấu hình chính:
  - cfg_mnet cho backbone MobileNet
  - cfg_re50 cho backbone ResNet50
- Các cấu hình này định nghĩa min_sizes, steps, variance, image_size và các thông số training/inference.

## Segmentation configuration

- Cấu hình U-Net được lưu trong [backend/segmentation/config.py](../../backend/segmentation/config.py).
- Các giá trị quan trọng gồm:
  - NUM_CLASSES = 19
  - INPUT_SIZE = (512, 512)
  - CROP_SIZE = (448, 448)
  - DEVICE được chọn tự động dựa trên CUDA availability

## Model paths

- Runtime detector và segmenter đọc model từ thư mục [backend/weights](../../backend/weights).
- Script khởi chạy [run.py](../../run.py) sẽ tự động tải các model ONNX nếu thiếu.
- Các model cần có tên:
  - mobilenet0.25_Final.onnx
  - Resnet50_Final.onnx
  - unet_face_celeb.onnx

## Training-related configuration

- [backend/train.py](../../backend/train.py) sử dụng các argument CLI như training_dataset, network, num_workers, lr, momentum, resume_net, save_folder.
- [backend/segmentation/train.py](../../backend/segmentation/train.py) cho phép cấu hình epochs, batch_size, lr, device và debug mode.
- [backend/segmentation/evaluate.py](../../backend/segmentation/evaluate.py) hỗ trợ chọn weights và giới hạn số lượng ảnh đánh giá.
