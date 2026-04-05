# Data Model

## Key Entities

### 1. Particle Detection
Represents a single detected raw material particle.

| Field | Type | Description |
|-------|------|-------------|
| `bbox_coordinates` | `Array[Float]` | Bounding Box in format `[x_min, y_min, x_max, y_max]` |
| `mask_area` | `Float` | The area of the instance mask in pixels |

### 2. Detection Metadata (detections.json)
The JSON representation of all Particle Detections in a single image.

```json
{
  "0": {
    "bbox_coordinates": [10.5, 20.1, 50.2, 60.8],
    "mask_area": 1200.5
  },
  "1": {
    "bbox_coordinates": [100.0, 200.0, 150.0, 250.0],
    "mask_area": 2500.0
  }
}
```

### 3. Annotated Image (.jpg)
The visual output showing the original image with overlaid instance masks.
- Each particle MUST have a unique colored instance mask.
- Output format: `.jpg`.

### 4. Training Data Format (YOLO Segmentation)
The generated annotations for training the Ultralytics model.
- Images: `.jpg` or `.png`
- Labels: `.txt` files with one line per object: `<class-index> <x1> <y1> <x2> <y2> ... <xn> <yn>` (normalized coordinates).
- Configuration: `data.yaml` defining `path`, `train`, `val`, `nc` (number of classes, which is 1 for "particle"), and `names`.