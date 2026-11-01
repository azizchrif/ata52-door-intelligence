from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")


def read_sdr(path: Path) -> pd.DataFrame:
    """Read one SDR CSV file, with a fallback encoding."""
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, low_memory=False, encoding="latin-1")


# 1. Nlawjou 3la kol el fichiers sdr_*.csv
files = sorted(RAW_DIR.glob("sdr_*.csv"))
print(f"Found {len(files)} files:")
for f in files:
    print(f"  - {f.name}")

# 2. Na9raw kol fichier w nzidou colonne year
frames = []
for f in files:
    year = int(f.stem.split("_")[1])   # "sdr_2025" -> 2025
    df_year = read_sdr(f)
    df_year["year"] = year
    frames.append(df_year)

# 3. Nlsa9hom kol fi DataFrame wa7ed
df = pd.concat(frames, ignore_index=True)
print(f"\nTotal rows: {len(df):,}")

# 4. Nfiltriw el portes (ATA 52)
df["JASCCode"] = df["JASCCode"].astype(str).str.strip()
doors = df[df["JASCCode"].str.startswith("52")]

# 5. 9addech men rapport kol 3am
summary = pd.DataFrame({
    "all_reports": df.groupby("year").size(),
    "door_reports": doors.groupby("year").size(),
})
summary["door_share"] = (summary["door_reports"] / summary["all_reports"]).round(3)

print("\nReports per year:")
print(summary)