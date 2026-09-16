from services.outage_service import check_outage


def test_active_outage_exists():
    outage = check_outage("Kasarani")

    assert outage is not None
    assert outage["outage_id"] == "OUT001"
    assert outage["status"] == "active"


def test_no_active_outage():
    outage = check_outage("Awendo")

    assert outage is None