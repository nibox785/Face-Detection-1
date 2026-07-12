"""Sơ bộ unit tests cho logic đánh giá chất lượng khuôn mặt."""

import numpy as np

from backend.quality.face_quality import (
    analyze_face_quality,
    check_face_size,
    check_head_pose,
    check_occlusion,
    check_visibility,
)


def test_check_face_size_returns_too_small_for_small_box():
    box = [0, 0, 10, 10]
    assert check_face_size(box, (100, 100)) == "Too Small"


def test_check_face_size_returns_normal_for_average_box():
    box = [0, 0, 80, 80]
    assert check_face_size(box, (100, 100)) == "Normal"


def test_check_visibility_returns_zero_for_empty_mask():
    mask = np.zeros((50, 50), dtype=np.uint8)
    box = [0, 0, 50, 50]
    assert check_visibility(mask, box) == 0


def test_check_occlusion_flags_low_visibility():
    assert check_occlusion(60) is True
    assert check_occlusion(70) is False


def test_check_head_pose_returns_normal_for_valid_landmarks():
    landmarks = [50, 60, 80, 60, 65, 75, 70, 85, 75, 90]
    assert check_head_pose(landmarks) == "Normal"


def test_analyze_face_quality_returns_expected_structure():
    box = [0, 0, 100, 100]
    mask = np.ones((100, 100), dtype=np.uint8)
    landmarks = [40, 50, 60, 50, 50, 70, 55, 80, 60, 80]

    result = analyze_face_quality(box, 0.9, landmarks, mask)

    assert set(result.keys()) == {"visibility", "quality_score", "pose", "status", "rating"}
    assert result["visibility"] >= 0
    assert result["quality_score"] >= 0
    assert result["rating"] in {"Excellent", "Good", "Acceptable", "Poor", "Unusable"}