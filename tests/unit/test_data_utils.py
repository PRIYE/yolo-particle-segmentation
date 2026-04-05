"""Unit tests for dataset utilities."""

from pathlib import Path

import numpy as np
import pytest

from src.data.dataset_utils import (
    equal_distribution_sample,
    list_images,
    mask_to_polygon_line,
    polygon_to_yolo_line,
)


def test_polygon_to_yolo_line_normalized():
    poly = np.array([[0.0, 0.0], [100.0, 0.0], [100.0, 100.0], [0.0, 100.0]])
    line = polygon_to_yolo_line(0, poly, image_width=100, image_height=100)
    parts = line.split()
    assert parts[0] == "0"
    assert len(parts) == 1 + 8
    assert float(parts[1]) == pytest.approx(0.0)
    assert float(parts[2]) == pytest.approx(0.0)


def test_equal_distribution_sample_flat_dir(tmp_path: Path):
    for i in range(5):
        (tmp_path / f"a{i}.jpg").write_bytes(b"fake")
    sampled = equal_distribution_sample(tmp_path, samples_per_class=3, seed=0)
    assert len(sampled) == 3


def test_equal_distribution_sample_per_subdir(tmp_path: Path):
    t1 = tmp_path / "type_a"
    t2 = tmp_path / "type_b"
    t1.mkdir()
    t2.mkdir()
    for i in range(3):
        (t1 / f"x{i}.jpg").write_bytes(b"1")
        (t2 / f"y{i}.png").write_bytes(b"2")
    sampled = equal_distribution_sample(tmp_path, samples_per_class=2, seed=123)
    assert len(sampled) == 4
    assert sum(p.parent.name == "type_a" for p in sampled) == 2


def test_mask_to_polygon_line():
    m = np.zeros((20, 30), dtype=np.uint8)
    m[5:15, 5:25] = 255
    line = mask_to_polygon_line(0, m, image_width=30, image_height=20)
    assert line.startswith("0 ")


def test_list_images(tmp_path: Path):
    (tmp_path / "a.JPG").write_text("x")
    (tmp_path / "b.txt").write_text("y")
    imgs = list_images(tmp_path)
    assert len(imgs) == 1
