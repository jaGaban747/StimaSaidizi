from fastapi import APIRouter, HTTPException

from services.token_service import check_token_transaction


router = APIRouter(
    prefix="/tokens",
    tags=["Tokens"],
)


@router.get("/{transaction_id}")
def read_token_transaction(transaction_id: str):
    transaction = check_token_transaction(transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Token transaction not found",
        )

    return transaction