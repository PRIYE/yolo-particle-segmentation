# Implementation Plan: Instance Segmentation System for Raw Material Particles

**Branch**: `001-instance-segmentation` | **Date**: 2026-04-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-instance-segmentation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Build an instance segmentation system to detect and delineate raw material particles on conveyor belts. The technical approach involves using a zero-shot automated strategy (Segment Anything Model / SAM) with equal distribution sampling to generate annotations from the unlabelled dataset. These annotations will be used to train an Ultralytics YOLOv11-seg model. A CLI inference pipeline (`pipeline.py`) will be created to process images and output annotated `.jpg`s and `detections.json` files.

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: Ultralytics (YOLOv11-seg), Segment Anything Model (SAM), OpenCV (`cv2`), NumPy, `argparse`, `json`
**Storage**: Local file system (images, JSON, YOLO format labels)
**Testing**: `pytest`
**Target Platform**: Linux/macOS CLI
**Project Type**: CLI Pipeline / Machine Learning Project
**Performance Goals**: > 0.5 mAP on validation set, responsive inference time (< 2s per image)
**Constraints**: Must handle varying lighting conditions, occlusions, and overlapping particles
**Scale/Scope**: Process directories of unlabelled images, train a model, and run inference

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Code Quality**: All code MUST be self-documenting, minimize cyclomatic complexity, and pass automated linting/formatting checks.
- **Testing Standards**: All new features MUST include automated tests. Code coverage MUST NOT decrease. Tests MUST be deterministic.
- **User Experience Consistency**: N/A (CLI tool, but output formats must strictly adhere to the spec).
- **Performance Requirements**: The application MUST maintain responsive load times and efficient resource utilization. Heavy computations MUST be deferred or optimized (e.g., using YOLO for fast inference).

## Project Structure

### Documentation (this feature)

```text
specs/001-instance-segmentation/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── data/
│   ├── generate_annotations.py  # SAM zero-shot annotation script
│   └── dataset_utils.py         # Utilities for sampling and YOLO format conversion
├── models/
│   └── train.py                 # YOLO training script
├── cli/
│   └── pipeline.py              # CLI inference pipeline
└── utils/
    ├── image_processing.py      # OpenCV mask overlay logic
    └── serialization.py         # JSON formatting logic

tests/
├── integration/
│   └── test_pipeline.py
└── unit/
    ├── test_data_utils.py
    └── test_serialization.py
```

**Structure Decision**: The project is structured as a single Python package (`src/`) with clear separation of concerns (data preparation, model training, CLI interface, and utilities). Tests are separated into unit and integration suites.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |