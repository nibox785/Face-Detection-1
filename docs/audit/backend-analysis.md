# Backend Analysis

Tài liệu tạm thời này mô tả tổng quan về backend của dự án Face Detection.

## Tổng quan

Backend được xây dựng bằng FastAPI và đóng vai trò trung tâm trong hệ thống. Nó chịu trách nhiệm:
- nhận ảnh đầu vào từ client
- chạy phát hiện khuôn mặt
- thực hiện phân đoạn khuôn mặt
- đánh giá chất lượng khuôn mặt
- trả về kết quả cho frontend

## Vòng đời backend

1. Khởi động ứng dụng
   - File [backend/main.py](../../backend/main.py) khởi tạo FastAPI app.
   - CORS được bật để hỗ trợ gọi từ frontend.
   - Các mô hình được cache theo nhu cầu để tránh tải lại thường xuyên.

2. Xử lý request
   - Endpoint POST /detect nhận file ảnh từ client.
   - Ảnh được giải mã bằng OpenCV.
   - Sau đó, backend chuyển ảnh vào pipeline phát hiện và phân đoạn.

3. Suy luận và hậu xử lý
   - Mô hình phát hiện khuôn mặt trả về box, score và landmarks.
   - Các crop khuôn mặt được dùng cho segmenter U-Net.
   - Mặt nạ nhị phân được tạo và dùng cho đánh giá chất lượng.
   - Kết quả được trả về dưới dạng JSON và các ảnh PNG có alpha.

## Luồng suy luận

### 1. Phát hiện khuôn mặt
- File [backend/models/face_detector.py](../../backend/models/face_detector.py)
- Sử dụng mô hình RetinaFace ONNX
- Tải các weights từ [backend/weights](../../backend/weights)
- Áp dụng preprocessing, decoding và NMS

### 2. Phân đoạn khuôn mặt
- File [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)
- Sử dụng mô hình U-Net ONNX
- Tạo binary mask từ crop khuôn mặt

### 3. Đánh giá chất lượng
- File [backend/quality/face_quality.py](../../backend/quality/face_quality.py)
- Đánh giá kích thước, độ che khuất, góc quay đầu và tính chất lượng tổng thể

## Các module chính

- [backend/main.py](../../backend/main.py): điểm vào API và điều phối luồng
- [backend/models/face_detector.py](../../backend/models/face_detector.py): phát hiện khuôn mặt
- [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py): phân đoạn khuôn mặt
- [backend/quality/face_quality.py](../../backend/quality/face_quality.py): phân tích chất lượng
- [backend/data/config.py](../../backend/data/config.py): cấu hình mạng RetinaFace
- [backend/utils](../../backend/utils): các util hỗ trợ decode box và NMS

## Phụ thuộc chính

- FastAPI
- Uvicorn
- OpenCV
- NumPy
- ONNX Runtime
- PyTorch
- TorchVision

## Ghi chú

Đây là tài liệu tạm thời, chưa phải bản chính thức, và có thể được cập nhật khi codebase phát triển thêm.
