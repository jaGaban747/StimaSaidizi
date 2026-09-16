from services.token_service import check_token_transaction


def test_issued_token_transaction():
    transaction = check_token_transaction("TXN001")

    assert transaction is not None
    assert transaction["payment_status"] == "successful"
    assert transaction["token_status"] == "issued"


def test_pending_token_transaction():
    transaction = check_token_transaction("TXN002")

    assert transaction is not None
    assert transaction["payment_status"] == "successful"
    assert transaction["token_status"] == "pending"


def test_nonexistent_token_transaction():
    transaction = check_token_transaction("TXN999")

    assert transaction is None