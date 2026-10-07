import pdfplumber
import re

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


text = extract_text_from_pdf(PDF_PATH)

invoice_number = extract_invoice_number(text)
invoice_date = extract_invoice_date(text)

print("Invoice Number:", invoice_number)
print("Invoice Date:", invoice_date)