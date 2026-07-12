import json
import re
import time
from pathlib import Path

import cv2
import numpy as np

DEFAULT_REPORT_ROOT = Path(__file__).resolve().parents[2] / "reports" / "inference"


def sanitize_name(name: str | None) -> str:
    if not name:
        return f"report_{int(time.time())}"
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._-")
    return safe_name or f"report_{int(time.time())}"


def save_detection_report(image_input, payload, annotated_image=None, report_name=None, report_root=None):
    """Persist a detection run as a folder containing input/annotated images and JSON payload."""
    report_root = Path(report_root) if report_root is not None else DEFAULT_REPORT_ROOT
    report_dir = report_root / sanitize_name(report_name)
    report_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(image_input, (bytes, bytearray)):
        image_array = np.frombuffer(image_input, np.uint8)
        image_array = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    elif isinstance(image_input, np.ndarray):
        image_array = image_input
    else:
        image_array = None

    if isinstance(image_array, np.ndarray) and image_array.ndim == 3:
        cv2.imwrite(str(report_dir / "input.jpg"), image_array)

    if isinstance(annotated_image, np.ndarray) and annotated_image.ndim == 3:
        cv2.imwrite(str(report_dir / "annotated.jpg"), annotated_image)

    with open(report_dir / "result.json", "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    return report_dir
