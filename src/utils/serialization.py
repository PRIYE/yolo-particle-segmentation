"""JSON serialization for detection metadata matching the project data model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union


def build_detection_entry(
    bbox_xyxy: Union[List[float], Tuple[float, float, float, float]],
    mask_area: float,
) -> Dict[str, Any]:
    """Build one particle detection dict with bbox and mask area."""
    x_min, y_min, x_max, y_max = (float(bbox_xyxy[0]), float(bbox_xyxy[1]), float(bbox_xyxy[2]), float(bbox_xyxy[3]))
    return {
        "bbox_coordinates": [x_min, y_min, x_max, y_max],
        "mask_area": float(mask_area),
    }


def build_detections_dict(
    detections: List[Dict[str, Any]],
    start_index: int = 1,
) -> Dict[str, Dict[str, Any]]:
    """
    Build the top-level detections mapping with sequential string keys ("1", "2", ...).

    Keys for bbox_coordinates and mask_area must match each detection entry.
    """
    out: Dict[str, Dict[str, Any]] = {}
    for i, det in enumerate(detections):
        key = str(start_index + i)
        out[key] = {
            "bbox_coordinates": list(det["bbox_coordinates"]),
            "mask_area": float(det["mask_area"]),
        }
    return out


def detections_to_json_serializable(detections: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Ensure all values are JSON-serializable (plain dicts, floats, lists)."""
    return {k: dict(v) for k, v in detections.items()}


def save_detections_json(
    detections: Dict[str, Dict[str, Any]],
    path: Union[str, Path],
    *,
    indent: int = 2,
) -> None:
    """Write detections.json with stable key ordering (numeric string order)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered_keys = sorted(detections.keys(), key=lambda x: int(x))
    ordered = {k: detections[k] for k in ordered_keys}
    with path.open("w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=indent, ensure_ascii=False)


def load_detections_json(path: Union[str, Path]) -> Dict[str, Dict[str, Any]]:
    """Load detections from JSON file."""
    with Path(path).open(encoding="utf-8") as f:
        data = json.load(f)
    return {str(k): v for k, v in data.items()}
