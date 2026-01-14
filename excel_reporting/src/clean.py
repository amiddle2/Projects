import pandas as pd

def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove duplicates (Excel: Remove Duplicates)
    df = df.drop_duplicates()

    # Convert revenue to numeric
    df["revenue"] = (
        df["revenue"]
        .replace(r"[\$,]", "", regex=True)
        .astype(float)
    )

    # Parse dates
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    return df


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Standardize text (Excel: TRIM / PROPER)
    df["region"] = df["region"].str.strip().str.title()

    return df
