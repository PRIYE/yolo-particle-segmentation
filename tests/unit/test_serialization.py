"""Unit tests for serialization utilities."""

import json
from pathlib import Path

import pytest

from src.utils.serialization import (
    build_detection_entry,
    build_detections_dict,
    load_detections_json,
    save_detections_json,
)


def test_build_detection_entry():
    e = build_detection_entry([10.0, 20.0, 50.0, 60.0], 123.4)
    assert e["bbox_coordinates"] == [10.0, 20.0, 50.0, 60.0]
    assert e["mask_area"] == pytest.approx(123.4)


def test_build_detections_dict_sequential_keys():
    dets = [
        build_detection_entry([0, 0, 1, 1], 10),
        build_detection_entry([2, 2, 3, 3], 20),
    ]
    out = build_detections_dict(dets, start_index=1)
    assert list(out.keys()) == ["1", "2"]
    assert out["1"]["bbox_coordinates"] == [0.0, 0.0, 1.0, 1.0]
    assert out["1"]["mask_area"] == 10.0
    assert out["2"]["mask_area"] == 20.0


def test_save_and_load_roundtrip(tmp_path: Path):
    data = {
        "1": {"bbox_coordinates": [1.0, 2.0, 3.0, 4.0], "mask_area": 100.0},
        "2": {"bbox_coordinates": [0.0, 0.0, 10.0, 10.0], "mask_area": 50.5},
    }
    p = tmp_path / "detections.json"
    save_detections_json(data, p)
    loaded = load_detections_json(p)
    assert loaded == data
    raw = json.loads(p.read_text(encoding="utf-8"))
    assert list(raw.keys()) == ["1", "2"]


def test_keys_match_bbox_and_mask_area():
    """Each key must map to both bbox_coordinates and mask_area."""
    out = build_detections_dict(
        [
            {"bbox_coordinates": [0, 0, 1, 1], "mask_area": 5.0},
        ],
        start_index=1,
    )
    assert set(out["1"].keys()) == {"bbox_coordinates", "mask_area"}
