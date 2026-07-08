# Coding Standards

Tài liệu này nêu các quy ước lập trình nên được giữ khi chỉnh sửa project.

## Python conventions

- Giữ code Python rõ ràng, có tên biến và hàm mô tả đúng ý nghĩa.
- Tránh viết logic quá dài trong một hàm; nên tách thành helper nếu logic phức tạp.
- Khi làm việc với ảnh, ưu tiên dùng NumPy/OpenCV theo phong cách hiện tại của repo.
- Nếu thêm exception handling, nên giữ lỗi có thông tin hữu ích và không phá vỡ toàn bộ request.

## API conventions

- Các endpoint HTTP nên được định nghĩa rõ ràng ở [backend/main.py](../../backend/main.py).
- Khi nhận upload file, nên dùng FastAPI File/Form và trả về response JSON có cấu trúc nhất quán.
- Khi trả kết quả detection, nên giữ định dạng dữ liệu rõ ràng gồm face_count, faces và latency_ms.

## Model and script conventions

- Các script training/export nên nhận tham số qua argparse.
- Khi làm việc với đường dẫn, nên dùng đường dẫn tương đối hoặc đường dẫn tính từ file hiện tại.
- Nên tránh hardcode đường dẫn không cần thiết; ưu tiên lấy từ cấu hình hoặc biến môi trường nếu phù hợp.

## Frontend conventions

- Frontend hiện đang là file tĩnh; nên giữ logic JS tập trung trong [frontend/js/app.js](../../frontend/js/app.js).
- Khi thêm UI mới, nên dùng các element đã có sẵn và giữ đồng bộ với cấu trúc DOM hiện tại.
- Nếu thêm chức năng export hoặc alert, nên tích hợp vào flow hiện có thay vì tạo luồng riêng biệt.

## Documentation conventions

- Khi sửa code, cập nhật tài liệu liên quan nếu thay đổi behavior hoặc cấu hình.
- Các tài liệu phát triển nên giữ ngôn ngữ rõ ràng, ngắn gọn và tập trung vào cách dùng và cấu trúc hiện tại.
