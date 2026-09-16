from fastapi import APIRouter, HTTPException

from services.outage_service import check_outage


router = APIRouter(
    prefix="/outages",
    tags=["Outages"],
)


@router.get("/{area}")
def read_outage(area: str):
    outage = check_outage(area)

    if outage is None:
        raise HTTPException(
            status_code=404,
            detail="No active outage found for this area",
        )

    return outage