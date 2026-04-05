#!/usr/bin/env python3
"""Root entry: YOLO segmentation training."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.models.train import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
