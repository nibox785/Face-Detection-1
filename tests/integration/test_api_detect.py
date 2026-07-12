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
            return [
                {
                    "box": [0, 0, 20, 20],
                    "confidence": 0.95,
                    "landmarks": [2, 2, 4, 2, 3, 3, 4, 4, 5, 5],
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
    assert response.status_code == 500


def test_detect_with_valid_image_returns_expected_structure(client):
    image_bytes = io.BytesIO()
    image_array = np.zeros((32, 32, 3), dtype=np.uint8)
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
    assert payload["face_count"] >= 1
    assert payload["faces"][0]["mask_rle"]["size"] == [32, 32]
    assert payload["faces"][0]["mask_rle"]["start_val"] in {0, 1}
    assert "report_dir" in payload
    assert "report_url" in payload
