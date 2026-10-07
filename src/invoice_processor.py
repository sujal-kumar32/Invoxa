from pathlib import Path
import pandas as pd

from pdf_extractor import extract_invoice
from validator import validate_invoice


INPUT_FOLDER = Path("input")
OUTPUT_PATH = Path("output/invoice_report.xlsx")


def get_invoice_files():
    return list(INPUT_FOLDER.glob("*.pdf"))


def process_invoices():
    invoice_files = get_invoice_files()
    invoices = []

    for pdf_file in invoice_files:
        print("Processing:", pdf_file.name)

        try:
            invoice = extract_invoice(pdf_file)

            missing_fields = validate_invoice(invoice)

            if missing_fields:
                print("  Missing:", ", ".join(missing_fields))
            else:
                print("  Valid invoice")

            invoices.append(invoice)

        except Exception as error:
            print("  Error:", error)

    return invoices


def export_to_excel(invoices):
    dataframe = pd.DataFrame(invoices)

    dataframe.to_excel(
        OUTPUT_PATH,
        index=False
    )


invoices = process_invoices()

export_to_excel(invoices)

print(f"Processed {len(invoices)} invoice(s).")
print("Excel report created:", OUTPUT_PATH)