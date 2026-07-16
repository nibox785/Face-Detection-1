# API `/detect` Reference

Endpoint nhận ảnh từ client, chạy qua toàn bộ pipeline AI (phát hiện → theo dõi → phân đoạn → đánh giá chất lượng) và trả về kết quả JSON chi tiết.

- **Đường dẫn**: `/detect`
- **Phương thức**: `POST`
- **Content-Type**: `multipart/form-data`

---

## 📥 Dữ Liệu Đầu Vào (Request Parameters)

| Trường | Kiểu | Mặc định | Mô tả |
| :--- | :--- | :--- | :--- |
| `image` | `File` (Binary) | *Bắt buộc* | Tệp ảnh JPEG/PNG cần phân tích. |
| `network` | `string` | `"mobile0.25"` | Backbone RetinaFace: `"mobile0.25"` (nhanh ~24ms) hoặc `"resnet50"` (chính xác). |
| `threshold` | `float` | `0.60` | Ngưỡng confidence tối thiểu để chấp nhận một detection. |
| `draw_mask` | `boolean` | `false` | Có chạy U-Net segmentation để tạo face mask hay không. |
| `upscale` | `boolean` | `false` | Phóng to ảnh lên 1280px rộng trước khi detect để nhận diện mặt xa/nhỏ. |
| `save_report` | `boolean` | `false` | Lưu kết quả dưới dạng report JSON trên đĩa Backend. |
| `report_name` | `string` | `null` | Tên tùy biến cho thư mục report được lưu. |
| `min_face_px` | `int` | `36` | Kích thước pixel tối thiểu (cạnh ngắn nhất) của một detection để vượt qua bộ lọc hình học. |

> [!NOTE]
> `min_face_px` là tham số điều khiển bộ lọc hình học (Geometric Filter) của SORT-like Tracker. Tăng giá trị này nếu hệ thống phát hiện nhầm lỗ thông gió, hoa văn hoặc chữ trên bảng hiệu thành khuôn mặt.

---

## ⚙️ Cơ Chế Xử Lý Nội Bộ (Internal Processing)

Khi API được gọi, backend thực hiện theo quy trình:

1. **Skip-frame Check**: Tracker kiểm tra `frame_counter % DETECTOR_INTERVAL`. Nếu là frame skip, bỏ qua RetinaFace và dùng Constant Velocity Predictor để dự báo vị trí track.
2. **RetinaFace Inference** (detector frames): Chạy ONNX inference, decode boxes và landmarks.
3. **Geometric Filter**: Loại bỏ detection có kích thước < `min_face_px` hoặc tỉ lệ `w/h` nằm ngoài `[0.4, 2.5]`.
4. **Hungarian Matching**: Tính IoU Cost Matrix giữa detections (đã lọc) và velocity-predicted track positions. Chạy `scipy.optimize.linear_sum_assignment` để phân công tối ưu.
5. **Hit-streak Gate**: Track mới (tentative) chỉ được xác nhận (confirmed) sau `N_HIT_CONFIRM = 2` lần ghép thành công liên tiếp.
6. **U-Net Segmentation** (mỗi 6 frame/track): Crop khuôn mặt, chạy U-Net ONNX, cache kết quả mask.
7. **Face Quality Analysis**: Tính visibility, occlusion, pose, composite score.
8. **Response Assembly**: Đóng gói JSON + Base64 PNG + RLE mask.

---

## 📤 Dữ Liệu Đầu Ra (Response JSON)

```json
{
  "image": "data:image/jpeg;base64,...",
  "face_count": 2,
  "latency_ms": 28,
  "fps": 35.7,
  "network": "mobile0.25",
  "request_id": "a1b2c3d4",
  "status": "ok",
  "report_dir": "reports/inference/sample_case",
  "report_url": "/reports/inference/sample_case",
  "faces": [
    {
      "id": 1,
      "box": [110, 80, 240, 250],
      "confidence": 0.998,
      "landmarks": [140, 150, 200, 150, 170, 180, 150, 220, 190, 220],
      "visibility": 87,
      "quality_score": 92,
      "pose": "Normal",
      "status": "Normal",
      "rating": "Excellent",
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

### Chi tiết các trường trong `faces[]`:

| Trường | Kiểu | Mô tả |
| :--- | :--- | :--- |
| `id` | `int` | Track ID ổn định, được giữ nguyên qua nhiều frame liên tiếp. |
| `box` | `[x1,y1,x2,y2]` | Tọa độ bounding box khuôn mặt (pixel). |
| `confidence` | `float` | Điểm tin cậy của detection (0.0 – 1.0). |
| `landmarks` | `float[10]` | 5 điểm mốc `[mắt_trái_x, y, mắt_phải_x, y, mũi_x, y, miệng_trái_x, y, miệng_phải_x, y]`. |
| `visibility` | `int` | % vùng mask che phủ trong bounding box (0–100). |
| `quality_score` | `int` | Điểm chất lượng tổng hợp (0–100). |
| `pose` | `string` | Hướng quay đầu: `Normal`, `Head Left`, `Head Right`, `Head Up`, `Head Down`. |
| `status` | `string` | Trạng thái chất lượng: `Normal`, `Face Occluded`. |
| `rating` | `string` | Phân loại chất lượng: `Excellent`, `Good`, `Acceptable`, `Poor`, `Unusable`. |
| `mask_rle` | `object` | Run-Length Encoding của binary face mask (dùng để export evidence). |
| `face_png_alpha` | `string` | Ảnh crop khuôn mặt tách nền (PNG base64 có kênh Alpha) để hiển thị trong Gallery. |

---

## 🔢 Mã Lỗi HTTP

| Mã | Ý nghĩa |
| :--- | :--- |
| `200 OK` | Pipeline hoàn thành thành công (có thể `face_count = 0` nếu không phát hiện mặt). |
| `400 Bad Request` | File ảnh không hợp lệ hoặc không đọc được. |
| `500 Internal Server Error` | Lỗi nội bộ server (ONNX inference thất bại, thiếu weight file...). |

---

## 💡 Ghi Chú Quan Trọng

> [!WARNING]
> **Hit-streak gate**: Track mới cần ≥ 2 frame liên tiếp phát hiện mới được xác nhận. Điều này có nghĩa là lần đầu bật camera, mục tiêu sẽ xuất hiện ở frame thứ 2 (không phải frame đầu tiên). Đây là hành vi by-design để chống false positive.

> [!NOTE]
> **frame_counter và `last_match_time`**: Track bị thu hồi (evicted) sau `MAX_MISS_SECS = 3.0` giây kể từ lần detector cuối cùng ghép thành công. Khi khuôn mặt rời khỏi camera, box sẽ tự biến mất sau tối đa 3 giây.
