# Quickstart

## Prerequisites
- Python 3.9+
- `pip` or `conda`

## Setup
1. Clone the repository and navigate to the project root.
2. Install dependencies:
   ```bash
   pip install ultralytics opencv-python numpy
   # If generating annotations with SAM:
   pip install segment-anything
   ```

## Training the Model
1. Ensure your dataset is organized and annotated (using the SAM zero-shot pipeline).
2. Run the training script:
   ```bash
   python train.py --data_yaml path/to/data.yaml --epochs 50 --imgsz 640
   ```
3. The trained weights will be saved in `runs/segment/train/weights/best.pt`.

## Running Inference
1. Use the trained weights to run inference on a directory of images:
   ```bash
   python pipeline.py --image_dir path/to/input_images --output_dir path/to/outputs
   ```
2. The `outputs/` folder will contain the annotated `.jpg` images and `detections.json` files.