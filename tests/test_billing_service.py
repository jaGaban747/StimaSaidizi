from services.billing_service import get_bill


def test_unpaid_bill():
    bill = get_bill("CUS002")

    assert bill is not None
    assert bill["bill_id"] == "BILL001"
    assert bill["amount_due"] == 4250.0
    assert bill["status"] == "unpaid"


def test_overdue_bill():
    bill = get_bill("CUS005")

    assert bill is not None
    assert bill["bill_id"] == "BILL002"
    assert bill["status"] == "overdue"


def test_customer_without_bill():
    bill = get_bill("CUS999")

    assert bill is None