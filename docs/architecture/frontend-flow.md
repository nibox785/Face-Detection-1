# Frontend Flow

Frontend là giao diện web tĩnh dùng để lấy đầu vào từ người dùng, gửi tới backend và hiển thị kết quả nhận dạng.

## Vai trò chính

- Cho phép chọn nguồn dữ liệu: ảnh tĩnh, video hoặc webcam.
- Thu thập frame từ media hiện tại.
- Gửi frame tới /detect bằng FormData.
- Vẽ overlay lên canvas để hiển thị bounding box, landmarks và mask.
- Cập nhật biểu đồ, telemetry và alert feed.
- Cho phép lưu frame, crop và snapshot bằng chứng.

## Luồng hoạt động

1. Frontend khởi tạo giao diện và các biểu đồ.
2. Người dùng chọn nguồn media hoặc upload file.
3. Khi có media, frontend tạo frame ảnh và gửi tới backend.
4. Backend trả về response JSON và ảnh đã annotate.
5. Frontend cập nhật state facesData, vẽ overlay và cập nhật các widget thống kê.
6. Với webcam và video, frontend lặp lại quá trình trên từng frame liên tiếp.

## Thành phần chính trên frontend

- Viewport: hiển thị media gốc và canvas overlay.
- Control panel: điều chỉnh mạng detector, ngưỡng confidence, chế độ xem và các tùy chọn overlay.
- Analytics panel: biểu đồ chất lượng, pose và lịch sử số mục tiêu.
- Evidence panel: lưu frame, crop, mask và metadata JSON.

## Trạng thái client-side

Frontend duy trì các trạng thái như:

- facesData để lưu kết quả phát hiện mới nhất
- selectedNetwork để chọn backbone detector
- currentViewMode để quyết định loại overlay hiển thị
- stream FPS và latency history cho telemetry
    