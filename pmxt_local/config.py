from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LocalProcessingConfig:
    filtered_root: Path
    tmp_root: Path
    filtered_materialization_workers: int
