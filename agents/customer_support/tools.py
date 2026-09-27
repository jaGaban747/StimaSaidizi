from services.customer_service import get_customer
from services.outage_service import check_outage
from services.token_service import check_token_transaction
from services.billing_service import get_bill
from services.case_service import create_support_case, escalate_case


def read_customer(customer_id: str) -> dict:
    """Look up a customer using their customer ID."""

    customer = get_customer(customer_id)

    if customer is None:
        return {
            "status": "not_found",
            "message": "No matching customer was found.",
        }

    return {
        "status": "found",
        "customer": customer,
    }


def verify_outage(area: str) -> dict:
    """Check whether there is a recorded active outage in an area."""

    outage = check_outage(area)

    if outage is None:
        return {
            "status": "not_found",
            "area": area,
            "message": "No recorded active outage was found for this area.",
        }

    return {
        "status": "found",
        "outage": outage,
    }


def verify_token_transaction(transaction_id: str) -> dict:
    """Check the status of a prepaid electricity token transaction."""

    transaction = check_token_transaction(transaction_id)

    if transaction is None:
        return {
            "status": "not_found",
            "transaction_id": transaction_id,
            "message": "No matching token transaction was found.",
        }

    return {
        "status": "found",
        "transaction_id": transaction["transaction_id"],
        "payment_status": transaction["payment_status"],
        "token_status": transaction["token_status"],
    }


def read_bill(customer_id: str) -> dict:
    """Retrieve the recorded electricity bill for a customer."""

    bill = get_bill(customer_id)

    if bill is None:
        return {
            "status": "not_found",
            "customer_id": customer_id,
            "message": "No matching bill was found.",
        }

    return {
        "status": "found",
        "bill": bill,
    }


def open_support_case(
    customer_id: str,
    category: str,
    summary: str,
    language: str = "en",
) -> dict:
    """Create a support case for an unresolved customer issue."""

    case = create_support_case(
        customer_id=customer_id,
        category=category,
        summary=summary,
        channel="web_chat",
        language=language,
    )

    return {
        "status": "created",
        "case_id": case["case_id"],
        "category": case["category"],
        "case_status": case["status"],
    }


def escalate_support_case(case_id: str, reason: str) -> dict:
    """Escalate an existing support case for human review."""

    case = escalate_case(case_id, reason)

    if case is None:
        return {
            "status": "not_found",
            "case_id": case_id,
            "message": "No matching support case was found.",
        }

    return {
        "status": "escalated",
        "case_id": case["case_id"],
        "category": case["category"],
        "case_status": case["status"],
    }