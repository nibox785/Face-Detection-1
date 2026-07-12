# Handoff Phiên Làm Việc: Face Detection + Segmentation Testing và Reporting

## Tóm tắt điều hành
- Phiên làm việc này tập trung vào việc ổn định và mở rộng bộ test cho pipeline phát hiện khuôn mặt và segmentation, rồi thêm một luồng sinh báo cáo nhẹ để có thể xem và lưu kết quả inference một cách trực quan.
- Dự án hiện đã có cấu trúc pytest thực tế cho các lớp unit, model và integration, cùng với hỗ trợ API để lưu kết quả đầu ra dưới dạng ảnh và JSON trong thư mục reports.
- Bộ test hiện đang chạy thành công và tạo nền tảng regression phù hợp cho các thay đổi trong tương lai.

## Mục tiêu
- Tạo và ổn định các test cho workflow phát hiện khuôn mặt và segmentation.
- Bao phủ các lớp unit, model và integration mà không phụ thuộc vào trọng số mô hình thật trong giai đoạn kiểm thử cơ bản.
- Thêm cơ chế ghi báo cáo để kết quả inference có thể được lưu lại và xem trực quan.
- Để lại hướng dẫn rõ ràng cho AI phiên làm việc tiếp theo để tiếp tục phát triển hiệu quả.

## Công việc đã hoàn thành
- Thêm tài liệu và cấu trúc test dưới thư mục tests.
- Tạo hỗ trợ import cho pytest thông qua file conftest để backend có thể import đúng.
- Implement unit test cho logic đánh giá chất lượng khuôn mặt.
- Implement model-level test cho wrapper RetinaFace detector.
- Implement model-level test cho segmentation postprocessing và predictor.
- Implement integration test cho endpoint detect của API.
- Thêm utility để sinh report cho mỗi lần inference.
- Gắn workflow ghi report vào endpoint /detect.
- Xác minh toàn bộ suite kiểm thử liên quan đã chạy thành công.

## Thay đổi về kiến trúc
- Giới thiệu phân lớp test:
  - unit: kiểm tra logic nhẹ
  - model: kiểm tra behavior của wrapper/model bằng stub deterministic
  - integration: kiểm tra API và tương tác dependency
- Thêm hỗ trợ lưu report cho mỗi lần inference:
  - ảnh đầu vào được lưu
  - ảnh kết quả đã annotate được lưu
  - payload JSON được lưu
  - báo cáo được viết vào thư mục reports/inference
- Mở rộng API detect để có thể lưu report khi được yêu cầu thông qua tham số form.

## Quyết định kỹ thuật
- Dùng pytest với stub object deterministic thay vì trọng số mô hình thật cho hầu hết các test nền tảng.
- Giữ test ổn định và thân thiện với CI bằng cách tránh dependency nặng khi chưa cần.
- Dùng monkeypatching cho wrapper model và dependency injection cho API để cô lập behavior cần test.
- Chọn định dạng report đơn giản bằng JSON + JPG để giữ tính năng nhẹ và dễ xem.
- Giữ behavior API cũ, chỉ thêm report generation ở chế độ opt-in để không ảnh hưởng khi không bật.

## Các file đã chỉnh sửa
- [tests/conftest.py](tests/conftest.py)
- [tests/unit/test_face_quality.py](tests/unit/test_face_quality.py)
- [tests/model/test_face_detector.py](tests/model/test_face_detector.py)
- [tests/model/test_segmentation.py](tests/model/test_segmentation.py)
- [tests/integration/test_api_detect.py](tests/integration/test_api_detect.py)
- [backend/segmentation/config.py](backend/segmentation/config.py)
- [backend/utils/reporting.py](backend/utils/reporting.py)
- [backend/main.py](backend/main.py)

## Tính năng đã triển khai
- Cấu trúc suite test pytest và coverage mẫu.
- Các test dành riêng cho segmenter bao gồm:
  - chuyển logits thành mask
  - shape và dtype đầu ra của predictor
  - behavior của preprocessing helper
  - generation binary mask theo kiểu pipeline
- Test integration cho endpoint detect.
- Tính năng report cho mỗi request detect khi bật:
  - input.jpg
  - annotated.jpg
  - result.json

## Lỗi đã sửa
- Sửa lỗi import path bằng cách thêm repository và backend vào sys.path khi chạy test.
- Sửa giả định về shape output của detector test để phù hợp với expected tensor của decoder.
- Sửa behavior integration test để phù hợp với exception handling thực tế của FastAPI/TestClient.
- Sửa thiếu config segmentation cần cho preprocessing import.
- Điều chỉnh fixture test cho preprocessing và report output.

## Refactoring
- Tạo phân tách rõ ràng hơn giữa logic test và behavior integration.
- Giữ test double tối giản và hướng tới behavior thực tế thay vì mock quá mức.
- Chuyển logic lưu report sang module utility riêng để endpoint API không bị rối.

## Kết quả test
- Suite unit/model/integration hiện đang pass.
- Số lượng từ lần verify gần nhất:
  - 15 passed
  - 1 warning
  - 0 failed

## Bằng chứng xác thực
- Đã verify bằng:
  - .\.venv\Scripts\python.exe -m pytest tests/model/test_segmentation.py -q
  - .\.venv\Scripts\python.exe -m pytest tests/unit tests/model tests/integration -q
- Bằng chứng từ lần chạy gần đây:
  - 15 passed, 1 warning trong 3.47s

## Tác động về hiệu năng
- Overhead của suite test còn nhỏ và chấp nhận được cho phát triển cục bộ và CI.
- Report generation thêm I/O file cho mỗi request, nhỏ đối với validation thủ công nhưng có thể tăng nếu dùng cho batch lớn.
- Tính năng report là opt-in và không ảnh hưởng behavior API bình thường nếu không bật.

## Vấn đề còn lại
- Các test hiện mạnh ở mức regression và smoke test, nhưng chưa validate trọng số mô hình thật trên ảnh thật end-to-end.
- Tính năng report hữu ích cho inspection thủ công, nhưng chưa có HTML gallery hay index để duyệt trực quan hơn.
- Chưa có pipeline benchmark hoặc metric-based evaluation tự động.
- Các helper preprocessing segmentation vẫn phụ thuộc vào cấu trúc dữ liệu ban đầu và đường dẫn dataset có thể không tồn tại trong môi trường local nếu chưa chuẩn bị đúng.

## Technical Debt
- Một số test vẫn dựa vào monkeypatching và stub thay vì chạy toàn bộ end-to-end model.
- Endpoint API còn chứa nhiều logic inline, có thể refactor thành service helpers để rõ ràng và dễ test hơn.
- Report generation còn cơ bản, có thể mở rộng để thêm per-face crop overlay và metadata phong phú hơn.

## Rủi ro
- Behavior mô hình thật có thể khác với stub test nếu ONNX/PyTorch model thực sự chạy trên dữ liệu production.
- Report artifacts có thể tích lũy trong thư mục reports nếu dùng nhiều mà không có retention policy.
- Validation hiện tại chưa thay thế được benchmark hoàn chỉnh trên tập dữ liệu đã được chọn và đánh nhãn.

## Bài học rút ra
- Test ổn định cho ML inference pipeline nên tập trung vào interface contract và expected tensor shape hơn là phụ thuộc hoàn toàn vào runtime dependency nặng.
- Integration test cho FastAPI cần tính đến exception semantics thật của framework, đặc biệt với input không hợp lệ.
- Report generation rất hữu ích cho debug và manual validation vì làm output dễ inspect mà không cần viết script riêng.

## Insight quan trọng
- Dự án hiện có thể được validate theo 3 góc nhìn:
  - logic correctness
  - model wrapper behavior
  - API integration behavior
- Chiến lược phân lớp này là một lựa chọn tốt cho các thay đổi tiếp theo trong pipeline detector/segmenter.
- Kiểm tra trực quan ảnh annotated là rất quan trọng để debug mô hình và review cho bên liên quan.

## Ngữ cảnh quan trọng
- Repository dùng FastAPI backend với detector và segmentation components.
- Chiến lược test hiện nhấn vào stability và chạy thực tế trên local/CI hơn là benchmark production-model đầy đủ.
- Reports được viết vào thư mục reports/inference trong workspace.
- Endpoint nhận các tham số form để lưu report và đặt tên report.

## Lệnh quan trọng
- Kích hoạt environment:
  - .\.venv\Scripts\Activate.ps1
- Chạy test cho segmenter:
  - .\.venv\Scripts\python.exe -m pytest tests/model/test_segmentation.py -q
- Chạy toàn bộ suite liên quan:
  - .\.venv\Scripts\python.exe -m pytest tests/unit tests/model tests/integration -q
- Khởi động backend:
  - .\.venv\Scripts\python.exe backend\main.py
- Ví dụ gọi API với report enabled:
  - curl -X POST "http://127.0.0.1:5000/detect" -F "image=@test.jpg" -F "save_report=true" -F "report_name=sample_case"

## Ghi chú môi trường
- Môi trường Python là virtualenv cục bộ tại .venv.
- Workspace đang chạy trên Windows.
- FastAPI TestClient và các package pytest liên quan đã được cài vào environment.
- Lần verify gần nhất hoàn tất thành công với một warning về deprecation của Starlette/httpx.

## TODO (Ưu tiên)
1. Thêm HTML report index để duyệt các report đã sinh một cách trực quan.
2. Thêm batch evaluation script cho một thư mục ảnh thật với expected output.
3. Thêm benchmark-style metrics cho chất lượng detect và segmentation.
4. Thêm test dùng trọng số mô hình thật trên một tập ảnh nhỏ được chọn lọc.
5. Refactor logic endpoint API thành service helpers để dễ bảo trì.

## Suggested Commit Message
- test: add segmentation and API coverage plus inference report output

## Suggested PR Description
- PR này thêm suite pytest thực tế cho workflow face detection và segmentation, bao gồm unit, model và integration coverage.
- Nó cũng giới thiệu tính năng opt-in inference reporting, lưu ảnh đầu vào, ảnh kết quả annotate và payload JSON cho mỗi request detect.
- Những thay đổi này cải thiện regression safety và giúp manual validation của detection/segmentation output dễ dàng hơn.

## Resume Prompt cho phiên AI tiếp theo
- Tiếp tục phát triển dự án Face-Detection từ trạng thái hiện tại.
- Repository hiện đã có cấu trúc pytest hoạt động cho unit, model và integration layers.
- Công việc gần đây đã thêm test cho segmentation và tính năng opt-in inference reporting cho API /detect.
- Các file liên quan gồm:
  - [tests/conftest.py](tests/conftest.py)
  - [tests/unit/test_face_quality.py](tests/unit/test_face_quality.py)
  - [tests/model/test_face_detector.py](tests/model/test_face_detector.py)
  - [tests/model/test_segmentation.py](tests/model/test_segmentation.py)
  - [tests/integration/test_api_detect.py](tests/integration/test_api_detect.py)
  - [backend/segmentation/config.py](backend/segmentation/config.py)
  - [backend/utils/reporting.py](backend/utils/reporting.py)
  - [backend/main.py](backend/main.py)
- Trạng thái validation hiện tại: suite pytest pass với 15 passed và 1 warning.
- Các bước tiếp theo ưu tiên:
  1. Thêm HTML report index hoặc gallery để duyệt report.
  2. Thêm batch evaluation workflow cho ảnh thật.
  3. Thêm test mạnh hơn với mô hình thật và tập dữ liệu đã chọn.
  4. Refactor endpoint API thành service functions nhỏ hơn để dễ bảo trì.
- Khi tiếp tục, hãy giữ tính năng report opt-in và giữ test ổn định, deterministic.
- Dùng environment ảo hiện tại tại .venv.
- Trước khi xem là hoàn tất, hãy chạy pytest để verify thay đổi.
