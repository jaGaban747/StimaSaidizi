from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.case_service import create_support_case, escalate_case


router = APIRouter(
    prefix="/support-cases",
    tags=["Support Cases"],
)


class CreateCaseRequest(BaseModel):
    customer_id: str
    category: str
    summary: str
    channel: str = "web_chat"
    language: str = "en"


class EscalateCaseRequest(BaseModel):
    reason: str


@router.post("/")
def create_case(request: CreateCaseRequest):
    return create_support_case(
        customer_id=request.customer_id,
        category=request.category,
        summary=request.summary,
        channel=request.channel,
        language=request.language,
    )


@router.patch("/{case_id}/escalate")
def escalate_support_case(
    case_id: str,
    request: EscalateCaseRequest,
):
    case = escalate_case(
        case_id=case_id,
        reason=request.reason,
    )

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Support case not found",
        )

    return case