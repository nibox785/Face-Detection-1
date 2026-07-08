# Testing Documentation

## Purpose

Thư mục này mô tả toàn bộ chiến lược kiểm thử của hệ thống AI.

Mỗi tài liệu chỉ chịu trách nhiệm cho một chủ đề duy nhất.

---

## Documents

| File | Purpose |
|------|---------|
| testing-strategy.md | Tổng quan chiến lược kiểm thử |
| unit-testing.md | Unit Test |
| model-testing.md | Model Validation |
| integration-testing.md | API Integration |
| pipeline-testing.md | Pipeline Testing |
| regression-testing.md | Regression Testing |
| benchmark-testing.md | Benchmark |
| coverage.md | Coverage Goal |

---

## Testing Pyramid

```text
Benchmark

Regression

Pipeline

Integration

Model

Unit
```

---

## Execution Flow

```
Developer

↓

Unit Test

↓

Model Test

↓

Integration Test

↓

Pipeline Test

↓

Regression Test

↓

Benchmark

↓

Release
```