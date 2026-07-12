# Xem xét AI

## Mục đích

Tài liệu này quy định cách xem xét và phê duyệt nội dung được tạo hoặc hỗ trợ bởi AI.

Nó bao gồm cả việc đánh giá nội dung kỹ thuật và tài liệu Markdown/ prompt mà AI tham gia tạo ra.

## Quy trình xem xét

1. Xác định mục đích của nội dung AI.
2. Kiểm tra tính chính xác, rõ ràng và phù hợp với phạm vi.
3. Đánh giá mức độ cần thiết của việc sử dụng AI trong tài liệu đó.
4. So sánh với các nguồn dữ liệu thực tế: code, tài liệu kỹ thuật, tiêu chuẩn dự án.
5. Phê duyệt hoặc yêu cầu chỉnh sửa trước khi nội dung được đưa vào tài liệu chính thức.
6. Ghi lại prompt và quyết định kiểm duyệt vào [prompt-history.md](prompt-history.md) và [decision-log.md](decision-log.md).

## Tiêu chí phê duyệt

- Nội dung phù hợp với nguyên tắc và phạm vi đã xác định.
- Không mâu thuẫn với các tài liệu liên quan.
- Có thể hiểu và kiểm tra được bởi người chịu trách nhiệm.
- Đã được xác minh bằng tay với nguồn dữ liệu thực tế khi cần.
- Có bản ghi prompt/response nếu nội dung do AI tạo hoặc hỗ trợ.

## Hướng dẫn kiểm duyệt

- Xác định phần nào của tài liệu là AI-generated, phần nào đã chỉnh sửa thủ công.
- Nếu AI tạo content cho code hoặc logic, hãy kiểm tra file nguồn tương ứng.
- Nếu AI tham gia tạo sơ đồ hoặc luồng, xác nhận rằng sơ đồ phản ánh đúng thực tế hiện có.
- Thực hiện review peer hoặc review chủ chốt trước khi merge tài liệu vào nhánh chính.
