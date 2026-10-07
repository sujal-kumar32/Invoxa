import pandas as pd


def export_invoice_to_excel(invoice, output_path):
    dataframe = pd.DataFrame([invoice])

    dataframe.to_excel(
        output_path,
        index=False
    )