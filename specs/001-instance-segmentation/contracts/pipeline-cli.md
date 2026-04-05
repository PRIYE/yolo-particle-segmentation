# CLI Interface Contract: `pipeline.py`

## Usage
`python pipeline.py --image_dir <path> --output_dir <path> [--weights <path>]`

## Arguments
- `--image_dir` (Required): The absolute or relative path to the directory containing input images (`.jpg`, `.png`, etc.).
- `--output_dir` (Required): The absolute or relative path to the directory where annotated `.jpg` images and `detections.json` files will be saved.
- `--weights` (Optional): The path to the trained YOLOv11-seg model weights. Defaults to `runs/segment/weights/best.pt`.

## Expected Behavior
1. The script MUST load the specified YOLO model weights.
2. It MUST iterate through all supported image files in the `--image_dir`.
3. For each image, it MUST perform instance segmentation inference.
4. It MUST save an annotated `.jpg` with unique colored instance masks overlaid on the original image to the `--output_dir`.
5. It MUST save a `detections.json` file to the `--output_dir` with the exact schema defined in the data model.
6. The script MUST handle empty images (no detections) gracefully.