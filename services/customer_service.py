import json
from pathlib import Path
from typing import Optional


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "customers.json"


def load_customers() -> list[dict]:
    """Load all synthetic customer records."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_customer(customer_id: str) -> Optional[dict]:
    """Return a customer matching the supplied customer ID."""
    customers = load_customers()

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer

    return None