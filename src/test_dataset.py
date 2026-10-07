from pathlib import Path
from decimal import Decimal

from pdf_extractor import extract_invoice


TEST_FOLDER = Path("test_invoices")


def get_expected_invoice(pdf_file):
    """
    Build expected values for the SuperStore test dataset.

    The customer name and invoice number are encoded in the filename.
    The remaining values are read directly from the PDF text.
    """

    parts = pdf_file.stem.split("_")

    invoice_number = parts[-1]
    customer = " ".join(parts[1:-1])

    import pdfplumber
    import re

    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join(
            page.extract_text() or ""
            for page in pdf.pages
        )

    date_match = re.search(
        r"Date:\s*([A-Za-z]+\s+\d{1,2}\s+\d{4})",
        text
    )

    subtotal_match = re.search(
        r"Subtotal:\s*\$?([\d,]+\.\d{2})",
        text
    )

    total_match = re.search(
        r"Total:\s*\$?([\d,]+\.\d{2})",
        text
    )

    return {
        "Invoice Number": invoice_number,
        "Invoice Date": date_match.group(1) if date_match else None,
        "Vendor": "SuperStore",
        "Customer": customer,
        "Subtotal": (
            Decimal(subtotal_match.group(1).replace(",", ""))
            if subtotal_match
            else None
        ),
        "Total": (
            Decimal(total_match.group(1).replace(",", ""))
            if total_match
            else None
        )
    }


def values_match(actual, expected):
    return actual == expected


def test_invoices():
    pdf_files = list(TEST_FOLDER.glob("*.pdf"))

    print(f"Found {len(pdf_files)} test invoices")
    print()

    fields = [
        "Invoice Number",
        "Invoice Date",
        "Vendor",
        "Customer",
        "Subtotal",
        "Total"
    ]

    correct_counts = {field: 0 for field in fields}
    error_count = 0

    for pdf_file in pdf_files:
        try:
            actual = extract_invoice(pdf_file)
            expected = get_expected_invoice(pdf_file)

            for field in fields:
                if values_match(actual[field], expected[field]):
                    correct_counts[field] += 1

            if all(
                values_match(actual[field], expected[field])
                for field in fields
            ):
                print(f"PASS: {pdf_file.name}")
            else:
                print(f"FAIL: {pdf_file.name}")

                for field in fields:
                    if not values_match(actual[field], expected[field]):
                        print(
                            f"  {field}: "
                            f"expected={expected[field]!r}, "
                            f"actual={actual[field]!r}"
                        )

        except Exception as error:
            error_count += 1
            print(f"ERROR: {pdf_file.name}")
            print(f"  {error}")

    print()
    print("=" * 60)
    print("ACCURACY REPORT")
    print("=" * 60)

    total = len(pdf_files)

    for field in fields:
        accuracy = (
            correct_counts[field] / total * 100
            if total
            else 0
        )

        print(
            f"{field}: "
            f"{correct_counts[field]}/{total} "
            f"({accuracy:.1f}%)"
        )

    print(f"Processing errors: {error_count}/{total}")

    total_correct = sum(correct_counts.values())
    total_checks = total * len(fields)

    overall_accuracy = (
        total_correct / total_checks * 100
        if total_checks
        else 0
    )

    print(
        f"Overall field accuracy: "
        f"{overall_accuracy:.1f}%"
    )


if __name__ == "__main__":
    test_invoices()