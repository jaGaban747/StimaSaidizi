import json
from pathlib import Path
from typing import Optional


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "bills.json"


def load_bills() -> list[dict]:
    """Load all synthetic billing records."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_bill(customer_id: str) -> Optional[dict]:
    """Return the bill matching the supplied customer ID."""
    bills = load_bills()

    for bill in bills:
        if bill["customer_id"].lower() == customer_id.lower():
            return bill

    return None