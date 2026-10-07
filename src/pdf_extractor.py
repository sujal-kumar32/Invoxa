import pdfplumber
import re
from decimal import Decimal








def extract_text_from_pdf(pdf_path):
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

    return extracted_text


def extract_invoice_number(text):
    patterns = [
        r"Invoice Number\s*[:#]?\s*([A-Za-z0-9-]+)",
        r"Invoice No\.?\s*[:#]?\s*([A-Za-z0-9-]+)",
        r"Invoice #\s*([A-Za-z0-9-]+)",
        r"^\#\s*([A-Za-z0-9-]+)$"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)

        if match:
            return match.group(1)

    return None


def extract_invoice_date(text):
    patterns = [
        r"Invoice Date\s*[:#]?\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})",
        r"Date\s*:\s*([A-Za-z]+\s+\d{1,2}\s+\d{4})",
        r"Date\s*:\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

    return None

def extract_vendor(text):
    patterns = [
        r"^(.+?)\s+INVOICE$",
        r"From:\s*\n(.+?)\s+Order Number"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()

    return None


def extract_customer(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        words = page.extract_words()

    customer_words = []

    for word in words:
        if 135 <= word["top"] <= 155 and word["x0"] < 150:
            customer_words.append(word["text"])

    if customer_words:
        return " ".join(customer_words)

    return None


def extract_amount(text, label):
    patterns = [
        rf"^\s*{re.escape(label)}\s*:\s*\$?([\d,]+\.\d{{2}})\s*$",
        rf"^\s*{re.escape(label)}\s+\$?([\d,]+\.\d{{2}})\s*$"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.MULTILINE
        )

        if match:
            return Decimal(match.group(1).replace(",", ""))

    return None

def extract_gstin(text):
    pattern = r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None

def extract_invoice(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    invoice_number = extract_invoice_number(text)
    invoice_date = extract_invoice_date(text)
    vendor = extract_vendor(text)
    customer = extract_customer(pdf_path)
    gstin = extract_gstin(text)

    subtotal = extract_amount(text, "Subtotal")
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

    return invoice




