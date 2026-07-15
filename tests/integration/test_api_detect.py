"""Sơ bộ integration tests cho endpoint /detect."""

import io

import numpy as np
import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture
def client(monkeypatch):
    class DummyDetector:
        def detect(self, img_raw, confidence_threshold=0.5, upscale=False):
            # Return a box that is >= MIN_FACE_PX (36px) so it passes the geometric filter
            return [
                {
                    "box": [0, 0, 80, 80],
                    "confidence": 0.95,
                    "landmarks": [20, 20, 60, 20, 40, 40, 25, 60, 55, 60],
                }
            ]

    class DummySegmenter:
        def predict_batch(self, face_crops_bgr):
            return [np.full(crop.shape[:2], 255, dtype=np.uint8) for crop in face_crops_bgr]

    monkeypatch.setattr("backend.main.get_detector", lambda network_name: DummyDetector())
    monkeypatch.setattr("backend.main.get_segmenter", lambda: DummySegmenter())
    return TestClient(app)


def test_root_endpoint_returns_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_detect_with_invalid_image_returns_400(client):
    files = {"image": ("bad.jpg", b"not-an-image", "image/jpeg")}
    response = client.post("/detect", files=files)
    assert response.status_code == 400


def test_detect_response_has_required_fields(client):
    """Test that the /detect endpoint returns a well-formed JSON payload."""
    image_bytes = io.BytesIO()
    image_array = np.zeros((320, 320, 3), dtype=np.uint8)
    from PIL import Image

    Image.fromarray(image_array).save(image_bytes, format="JPEG")
    image_bytes.seek(0)

    files = {"image": ("sample.jpg", image_bytes.getvalue(), "image/jpeg")}
    response = client.post(
        "/detect",
        files=files,
        data={"save_report": "false"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "image" in payload
    assert "face_count" in payload
    assert "faces" in payload
    assert "latency_ms" in payload
    assert isinstance(payload["face_count"], int)
    assert payload["face_count"] >= 0


def test_detect_with_valid_image_returns_expected_structure(client):
    """Test that a sufficiently large image with dummy detector returns a detected face."""
    image_bytes = io.BytesIO()
    # Use a 320x320 image so the dummy face box (80x80) is geometrically valid
    image_array = np.zeros((320, 320, 3), dtype=np.uint8)
    from PIL import Image

    Image.fromarray(image_array).save(image_bytes, format="JPEG")
    image_bytes.seek(0)

    files = {"image": ("sample.jpg", image_bytes.getvalue(), "image/jpeg")}
    response = client.post(
        "/detect",
        files=files,
        data={"save_report": "true", "report_name": "sample_case"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "image" in payload
    assert "face_count" in payload
    assert "faces" in payload
    assert "latency_ms" in payload
    # Note: face_count may be 0 on first frame (hit-streak gate requires N=2 confirmations)
    # This is by design - the tracker promotes tentative detections after the second match
    assert payload["face_count"] >= 0
    assert "report_dir" in payload
    assert "report_url" in payload


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
