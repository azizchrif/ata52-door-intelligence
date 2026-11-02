"""Shared helpers to load FAA SDR files."""
from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")


def read_sdr(path: Path) -> pd.DataFrame:
    """Read one SDR CSV file, with a fallback encoding."""
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, low_memory=False, encoding="latin-1")


def load_all(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Load every sdr_YYYY.csv file into one DataFrame with a year column."""
    frames = []
    for f in sorted(raw_dir.glob("sdr_*.csv")):
        df_year = read_sdr(f)
        df_year["year"] = int(f.stem.split("_")[1])
        frames.append(df_year)
    df = pd.concat(frames, ignore_index=True)
    df["JASCCode"] = df["JASCCode"].astype(str).str.strip()
    return df


def door_reports(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only ATA 52 (doors) reports."""
    return df[df["JASCCode"].str.startswith("52")]