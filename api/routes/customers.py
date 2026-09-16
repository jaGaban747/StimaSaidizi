from fastapi import APIRouter, HTTPException

from services.customer_service import get_customer


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get("/{customer_id}")
def read_customer(customer_id: str):
    customer = get_customer(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer