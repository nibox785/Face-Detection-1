# Executive Summary

Tài liệu này là bản tóm tắt tạm thời về cấu trúc và hoạt động của dự án Face Detection. Mục đích là cung cấp cái nhìn nhanh về backend, frontend, pipeline huấn luyện, kiểm thử và phụ thuộc, phục vụ cho việc rà soát ban đầu hoặc audit nội bộ.

## Tổng quan dự án

Dự án là một hệ thống giám sát khuôn mặt AI chạy trên nền web, kết hợp các chức năng:
- phát hiện khuôn mặt bằng RetinaFace
- phân đoạn khuôn mặt bằng U-Net
- đánh giá chất lượng khuôn mặt
- hiển thị kết quả trên giao diện dashboard

Backend được xây dựng bằng FastAPI, frontend là giao diện tĩnh bằng HTML/CSS/JavaScript, và các mô hình chạy chủ yếu bằng ONNX Runtime để tăng tốc suy luận.

## Điểm mạnh

- Mô hình kiến trúc rõ ràng: backend, frontend, training pipeline và evaluation pipeline được tách rành mạch.
- Có luồng suy luận hoàn chỉnh từ ảnh đầu vào tới kết quả phân tích.
- Có thể chạy với nhiều nguồn dữ liệu: ảnh tĩnh, video và webcam.
- Có sẵn các script huấn luyện, đánh giá và export mô hình.

## Điểm cần chú ý

- Kho dự án có nhiều file cũ và script nghiên cứu, cần phân biệt rõ giữa runtime pipeline và training/evaluation pipeline.
- Test suite hiện tại chưa được triển khai đầy đủ theo cấu trúc pytest.
- Các mô hình lớn được lưu dưới dạng ONNX và có thể phụ thuộc vào việc có sẵn weights tại runtime.
- Một số module training/evaluation vẫn mang tính nghiên cứu và cần được chuẩn hóa nếu muốn dùng cho production.

## Khuyến nghị ban đầu

1. Hoàn thiện bộ test tự động cho backend và API.
2. Tách rõ runtime pipeline và training pipeline trong tài liệu và cấu trúc mã.
3. Chuẩn hóa cấu trúc tài liệu và các script kiểm thử.
4. Đánh giá lại việc sử dụng ONNX Runtime và cách tải model trong môi trường production.

> Lưu ý: đây là tài liệu tạm thời, không phải tài liệu chính thức.
