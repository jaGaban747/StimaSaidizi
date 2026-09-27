from services.token_service import check_token_transaction


def verify_token_transaction(transaction_id: str) -> dict:
    """
    Check the status of a prepaid electricity token transaction.

    Args:
        transaction_id: The transaction reference supplied by the customer.

    Returns:
        A safe summary of the transaction status.
    """

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