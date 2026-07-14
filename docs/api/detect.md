# API `/detect` Reference

Endpoint dùng để nhận ảnh từ người dùng, chạy qua pipeline nhận diện, phân đoạn mặt, đánh giá chất lượng và trả về kết quả chi tiết.

- **Đường dẫn**: `/detect`
- **Phương thức**: `POST`
- **Content-Type**: `multipart/form-data`

---

## 📥 Dữ Liệu Đầu Vào (Request parameters)

Hỗ trợ các trường dữ liệu dạng Form:

| Trường | Kiểu dữ liệu | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- |
| `image` | `File` (Binary) | *Bắt buộc* | Tệp ảnh JPEG, PNG cần phân tích chất lượng khuôn mặt. |
| `network` | `string` | `"mobile0.25"` | Backbone nhận diện: `"mobile0.25"` (nhanh) hoặc `"resnet50"` (chính xác). |
| `threshold` | `float` | `0.5` | Ngưỡng tin cậy (confidence) để lọc khuôn mặt. |
| `draw_mask` | `boolean` | `false` | Có chạy mô hình phân đoạn U-Net để lấy mặt nạ hay không. |
| `upscale` | `boolean` | `false` | Phóng đại ảnh gốc trước khi detect để tăng khả năng nhận diện mặt siêu nhỏ. |
| `save_report` | `boolean` | `false` | Lưu kết quả dưới dạng tệp báo cáo bằng chứng (.json) trên đĩa Backend. |
| `report_name` | `string` | `null` | Tên tùy biến cho báo cáo được lưu. |

---

## 📤 Dữ Liệu Đầu Ra (Response JSON)

Trả về kết quả JSON với cấu trúc:

```json
{
  "image": "sample.jpg",
  "face_count": 1,
  "latency_ms": 115,
  "report_dir": "reports/inference/sample_case",
  "report_url": "/reports/inference/sample_case",
  "faces": [
    {
      "box": [110, 80, 240, 250],
      "confidence": 0.998,
      "landmarks": [140, 150, 200, 150, 170, 180, 150, 220, 190, 220],
      "quality": {
        "score": 95,
        "is_blurry": false,
        "visibility": 98.5,
        "is_occluded": false,
        "pose": {
          "yaw": 3.5,
          "pitch": -2.0,
          "roll": 1.2
        },
        "status": "Excellent"
      },
      "mask_rle": {
        "size": [480, 640],
        "counts": "...",
        "start_val": 0
      },
      "face_png_alpha": "data:image/png;base64,..."
    }
  ]
}
```

### Chi tiết các thuộc tính:
*   `box`: Tọa độ hình hộp khuôn mặt `[x1, y1, x2, y2]`.
*   `landmarks`: 5 điểm mốc đặc trưng `[mắt trái x, y, mắt phải x, y, mũi x, y, khóe miệng trái x, y, khóe miệng phải x, y]`.
*   `quality.score`: Điểm chất lượng tổng hợp (0 - 100).
*   `quality.status`: Phân loại chất lượng khuôn mặt (`"Excellent"`, `"Good"`, `"Acceptable"`, `"Poor"`, `"Unusable"`).
*   `mask_rle`: Chuỗi nén Run-Length Encoding của mặt nạ nhị phân.
*   `face_png_alpha`: Ảnh crop khuôn mặt tách nền (PNG base64) để hiển thị trong Gallery.
