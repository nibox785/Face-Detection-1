"""Structured logging utilities for the AI face surveillance backend."""
from .structured_logger import get_app_logger, log_inference_event, log_benchmark_event, generate_request_id

__all__ = [
    "get_app_logger",
    "log_inference_event",
    "log_benchmark_event",
    "generate_request_id",
]
