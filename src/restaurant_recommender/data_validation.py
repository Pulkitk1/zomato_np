"""
Basic data validation and exploration helpers for Phase 1.

These utilities are intentionally lightweight and are used by tests to confirm:
- The dataset schema contains the expected core columns.
- There is at least some data available after loading.
"""

from __future__ import annotations

from typing import Iterable, Mapping

import pandas as pd

from .config import CORE_COLUMNS


def validate_core_columns(df: pd.DataFrame) -> None:
    """
    Ensure that all required core columns are present in the DataFrame.

    Raises:
        ValueError: if any core columns are missing.
    """

    missing = [col for col in CORE_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing expected core columns: {missing}")


def basic_summary(df: pd.DataFrame) -> Mapping[str, object]:
    """
    Return a small summary of the dataset, useful for logging or debugging.

    The goal is not exhaustive EDA, just enough to confirm the data looks sane.
    """

    summary: dict[str, object] = {
        "num_rows": int(len(df)),
        "num_columns": int(df.shape[1]),
        "columns": list(df.columns),
    }

    numeric_like_cols: Iterable[str] = [
        "votes",
    ]

    for col in numeric_like_cols:
        if col in df.columns:
            series = df[col].dropna()
            if not series.empty:
                summary[f"{col}_min"] = float(series.min())
                summary[f"{col}_max"] = float(series.max())

    return summary


__all__ = [
    "validate_core_columns",
    "basic_summary",
]

