"""
Data loading utilities for the Zomato restaurant recommendation dataset (Phase 1).

Responsibilities in this phase:
- Load the dataset from Hugging Face using `datasets`.
- Expose helpers focused on the core columns we care about.
- Provide an optional, lightweight caching interface for processed tabular data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from datasets import Dataset, load_dataset
import pandas as pd

from .config import CORE_COLUMNS, DATASET_NAME, get_default_cache_dir


def load_raw_dataset(split: str = "train") -> Dataset:
    """
    Load the raw Hugging Face dataset split.

    This uses the standard Hugging Face `datasets` caching mechanism under the hood,
    so repeated calls will not re-download the data.
    """

    return load_dataset(DATASET_NAME, split=split)


def load_core_dataframe(split: str = "train", *, sample_size: Optional[int] = None) -> pd.DataFrame:
    """
    Load the dataset as a pandas DataFrame containing only the core columns.

    Args:
        split: Dataset split to load (default: "train").
        sample_size: If provided, limit the DataFrame to the first N rows
            for quicker local experimentation and tests.
    """

    ds = load_raw_dataset(split=split)

    if sample_size is not None:
        sample_size = min(sample_size, len(ds))
        ds = ds.select(range(sample_size))

    df = ds.to_pandas()
    # Only keep the core columns that actually exist in the dataset,
    # which makes the function more robust if the upstream schema evolves.
    available_core_cols = [c for c in CORE_COLUMNS if c in df.columns]
    return df[available_core_cols]


def cache_core_dataframe(
    *,
    split: str = "train",
    sample_size: Optional[int] = None,
    cache_dir: Optional[Path] = None,
    filename: str = "core_zomato.parquet",
) -> Path:
    """
    Materialize the core columns of the dataset into a Parquet file.

    This is an optional convenience around Hugging Face's own cache and is
    primarily intended for:
    - Faster startup in later phases.
    - Easier offline exploration in notebooks or BI tools.

    Returns:
        The path to the Parquet file on disk.
    """

    if cache_dir is None:
        cache_dir = get_default_cache_dir()

    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / filename

    df = load_core_dataframe(split=split, sample_size=sample_size)
    df.to_parquet(path, index=False)
    return path


__all__ = [
    "load_raw_dataset",
    "load_core_dataframe",
    "cache_core_dataframe",
    "DATASET_NAME",
    "CORE_COLUMNS",
]

