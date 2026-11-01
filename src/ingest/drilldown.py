from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")


def read_sdr(path: Path) -> pd.DataFrame:
    """Read one SDR CSV file, with a fallback encoding."""
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, low_memory=False, encoding="latin-1")


# Load all years
frames = []
for f in sorted(RAW_DIR.glob("sdr_*.csv")):
    df_year = read_sdr(f)
    df_year["year"] = int(f.stem.split("_")[1])
    frames.append(df_year)
df = pd.concat(frames, ignore_index=True)

# Doors only
df["JASCCode"] = df["JASCCode"].astype(str).str.strip()
doors = df[df["JASCCode"].str.startswith("52")]

# 1. Sub-code x year
pivot = pd.crosstab(doors["JASCCode"], doors["year"])
pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index].head(8)
print("Door reports by JASC code and year:")
print(pivot)

# 2. Top operators x year
top_ops = doors["OperatorDesignator"].value_counts().head(8).index
ops = pd.crosstab(
    doors.loc[doors["OperatorDesignator"].isin(top_ops), "OperatorDesignator"],
    doors["year"],
)
print("\nTop 8 operators by door reports per year:")
print(ops)

# 3. Find the aircraft columns
aircraft_cols = [c for c in df.columns if "aircraft" in c.lower() or "make" in c.lower() or "model" in c.lower()]
print("\nAircraft-related columns:")
print(aircraft_cols)