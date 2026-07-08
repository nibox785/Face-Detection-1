# Testing Analysis

Tài liệu tạm thời này mô tả hiện trạng kiểm thử của dự án Face Detection.

## Tổng quan

Thư mục kiểm thử hiện có cấu trúc chuẩn theo [tests/README.md](../../tests/README.md), nhưng các thư mục con như unit, model, integration, pipeline, regression và benchmark hiện đang trống.

## Coverage hiện tại

Các kiểm thử hiện có chủ yếu là các script chạy riêng lẻ thay vì pytest suite:
- [backend/test_widerface.py](../../backend/test_widerface.py)
- [backend/test_fddb.py](../../backend/test_fddb.py)
- [backend/segmentation/evaluate.py](../../backend/segmentation/evaluate.py)

Những script này chủ yếu kiểm tra:
- khả năng chạy inference trên dataset
- xuất kết quả detecion sang file txt
- tính toán metrics cho segmentation

## Coverage còn thiếu

Chưa có test tự động cho các phần sau:
- unit test cho preprocessing và augmentations
- unit test cho box decoding, landmark decoding và NMS
- unit test cho face quality scoring
- integration test cho full pipeline /detect
- regression test cho model loading và runtime fallback
- benchmark/performance test

## Chiến lược kiểm thử

Hiện tại, chiến lược kiểm thử là dạng script-driven evaluation thay vì automated regression suite. Điều này phù hợp để kiểm tra mô hình trên dataset, nhưng chưa đủ cho việc bảo trì và phát triển dài hạn.

## Khuyến nghị ban đầu

1. Xây dựng pytest suite cho backend.
2. Thêm unit test cho các module cốt lõi.
3. Thêm integration test cho API endpoint.
4. Chuẩn hóa kết quả kiểm thử và lưu báo cáo tự động.

> Đây là tài liệu tạm thời, không phải bản chính thức.
