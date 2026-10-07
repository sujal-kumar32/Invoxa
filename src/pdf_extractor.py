import pdfplumber

PDF_PATH = "input/sample_invoice.pdf"


def extract_text_from_pdf(pdf_path):
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            if text:
                extracted_text += f"\n--- Page {page_number} ---\n"
                extracted_text += text

    return extracted_text


text = extract_text_from_pdf(PDF_PATH)

print(text)