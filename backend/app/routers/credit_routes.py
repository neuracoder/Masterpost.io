from fastapi import APIRouter, Depends
from app.models.schemas import UseCreditsRequest
from app.services.credit_service import (
    get_balance, use_credits, get_transaction_history
)
from app.routers.auth_routes import get_current_user_id

router = APIRouter(prefix="/api/credits", tags=["Credits"])

@router.get("/balance")
async def get_credit_balance(user_id: str = Depends(get_current_user_id)):
    """Obtener balance de créditos"""
    return await get_balance(user_id)

@router.post("/use")
async def use_user_credits(
    request: UseCreditsRequest,
    user_id: str = Depends(get_current_user_id)
):
    """Usar créditos"""
    return await use_credits(
        user_id=user_id,
        credits_needed=request.credits,
        transaction_type=request.transaction_type,
        description=request.description
    )

@router.get("/history")
async def get_credit_history(
    limit: int = 50,
    offset: int = 0,
    user_id: str = Depends(get_current_user_id)
):
    """Obtener historial de transacciones"""
    return await get_transaction_history(user_id, limit, offset)
