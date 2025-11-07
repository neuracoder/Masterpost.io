"""
Servicio para verificar créditos antes de procesar
"""

from app.services.credit_service import get_balance
from fastapi import HTTPException, status
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class InsufficientCreditsError(HTTPException):
    """Error cuando no hay créditos suficientes"""
    def __init__(self, required: int, available: int):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "error": "insufficient_credits",
                "message": f"Insufficient credits. Required: {required}, Available: {available}",
                "credits_required": required,
                "credits_available": available,
                "credits_needed": required - available
            }
        )

async def verify_credits(
    user_id: str,
    images_count: int,
    processing_tier: str = "basic"
) -> Dict[str, Any]:
    """
    Verificar que el usuario tenga créditos suficientes

    Args:
        user_id: ID del usuario
        images_count: Número de imágenes a procesar
        processing_tier: "basic" (1 crédito) o "premium" (3 créditos)

    Returns:
        Dict con información de créditos

    Raises:
        InsufficientCreditsError: Si no hay créditos suficientes
    """

    # 1. Calcular créditos necesarios
    credits_per_image = 1 if processing_tier.lower() == "basic" else 3
    credits_required = images_count * credits_per_image

    logger.info(f"[CREDIT CHECK] User {user_id}: {images_count} images x {credits_per_image} credits = {credits_required} credits needed")

    # 2. Consultar balance actual
    try:
        balance_info = await get_balance(user_id)
        credits_available = balance_info.get('credits', 0)

        logger.info(f"[CREDIT CHECK] User {user_id}: {credits_available} credits available")

    except Exception as e:
        logger.error(f"[CREDIT CHECK] Error getting balance for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error checking credit balance"
        )

    # 3. Verificar si tiene suficientes
    if credits_available < credits_required:
        logger.warning(
            f"[CREDIT CHECK] User {user_id}: INSUFFICIENT CREDITS "
            f"(need {credits_required}, have {credits_available})"
        )
        raise InsufficientCreditsError(
            required=credits_required,
            available=credits_available
        )

    # 4. Retornar info si todo OK
    logger.info(f"[CREDIT CHECK] User {user_id}: ✅ SUFFICIENT CREDITS")

    return {
        "sufficient": True,
        "credits_required": credits_required,
        "credits_available": credits_available,
        "credits_remaining_after": credits_available - credits_required,
        "processing_tier": processing_tier,
        "images_count": images_count
    }

async def check_credits_for_job(
    user_id: str,
    job_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Verificar créditos para un job completo

    Args:
        user_id: ID del usuario
        job_data: Datos del job con images_count y processing_tier

    Returns:
        Dict con información de verificación
    """
    images_count = job_data.get('images_count', 0)
    processing_tier = job_data.get('processing_tier', 'basic')

    return await verify_credits(
        user_id=user_id,
        images_count=images_count,
        processing_tier=processing_tier
    )
