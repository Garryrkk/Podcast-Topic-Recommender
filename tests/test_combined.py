# tests/test_combined.py

import os
import sys
import pandas as pd
import pytest

# --- Make this file runnable directly OR via pytest ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from combined.combined import load_csv_safe  # uses (path, name)


# ---------- Helpers used only in tests ----------
def merge_no_dupes(*dfs):
    """
    Concatenate non-None, non-empty DataFrames and drop duplicate rows by 'text'.
    Returns an empty DataFrame with the expected columns if everything is missing.
    """
    frames = [df for df in dfs if df is not None and not df.empty]
    if not frames:
        return pd.DataFrame(columns=["topic", "text"])

    merged = pd.concat(frames, ignore_index=True)
    # Ensure expected columns exist for safety in case input differs
    for col in ["topic", "text"]:
        if col not in merged.columns:
            merged[col] = ""
    merged = merged.drop_duplicates(subset=["text"])
    return merged


# ---------- Fixtures ----------
@pytest.fixture
def sample_reddit_csv(tmp_path):
    file_path = tmp_path / "reddit_posts.csv"
    data = """topic,text
Mental Health,"Example Reddit post about mental health"
Work & Study Life,"Balancing work and studies"
"""
    file_path.write_text(data, encoding="utf-8")
    return str(file_path)


@pytest.fixture
def sample_youtube_csv(tmp_path):
    # Intentionally include a duplicate 'text' that appears in sample_reddit_csv
    # to verify de-duplication works across sources.
    file_path = tmp_path / "youtube_trends.csv"
    data = """topic,text
Self Care,"Top 10 self care tips"
Mental Health,"Dealing with anxiety"
Work & Study Life,"Balancing work and studies"
"""
    file_path.write_text(data, encoding="utf-8")
    return str(file_path)


# ---------- Tests ----------
def test_read_csv_correctly(sample_reddit_csv):
    df = load_csv_safe(sample_reddit_csv, "Reddit")
    assert df is not None
    assert not df.empty
    assert "topic" in df.columns
    assert "text" in df.columns


def test_read_csv_missing_file(tmp_path):
    missing_path = tmp_path / "missing.csv"
    df = load_csv_safe(str(missing_path), "Missing")
    # combined.load_csv_safe returns None on failure
    assert df is None


def test_merge_without_duplicates(sample_reddit_csv, sample_youtube_csv):
    df_reddit = load_csv_safe(sample_reddit_csv, "Reddit")
    df_youtube = load_csv_safe(sample_youtube_csv, "YouTube")

    merged = merge_no_dupes(df_reddit, df_youtube)

    # Ensure de-duplication by text worked
    assert merged["text"].nunique() == len(merged)

    # Ensure topics from both sources exist
    assert any(merged["topic"].str.contains("Self Care", case=False, na=False))
    assert any(merged["topic"].str.contains("Work & Study Life", case=False, na=False))


def test_return_topics_if_one_source_missing(sample_reddit_csv, tmp_path):
    df_reddit = load_csv_safe(sample_reddit_csv, "Reddit")
    # Simulate missing YouTube by pointing to a non-existent file
    missing_path = tmp_path / "does_not_exist.csv"
    df_youtube = load_csv_safe(str(missing_path), "YouTube")
    assert df_youtube is None  # sanity check

    merged = merge_no_dupes(df_reddit, df_youtube)

    assert not merged.empty, "Should still return Reddit topics when YouTube is missing"
    assert "topic" in merged.columns and "text" in merged.columns
    assert any(merged["topic"].str.contains("Work & Study Life", case=False, na=False))
