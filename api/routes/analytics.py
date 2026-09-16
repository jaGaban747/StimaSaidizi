from fastapi import APIRouter

from services.analytics_service import (
    total_cases,
    cases_by_category,
    cases_by_status,
    resolution_rate,
    escalation_rate,
    average_resolution_time,
    average_resolution_time_by_location_class,
    unresolved_cases,
    most_common_enquiry_category,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/summary")
def analytics_summary():
    """Return a management summary of customer-support activity."""

    return {
        "total_cases": total_cases(),
        "cases_by_category": cases_by_category(),
        "cases_by_status": cases_by_status(),
        "resolution_rate_percent": resolution_rate(),
        "escalation_rate_percent": escalation_rate(),
        "average_resolution_time_minutes": average_resolution_time(),
        "average_resolution_time_by_location_class": (
            average_resolution_time_by_location_class()
        ),
        "most_common_enquiry_category": (
            most_common_enquiry_category()
        ),
    }


@router.get("/unresolved")
def read_unresolved_cases():
    """Return support cases that have not been resolved."""
    return unresolved_cases()