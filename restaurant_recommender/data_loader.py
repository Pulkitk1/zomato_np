"""
Data loading utilities for the Zomato restaurant recommendation dataset (Phase 1).

Responsibilities in this phase:
- Load the dataset from Hugging Face using `datasets`.
- Expose helpers focused on the core columns we care about.
- Provide an optional, lightweight caching interface for processed tabular data.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

# Vercel Fix: Ensure Hugging Face uses the writable /tmp directory
if os.environ.get("VERCEL"):
    os.environ["HF_DATASETS_CACHE"] = "/tmp/huggingface_datasets"
    os.environ["HUGGINGFACE_HUB_CACHE"] = "/tmp/huggingface_hub"

from datasets import Dataset, load_dataset
import pandas as pd

from .config import CORE_COLUMNS, DATASET_NAME, get_default_cache_dir


def load_raw_dataset(split: str = "train", streaming: bool = False) -> Dataset:
    """
    Load the raw Hugging Face dataset split with optional streaming.
    """

    return load_dataset(DATASET_NAME, split=split, streaming=streaming)


def load_core_dataframe(split: str = "train", *, sample_size: Optional[int] = None) -> pd.DataFrame:
    """
    Load the dataset as a pandas DataFrame containing only the core columns.

    Uses streaming if sample_size is specified to avoid full downloads on serverless.
    """

    # Vercel fix: Use streaming for small samples to avoid 500MB+ download
    streaming = sample_size is not None and sample_size <= 10000
    ds = load_raw_dataset(split=split, streaming=streaming)

    if sample_size is not None:
        if streaming:
            # For streaming datasets, we take only N rows
            ds = ds.take(sample_size)
        else:
            sample_size = min(sample_size, len(ds))
            ds = ds.select(range(sample_size))

    df = pd.DataFrame(list(ds)) if streaming else ds.to_pandas()
    
    # Only keep the core columns that actually exist.
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

