import json
import logging
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

LOG_ROOT = Path(__file__).resolve().parents[2] / "logs"
INFERENCE_LOG_PATH = LOG_ROOT / "inference" / "inference.log"
BENCHMARK_LOG_PATH = LOG_ROOT / "benchmark" / "benchmark.log"

LOG_ROOT.mkdir(parents=True, exist_ok=True)
INFERENCE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
BENCHMARK_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extras"):
            payload.update(record.extras)
        return json.dumps(payload, ensure_ascii=False)


def _create_logger(name: str, log_path: Path) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(JsonFormatter())
        logger.addHandler(stream_handler)
    return logger


def get_app_logger() -> logging.Logger:
    return _create_logger("face_surveillance_app", INFERENCE_LOG_PATH)


def get_benchmark_logger() -> logging.Logger:
    return _create_logger("face_surveillance_benchmark", BENCHMARK_LOG_PATH)


def generate_request_id() -> str:
    return str(uuid.uuid4())


def log_inference_event(event: str, request_id: str, model: str, stage: str, face_count: int, latency_ms: float, extra=None):
    logger = get_app_logger()
    payload = {
        "event": event,
        "request_id": request_id,
        "model": model,
        "stage": stage,
        "face_count": face_count,
        "latency_ms": latency_ms,
        "fps": 1000.0 / max(latency_ms, 1),
        "status": "ok",
    }
    if extra:
        payload["extra"] = extra
    logger.info("inference_event", extra={"extras": payload})


def log_benchmark_event(mode: str, model: str, metrics: dict, extra=None):
    logger = get_benchmark_logger()
    payload = {
        "event": "benchmark_result",
        "mode": mode,
        "model": model,
        "metrics": metrics,
    }
    if extra:
        payload["extra"] = extra
    logger.info("benchmark_event", extra={"extras": payload})
