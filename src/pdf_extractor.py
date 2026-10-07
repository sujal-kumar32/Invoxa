import pdfplumber
import re
from decimal import Decimal




PDF_PATH = "input/sample_invoice.pdf"


def extract_text_from_pdf(pdf_path):
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

    return extracted_text


def extract_invoice_number(text):
    pattern = r"Invoice Number\s+([A-Za-z0-9-]+)"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1)

    return None

def extract_invoice_date(text):
    pattern = r"Invoice Date\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1)

    return None

def extract_vendor(text):
    pattern = r"From:\s*\n(.+?)\s+Order Number"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None

def extract_customer(text):
    pattern = r"To:\s*\n([^\n]+)"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None

def extract_amount(text, label):
    pattern = rf"^{label}\s+\$?([\d,]+\.\d{{2}})$"

    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)

    if match:
        return Decimal(match.group(1).replace(",", ""))

    return None

def extract_gstin(text):
    pattern = r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


text = extract_text_from_pdf(PDF_PATH)

invoice_number = extract_invoice_number(text)
invoice_date = extract_invoice_date(text)
vendor = extract_vendor(text)
customer = extract_customer(text)
gstin = extract_gstin(text)

subtotal = extract_amount(text, "Sub Total")
tax = extract_amount(text, "Tax")
total = extract_amount(text, "Total")

invoice = {
    "Invoice Number": invoice_number,
    "Invoice Date": invoice_date,
    "Vendor": vendor,
    "Customer": customer,
    "GSTIN": gstin,
    "Subtotal": subtotal,
    "Tax": tax,
    "Total": total
}

print(invoice)