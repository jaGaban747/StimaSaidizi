import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "outages.json"

KENYA_TIMEZONE = ZoneInfo("Africa/Nairobi")


def load_outages() -> list[dict]:
    """Load all synthetic outage records."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def check_outage(area: str) -> Optional[dict]:
    """Return an active outage with restoration-estimate validity."""

    outages = load_outages()

    for outage in outages:
        if (
            outage["area"].lower() == area.lower()
            and outage["status"] == "active"
        ):
            result = outage.copy()

            estimate = result.get("estimated_restoration")

            if estimate:
                estimated_time = datetime.fromisoformat(estimate)

                if estimated_time.tzinfo is None:
                    estimated_time = estimated_time.replace(
                        tzinfo=KENYA_TIMEZONE
                    )

                result["restoration_estimate_expired"] = (
                    estimated_time < datetime.now(KENYA_TIMEZONE)
                )
            else:
                result["restoration_estimate_expired"] = None

            return result

    return None
