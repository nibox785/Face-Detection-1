# API `/health` Reference

Endpoint dùng để giám sát trạng thái sức khỏe (health check) của máy chủ FastAPI backend.

- **Đường dẫn**: `/health`
- **Phương thức**: `GET`
- **Quyền truy cập**: Không yêu cầu xác thực

---

## 📤 Dữ Liệu Đầu Ra (Response JSON)

Trả về mã trạng thái HTTP `200 OK` cùng nội dung JSON:

```json
{
  "status": "healthy",
  "timestamp": 1784026884.914
}
```

### Chi tiết các thuộc tính:
*   `status`: Trạng thái hệ thống (luôn trả về `"healthy"` nếu server hoạt động bình thường).
*   `timestamp`: Mốc thời gian Unix epoch hiện tại ở phía backend (dùng để đo kiểm tra độ lệch giờ hoặc kiểm tra phản hồi sống).
