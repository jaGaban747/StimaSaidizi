from services.customer_service import get_customer


def test_get_existing_customer():
    customer = get_customer("CUS001")

    assert customer is not None
    assert customer["customer_id"] == "CUS001"
    assert customer["name"] == "Amina Kamau"
    assert customer["area"] == "Kasarani"


def test_get_nonexistent_customer():
    customer = get_customer("CUS999")

    assert customer is None