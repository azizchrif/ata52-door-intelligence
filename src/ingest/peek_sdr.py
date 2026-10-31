import pandas as pd

# 1. Win el fichier
CSV_PATH = "data/raw/sdr_2025.csv"

# 2. Na9raw el CSV
try:
    df = pd.read_csv(CSV_PATH, low_memory=False)
except UnicodeDecodeError:
    df = pd.read_csv(CSV_PATH, low_memory=False, encoding="latin-1")

# 3. 9addech men ligne w colonne
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

# 4. Esami el colonnes
print("\nColumns:")
for col in df.columns:
    print(f"  - {col}")

# 5. 3 lignes lowla
print("\nFirst 3 rows:")
print(df.head(3).T)
# 6. Rapports mte3 el portes (ATA 52)
jasc = df["JASCCode"].astype(str).str.strip()
is_door = jasc.str.startswith("52")
doors = df[is_door]

total = len(df)
n_doors = len(doors)
print(f"\nDoor reports (ATA 52): {n_doors:,} / {total:,} ({n_doors / total:.1%})")

# 7. Top 10 codes 52xx
print("\nTop 10 door JASC codes:")
print(jasc[is_door].value_counts().head(10))