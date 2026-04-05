"""Train Ultralytics YOLO segmentation on generated dataset."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from ultralytics import YOLO


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Train YOLO segmentation (YOLOv8/YOLO11-seg via Ultralytics).")
    p.add_argument(
        "--data",
        type=Path,
        default=Path("data/yolo_dataset/data.yaml"),
        help="Path to data.yaml",
    )
    p.add_argument(
        "--model",
        type=str,
        default="yolo11n-seg.pt",
        help="Base weights (e.g. yolo11n-seg.pt, yolov8n-seg.pt).",
    )
    p.add_argument("--epochs", type=int, default=50)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--device", type=str, default="", help="cuda device or cpu")
    p.add_argument("--workers", type=int, default=8, help="number of dataloader workers")
    # Default yields runs/segment/weights/best.pt (matches pipeline default --weights)
    p.add_argument("--project", type=str, default="runs")
    p.add_argument("--name", type=str, default="segment")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    data_yaml = args.data
    if not data_yaml.is_file():
        raise FileNotFoundError(f"Dataset yaml not found: {data_yaml}")

    model = YOLO(args.model)
    train_kw = dict(
        data=str(data_yaml),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        project=args.project,
        name=args.name,
        workers=args.workers,
    )
    if args.device:
        train_kw["device"] = args.device

    model.train(**train_kw)
    best = Path(args.project) / args.name / "weights" / "best.pt"
    print(f"Training finished. Weights: {best.resolve() if best.is_file() else 'see runs/'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
