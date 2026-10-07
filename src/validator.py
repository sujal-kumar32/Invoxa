REQUIRED_FIELDS = [
    "Invoice Number",
    "Invoice Date",
    "Vendor",
    "Customer",
    "Subtotal",
    "Total"
]


def validate_invoice(invoice):
    missing_fields = []

    for field in REQUIRED_FIELDS:
        if not invoice.get(field):
            missing_fields.append(field)

    return missing_fields