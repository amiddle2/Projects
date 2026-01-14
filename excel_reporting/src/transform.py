import pandas as pd
import numpy as np

def merge_data(
    sales: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame
) -> pd.DataFrame:
    df = sales.merge(customers, on="customer_id", how="left")
    df = df.merge(products, on="product_id", how="left")
    return df


def add_calculated_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Excel: =Revenue - UnitCost
    df["profit"] = df["revenue"] - df["unit_cost"]

    # Excel: IF()
    df["high_value_order"] = np.where(df["revenue"] > 1000, "Yes", "No")

    return df


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    # Excel: Pivot Table
    summary = pd.pivot_table(
        df,
        values="revenue",
        index="region",
        columns="category",
        aggfunc="sum",
        fill_value=0
    )

    return summary
