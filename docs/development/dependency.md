# Dependencies (Phụ Thuộc)

Tài liệu này mô tả toàn bộ phụ thuộc của dự án và vai trò của từng thư viện.

---

## Runtime Dependencies (bắt buộc để chạy server)

Được định nghĩa trong [requirements.txt](../../requirements.txt):

| Thư viện | Mục đích |
|---|---|
| `fastapi` | Web framework xây dựng API HTTP và route backend |
| `uvicorn` | ASGI server để chạy ứng dụng FastAPI |
| `onnxruntime` | Chạy mô hình ONNX (RetinaFace + U-Net) trên CPU, nhanh hơn PyTorch 2–3× |
| `onnx` | Hỗ trợ export và thao tác mô hình ONNX |
| `opencv-python` | Đọc/ghi ảnh, tiền xử lý, vẽ bounding box, tạo PNG alpha kênh trong suốt |
| `numpy` | Xử lý ma trận: IoU matrix, binary mask, tensor inference |
| `scipy` | **★ Mới:** `scipy.optimize.linear_sum_assignment` — Hungarian Algorithm cho SORT-like tracker |
| `pillow` | Xử lý ảnh trong scripts và testing |
| `torch` | Giải mã hình học legacy (PriorBox decode), export ONNX |
| `torchvision` | Transform và dataset support cho training |
| `python-multipart` | Nhận file upload qua form-data trong FastAPI |

---

## Frontend Dependencies (CDN, không cần cài)

| Thư viện | Nguồn | Mục đích |
|---|---|---|
| `ApexCharts.js` | CDN jsDelivr | Biểu đồ Donut, Bar, Line thời gian thực |
| `Feather Icons` | CDN jsDelivr | Icon bộ điều khiển và HUD |
| `Google Fonts (Inter + JetBrains Mono)` | Google Fonts CDN | Typography giao diện và telemetry data |

---

## Testing Dependencies

| Thư viện | Mục đích |
|---|---|
| `pytest` | Test runner chính |
| `pytest-anyio` | Async test support |
| `httpx` | HTTP client cho FastAPI TestClient |
| `pillow` | Tạo ảnh test trong integration tests |

---

## Ghi Chú Quan Trọng

> [!IMPORTANT]
> **`scipy` là dependency bắt buộc mới** được thêm vào từ phiên bản SORT-like Tracker. Nếu upgrade từ phiên bản cũ, cần chạy lại `pip install -r requirements.txt` để cài `scipy`.

> [!NOTE]
> - **Runtime inference** tập trung vào ONNX Runtime (không cần GPU cho inference).
> - **Training** vẫn dùng PyTorch, cần GPU để chạy nhanh.
> - Nếu gặp lỗi incompatibility `torch` ↔ `torchvision`, kiểm tra phiên bản tương thích tại [pytorch.org/get-started](https://pytorch.org/get-started/locally/).

---

## Kiểm Tra Phụ Thuộc

```bash
# Cài toàn bộ dependencies
pip install -r requirements.txt

# Kiểm tra scipy đã có chưa
pip show scipy

# Kiểm tra ONNX Runtime
python -c "import onnxruntime; print(onnxruntime.__version__)"
```
