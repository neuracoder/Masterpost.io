"""
Ejemplo de cómo integrar la deducción de créditos en el procesamiento
Este archivo es solo de referencia para cuando se habilite el router de proceso
"""

from app.services.credit_verification_service import verify_credits
from app.services.credit_deduction_service import deduct_credits_with_retry
import logging

logger = logging.getLogger(__name__)

async def process_images_with_credits(
    user_id: str,
    job_id: str,
    images_count: int,
    processing_tier: str,
    # ... otros parámetros del procesamiento ...
):
    """
    Flujo completo: Verificar → Procesar → Deducir

    Este es un EJEMPLO de cómo debe ser el flujo cuando se integre
    """

    # ============================================================
    # PASO 1: VERIFICAR CRÉDITOS (MÓDULO 3)
    # ============================================================
    logger.info(f"[PROCESS] Step 1/3: Verifying credits for job {job_id}")

    try:
        credit_check = await verify_credits(
            user_id=user_id,
            images_count=images_count,
            processing_tier=processing_tier
        )

        logger.info(f"[PROCESS] ✅ Credits verified: {credit_check}")

    except Exception as e:
        logger.error(f"[PROCESS] ❌ Credit verification failed: {e}")
        raise

    # ============================================================
    # PASO 2: PROCESAR IMÁGENES (código existente)
    # ============================================================
    logger.info(f"[PROCESS] Step 2/3: Processing {images_count} images")

    # Aquí iría el código de procesamiento actual
    # Por ejemplo:
    # processing_result = await process_job(job_id, ...)

    # Simulación de resultado:
    processing_result = {
        "success": True,
        "images_processed": images_count,
        "images_successful": images_count,  # O menos si algunas fallaron
        "images_failed": 0
    }

    logger.info(f"[PROCESS] ✅ Processing completed: {processing_result}")

    # ============================================================
    # PASO 3: DEDUCIR CRÉDITOS (MÓDULO 4)
    # ============================================================
    logger.info(f"[PROCESS] Step 3/3: Deducting credits")

    if processing_result["success"]:
        try:
            deduction_result = await deduct_credits_with_retry(
                user_id=user_id,
                images_count=images_count,
                processing_tier=processing_tier,
                job_id=job_id,
                successful_count=processing_result["images_successful"]
            )

            logger.info(f"[PROCESS] ✅ Credits deducted: {deduction_result}")

            # Agregar info de créditos al resultado
            processing_result["credits_info"] = deduction_result

        except Exception as e:
            # No fallar el procesamiento si falla la deducción
            # Solo logear el error
            logger.error(f"[PROCESS] ⚠️  Credit deduction failed: {e}")
            processing_result["credits_info"] = {
                "success": False,
                "error": str(e)
            }

    # ============================================================
    # RETORNAR RESULTADO COMPLETO
    # ============================================================
    return processing_result

# ============================================================
# EJEMPLO DE INTEGRACIÓN EN ENDPOINT
# ============================================================

"""
@router.post("/api/v1/process")
async def process_images_endpoint(
    request: ProcessRequest,
    user_id: str = Depends(get_current_user_id)
):
    result = await process_images_with_credits(
        user_id=user_id,
        job_id=request.job_id,
        images_count=request.images_count,
        processing_tier="premium" if request.enable_premium else "basic"
    )

    return {
        "job_id": request.job_id,
        "status": "completed" if result["success"] else "failed",
        "images_processed": result["images_successful"],
        "credits_deducted": result["credits_info"].get("credits_deducted", 0),
        "credits_remaining": result["credits_info"].get("credits_remaining", 0)
    }
"""
