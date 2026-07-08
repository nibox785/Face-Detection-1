# Architecture Documentation

## Purpose

Mô tả toàn bộ kiến trúc của hệ thống AI Crowd Face Surveillance.

---

## Documents

| File | Description |
|------|-------------|
| system-overview.md | Tổng quan hệ thống |
| ai-pipeline.md | Luồng AI |
| backend-flow.md | Backend |
| frontend-flow.md | Frontend |
| inference-lifecycle.md | Inference |

---

## Architecture Layers

```text
Frontend

↓

FastAPI

↓

RetinaFace

↓

UNet

↓

Face Quality

↓

Response
```