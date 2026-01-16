import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw"

def load_sales() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "sales.csv")

def load_customers() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "customers.csv")

def load_products() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "products.csv")
