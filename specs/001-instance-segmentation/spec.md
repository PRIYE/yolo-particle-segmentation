# Feature Specification: Instance Segmentation System for Raw Material Particles

**Feature Branch**: `001-instance-segmentation`  
**Created**: 2026-04-05  
**Status**: Draft  
**Input**: User description: "Build an instance segmentation system to detect and delineate raw material particles on conveyor belts. Key requirements: 1. The dataset is unlabelled but organized into folders by material type (e.g., type1, type2). We need a strategy to generate annotations that covers all material types. 2. Create a CLI inference pipeline (pipeline.py) that accepts --image_dir and --output_dir. 3. For each image, output an annotated .jpg with unique coloured instance masks overlaid on particles. 4. For each image, output a detections.json with sequential keys containing bbox_coordinates ([x_min, y_min, x_max, y_max]) and mask_area. 5. Deliverables must include pipeline.py, a training script/notebook (train.py), model weights, generated annotations, the outputs/ folder, and a comprehensive README.md."

## Clarifications

### Session 2026-04-05
- Q: How should we generate annotations for the unlabelled dataset across the different material types? → A: Zero-shot automated only (e.g., using Segment Anything Model / SAM)
- Q: How should we approach stratified sampling across the different "type" folders to ensure the model generalizes well? → A: Equal distribution (Sample an equal number of images from each material type folder)
- Q: Which deep learning framework should be used for building and training the instance segmentation model? → A: Ultralytics (e.g., YOLOv8-seg or YOLOv11-seg)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Annotations for Unlabelled Data (Priority: P1)

As a data scientist, I need a strategy and tooling to generate instance segmentation annotations for an unlabelled dataset organized by material type, so that I can train a supervised instance segmentation model.

**Why this priority**: Without annotations, the model cannot be trained. This is the foundational step for the entire system.

**Independent Test**: Can be fully tested by running the annotation generation process on a subset of the data and visually verifying that the generated masks correctly delineate the particles.

**Acceptance Scenarios**:

1. **Given** an unlabelled dataset organized into folders by material type, **When** the annotation strategy is applied, **Then** it produces valid instance segmentation annotations (masks and bounding boxes) covering all material types.

---

### User Story 2 - Train the Instance Segmentation Model (Priority: P1)

As a machine learning engineer, I need a training script or notebook (`train.py`) that uses the generated annotations to train an instance segmentation model, so that the model can learn to detect and delineate raw material particles.

**Why this priority**: Training the model is the core technical deliverable that enables the inference pipeline.

**Independent Test**: Can be fully tested by executing `train.py` and verifying that it outputs trained model weights and training metrics (loss, mAP).

**Acceptance Scenarios**:

1. **Given** the generated annotations and raw images, **When** `train.py` is executed, **Then** it trains the model and saves the resulting model weights to disk.

---

### User Story 3 - Run CLI Inference Pipeline (Priority: P1)

As an end-user or system integrator, I need a CLI inference pipeline (`pipeline.py`) that processes a directory of images and outputs annotated images and detection metadata, so that I can analyze the particle distribution on the conveyor belt.

**Why this priority**: This is the primary interface for using the trained model in a production-like setting.

**Independent Test**: Can be fully tested by running `python pipeline.py --image_dir <input> --output_dir <output>` and verifying the generated files.

**Acceptance Scenarios**:

1. **Given** a trained model and a directory of input images, **When** `pipeline.py` is run with `--image_dir` and `--output_dir` arguments, **Then** it processes all images in the input directory.
2. **Given** an input image, **When** processed by the pipeline, **Then** it outputs an annotated `.jpg` with unique colored instance masks overlaid on the particles.
3. **Given** an input image, **When** processed by the pipeline, **Then** it outputs a `detections.json` file containing sequential keys with `bbox_coordinates` ([x_min, y_min, x_max, y_max]) and `mask_area` for each detected particle.

### Edge Cases

- What happens when an image contains no particles? (Should output an image with no overlays and an empty JSON).
- What happens when particles are heavily occluded or overlapping?
- How does the system handle unsupported image formats in the `--image_dir`?
- How does the annotation strategy handle varying lighting conditions across different material types?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST include a defined strategy/script to generate annotations from the unlabelled dataset covering all material types, utilizing a zero-shot automated approach exclusively (e.g., Segment Anything Model / SAM). The sampling strategy MUST ensure an equal distribution of images across all available material types.
- **FR-002**: System MUST provide a training script or notebook (`train.py`) that produces trained model weights, utilizing the Ultralytics framework (e.g., YOLOv8-seg or YOLOv11-seg).
- **FR-003**: System MUST provide a CLI inference pipeline (`pipeline.py`) accepting `--image_dir` and `--output_dir` arguments.
- **FR-004**: System MUST output an annotated `.jpg` for each processed image, featuring unique colored instance masks overlaid on detected particles.
- **FR-005**: System MUST output a `detections.json` for each processed image.
- **FR-006**: The `detections.json` MUST contain sequential keys for each detection.
- **FR-007**: Each entry in `detections.json` MUST include `bbox_coordinates` in the format `[x_min, y_min, x_max, y_max]`.
- **FR-008**: Each entry in `detections.json` MUST include the `mask_area` (number of pixels or physical area if calibrated [NEEDS CLARIFICATION: assume pixel area for now]).
- **FR-009**: Deliverables MUST include a comprehensive `README.md` explaining the annotation strategy, training process, and how to run the pipeline.
- **FR-010**: Deliverables MUST include the generated annotations, model weights, and an `outputs/` folder containing sample results.

### Key Entities

- **Particle Detection**: Represents a single detected raw material particle. Attributes: Bounding Box (`[x_min, y_min, x_max, y_max]`), Mask Area, Instance Mask.
- **Annotated Image**: The visual output showing the original image with overlaid instance masks.
- **Detection Metadata**: The JSON representation of all Particle Detections in a single image.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The annotation strategy successfully generates usable training data for all provided material types.
- **SC-002**: The trained model achieves a reasonable baseline performance (e.g., > 0.5 mAP) on a validation set of the generated annotations.
- **SC-003**: The `pipeline.py` script successfully processes 100% of valid input images without crashing.
- **SC-004**: The output `detections.json` files strictly adhere to the required schema (`bbox_coordinates` and `mask_area`).
- **SC-005**: All required deliverables (`pipeline.py`, `train.py`, weights, annotations, `outputs/`, `README.md`) are present and functional.