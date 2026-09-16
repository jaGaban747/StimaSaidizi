import json

import services.case_service as case_service


def test_create_support_case(tmp_path, monkeypatch):
    test_file = tmp_path / "support_cases.json"

    initial_cases = [
        {
            "case_id": "CASE001",
            "customer_id": "CUS001",
            "category": "outage",
            "status": "resolved",
        }
    ]

    test_file.write_text(
        json.dumps(initial_cases),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        case_service,
        "DATA_FILE",
        test_file,
    )

    new_case = case_service.create_support_case(
        customer_id="CUS004",
        category="outage",
        summary="Test isolated supply fault.",
    )

    assert new_case["case_id"] == "CASE002"
    assert new_case["customer_id"] == "CUS004"
    assert new_case["category"] == "outage"
    assert new_case["status"] == "open"
    assert new_case["escalation_reason"] is None

    saved_cases = json.loads(
        test_file.read_text(encoding="utf-8")
    )

    assert len(saved_cases) == 2
    assert saved_cases[-1]["case_id"] == "CASE002"
def test_escalate_support_case(tmp_path, monkeypatch):
    test_file = tmp_path / "support_cases.json"

    initial_cases = [
        {
            "case_id": "CASE001",
            "customer_id": "CUS004",
            "category": "outage",
            "channel": "web_chat",
            "language": "en",
            "created_at": "2026-09-16T10:00:00",
            "updated_at": "2026-09-16T10:00:00",
            "status": "open",
            "resolution_time_minutes": None,
            "escalation_reason": None,
            "summary": "Customer reports loss of power.",
        }
    ]

    test_file.write_text(
        json.dumps(initial_cases),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        case_service,
        "DATA_FILE",
        test_file,
    )

    escalated_case = case_service.escalate_case(
        case_id="CASE001",
        reason="Possible isolated supply fault.",
    )

    assert escalated_case is not None
    assert escalated_case["case_id"] == "CASE001"
    assert escalated_case["status"] == "escalated"
    assert (
        escalated_case["escalation_reason"]
        == "Possible isolated supply fault."
    )

    saved_cases = json.loads(
        test_file.read_text(encoding="utf-8")
    )

    assert saved_cases[0]["status"] == "escalated"
    assert (
        saved_cases[0]["escalation_reason"]
        == "Possible isolated supply fault."
    )