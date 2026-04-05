#!/usr/bin/env python3
"""Root entry: inference pipeline (delegates to src.cli.pipeline)."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.cli.pipeline import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
