import cv2
import numpy as np
import torch

from backend.segmentation import preprocess as segmentation_preprocess
from backend.segmentation.postprocess import logits_to_binary_mask
from backend.segmentation.predict import UNetPredictor


def test_logits_to_binary_mask_marks_face_classes_as_foreground():
    logits = np.zeros((1, 19, 4, 4), dtype=np.float32)
    logits[0, 1, 0, 0] = 1.0
    logits[0, 14, 1, 1] = 1.0

    mask = logits_to_binary_mask(logits)

    assert mask.shape == (4, 4)
    assert mask[0, 0] == 255
    assert mask[1, 1] == 0


def test_unet_predictor_predict_returns_mask_with_original_shape(monkeypatch):
    class DummyModel:
        def __init__(self, *args, **kwargs):
            self.device = None

        def to(self, device):
            self.device = device
            return self

        def eval(self):
            return self

        def __call__(self, x):
            logits = torch.zeros((1, 19, 512, 512), dtype=torch.float32)
            logits[:, 1, :, :] = 1.0
            return logits

    monkeypatch.setattr("backend.segmentation.predict.os.path.exists", lambda _path: False)
    monkeypatch.setattr("backend.segmentation.predict.UNet", DummyModel)

    predictor = UNetPredictor(weights_path="unused.pth", device="cpu")
    image = np.zeros((24, 32, 3), dtype=np.uint8)

    mask = predictor.predict(image)

    assert mask.shape == (24, 32)
    assert mask.dtype == np.uint8
    assert np.unique(mask).tolist() in ([0, 255], [255])


def test_unet_predictor_pipeline_produces_binary_mask(monkeypatch):
    class DummyModel:
        def __init__(self, *args, **kwargs):
            self.device = None

        def to(self, device):
            self.device = device
            return self

        def eval(self):
            return self

        def __call__(self, x):
            logits = torch.zeros((1, 19, 512, 512), dtype=torch.float32)
            logits[:, 1, :, :] = 1.0
            return logits

    monkeypatch.setattr("backend.segmentation.predict.os.path.exists", lambda _path: False)
    monkeypatch.setattr("backend.segmentation.predict.UNet", DummyModel)

    predictor = UNetPredictor(weights_path="unused.pth", device="cpu")
    image = np.random.randint(0, 255, size=(64, 80, 3), dtype=np.uint8)

    mask = predictor.predict(image)

    assert mask.shape == (64, 80)
    assert mask.dtype == np.uint8
    assert np.all(np.isin(mask, [0, 255]))
    assert np.count_nonzero(mask) == mask.size


def test_preprocess_single_mask_combines_attribute_masks(tmp_path, monkeypatch):
    monkeypatch.setattr(segmentation_preprocess, "MASK_DIR", str(tmp_path))
    monkeypatch.setattr(segmentation_preprocess, "MASK_ANNO_DIR", str(tmp_path / "annotations"))

    class DummyImage:
        def __init__(self, array):
            self.array = array

        def convert(self, _mode):
            return self.array

    monkeypatch.setattr(
        segmentation_preprocess.Image,
        "open",
        lambda _path: DummyImage(np.full((512, 512), 225, dtype=np.uint8)),
    )
    annotations_dir = tmp_path / "annotations" / "0"
    annotations_dir.mkdir(parents=True, exist_ok=True)
    (annotations_dir / "00001_skin.png").write_bytes(b"dummy")

    result = segmentation_preprocess.preprocess_single_mask(1)

    assert result[0] == 1
    assert result[1] is True

    saved_mask = cv2.imread(str(tmp_path / "1.png"), cv2.IMREAD_GRAYSCALE)
    assert saved_mask.shape == (512, 512)
    assert np.count_nonzero(saved_mask) > 0
    assert saved_mask[0, 0] in {0, 1}
