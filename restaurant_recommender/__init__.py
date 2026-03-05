"""
Restaurant recommender data package for Phase 1.

This package currently focuses on:
- Loading the Zomato dataset from Hugging Face.
- Providing a clean interface for core columns used by later phases.
"""

from .data_loader import (
    DATASET_NAME,
    CORE_COLUMNS,
    load_raw_dataset,
    load_core_dataframe,
)

__all__ = [
    "DATASET_NAME",
    "CORE_COLUMNS",
    "load_raw_dataset",
    "load_core_dataframe",
]

