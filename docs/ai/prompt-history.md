# Lịch sử prompt

## Mục đích

Tài liệu này ghi nhận các prompt và biến thể được sử dụng trong quy trình làm việc với AI.

Nó đóng vai trò như một hồ sơ audit cho việc tương tác với AI và giúp tái sử dụng prompt hiệu quả.

## Nội dung ghi nhận

- Mục đích prompt.
- Phiên bản hoặc biến thể của prompt.
- Ngày tạo hoặc cập nhật.
- Kết quả chính và những thay đổi quan trọng.
- Người tạo prompt và người review.
- Tên tài liệu hoặc feature liên quan.

## Mẫu ghi nhận

| Ngày | Prompt / Mục đích | Phiên bản / Biến thể | Kết quả | Người tạo | Người review |
|------|------------------|----------------------|---------|----------|--------------|
| 2026-07-08 | Mô tả lại workflow AI + tài liệu trong dự án Face-Detection | v1 | Tạo nội dung AI governance và module đề xuất | admin | reviewer |
| 2026-07-10 | Thêm và ổn định test cho unit/model/integration, bao gồm segmenter và API detect | v2 | Tạo suite pytest cho face quality, detector, segmentation, integration; sửa lỗi import, shape mock, exception handling; thêm report generation cho /detect | admin | reviewer |
| 2026-07-10 | Tạo handoff session và lưu prompt summary cho phiên tiếp theo | v3 | Tạo tài liệu handoff và summary cho việc tiếp tục phát triển mà không cần đọc toàn bộ chat cũ | admin | reviewer |
| 2026-07-13 | Tạo file `.agent` cho phiên Face-Detection, tóm tắt kiến trúc, phase, log inference và các tài liệu cần đọc | v4 | Thêm `.face-detection.agent` để session AI tiếp theo có thể đọc 1 file duy nhất và tiếp cận nhanh hệ thống | admin | reviewer |

## Nguyên tắc

- Lịch sử nên được giữ có tổ chức và dễ tìm kiếm.
- Các prompt quan trọng nên được lưu lại để hỗ trợ xem xét và tái sử dụng.
- Nội dung nên tập trung vào mục đích và ý nghĩa thay vì chi tiết triển khai.
- Ghi rõ prompt gốc và các biến thể quan trọng.
- Nếu prompt tạo ra thay đổi trong code hoặc kiến trúc, liên kết tới quyết định và ticket/issue nếu có.
