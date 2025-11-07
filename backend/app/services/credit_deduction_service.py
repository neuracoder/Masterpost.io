"""
Servicio para deducir créditos después de procesar
"""

from app.services.credit_service import use_credits
from typing import Dict, Any
import logging
import asyncio

logger = logging.getLogger(__name__)

async def deduct_credits_for_processing(
    user_id: str,
    images_count: int,
    processing_tier: str,
    job_id: str,
    successful_count: int = None
) -> Dict[str, Any]:
    """
    Deducir créditos después de procesar imágenes

    Args:
        user_id: ID del usuario
        images_count: Número de imágenes procesadas
        processing_tier: "basic" o "premium"
        job_id: ID del job procesado
        successful_count: Número de imágenes exitosas (si es diferente de images_count)

    Returns:
        Dict con resultado de la deducción
    """

    # 1. Calcular créditos a deducir
    credits_per_image = 1 if processing_tier.lower() == "basic" else 3

    # Si algunas imágenes fallaron, solo cobrar las exitosas
    actual_count = successful_count if successful_count is not None else images_count
    credits_to_deduct = actual_count * credits_per_image

    if credits_to_deduct == 0:
        logger.warning(f"[DEDUCTION] Job {job_id}: No credits to deduct (0 successful images)")
        return {
            "success": False,
            "credits_deducted": 0,
            "reason": "no_successful_images"
        }

    logger.info(
        f"[DEDUCTION] Job {job_id}: Deducting {credits_to_deduct} credits "
        f"({actual_count} images × {credits_per_image} credits)"
    )

    # 2. Determinar tipo de transacción
    transaction_type = f"usage_{processing_tier.lower()}"

    # 3. Crear descripción detallada
    description = (
        f"Processed {actual_count} image(s) - Job {job_id} - "
        f"Tier: {processing_tier.upper()}"
    )

    if successful_count is not None and successful_count < images_count:
        description += f" ({images_count - successful_count} failed)"

    # 4. Deducir créditos usando el servicio de créditos
    try:
        result = await use_credits(
            user_id=user_id,
            credits_needed=credits_to_deduct,
            transaction_type=transaction_type,
            description=description
        )

        logger.info(
            f"[DEDUCTION] Job {job_id}: ✅ Credits deducted successfully - "
            f"Remaining: {result.get('credits_remaining', 'unknown')}"
        )

        return {
            "success": True,
            "credits_deducted": credits_to_deduct,
            "credits_remaining": result.get('credits_remaining'),
            "transaction_type": transaction_type,
            "job_id": job_id
        }

    except Exception as e:
        logger.error(
            f"[DEDUCTION] Job {job_id}: ❌ Failed to deduct credits - {str(e)}"
        )

        # No lanzar excepción - el procesamiento ya se hizo
        # Solo logear el error
        return {
            "success": False,
            "credits_deducted": 0,
            "error": str(e),
            "job_id": job_id
        }

async def deduct_credits_with_retry(
    user_id: str,
    images_count: int,
    processing_tier: str,
    job_id: str,
    successful_count: int = None,
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Deducir créditos con reintentos en caso de fallo

    Args:
        user_id: ID del usuario
        images_count: Número de imágenes procesadas
        processing_tier: "basic" o "premium"
        job_id: ID del job procesado
        successful_count: Número de imágenes exitosas
        max_retries: Número máximo de reintentos

    Returns:
        Dict con resultado de la deducción
    """

    for attempt in range(max_retries):
        result = await deduct_credits_for_processing(
            user_id=user_id,
            images_count=images_count,
            processing_tier=processing_tier,
            job_id=job_id,
            successful_count=successful_count
        )

        if result["success"]:
            if attempt > 0:
                logger.info(f"[DEDUCTION] Job {job_id}: Succeeded on attempt {attempt + 1}")
            return result

        if attempt < max_retries - 1:
            logger.warning(
                f"[DEDUCTION] Job {job_id}: Attempt {attempt + 1} failed, retrying..."
            )
            await asyncio.sleep(1)  # Esperar 1 segundo antes de reintentar

    logger.error(
        f"[DEDUCTION] Job {job_id}: ❌ Failed after {max_retries} attempts"
    )

    return result
