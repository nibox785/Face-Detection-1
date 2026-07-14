# API `/ws/detect` Reference (Lộ trình phát triển)

> [!NOTE]
> Kết nối WebSockets thời gian thực hiện đang nằm trong **Kế hoạch phát triển tiếp theo (Future Roadmap)** nhằm hỗ trợ tối ưu hóa trễ truyền tải mạng mức siêu thấp cho các camera an ninh chuyên nghiệp. Giao tiếp chính hiện tại vẫn đang qua HTTP POST `/detect`.

---

## 📡 Thiết lập Kết nối

- **Đường dẫn**: `/ws/detect`
- **Giao thức**: `WS` / `WSS` (WebSocket)

---

## 📥 Dữ Liệu Truyền Vào từ Client (Gửi nhị phân)

Client gửi trực tiếp chuỗi nhị phân chứa luồng dữ liệu của khung hình webcam:
*   Định dạng: `ArrayBuffer` hoặc `Blob` nhị phân của ảnh nén JPEG.
*   Tần suất gửi: 15 - 30 frame/giây.

---

## 📤 Dữ Liệu Phản Hồi từ Server (JSON)

Sau khi xử lý xong khung hình, Backend đẩy kết quả phân tích về Client qua cùng kết nối socket:

```json
{
  "event": "detection_result",
  "face_count": 1,
  "faces": [
    {
      "box": [110, 80, 240, 250],
      "confidence": 0.998,
      "quality": {
        "score": 95,
        "status": "Excellent"
      }
    }
  ]
}
```
