import os
from pathlib import Path

import pandas as pd

from restaurant_recommender.data_loader import (
    DATASET_NAME,
    CORE_COLUMNS,
    cache_core_dataframe,
    load_core_dataframe,
    load_raw_dataset,
)
from restaurant_recommender.data_validation import basic_summary, validate_core_columns


def test_can_load_raw_dataset_small_sample():
    """
    Smoke test: the Hugging Face dataset can be loaded and has rows.
    """

    ds = load_raw_dataset(split="train")
    assert len(ds) > 0
    # Ensure some of the expected columns are present.
    for col in CORE_COLUMNS[:3]:
        assert col in ds.column_names


def test_core_dataframe_has_required_columns_and_rows():
    """
    Ensure the core DataFrame has the expected columns and at least one row.
    """

    df: pd.DataFrame = load_core_dataframe(split="train", sample_size=200)
    assert not df.empty
    validate_core_columns(df)


def test_can_cache_core_dataframe_to_parquet(tmp_path: Path):
    """
    Verify that we can materialize a Parquet snapshot and read it back.
    """

    cache_path = cache_core_dataframe(sample_size=100, cache_dir=tmp_path)
    assert cache_path.exists()
    loaded = pd.read_parquet(cache_path)
    assert not loaded.empty
    validate_core_columns(loaded)


def test_basic_summary_contains_expected_keys():
    """
    The basic summary helper should return a minimal but useful description.
    """

    df = load_core_dataframe(sample_size=50)
    summary = basic_summary(df)
    assert summary["num_rows"] > 0
    assert "num_columns" in summary
    assert isinstance(summary.get("columns"), list)

