"""Sơ bộ model tests cho wrapper detector RetinaFace."""

import numpy as np
import pytest

from backend.models.face_detector import RetinaFaceDetector


@pytest.fixture
def dummy_image():
    return np.zeros((64, 64, 3), dtype=np.uint8)


def test_detector_class_can_be_instantiated(monkeypatch, dummy_image):
    class DummySession:
        def get_inputs(self):
            return [type("Input", (), {"name": "input"})()]

        def run(self, *_args, **_kwargs):
            return [
                np.zeros((1, 168, 4), dtype=np.float32),
                np.zeros((1, 168, 2), dtype=np.float32),
                np.zeros((1, 168, 10), dtype=np.float32),
            ]

    monkeypatch.setattr(
        "backend.models.face_detector.ort.InferenceSession",
        lambda *args, **kwargs: DummySession(),
    )

    detector = RetinaFaceDetector(network_name="mobile0.25", weights_dir=".")
    assert detector is not None


def test_detector_detect_returns_list(monkeypatch, dummy_image):
    class DummySession:
        def get_inputs(self):
            return [type("Input", (), {"name": "input"})()]

        def run(self, *_args, **_kwargs):
            return [
                np.zeros((1, 168, 4), dtype=np.float32),
                np.zeros((1, 168, 2), dtype=np.float32),
                np.zeros((1, 168, 10), dtype=np.float32),
            ]

    monkeypatch.setattr(
        "backend.models.face_detector.ort.InferenceSession",
        lambda *args, **kwargs: DummySession(),
    )

    detector = RetinaFaceDetector(network_name="mobile0.25", weights_dir=".")
    result = detector.detect(dummy_image, confidence_threshold=0.0)

    assert isinstance(result, list)
