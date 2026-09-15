import json
from pathlib import Path
from typing import Optional


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "token_transactions.json"
)


def load_token_transactions() -> list[dict]:
    """Load all synthetic prepaid token transaction records."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def check_token_transaction(transaction_id: str) -> Optional[dict]:
    """Return the prepaid token transaction matching the supplied ID."""
    transactions = load_token_transactions()

    for transaction in transactions:
        if transaction["transaction_id"].lower() == transaction_id.lower():
            return transaction

    return None