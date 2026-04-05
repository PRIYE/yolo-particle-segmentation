# Instance Segmentation — Raw Material Particles

Pipeline for generating pseudo-labels (optional SAM), training Ultralytics YOLO segmentation, and running batch inference with `detections.json` and colored instance overlays.

## Environment

Use Conda (Python 3.9+ recommended; tested on 3.12):

```bash
conda create -n myvenv python=3.9 -y
conda activate myvenv
pip install -r requirements.txt
pip install git+https://github.com/facebookresearch/segment-anything.git
```

Core packages: `ultralytics`, `opencv-python`, `numpy`, `pytest`, `ruff`. SAM is optional if you use `--mock` annotation mode.

## Layout

- `src/data/generate_annotations.py` — sample images per class, mock or SAM masks → YOLO labels + `data.yaml`
- `src/models/train.py` — YOLO11-seg training (`train.py` at repo root)
- `src/cli/pipeline.py` — inference (`pipeline.py` at repo root)
- `src/utils/` — JSON schema helpers and OpenCV mask overlay

## Annotation (User Story 1)

Equal sampling per material subfolder, then labels under `--output`:

```bash
python -m src.data.generate_annotations \
  --data_root data/sample_raw \
  --output data/yolo_dataset \
  --samples_per_class 5 \
  --mock
```

For Meta SAM automatic masks, download a checkpoint (e.g. `sam_vit_b_01ec64.pth`) and omit `--mock`:

```bash
python -m src.data.generate_annotations \
  --data_root data/sample_raw \
  --output data/yolo_dataset \
  --samples_per_class 5 \
  --sam_checkpoint /path/to/sam_vit_b_01ec64.pth
```

## Training (User Story 2)

```bash
python train.py --data data/yolo_dataset/data.yaml --epochs 50 --imgsz 640 --batch 8 --device mps
```

Weights are written to `runs/segment/weights/best.pt` by default (`--project runs`, `--name segment`).

## Inference (User Story 3)

Only `--image_dir` and `--output_dir` are required; `--weights` defaults to `runs/segment/weights/best.pt` (falls back to downloaded `yolo11n-seg.pt` if missing):

```bash
python pipeline.py --image_dir path/to/images --output_dir path/to/out --weights runs/segment/weights/best.pt
```

Per input image `name.ext`, the pipeline writes:

- `name.jpg` — original image with distinct HSV-based instance colors and contours
- `name.json` — keys `"1"`, `"2"`, … with `bbox_coordinates` `[x_min, y_min, x_max, y_max]` and `mask_area` (pixels)

## Tests

```bash
pytest tests/unit tests/integration -q
```

## Lint

```bash
ruff check src tests pipeline.py train.py
```

## Process Completed So Far & Deliverables Checklist

The following processes have been completed to fulfill the assignment requirements:

1. **Environment Setup & Optimization**: 
   - Set up a native Apple Silicon (ARM64) Python environment using Miniforge to ensure PyTorch can utilize the Mac's GPU (MPS).
   - Resolved `float64` compatibility issues with the MPS backend to ensure stable execution.

2. **Data Annotation Strategy (Unlabelled Data)**:
   - Implemented a zero-shot annotation generation pipeline using Meta's **Segment Anything Model (SAM)**.
   - Used **equal distribution stratified sampling** across all material type folders to prevent class imbalance.
   - Converted the generated masks into YOLO segmentation format (`.txt` labels and `data.yaml`).
   - *Deliverable Status*: ✅ Generated annotations are present in the `data/yolo_dataset_sam` directory.

3. **Model Training**:
   - Built a modular training script (`train.py`) using the **Ultralytics YOLOv11-seg** framework.
   - Trained the model on the generated dataset, optimizing hyperparameters (`imgsz`, `batch`, `workers`) to maximize GPU utilization on an 8GB M1 Mac without hitting Out-Of-Memory (OOM) errors.
   - *Deliverable Status*: ✅ `train.py` is present. Trained model weights (`best.pt`) are saved in the `runs/segment/` directory.

4. **Inference Pipeline**:
   - Built a robust CLI script (`pipeline.py`) using `argparse` that accepts `--image_dir` and `--output_dir`.
   - Implemented custom OpenCV image processing to overlay **unique, highly distinct colored instance masks** and contours on every detected particle.
   - Implemented custom JSON serialization to output `detections.json` with strict schema adherence (sequential string keys, `bbox_coordinates` in `[x_min, y_min, x_max, y_max]` format, and `mask_area` in pixels).
   - *Deliverable Status*: ✅ `pipeline.py` is present. The `outputs/` folder contains the generated `.jpg` and `.json` files.

5. **Documentation**:
   - *Deliverable Status*: ✅ This comprehensive `README.md` serves as the guide for environment setup, annotation, training, and inference.
