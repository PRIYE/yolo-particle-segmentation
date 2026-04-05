"""CLI inference: batch segmentation, annotated images, and detections.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Sequence, Tuple

import cv2
import numpy as np
from ultralytics import YOLO

from src.utils.image_processing import (
    distinct_colors,
    mask_area_from_binary,
    overlay_instance_masks,
)
from src.utils.serialization import build_detections_dict, save_detections_json

DEFAULT_WEIGHTS = Path("runs/segment/weights/best.pt")
IMAGE_GLOB_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def list_input_images(image_dir: Path) -> List[Path]:
    """Return sorted image paths in ``image_dir`` (recursive)."""
    files: List[Path] = []
    for p in sorted(image_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in IMAGE_GLOB_EXTENSIONS:
            files.append(p)
    return files


def _masks_from_result(result, orig_hw: Tuple[int, int]) -> Tuple[np.ndarray, List[np.ndarray]]:
    """Binary masks (H,W) uint8 0/255 and matching xyxy boxes from mask extents."""
    h, w = orig_hw
    masks_list: List[np.ndarray] = []
    boxes_list: List[List[float]] = []
    if result.masks is None:
        return np.empty((0, 4)), []

    try:
        xy_list = result.masks.xy
    except Exception:
        return np.empty((0, 4)), []

    for poly in xy_list:
        if poly is None or len(poly) < 3:
            continue
        mask = np.zeros((h, w), dtype=np.uint8)
        pts = np.array(poly, dtype=np.int32).reshape(-1, 1, 2)
        cv2.fillPoly(mask, [pts], 255)
        ys, xs = np.where(mask > 0)
        if len(xs) == 0:
            continue
        masks_list.append(mask)
        boxes_list.append(
            [float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max())]
        )

    if not masks_list:
        return np.empty((0, 4)), []

    return np.asarray(boxes_list, dtype=np.float64), masks_list


def run_inference_on_image(
    model: YOLO,
    image_path: Path,
    conf: float = 0.25,
):
    """Load one image and return (first YOLO result, BGR image)."""
    image_bgr = cv2.imread(str(image_path))
    if image_bgr is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    results = model.predict(source=image_bgr, conf=conf, verbose=False)
    return results[0], image_bgr


def build_detection_dicts_from_result(result, image_bgr: np.ndarray) -> dict:
    """Build serializable detection list entries (bbox + mask_area)."""
    oh, ow = image_bgr.shape[:2]
    boxes, masks = _masks_from_result(result, (oh, ow))
    entries: List[dict] = []
    for i in range(len(masks)):
        bbox = boxes[i]
        x_min, y_min, x_max, y_max = float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
        area = mask_area_from_binary(masks[i])
        entries.append(
            {
                "bbox_coordinates": [x_min, y_min, x_max, y_max],
                "mask_area": area,
            }
        )
    return build_detections_dict(entries, start_index=1)


def annotate_image(image_bgr: np.ndarray, result, alpha: float = 0.5) -> np.ndarray:
    """Draw colored instance overlays and contours on ``image_bgr``."""
    oh, ow = image_bgr.shape[:2]
    _, masks = _masks_from_result(result, (oh, ow))
    if not masks:
        return image_bgr
    colored = overlay_instance_masks(image_bgr, masks, alpha=alpha)
    # Strong contour lines using same palette
    colors = distinct_colors(len(masks))
    out = colored
    for i, m in enumerate(masks):
        contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(out, contours, -1, colors[i], 2)
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Instance segmentation inference pipeline.")
    p.add_argument("--image_dir", type=Path, required=True)
    p.add_argument("--output_dir", type=Path, required=True)
    p.add_argument("--weights", type=Path, default=None, help="YOLO-seg weights (.pt)")
    p.add_argument("--conf", type=float, default=0.25)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    weights = args.weights if args.weights is not None else DEFAULT_WEIGHTS
    if not Path(weights).is_file():
        print(
            f"Weights not found at {weights}. Using pretrained yolo11n-seg.pt for a working demo.",
            file=sys.stderr,
        )
        weights = Path("yolo11n-seg.pt")

    model = YOLO(str(weights))

    image_dir = args.image_dir
    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    images = list_input_images(image_dir)
    if not images:
        print(f"No images found in {image_dir}", file=sys.stderr)
        return 1

    for img_path in images:
        result, bgr = run_inference_on_image(model, img_path, conf=args.conf)
        det = build_detection_dicts_from_result(result, bgr)
        stem = img_path.stem
        annotated = annotate_image(bgr, result)
        out_img = out_dir / f"{stem}.jpg"
        cv2.imwrite(str(out_img), annotated)
        out_json = out_dir / f"{stem}.json"
        save_detections_json(det, out_json)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
