import pandas as pd

from src.ingest.sdr import door_reports, load_all

df = load_all()
doors = door_reports(df).copy()

# Clean aircraft names: same text, same case
doors["AircraftMake"] = doors["AircraftMake"].astype(str).str.strip().str.upper()
doors["AircraftModel"] = doors["AircraftModel"].astype(str).str.strip().str.upper()

# 1. Top makes
print("Top 10 aircraft makes (door reports, 2021-2025):")
print(doors["AircraftMake"].value_counts().head(10))

# 2. Top models
print("\nTop 15 aircraft models:")
print(doors["AircraftModel"].value_counts().head(15))

# 3. Emergency exits (5220): which models drive the rise?
exits = doors[doors["JASCCode"] == "5220"]
top_models = exits["AircraftModel"].value_counts().head(8).index
exits_top = exits[exits["AircraftModel"].isin(top_models)]
print("\nEmergency exit reports (5220) by model and year:")
print(pd.crosstab(exits_top["AircraftModel"], exits_top["year"]))

# 4. The two operators behind the 2025 rise
ops_2025 = doors[(doors["year"] == 2025) & (doors["OperatorDesignator"].isin(["AALA", "CALA"]))]
print("\nAALA + CALA in 2025, top JASC codes:")
print(pd.crosstab(ops_2025["JASCCode"], ops_2025["OperatorDesignator"]).sort_values("AALA", ascending=False).head(8))
print("\nAALA + CALA in 2025, top models:")
print(pd.crosstab(ops_2025["AircraftModel"], ops_2025["OperatorDesignator"]).sort_values("AALA", ascending=False).head(8))