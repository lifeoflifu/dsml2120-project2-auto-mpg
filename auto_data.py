from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parent / "data" / "auto-mpg.csv"
KAGGLE_URL = "https://www.kaggle.com/datasets/uciml/autompg-dataset"
UCI_URL = "https://doi.org/10.24432/C5859H"
ORIGINS = {1: "United States", 2: "Europe", 3: "Japan"}
BRAND_ALIASES = {
    "amc": "AMC",
    "bmw": "BMW",
    "chevroelt": "Chevrolet",
    "chevy": "Chevrolet",
    "maxda": "Mazda",
    "mercedes": "Mercedes-Benz",
    "mercedes-benz": "Mercedes-Benz",
    "toyouta": "Toyota",
    "vokswagen": "Volkswagen",
    "vw": "Volkswagen",
    "hi": "HI (source label)",
    "capri": "Capri (source label)",
}


@st.cache_data(show_spinner=False)
def load_data(file_modified_ns: int) -> tuple[pd.DataFrame, datetime]:
    """Read the local snapshot again when its file modification time changes."""
    data = pd.read_csv(DATA_PATH, na_values=["?"])
    data.columns = data.columns.str.strip().str.replace(" ", "_")
    data["model_year"] = data["model_year"] + 1900
    data["origin_label"] = data["origin"].map(ORIGINS)
    prefix = data["car_name"].str.strip().str.lower().str.split().str[0]
    data["brand"] = prefix.map(BRAND_ALIASES).fillna(prefix.str.title())
    return data, datetime.now(timezone.utc)


def brand_summary(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby("brand", as_index=False)
        .agg(average_mpg=("mpg", "mean"), cars=("mpg", "size"))
        .sort_values(["average_mpg", "brand"], ascending=[False, True])
    )


def year_summary(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby("model_year", as_index=False)
        .agg(median_mpg=("mpg", "median"), cars=("mpg", "size"))
        .sort_values("model_year")
    )
