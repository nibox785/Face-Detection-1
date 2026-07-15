# Tài Liệu Dự Án — AI Crowd Face Surveillance Console

Đây là thư mục tài liệu kỹ thuật đầy đủ cho hệ thống giám sát khuôn mặt đám đông. Tất cả tài liệu được cập nhật theo trạng thái code hiện tại.

---

## 📑 Mục Lục Nhanh

### 🏗 Kiến Trúc Hệ Thống
| Tài liệu | Mô tả |
|---|---|
| [system-overview.md](architecture/system-overview.md) | Tổng quan toàn hệ thống, sơ đồ component, changelog |
| [ai-pipeline.md](architecture/ai-pipeline.md) | **Pipeline AI chi tiết**: skip-frame, geometric filter, Hungarian matching, hit-streak gate, U-Net throttling |
| [backend-flow.md](architecture/backend-flow.md) | Luồng xử lý backend |
| [frontend-flow.md](architecture/frontend-flow.md) | Luồng xử lý frontend |
| [inference-lifecycle.md](architecture/inference-lifecycle.md) | Vòng đời một inference request |

### 🔌 API Reference
| Tài liệu | Mô tả |
|---|---|
| [detect.md](api/detect.md) | **Endpoint /detect** — Request params (bao gồm `min_face_px` mới), Response schema đầy đủ |
| [health.md](api/health.md) | Endpoint /health |
| [overview.md](api/overview.md) | Tổng quan API |

### 🎯 Tính Năng
| Tài liệu | Mô tả |
|---|---|
| [face-detection.md](features/face-detection.md) | **Phát hiện & Theo dõi** — SORT-like tracker, geometric filter, Hungarian matching, velocity predictor |
| [face-segmentation.md](features/face-segmentation.md) | U-Net ONNX segmentation |
| [quality-assessment.md](features/quality-assessment.md) | **Face Quality** — Visibility, Occlusion, Head Pose, Score, Rating |
| [camera.md](features/camera.md) | Camera/Media stream management |

### 🛠 Phát Triển
| Tài liệu | Mô tả |
|---|---|
| [project-structure.md](development/project-structure.md) | **Cấu trúc thư mục đầy đủ** với chú thích từng file |
| [dependency.md](development/dependency.md) | **Dependencies** (bao gồm `scipy` mới cho Hungarian Algorithm) |
| [configuration.md](development/configuration.md) | Biến môi trường và cấu hình |
| [coding-style.md](development/coding-style.md) | Quy ước code |

### 🧪 Kiểm Thử
| Tài liệu | Mô tả |
|---|---|
| [testing-strategy.md](testing/testing-strategy.md) | Chiến lược kiểm thử tổng thể |
| [integration-testing.md](testing/integration-testing.md) | Integration test API /detect |
| [unit-testing.md](testing/unit-testing.md) | Unit test face_quality |
| [benchmark-testing.md](testing/benchmark-testing.md) | Benchmark latency & FPS |

### 🚀 Triển Khai
| Tài liệu | Mô tả |
|---|---|
| [local.md](deployment/local.md) | Hướng dẫn chạy local |
| [docker.md](deployment/docker.md) | Hướng dẫn Docker |

---

## 📋 Nguyên Tắc Tài Liệu

- **Mỗi file một trách nhiệm**: Tài liệu chỉ mô tả những gì liên quan trực tiếp đến chủ đề của nó.
- **Luôn đồng bộ với code**: Khi thay đổi code, cập nhật file tài liệu tương ứng.
- **Liên kết chéo thay vì sao chép**: Dùng link markdown thay vì lặp lại nội dung.
- **Ghi rõ trạng thái hiện tại**: Nếu một tính năng đã thay đổi, cập nhật tài liệu ngay.

---

## 🔄 Lịch Sử Cập Nhật Tài Liệu

| Ngày | File cập nhật | Lý do |
|---|---|---|
| 2026-07-16 | `README.md` (gốc) | SORT-like tracker, session gallery, min_face_px slider |
| 2026-07-16 | `docs/api/detect.md` | Thêm `min_face_px` param, update response schema với `id` |
| 2026-07-16 | `docs/architecture/ai-pipeline.md` | Chi tiết đầy đủ SORT pipeline |
| 2026-07-16 | `docs/architecture/system-overview.md` | Cập nhật component diagram, changelog |
| 2026-07-16 | `docs/features/face-detection.md` | SORT tracker, geometric filter, Hungarian, hit-streak |
| 2026-07-16 | `docs/features/quality-assessment.md` | Chi tiết thuật toán và công thức |
| 2026-07-16 | `docs/development/project-structure.md` | Cấu trúc hoàn chỉnh với chú thích đầy đủ |
| 2026-07-16 | `docs/development/dependency.md` | Thêm `scipy` dependency |
| 2026-07-16 | `tests/README.md` | 21 tests, ghi chú SORT hit-streak gate |
