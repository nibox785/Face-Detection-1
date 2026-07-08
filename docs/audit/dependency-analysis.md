# Dependency Analysis

Tài liệu tạm thời này tóm tắt các phụ thuộc chính của dự án Face Detection.

## Phụ thuộc Python chính

- FastAPI: xây dựng API backend
- Uvicorn: chạy server ASGI
- ONNX Runtime: chạy inference mô hình ONNX
- ONNX: định dạng mô hình và export
- OpenCV: xử lý ảnh và video
- NumPy: tính toán số học và xử lý tensor
- Pillow: xử lý ảnh bổ sung
- PyTorch: huấn luyện và export mô hình
- TorchVision: hỗ trợ transform và data pipeline
- python-multipart: hỗ trợ upload file trong FastAPI

## Phụ thuộc liên quan tới mô hình

- RetinaFace detector
- U-Net segmenter
- các weights ONNX và checkpoint PyTorch

## Phụ thuộc frontend

- HTML/CSS/JavaScript thuần
- Feather Icons CDN
- ApexCharts CDN
- Google Fonts

## Nhận xét

Dự án phụ thuộc khá nhiều vào thư viện xử lý ảnh và deep learning. Với runtime hiện tại, ONNX Runtime là thành phần trung tâm cho suy luận, còn PyTorch vẫn giữ vai trò quan trọng cho huấn luyện và export mô hình.
