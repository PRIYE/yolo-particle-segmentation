---
description: "Task list template for feature implementation"
---

# Tasks: Instance Segmentation System for Raw Material Particles

**Input**: Design documents from `/specs/001-instance-segmentation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (`src/data`, `src/models`, `src/cli`, `src/utils`, `tests/`)
- [x] T002 Initialize Python project with `ultralytics`, `segment-anything`, `opencv-python`, `numpy`, and `pytest` dependencies
- [x] T003 [P] Configure linting and formatting tools (e.g., `flake8`, `black`, or `ruff`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement basic JSON serialization utilities in `src/utils/serialization.py` to match the data model schema
- [x] T005 [P] Implement image processing utilities (mask overlay, contour area calculation) in `src/utils/image_processing.py`
- [x] T006 Write unit tests for serialization utilities in `tests/unit/test_serialization.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate Annotations for Unlabelled Data (Priority: P1) 🎯 MVP

**Goal**: As a data scientist, I need a strategy and tooling to generate instance segmentation annotations for an unlabelled dataset organized by material type, so that I can train a supervised instance segmentation model.

**Independent Test**: Can be fully tested by running the annotation generation process on a subset of the data and visually verifying that the generated masks correctly delineate the particles.

### Implementation for User Story 1

- [x] T007 [P] [US1] Create dataset utilities for equal distribution sampling in `src/data/dataset_utils.py`
- [x] T008 [P] [US1] Write unit tests for dataset sampling in `tests/unit/test_data_utils.py`
- [x] T009 [US1] Implement SAM zero-shot annotation logic in `src/data/generate_annotations.py`
- [x] T010 [US1] Implement conversion logic from SAM output to YOLO segmentation format (`.txt` files and `data.yaml`) in `src/data/dataset_utils.py`
- [x] T011 [US1] Execute `src/data/generate_annotations.py` on the provided dataset to generate the training annotations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. The dataset is ready for training.

---

## Phase 4: User Story 2 - Train the Instance Segmentation Model (Priority: P1)

**Goal**: As a machine learning engineer, I need a training script or notebook (`train.py`) that uses the generated annotations to train an instance segmentation model, so that the model can learn to detect and delineate raw material particles.

**Independent Test**: Can be fully tested by executing `train.py` and verifying that it outputs trained model weights and training metrics (loss, mAP).

### Implementation for User Story 2

- [x] T012 [US2] Create the YOLO training script in `src/models/train.py` using Ultralytics YOLOv11-seg
- [x] T013 [US2] Configure training hyperparameters (epochs, imgsz, etc.) and dataset paths in `src/models/train.py`
- [x] T014 [US2] Execute `src/models/train.py` to train the model and generate `best.pt` weights

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. We have a trained model.

---

## Phase 5: User Story 3 - Run CLI Inference Pipeline (Priority: P1)

**Goal**: As an end-user or system integrator, I need a CLI inference pipeline (`pipeline.py`) that processes a directory of images and outputs annotated images and detection metadata, so that I can analyze the particle distribution on the conveyor belt.

**Independent Test**: Can be fully tested by running `python pipeline.py --image_dir <input> --output_dir <output>` and verifying the generated files.

### Implementation for User Story 3

- [x] T015 [P] [US3] Implement CLI argument parsing using `argparse` in `src/cli/pipeline.py` (`--image_dir`, `--output_dir`, `--weights`)
- [x] T016 [US3] Implement batch image loading and YOLO inference logic in `src/cli/pipeline.py`
- [x] T017 [US3] Integrate `image_processing.py` to generate and save annotated `.jpg` images with unique colored instance masks
- [x] T018 [US3] Integrate `serialization.py` to generate and save `detections.json` with `bbox_coordinates` and `mask_area`
- [x] T019 [US3] Write integration tests for the CLI pipeline in `tests/integration/test_pipeline.py`

**Checkpoint**: All user stories should now be independently functional. The end-to-end system is complete.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final deliverables

- [x] T020 [P] Write comprehensive `README.md` with setup, training, and inference steps
- [x] T021 Code cleanup, refactoring, and ensuring all functions have docstrings
- [x] T022 Ensure the `outputs/` folder is created and populated with sample results
- [x] T023 Verify all deliverables (`pipeline.py`, `train.py`, model weights, generated annotations, `outputs/`, `README.md`) are present

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 (Data Annotation) MUST be completed before US2 (Training) can be executed.
  - US2 (Training) MUST be completed before US3 (Inference Pipeline) can be fully tested with custom weights.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P1)**: Code can be written in parallel, but execution depends on US1 output.
- **User Story 3 (P1)**: Code can be written in parallel, but end-to-end testing depends on US2 output.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- T007 (Dataset Utils) and T015 (CLI Parsing) can be developed in parallel by different team members.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Verify annotations are generated correctly.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Annotations Ready
3. Add User Story 2 → Test independently → Model Trained
4. Add User Story 3 → Test independently → CLI Pipeline Ready
5. Complete Phase 6 (Polish) to finalize deliverables.