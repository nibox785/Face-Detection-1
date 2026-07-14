import os
import time
import io
import pytest
import numpy as np
import cv2
from PIL import Image
from fastapi.testclient import TestClient

from backend.main import app
from backend.models.face_detector import RetinaFaceDetector
from backend.models.face_segmenter import UNetFaceSegmenter

# Test fixture for dummy image
@pytest.fixture
def sample_image():
    # 640x480 dummy image
    return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

@pytest.fixture
def client():
    return TestClient(app)

def test_detector_performance(sample_image):
    print("\n" + "="*50)
    print(" DETECTOR PERFORMANCE BENCHMARK ")
    print("="*50)
    
    # Benchmark MobileNet0.25
    try:
        detector_mnet = RetinaFaceDetector(network_name="mobile0.25")
        # Warmup
        _ = detector_mnet.detect(sample_image)
        
        t0 = time.time()
        iterations = 5
        for _ in range(iterations):
            _ = detector_mnet.detect(sample_image)
        t_avg_mnet = (time.time() - t0) / iterations * 1000
        print(f"[*] MobileNet0.25 avg latency: {t_avg_mnet:.2f} ms")
    except Exception as e:
        print(f"[-] MobileNet0.25 benchmark failed: {e}")
        t_avg_mnet = None

    # Benchmark ResNet50
    try:
        detector_re50 = RetinaFaceDetector(network_name="resnet50")
        # Warmup
        _ = detector_re50.detect(sample_image)
        
        t0 = time.time()
        iterations = 3 # ResNet50 is heavy, run 3 times
        for _ in range(iterations):
            _ = detector_re50.detect(sample_image)
        t_avg_re50 = (time.time() - t0) / iterations * 1000
        print(f"[*] ResNet50 avg latency: {t_avg_re50:.2f} ms")
    except Exception as e:
        print(f"[-] ResNet50 benchmark failed (perhaps weights not present): {e}")
        t_avg_re50 = None
        
    assert t_avg_mnet is not None or t_avg_re50 is not None

def test_segmenter_performance():
    print("\n" + "="*50)
    print(" SEGMENTER PERFORMANCE BENCHMARK ")
    print("="*50)
    
    try:
        segmenter = UNetFaceSegmenter()
        # Create a sample face crop matching standard sizes
        crop = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Warmup
        _ = segmenter.predict(crop)
        
        t0 = time.time()
        iterations = 10
        for _ in range(iterations):
            _ = segmenter.predict(crop)
        t_avg = (time.time() - t0) / iterations * 1000
        print(f"[*] U-Net Segmenter (input shape: {segmenter.input_width}x{segmenter.input_height})")
        print(f"    Avg latency per face crop: {t_avg:.2f} ms")
        assert t_avg > 0
    except Exception as e:
        print(f"[-] U-Net Segmenter benchmark failed: {e}")
        pytest.fail(f"U-Net Segmenter benchmark failed: {e}")

def test_api_detect_pipeline_performance(client):
    print("\n" + "="*50)
    print(" END-TO-END API /detect PIPELINE BENCHMARK ")
    print("="*50)
    
    # Create valid JPEG in memory
    img_bytes = io.BytesIO()
    img_array = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    Image.fromarray(img_array).save(img_bytes, format="JPEG")
    img_data = img_bytes.getvalue()
    
    # Test with draw_mask = false
    files = {"image": ("test_frame.jpg", img_data, "image/jpeg")}
    data_no_mask = {"network": "mobile0.25", "threshold": 0.5, "draw_mask": "false", "upscale": "false"}
    
    # Warmup
    _ = client.post("/detect", files=files, data=data_no_mask)
    
    t0 = time.time()
    iterations = 5
    for _ in range(iterations):
        files = {"image": ("test_frame.jpg", img_data, "image/jpeg")}
        _ = client.post("/detect", files=files, data=data_no_mask)
    t_avg_no_mask = (time.time() - t0) / iterations * 1000
    print(f"[*] Pipeline /detect (draw_mask=False) avg latency: {t_avg_no_mask:.2f} ms")

    # Test with draw_mask = true
    files = {"image": ("test_frame.jpg", img_data, "image/jpeg")}
    data_with_mask = {"network": "mobile0.25", "threshold": 0.5, "draw_mask": "true", "upscale": "false"}
    
    # Warmup
    _ = client.post("/detect", files=files, data=data_with_mask)
    
    t0 = time.time()
    for _ in range(iterations):
        files = {"image": ("test_frame.jpg", img_data, "image/jpeg")}
        _ = client.post("/detect", files=files, data=data_with_mask)
    t_avg_with_mask = (time.time() - t0) / iterations * 1000
    print(f"[*] Pipeline /detect (draw_mask=True) avg latency: {t_avg_with_mask:.2f} ms")
    
    print("="*50 + "\n")
    assert t_avg_no_mask > 0
    assert t_avg_with_mask > 0
