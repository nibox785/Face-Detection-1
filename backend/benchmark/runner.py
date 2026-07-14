import argparse
import json
import time
from pathlib import Path

from ..app_logging.structured_logger import log_benchmark_event
from ..models.face_detector import RetinaFaceDetector
from ..models.face_segmenter import UNetFaceSegmenter
from .metrics import compute_summary_metrics
from .reporter import BenchmarkReporter

DATA_ROOT = Path(__file__).resolve().parents[2] / "tests" / "datasets"
DEFAULT_IMAGE = DATA_ROOT / "benchmark_sample.jpg"


class BenchmarkRunner:
    def __init__(self, repeat=10, network="mobile0.25", image_path=None):
        self.repeat = repeat
        self.network = network
        self.image_path = Path(image_path) if image_path else DEFAULT_IMAGE
        self.detector = RetinaFaceDetector(network_name=network)
        self.segmenter = UNetFaceSegmenter()
        self.results = []

    def _load_image(self):
        import cv2
        if not self.image_path.exists():
            raise FileNotFoundError(f"Benchmark image not found: {self.image_path}")
        return cv2.imread(str(self.image_path))

    def run_pipeline(self):
        img_raw = self._load_image()
        for i in range(self.repeat):
            t_start = time.time()
            faces = self.detector.detect(img_raw, confidence_threshold=0.5, upscale=False)
            unet_crops = []
            for face in faces:
                x1, y1, x2, y2 = map(int, face['box'])
                unet_crops.append(img_raw[y1:y2, x1:x2])
            masks = self.segmenter.predict_batch(unet_crops)
            latency_ms = (time.time() - t_start) * 1000.0
            result = {
                "run_index": i,
                "model": self.network,
                "mode": "pipeline",
                "latency_ms": latency_ms,
                "face_count": len(faces),
                "fallback_count": sum(1 for crop in unet_crops if crop.size == 0),
            }
            self.results.append(result)
            log_benchmark_event("pipeline", self.network, result)
        return self.results

    def run_detector(self):
        img_raw = self._load_image()
        for i in range(self.repeat):
            t_start = time.time()
            faces = self.detector.detect(img_raw, confidence_threshold=0.5, upscale=False)
            latency_ms = (time.time() - t_start) * 1000.0
            result = {
                "run_index": i,
                "model": self.network,
                "mode": "detector",
                "latency_ms": latency_ms,
                "face_count": len(faces),
            }
            self.results.append(result)
            log_benchmark_event("detector", self.network, result)
        return self.results

    def run_segmenter(self):
        img_raw = self._load_image()
        faces = self.detector.detect(img_raw, confidence_threshold=0.5, upscale=False)
        crops = [img_raw[int(f['box'][1]):int(f['box'][3]), int(f['box'][0]):int(f['box'][2])] for f in faces]
        for i in range(self.repeat):
            t_start = time.time()
            masks = self.segmenter.predict_batch(crops)
            latency_ms = (time.time() - t_start) * 1000.0
            result = {
                "run_index": i,
                "model": self.network,
                "mode": "segmenter",
                "latency_ms": latency_ms,
                "mask_count": len(masks),
            }
            self.results.append(result)
            log_benchmark_event("segmenter", self.network, result)
        return self.results

    def save_report(self):
        summary = compute_summary_metrics(self.results)
        BenchmarkReporter.save_json(summary)
        BenchmarkReporter.save_csv(summary)
        BenchmarkReporter.save_markdown(summary)
        return summary


def main():
    parser = argparse.ArgumentParser(description="Run benchmark for face surveillance components.")
    parser.add_argument("--mode", choices=["detector", "segmenter", "pipeline"], default="pipeline")
    parser.add_argument("--repeat", type=int, default=10)
    parser.add_argument("--network", choices=["mobile0.25", "resnet50"], default="mobile0.25")
    parser.add_argument("--image", type=str, default=None)
    args = parser.parse_args()

    runner = BenchmarkRunner(repeat=args.repeat, network=args.network, image_path=args.image)
    if args.mode == "detector":
        runner.run_detector()
    elif args.mode == "segmenter":
        runner.run_segmenter()
    else:
        runner.run_pipeline()
    summary = runner.save_report()
    print("Benchmark complete. Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
