import json
from datetime import datetime
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "support_cases.json"
)


def load_support_cases() -> list[dict]:
    """Load all synthetic support cases."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_support_cases(cases: list[dict]) -> None:
    """Save support cases to the synthetic data file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(cases, file, indent=2)


def create_support_case(
    customer_id: str,
    category: str,
    summary: str,
    channel: str = "web_chat",
    language: str = "en",
) -> dict:
    """Create and store a new support case."""

    cases = load_support_cases()

    case_numbers = [
        int(case["case_id"].replace("CASE", ""))
        for case in cases
    ]

    next_number = max(case_numbers, default=0) + 1
    case_id = f"CASE{next_number:03d}"

    timestamp = datetime.now().isoformat(timespec="seconds")

    new_case = {
        "case_id": case_id,
        "customer_id": customer_id,
        "category": category,
        "channel": channel,
        "language": language,
        "created_at": timestamp,
        "updated_at": timestamp,
        "status": "open",
        "resolution_time_minutes": None,
        "escalation_reason": None,
        "summary": summary,
    }

    cases.append(new_case)
    save_support_cases(cases)

    return new_case
def escalate_case(case_id: str, reason: str) -> dict | None:
    """Escalate an existing support case."""

    cases = load_support_cases()

    for case in cases:
        if case["case_id"].lower() == case_id.lower():
            case["status"] = "escalated"
            case["escalation_reason"] = reason
            case["updated_at"] = datetime.now().isoformat(timespec="seconds")

            save_support_cases(cases)

            return case

    return None