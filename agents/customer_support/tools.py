from services.token_service import check_token_transaction


def verify_token_transaction(transaction_id: str) -> dict:
    """
    Check the status of a prepaid electricity token transaction.

    Args:
        transaction_id: The transaction reference supplied by the customer.

    Returns:
        A dictionary indicating whether the transaction exists.
    """

    transaction = check_token_transaction(transaction_id)

    if transaction is None:
        return {
            "status": "not_found",
            "message": "No matching token transaction was found.",
        }

    return {
        "status": "found",
        "message": "The transaction was found successfully.",
    }