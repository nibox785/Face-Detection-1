# Tổng quan hệ thống

Hệ thống được triển khai như một ứng dụng web giám sát khuôn mặt bằng trí tuệ nhân tạo, chạy trên một backend FastAPI và một frontend tĩnh. Người dùng tương tác qua trình duyệt, gửi ảnh hoặc khung hình video vào backend, backend gọi mô hình phát hiện và phân đoạn, sau đó trả lại kết quả đã annotate để frontend hiển thị và lưu trữ bằng chứng.

## Cấu trúc triển khai

- Backend chính nằm ở [backend/main.py](backend/main.py). File này tạo FastAPI app, phục vụ route gốc, route /detect và mount tài nguyên tĩnh frontend.
- Logic phát hiện khuôn mặt nằm ở [backend/models/face_detector.py](backend/models/face_detector.py).
- Logic phân đoạn khuôn mặt nằm ở [backend/models/face_segmenter.py](backend/models/face_segmenter.py).
- Logic đánh giá chất lượng nằm ở [backend/quality/face_quality.py](backend/quality/face_quality.py).
- Frontend UI và vòng lặp xử lý media nằm ở [frontend/index.html](frontend/index.html) và [frontend/js/app.js](frontend/js/app.js).
- Khởi chạy hệ thống được thực hiện bởi [run.py](run.py), nơi kiểm tra và tải model ONNX nếu thiếu.

## Vai trò của từng lớp

- Presentation layer: frontend hiển thị viewport, overlay, biểu đồ và nút xuất bằng chứng.
- API layer: backend nhận request, chuẩn hóa input và trả về kết quả JSON plus hình ảnh annotate.
- AI layer: RetinaFace phát hiện khuôn mặt, U-Net phân đoạn mặt nạ, logic chất lượng đánh giá face quality.
- Supporting layer: file export, telemetry, cảnh báo âm thanh, cache mô hình.

## Luồng vận hành tổng thể

1. Frontend thu thập frame từ ảnh, video hoặc webcam.
2. Frontend gửi frame tới endpoint /detect.
3. Backend giải mã ảnh, gọi detector, tạo mask và đánh giá chất lượng.
4. Backend trả về ảnh đã annotate và danh sách thông tin khuôn mặt.
5. Frontend vẽ overlay, cập nhật biểu đồ và cung cấp chức năng lưu trữ bằng chứng.

## Mô tả sơ đồ thành phần

Các thành phần chính có thể được hiểu như sau:

- Client UI: quản lý nguồn media và hiển thị kết quả.
- API Server: nhận request và điều phối xử lý.
- Detector Service: thực hiện phát hiện khuôn mặt.
- Segmenter Service: thực hiện phân vùng khuôn mặt.
- Quality Analyzer: đánh giá độ visibility, occlusion, pose và quality score.
- Export/Telemetry: lưu frame, crop, mask và ghi log cảnh báo.

## AI-assisted documentation workflow

Hệ thống không chỉ là runtime AI. Nó còn bao gồm quy trình làm việc với AI để thiết kế, ghi nhận và review tài liệu.

1. Yêu cầu hoặc vấn đề được xác định trong Markdown.
2. Prompt được soạn thảo và ghi lại trong [docs/ai/prompt-history.md](../ai/prompt-history.md).
3. AI hỗ trợ tạo nội dung, đề xuất kiến trúc hoặc phân tích logic.
4. Nội dung được kiểm duyệt, sửa lại và xác minh bằng tay.
5. Quyết định cập nhật được ghi vào [docs/ai/decision-log.md](../ai/decision-log.md) và liên kết với phiên bản mô hình nếu cần.

## AI + Logic Execution Flow

Luồng chính cho AI và logic trong runtime nên được tách rõ thành hai bước:

1. Data ingestion
   - Frontend thu thập frame từ ảnh, video hoặc webcam.
   - Backend nhận request và giải mã ảnh.
2. AI perception
   - RetinaFace thực hiện phát hiện khuôn mặt và landmarks.
   - U-Net phân đoạn mặt nạ cho từng khuôn mặt hợp lệ.
3. Feature extraction
   - Tính diện tích mặt nạ, tỷ lệ mặt/mask, mức occlusion và các chỉ số pose.
   - Chuẩn bị dữ liệu thô cho logic đánh giá.
4. Decision logic
   - Áp dụng rule-based policy để phân loại chất lượng.
   - Quyết định face status (valid / low_quality / occluded / suspicious).
   - Xác định có cần cảnh báo, lưu evidence hay bỏ qua.
5. Output & action
   - Trả về JSON chứa cả AI output và business decision.
   - Frontend hiển thị bounding box, mask, rating và cảnh báo.

## Backend detect pipeline and policy layer

Phần backend `/detect` nên được tổ chức theo ba lớp riêng biệt:

- Orchestration layer
  - Nhận request và giải mã ảnh.
  - Chuyển tham số đầu vào như network, threshold, draw_mask, upscale.
  - Điều phối detector, segmenter, quality analyzer và policy engine.
- AI layer
  - RetinaFace cung cấp các bounding box, confidence và landmarks.
  - U-Net tạo binary mask cho khuôn mặt.
  - Quality analyzer trích xuất các chỉ số như occlusion, pose và visibility.
- Policy layer
  - Áp dụng cấu hình ngưỡng và quy tắc để phân loại face status.
  - Xác định hành động: báo cáo, cảnh báo, lưu bằng chứng, hoặc loại bỏ detection.
  - Tách rõ kết quả AI (AI output) và quyết định nghiệp vụ (decision output).

### Chi tiết bước backend

1. Preprocess
   - Đọc ảnh từ `UploadFile`.
   - Giải mã bằng OpenCV.
   - Kiểm tra hợp lệ và kích thước.
2. Detect
   - Khởi tạo hoặc lấy detector cache.
   - Gọi `detecter.detect(...)` để lấy danh sách face candidates.
3. Segment
   - Xây batch crop mặt hợp lệ.
   - Gọi `UNetFaceSegmenter.predict_batch(...)`.
   - Fallback sang ellipse khi U-Net lỗi hoặc face quá nhỏ.
4. Extract
   - Gán mask về vị trí gốc.
   - Tạo ảnh `face_png_alpha` và `mask_rle`.
   - Tính các đặc trưng bổ sung cho policy.
5. Decide
   - Gọi `QualityPolicy` / `FaceDecisionEngine` để áp dụng rule.
   - Trả về `status`, `rating`, `alert_level`, `should_save_evidence`.
6. Render
   - Vẽ bounding box, landmarks, mask overlay lên ảnh annotate.
   - Tạo base64 JPEG để trả response.

### Đề xuất module

- `backend/policies/face_policy.py`
  - chứa các rule threshold và trạng thái face.
- `backend/services/detect_service.py`
  - tách phần orchestrator ra khỏi route.
- `backend/quality/quality_policy.py`
  - tạo một tầng policy riêng biệt để dễ test.
- `backend/config/ai_policy.py`
  - giữ các tham số như `min_confidence`, `max_occlusion`, `min_mask_area`, `alert_density_threshold`.

### Mô tả response tốt hơn

Response nên chứa hai phần:

- `ai_output`
  - box, confidence, landmarks, mask_rle, face_png_alpha.
- `decision_output`
  - status, rating, pose, visibility, alert_reason, evidence_required.

Định nghĩa này giúp frontend và tài liệu AI dễ tách nhiệm vụ giữa “đầu vào mô hình” và “quyết định sản phẩm”.

## Mối liên hệ giữa runtime và tài liệu

- Runtime AI: phát hiện và phân đoạn khuôn mặt, đánh giá chất lượng.
- Runtime logic: xác định hành động dựa trên kết quả AI và policy của hệ thống.
- Documentation AI: quản trị prompt, quy trình review, ghi nhận quyết định và kiến trúc.
- Markdown đóng vai trò là ngôn ngữ chung giữa nhóm sản phẩm và AI.

Việc hoàn thiện hệ thống cần bao gồm cả hai mặt: pipeline kỹ thuật của backend/frontend và quy trình AI-assisted documentation để đảm bảo các thay đổi được traceable, kiểm soát và dễ review.
