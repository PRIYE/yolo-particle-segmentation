"""Integration tests for pipeline CLI."""

import json
from pathlib import Path

import cv2
import numpy as np

from src.cli import pipeline as pipeline_mod


def _make_sample_image(path: Path) -> None:
    img = np.zeros((256, 320, 3), dtype=np.uint8)
    cv2.circle(img, (160, 128), 60, (200, 180, 160), -1)
    cv2.circle(img, (80, 80), 25, (120, 140, 100), -1)
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), img)


def test_pipeline_runs_and_writes_json_schema(tmp_path: Path, monkeypatch):
    inp = tmp_path / "in"
    out = tmp_path / "out"
    _make_sample_image(inp / "sample.jpg")

    # Avoid depending on trained weights: use small pretrained seg model name.
    weights = "yolo11n-seg.pt"

    argv = [
        "--image_dir",
        str(inp),
        "--output_dir",
        str(out),
        "--weights",
        weights,
        "--conf",
        "0.01",
    ]
    monkeypatch.chdir(tmp_path)
    code = pipeline_mod.main(argv)
    assert code == 0

    jpath = out / "sample_detections.json"
    assert jpath.is_file()
    data = json.loads(jpath.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    for k, v in data.items():
        assert k.isdigit()
        assert int(k) >= 1
        assert "bbox_coordinates" in v and "mask_area" in v
        assert len(v["bbox_coordinates"]) == 4
        assert v["bbox_coordinates"][0] <= v["bbox_coordinates"][2]
        assert v["bbox_coordinates"][1] <= v["bbox_coordinates"][3]

    ann = out / "sample_annotated.jpg"
    assert ann.is_file()


def test_empty_image_dir(tmp_path: Path, monkeypatch):
    empty = tmp_path / "empty_in"
    empty.mkdir()
    out = tmp_path / "out"
    monkeypatch.chdir(tmp_path)
    code = pipeline_mod.main(
        ["--image_dir", str(empty), "--output_dir", str(out), "--weights", "yolo11n-seg.pt"]
    )
    assert code == 1
