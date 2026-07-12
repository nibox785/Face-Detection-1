# AI Context Log

## Files read
- [README.md](../../README.md)
- [docs/testing/README.md](../../docs/testing/README.md)
- [docs/testing/integration-testing.md](../../docs/testing/integration-testing.md)
- [backend/main.py](../../backend/main.py)
- [backend/models/face_detector.py](../../backend/models/face_detector.py)
- [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)
- [backend/quality/face_quality.py](../../backend/quality/face_quality.py)

## Decisions
- Integration testing nên tập trung vào endpoint /detect vì đây là điểm nối giữa request, detector, segmenter, quality assessment và response payload.
- Roadmap nên phản ánh hướng triển khai thực tế: pytest + HTML report + coverage + dashboard Streamlit.
- Nội dung tài liệu phải gắn với implementation hiện tại của backend và không invent thêm thành phần chưa có.

## Assumptions
- Dashboard Streamlit được đề xuất như một hướng phát triển tiếp theo, không phải là requirement hiện tại của repository.
- Tests integration có thể dựa trên FastAPI TestClient hoặc các công cụ HTTP tương đương.

## Missing information
- Chưa có test integration hiện thực trong thư mục tests/integration.
- Chưa có fixture ảnh mẫu và report artifact được ghi nhận trong repo.

## TODO
- Bổ sung các test integration thực tế khi có fixture ảnh và môi trường pytest sẵn sàng.
- Thêm tài liệu cho dashboard testing center nếu triển khai Streamlit sau này.