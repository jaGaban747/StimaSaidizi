import json
from pathlib import Path
from datetime import datetime


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "support_cases.json"
)
CUSTOMERS_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "customers.json"
)
def load_customers() -> list[dict]:
    """Load all synthetic customer records."""
    with CUSTOMERS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_support_cases() -> list[dict]:
    """Load all support case records."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def total_cases() -> int:
    """Return the total number of support cases."""
    cases = load_support_cases()
    return len(cases)
def cases_by_category() -> dict[str, int]:
    """Return the number of support cases in each category."""
    cases = load_support_cases()

    counts = {}

    for case in cases:
        category = case["category"]
        counts[category] = counts.get(category, 0) + 1

    return counts
def cases_by_status() -> dict[str, int]:
    """Return the number of support cases in each status."""
    cases = load_support_cases()

    counts = {}

    for case in cases:
        status = case["status"]
        counts[status] = counts.get(status, 0) + 1

    return counts
def resolution_rate() -> float:
    """Return the percentage of support cases that are resolved."""
    cases = load_support_cases()

    if not cases:
        return 0.0

    resolved = sum(
        1 for case in cases
        if case["status"] == "resolved"
    )

    return round((resolved / len(cases)) * 100, 2)


def escalation_rate() -> float:
    """Return the percentage of support cases that are escalated."""
    cases = load_support_cases()

    if not cases:
        return 0.0

    escalated = sum(
        1 for case in cases
        if case["status"] == "escalated"
    )

    return round((escalated / len(cases)) * 100, 2)
def average_resolution_time() -> float:
    """Return the average resolution time for resolved cases."""
    cases = load_support_cases()

    resolution_times = [
        case["resolution_time_minutes"]
        for case in cases
        if (
            case["status"] == "resolved"
            and case["resolution_time_minutes"] is not None
        )
    ]

    if not resolution_times:
        return 0.0

    return round(
        sum(resolution_times) / len(resolution_times),
        2
    )
def average_resolution_time_by_location_class() -> dict[str, float]:
    """Return average resolution time grouped by rural or urban location."""
    cases = load_support_cases()
    customers = load_customers()

    customer_locations = {
        customer["customer_id"]: customer["location_class"]
        for customer in customers
    }

    resolution_times = {
        "urban": [],
        "rural": [],
    }

    for case in cases:
        if (
            case["status"] == "resolved"
            and case["resolution_time_minutes"] is not None
        ):
            location_class = customer_locations.get(case["customer_id"])

            if location_class in resolution_times:
                resolution_times[location_class].append(
                    case["resolution_time_minutes"]
                )

    averages = {}

    for location_class, times in resolution_times.items():
        averages[location_class] = (
            round(sum(times) / len(times), 2)
            if times
            else 0.0
        )

    return averages
def unresolved_cases() -> list[dict]:
    """Return all open or escalated support cases."""
    cases = load_support_cases()

    return [
        case
        for case in cases
        if case["status"] in {"open", "escalated"}
    ]
def open_cases_by_age(
    reference_time: str = "2026-09-16T02:00:00"
) -> list[dict]:
    """Return unresolved cases with their age in minutes."""

    cases = unresolved_cases()
    reference = datetime.fromisoformat(reference_time)

    results = []

    for case in cases:
        created_at = datetime.fromisoformat(case["created_at"])

        age_minutes = int(
            (reference - created_at).total_seconds() / 60
        )

        results.append({
            "case_id": case["case_id"],
            "status": case["status"],
            "category": case["category"],
            "age_minutes": age_minutes,
        })

    return sorted(
        results,
        key=lambda case: case["age_minutes"],
        reverse=True,
    )
def most_common_enquiry_category() -> dict | None:
    """Return the most common support case category."""

    category_counts = cases_by_category()

    if not category_counts:
        return None

    category = max(
        category_counts,
        key=category_counts.get
    )

    return {
        "category": category,
        "count": category_counts[category],
    }