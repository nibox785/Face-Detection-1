# Phase 01 - Discovery Context

## Phase Name
Phase 01 - Discovery

## Task Objective
Tạo hiểu biết ban đầu về hệ thống bằng cách đọc repository, backend, frontend, tài liệu và cấu trúc test để xây dựng tài liệu phân tích và kiến trúc phù hợp với hiện trạng code.

## Files Read
- [README.md](../../README.md)
- [requirements.txt](../../requirements.txt)
- [run.py](../../run.py)
- [backend/main.py](../../backend/main.py)
- [backend/models/face_detector.py](../../backend/models/face_detector.py)
- [backend/models/face_segmenter.py](../../backend/models/face_segmenter.py)
- [backend/quality/face_quality.py](../../backend/quality/face_quality.py)
- [frontend/js/app.js](../../frontend/js/app.js)
- [backend/train.py](../../backend/train.py)
- [backend/convert_to_onnx.py](../../backend/convert_to_onnx.py)
- [backend/segmentation/train.py](../../backend/segmentation/train.py)
- [backend/segmentation/evaluate.py](../../backend/segmentation/evaluate.py)
- [tests/README.md](../../tests/README.md)

## Files Generated
- [docs/requirements/README.md](../../docs/requirements/README.md)
- [docs/requirements/functional.md](../../docs/requirements/functional.md)
- [docs/requirements/non-functional.md](../../docs/requirements/non-functional.md)
- [docs/requirements/constraints.md](../../docs/requirements/constraints.md)
- [docs/requirements/assumptions.md](../../docs/requirements/assumptions.md)
- [docs/requirements/acceptance.md](../../docs/requirements/acceptance.md)
- [docs/features/README.md](../../docs/features/README.md)
- [docs/features/face-detection.md](../../docs/features/face-detection.md)
- [docs/features/face-segmentation.md](../../docs/features/face-segmentation.md)
- [docs/features/quality-assessment.md](../../docs/features/quality-assessment.md)
- [docs/features/camera.md](../../docs/features/camera.md)
- [docs/architecture/system-overview.md](../../docs/architecture/system-overview.md)
- [docs/architecture/backend-flow.md](../../docs/architecture/backend-flow.md)
- [docs/architecture/frontend-flow.md](../../docs/architecture/frontend-flow.md)
- [docs/architecture/ai-pipeline.md](../../docs/architecture/ai-pipeline.md)
- [docs/architecture/inference-lifecycle.md](../../docs/architecture/inference-lifecycle.md)
- [docs/development/dependency.md](../../docs/development/dependency.md)
- [docs/development/configuration.md](../../docs/development/configuration.md)
- [docs/development/project-structure.md](../../docs/development/project-structure.md)
- [docs/development/coding-style.md](../../docs/development/coding-style.md)
- [docs/testing/testing-strategy.md](../../docs/testing/testing-strategy.md)
- [docs/testing/unit-testing.md](../../docs/testing/unit-testing.md)
- [docs/testing/model-testing.md](../../docs/testing/model-testing.md)
- [docs/testing/integration-testing.md](../../docs/testing/integration-testing.md)
- [docs/testing/pipeline-testing.md](../../docs/testing/pipeline-testing.md)
- [docs/testing/regression-testing.md](../../docs/testing/regression-testing.md)
- [docs/testing/benchmark-testing.md](../../docs/testing/benchmark-testing.md)
- [docs/testing/coverage.md](../../docs/testing/coverage.md)

## Assumptions
- Repository là nguồn truth chính cho hiểu biết hiện trạng hệ thống.
- Không thêm tính năng mới ngoài những gì đã được code và xác nhận qua file.
- Testing hiện tại chủ yếu là script đánh giá mô hình, chưa phải pytest suite hoàn chỉnh.

## Open Questions
- Có cần triển khai pytest suite thực tế cho các module backend không?
- Có sẵn dataset mẫu và weights cho việc chạy integration test đầy đủ không?

## TODO
- Bổ sung test thực tế vào [tests](../../tests).
- Cập nhật tài liệu khi có thay đổi behavior hoặc cấu hình mới.
