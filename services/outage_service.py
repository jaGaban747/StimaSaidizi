import json
from pathlib import Path
from typing import Optional


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "outages.json"


def load_outages() -> list[dict]:
    """Load all synthetic outage records."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def check_outage(area: str) -> Optional[dict]:
    """Return an active outage for the supplied area."""
    outages = load_outages()

    for outage in outages:
        if (
            outage["area"].lower() == area.lower()
            and outage["status"] == "active"
        ):
            return outage

    return None