# Dependencies

Tài liệu này mô tả các dependency chính dùng trong quá trình phát triển và chạy ứng dụng.

## Runtime dependencies

Các package dưới đây được định nghĩa trong [requirements.txt](../../requirements.txt) và là bắt buộc để chạy backend và inference:

- FastAPI: xây dựng API HTTP và route cho backend.
- Uvicorn: máy chủ ASGI để chạy ứng dụng FastAPI.
- ONNX Runtime: chạy các mô hình ONNX cho detector và segmenter.
- ONNX: hỗ trợ export và thao tác với mô hình ONNX.
- OpenCV: đọc/viết ảnh, tiền xử lý, vẽ overlay, tạo PNG alpha.
- NumPy: xử lý tensor, mask và dữ liệu hình ảnh.
- Pillow: xử lý ảnh trong các script liên quan.
- PyTorch: dùng cho training và export model, cùng với các hàm decode box và prior box.
- TorchVision: hỗ trợ transform và dataset cho training/đánh giá.
- python-multipart: nhận file upload qua FastAPI.

## Development and training dependencies

Các script huấn luyện và export model dùng thêm các thành phần của PyTorch và thư viện hỗ trợ hình ảnh. Khi làm việc với training pipeline, cần đảm bảo môi trường có GPU hỗ trợ nếu muốn chạy training thật nhanh.

## Dependency notes

- Runtime inference hiện tập trung vào ONNX Runtime, nhưng training và export vẫn dựa trên PyTorch.
- Nếu làm việc với mô hình RetinaFace và U-Net, việc cài đúng các versions phù hợp của torch/torchvision là quan trọng để tránh incompatibility với code cũ.
