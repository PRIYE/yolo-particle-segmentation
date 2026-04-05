# Research & Technical Decisions

## 1. Segmentation Model Selection
- **Decision**: Ultralytics YOLOv11-seg (or YOLOv8-seg)
- **Rationale**: The specification explicitly mandates the Ultralytics framework. YOLO models are highly optimized for real-time inference and provide excellent out-of-the-box CLI and Python APIs. They are well-suited for industrial applications like particle detection on conveyor belts where both accuracy and speed are critical.
- **Alternatives considered**: Mask R-CNN (PyTorch/TorchVision) and Detectron2 were rejected during the clarification phase in favor of the simpler and faster Ultralytics ecosystem.

## 2. Data Preparation and Annotation Pipeline
- **Decision**: Zero-shot automated annotation using Segment Anything Model (SAM) with equal distribution sampling.
- **Rationale**: The dataset is unlabelled and organized by material type. SAM provides robust zero-shot mask generation. To prevent bias, we will sample an equal number of images from each material type folder (e.g., `type1`, `type2`, `type3`, `type4`, `type5`). The pipeline will:
  1. Iterate through each material type folder.
  2. Sample `N` images per folder.
  3. Run SAM to generate masks and bounding boxes.
  4. Convert SAM outputs to YOLO segmentation format (`<class-index> <x1> <y1> <x2> <y2> ... <xn> <yn>`).
- **Alternatives considered**: Manual pseudo-labelling was rejected due to the time constraint and scale.

## 3. CLI Pipeline Architecture (`pipeline.py`)
- **Decision**: Python script using `argparse` with Ultralytics YOLO Python API.
- **Rationale**: `argparse` is the standard library for robust CLI interfaces. The pipeline will accept `--image_dir` and `--output_dir`. It will load the trained YOLO model, iterate over images in `--image_dir`, perform inference, and save the results.
- **Alternatives considered**: `click` or `typer`. `argparse` is chosen to minimize external dependencies for basic CLI functionality.

## 4. Image Processing and Mask Overlay Libraries
- **Decision**: OpenCV (`cv2`) and NumPy.
- **Rationale**: OpenCV is the industry standard for fast image I/O and drawing operations. YOLO's native plotting (`results[0].plot()`) uses OpenCV under the hood and can be leveraged to generate the annotated `.jpg` with unique colored instance masks.
- **Alternatives considered**: Matplotlib (slower, better for interactive plotting rather than batch processing) and PIL/Pillow.

## 5. JSON Serialization Logic
- **Decision**: Standard Python `json` library with custom extraction from YOLO `Results` object.
- **Rationale**: The spec requires a `detections.json` with sequential keys (e.g., `"0"`, `"1"`, `"2"`) containing `bbox_coordinates` (`[x_min, y_min, x_max, y_max]`) and `mask_area` (in pixels). YOLO returns bounding boxes in `xyxy` format and masks as polygons or binary masks. We will calculate the mask area using `cv2.contourArea()` on the polygon or by summing the binary mask pixels.
- **Alternatives considered**: Saving raw YOLO output (rejected because it doesn't match the required schema).