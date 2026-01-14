from pathlib import Path

from src.load import load_sales, load_customers, load_products
from src.clean import clean_sales, clean_customers
from src.transform import (
    merge_data,
    add_calculated_fields,
    create_summary
)
from src.report import write_excel_report

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "sales_report.xlsx"

def main():
    sales = clean_sales(load_sales())
    customers = clean_customers(load_customers())
    products = load_products()

    df = merge_data(sales, customers, products)
    df = add_calculated_fields(df)

    summary = create_summary(df)

    write_excel_report(df, summary, OUTPUT_FILE)

    print(f"Report generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()