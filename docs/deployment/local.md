# Hướng Dẫn Cài Đặt & Triển Khai Local

Tài liệu này hướng dẫn cách thiết lập môi trường chạy thử và phát triển dự án Face Detection & Quality Assessment trên máy tính cá nhân (môi trường cục bộ).

---

## 🛠️ Yêu Cầu Hệ Thống

*   **Hệ điều hành**: Windows 10/11, Ubuntu 20.04+, hoặc macOS.
*   **Python**: Phiên bản từ `3.8` đến `3.12`.
*   **ONNX Runtime**: Phục vụ việc chạy suy luận mô hình tốc độ cao trên CPU/GPU.

---

## 🚀 Các Bước Cài Đặt

### 1. Tạo môi trường ảo (Virtual Environment)
Khuyến nghị tạo môi trường ảo để quản lý thư viện độc lập:
```bash
python -m venv venv
venv\Scripts\activate     # Trên Windows
source venv/bin/activate  # Trên Linux/macOS
```

### 2. Cài đặt các gói phụ thuộc
```bash
pip install -r requirements.txt
```

---

## ⚙️ Cấu Hình Biến Môi Trường Tối Ưu Hiệu Năng

Hệ thống hỗ trợ cấu hình tinh chỉnh luồng xử lý và tăng tốc phần cứng thông qua các biến môi trường:

| Tên biến | Kiểu dữ liệu | Mặc định | Ý nghĩa |
| :--- | :--- | :--- | :--- |
| `ONNX_INTRA_OP_THREADS` | `int` | `4` | Số lượng luồng xử lý tính toán song song song nội bộ của ONNX Runtime trên CPU. Điều chỉnh tăng/giảm tùy theo số nhân vật lý của CPU. |

---

## ⚡ Cấu Hình Tăng Tốc Phần Cứng (CPU / GPU)

Hệ thống được thiết kế để tự động nạp các Execution Provider tăng tốc tốt nhất của ONNX Runtime trên máy tính của bạn:

1.  **Chạy trên CPU (Mặc định)**:
    *   Sử dụng thư viện `onnxruntime` chuẩn.
    *   Hệ thống tự động sử dụng `CPUExecutionProvider`.
2.  **Tăng tốc trên GPU (NVIDIA CUDA)**:
    *   Yêu cầu cài đặt driver CUDA và thư viện `onnxruntime-gpu`:
        ```bash
        pip uninstall onnxruntime
        pip install onnxruntime-gpu
        ```
    *   Hệ thống sẽ tự nhận diện và kích hoạt `CUDAExecutionProvider`, đưa độ trễ AI về mức siêu thấp (<10ms).

---

## 🧪 Khởi Chạy Kiểm Thử & Kiểm Hiệu Năng (Benchmark)

Chạy kiểm tra tính đúng đắn của code và đo tốc độ:
```bash
pytest                                                # Chạy toàn bộ 20 test cases
pytest tests/benchmark/test_performance_benchmark.py -v -s  # Chạy riêng benchmark và in kết quả ra màn hình
```
