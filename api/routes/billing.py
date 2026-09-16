from fastapi import APIRouter, HTTPException

from services.billing_service import get_bill


router = APIRouter(
    prefix="/billing",
    tags=["Billing"],
)


@router.get("/{customer_id}")
def read_bill(customer_id: str):
    bill = get_bill(customer_id)

    if bill is None:
        raise HTTPException(
            status_code=404,
            detail="Bill not found for this customer",
        )

    return bill