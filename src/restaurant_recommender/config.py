"""
Configuration values for the restaurant recommender project (Phase 1).

Later phases can extend this module with additional settings, but for now it
captures the dataset identifier and the small set of core columns we care about.
"""

from __future__ import annotations

from pathlib import Path

# Hugging Face dataset identifier used by `datasets.load_dataset`.
DATASET_NAME: str = "ManikaSaini/zomato-restaurant-recommendation"

# Core columns that will be used throughout the project.
CORE_COLUMNS: list[str] = [
    "name",
    "address",
    "location",
    "rate",
    "approx_cost(for two people)",
    "cuisines",
    "rest_type",
    "online_order",
    "book_table",
    "votes",
]


def get_default_cache_dir() -> Path:
    """
    Return a default directory for optional local caching of processed data.

    This does not affect Hugging Face's own cache; it is a project-level location
    that later phases can use to store Parquet/CSV snapshots.
    """

    return Path("data_cache").resolve()

