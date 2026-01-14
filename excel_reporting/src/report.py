import pandas as pd

def write_excel_report(
    detailed_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    output_path: str
) -> None:

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        detailed_df.to_excel(
            writer,
            sheet_name="Cleaned_Data",
            index=False
        )

        summary_df.to_excel(
            writer,
            sheet_name="Summary_Pivot"
        )

        workbook = writer.book
        worksheet = writer.sheets["Cleaned_Data"]

        # Excel-like formatting
        header_format = workbook.add_format({
            "bold": True,
            "border": 1
        })

        for col_num, col_name in enumerate(detailed_df.columns):
            worksheet.write(0, col_num, col_name, header_format)
            worksheet.set_column(col_num, col_num, 15)
