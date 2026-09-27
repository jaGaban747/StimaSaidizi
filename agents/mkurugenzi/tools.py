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


def get_analytics_summary() -> dict:
    """Return a summary of the synthetic customer-support metrics."""

    return {
        "total_cases": total_cases(),
        "cases_by_category": cases_by_category(),
        "cases_by_status": cases_by_status(),
        "resolution_rate_percent": resolution_rate(),
        "escalation_rate_percent": escalation_rate(),
        "average_resolution_time_minutes": average_resolution_time(),
        "average_resolution_time_by_location_class_minutes":
            average_resolution_time_by_location_class(),
        "most_common_enquiry_category": most_common_enquiry_category(),
    }


def get_unresolved_cases() -> dict:
    """Return all currently open or escalated support cases."""

    cases = unresolved_cases()

    return {
        "count": len(cases),
        "cases": cases,
    }