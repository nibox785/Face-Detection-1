# Test Suite

## Purpose

Thư mục này chứa toàn bộ mã nguồn kiểm thử.

Chiến lược kiểm thử được mô tả tại:

docs/testing/

---

## Directory

```text
tests/

unit/

model/

integration/

pipeline/

benchmark/

regression/
```

---

## Run

```bash
pytest
```

Unit

```bash
pytest tests/unit
```

Model

```bash
pytest tests/model
```

Pipeline

```bash
pytest tests/pipeline
```

Regression

```bash
pytest tests/regression
```

Benchmark

```bash
pytest tests/benchmark
```