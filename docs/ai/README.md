# Quản trị AI của kho lưu trữ

## Mục đích

Tài liệu này xác định khung quản trị cho việc sử dụng, xem xét và ghi nhận hoạt động AI trong kho lưu trữ.

Nội dung tập trung vào hai phần chính:
- quản lý AI cho hệ thống runtime (mô hình, inference, chất lượng),
- quy trình làm việc với AI để tạo và rà soát tài liệu, thiết kế và thảo luận hệ thống.

## Phạm vi

Khung này áp dụng cho:
- quy tắc AI,
- quy trình xem xét,
- bối cảnh sử dụng,
- nhật ký quyết định,
- lịch sử prompt,
- quản lý phiên bản mô hình,
- cách sử dụng Markdown để hợp tác với AI và ghi nhận kết quả.

## Các tài liệu chính

- [ai-rules.md](ai-rules.md): xác định nguyên tắc và giới hạn sử dụng AI.
- [ai-review.md](ai-review.md): quy định cách đánh giá và phê duyệt nội dung AI.
- [ai-context.md](ai-context.md): ghi nhận bối cảnh, mục tiêu và phạm vi sử dụng AI.
- [decision-log.md](decision-log.md): lưu lại các quyết định quan trọng liên quan đến AI.
- [prompt-history.md](prompt-history.md): ghi nhận các prompt và biến thể được sử dụng.
- [model-version.md](model-version.md): theo dõi thông tin về mô hình và thay đổi liên quan.

## AI-assisted documentation workflow

1. Xác định yêu cầu, câu hỏi hoặc vấn đề cần giải quyết.
2. Soạn thảo prompt trong Markdown và ghi vào [prompt-history.md](prompt-history.md).
3. Dùng AI để tạo nội dung khởi đầu hoặc đề xuất giải pháp.
4. Rà soát, chỉnh sửa và xác minh bằng tay.
5. Ghi lại quyết định cuối cùng vào [decision-log.md](decision-log.md) và cập nhật [model-version.md](model-version.md) khi cần.

## Nguyên tắc chung

- Giữ nội dung AI rõ ràng, có mục đích và có thể kiểm soát.
- Phân biệt giữa hướng dẫn, kết quả và quyết định.
- Ghi nhận toàn bộ prompt và phản hồi quan trọng để đảm bảo truy xuất được.
- Duy trì tính nhất quán giữa các tài liệu liên quan.
- Cập nhật tài liệu khi quy trình hoặc phạm vi thay đổi.

## Quan hệ giữa tài liệu và hệ thống

- Tài liệu kiến trúc mô tả cấu trúc runtime của hệ thống.
- Tài liệu AI mô tả quy trình làm việc với AI, quyền kiểm soát và các quyết định quản trị.
- Tài liệu prompt và decision log là chứng cứ cho các bước thảo luận và thay đổi.
