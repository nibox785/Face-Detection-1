# Nhật ký quyết định

## Mục đích

Tài liệu này lưu lại các quyết định quan trọng liên quan đến việc sử dụng và quản trị AI.

## Cách ghi nhận

Mỗi quyết định nên nêu rõ:

- Mục tiêu của quyết định.
- Ngày và người chịu trách nhiệm.
- Lý do cơ bản cho quyết định.
- Tác động đến tài liệu hoặc quy trình liên quan.

## Quyết định phiên 2026-07-13

- Quyết định ghi nhận: dùng file `.face-detection.agent` tại gốc workspace như điểm khởi đầu duy nhất cho AI session tiếp theo. File này phải chứa tóm tắt kiến trúc, phase, file ưu tiên đọc và hướng dẫn kiểm tra.
- Quyết định logging: mở rộng tài liệu `docs/logging/inference-log.md` và `docs/logging/README.md` để làm rõ structured JSON logging và schema của event inference.
- Quyết định kỹ thuật: giữ import backend theo package-relative để backend chạy ổn định, tránh sửa lỗi import lại trong các phase tiếp theo.

## Yêu cầu

- Các quyết định quan trọng nên được ghi nhận ngay khi được đưa ra.
- Nếu quyết định được thay đổi hoặc bỏ qua, trạng thái mới cũng nên được ghi lại.
- Tài liệu này nên giữ được tính liên tục và dễ tra cứu.
