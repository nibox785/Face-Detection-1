# API Overview

Hệ thống cung cấp giao diện lập trình ứng dụng RESTful API dựa trên nền tảng **FastAPI**, phục vụ việc nhận dạng, phân tích chất lượng khuôn mặt real-time và quản lý báo cáo.

---

## 🚀 Cấu Hình Máy Chủ

*   **Host**: `0.0.0.0` (Mở cho tất cả các thiết bị trong mạng LAN)
*   **Port**: `5000` (Mặc định)
*   **Tài nguyên tĩnh**: FastAPI serve toàn bộ tài nguyên static của Frontend (HTML/CSS/JS) trực tiếp tại root `/`.

---

## 📌 Danh Sách Endpoints

| Endpoint | Phương thức | Mô tả | Trạng thái |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Trả về giao diện Frontend tĩnh (`index.html`). | 🟢 Đang hoạt động |
| `/detect` | `POST` | Pipeline nhận diện khuôn mặt và đánh giá chất lượng. | 🟢 Đang hoạt động |
| `/health` | `GET` | Kiểm tra trạng thái hoạt động của Backend server. | 🟢 Đang hoạt động |
| `/ws/detect` | `WS` | Luồng dữ liệu WebSocket nhị phân để tối ưu FPS. | 🟡 Lộ trình phát triển |

---

## 📝 Tài liệu cụ thể:
*   [Tài liệu API /detect](detect.md)
*   [Tài liệu API /health](health.md)
*   [Tài liệu WebSocket](websocket.md)
