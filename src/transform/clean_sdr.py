"""Cleaning rules for FAA SDR aircraft fields."""
import re

import pandas as pd

# FAA abbreviation -> clean manufacturer name
MAKE_MAP = {
    "BOEING": "BOEING",
    "AIRBUS": "AIRBUS",
    "CNDAIR": "BOMBARDIER",   # Canadair = CRJ family, same as Bombardier
    "BOMBDR": "BOMBARDIER",
    "EMB": "EMBRAER",
    "DOUG": "MCDONNELL DOUGLAS",
}

# Canadair CL-600 type code -> commercial name
CRJ_MAP = {"2B19": "CRJ200", "2C10": "CRJ700", "2D24": "CRJ900", "2E25": "CRJ1000"}


def normalize_make(make: str) -> str:
    """Map an FAA make abbreviation to a clean manufacturer name."""
    make = str(make).strip().upper()
    return MAKE_MAP.get(make, make)


def model_family(model: str) -> str:
    """Turn an FAA model code into an aircraft family, e.g. A321231 -> A321."""
    model = str(model).strip().upper()

    # Airbus: A321231, A321253NX, A320* -> A321, A320
    match = re.match(r"^A(3\d\d)", model)
    if match:
        return "A" + match.group(1)

    # Canadair regional jets: CL6002D24 -> CRJ900
    if model.startswith("CL600"):
        return CRJ_MAP.get(model[5:9], "CRJ")

    # Boeing: 737823 -> 737-800, 757232 -> 757-200
    match = re.match(r"^(7[0-8]7)(\d)", model)
    if match and len(model) >= 6:
        return f"{match.group(1)}-{match.group(2)}00"
    if re.match(r"^7[0-8]7", model):
        return model[:3]

    return model


def clean_aircraft(df: pd.DataFrame) -> pd.DataFrame:
    """Add clean make and model family columns."""
    df = df.copy()
    df["make_clean"] = df["AircraftMake"].map(normalize_make)
    df["model_family"] = df["AircraftModel"].map(model_family)
    return df