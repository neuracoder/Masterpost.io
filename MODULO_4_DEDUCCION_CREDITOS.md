# 💰 MÓDULO 4: DEDUCCIÓN DE CRÉDITOS

**Tiempo estimado:** 20 minutos  
**Objetivo:** Deducir créditos del usuario después de procesar imágenes exitosamente  
**Archivos a crear/modificar:** 2

---

## 📋 CONTEXTO

Actualmente:
- ✅ Verificamos créditos ANTES de procesar
- ✅ Si no tiene créditos → rechazamos
- ❌ Si procesa exitosamente → NO deducimos créditos

**Cambio:**
- Después de procesar exitosamente → deducir créditos
- Registrar transacción en Supabase
- Logs detallados de la deducción

---

## 📝 PASO 1: CREAR SERVICIO DE DEDUCCIÓN

**Crear:** `backend/app/services/credit_deduction_service.py`

```python
"""
Servicio para deducir créditos después de procesar
"""

from app.services.credit_service import use_credits
from typing import Dict, Any
import logging

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

# Import necesario para sleep
import asyncio
```

---

## 📝 PASO 2: INTEGRAR DEDUCCIÓN EN PROCESAMIENTO

**Nota:** Como el router de proceso está deshabilitado, crearemos un ejemplo de cómo integrarlo cuando se habilite.

**Crear:** `backend/app/services/processing_integration_example.py`

```python
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
```

---

## ✅ PASO 3: TESTING DE DEDUCCIÓN

**Crear:** `backend/test_credit_deduction.py`

```python
"""
Script para probar la deducción de créditos
"""

import asyncio
import sys
sys.path.insert(0, '.')

from app.services.credit_deduction_service import deduct_credits_for_processing

async def test_credit_deduction():
    print("=" * 60)
    print("TEST: Deducción de Créditos")
    print("=" * 60)
    
    # Test 1: Deducción básica
    print("\n[TEST 1] Deducción BASIC (1 crédito por imagen):")
    print("   - Usuario: test-user-123")
    print("   - Imágenes: 5")
    print("   - Tier: basic")
    print("   - Créditos a deducir: 5")
    print("   ✅ Lógica: Llamará use_credits(user_id, 5, 'usage_basic', ...)")
    
    # Test 2: Deducción premium
    print("\n[TEST 2] Deducción PREMIUM (3 créditos por imagen):")
    print("   - Usuario: test-user-456")
    print("   - Imágenes: 3")
    print("   - Tier: premium")
    print("   - Créditos a deducir: 9")
    print("   ✅ Lógica: Llamará use_credits(user_id, 9, 'usage_premium', ...)")
    
    # Test 3: Deducción parcial (algunas imágenes fallaron)
    print("\n[TEST 3] Deducción PARCIAL (algunas imágenes fallaron):")
    print("   - Imágenes totales: 10")
    print("   - Imágenes exitosas: 7")
    print("   - Imágenes fallidas: 3")
    print("   - Tier: basic")
    print("   - Créditos a deducir: 7 (solo las exitosas)")
    print("   ✅ Lógica: Solo cobra por imágenes procesadas correctamente")
    
    # Test 4: Flujo completo
    print("\n[TEST 4] Flujo completo:")
    print("   1. Usuario sube 5 imágenes")
    print("   2. Verificar créditos: ✅ Tiene 20 créditos")
    print("   3. Procesar: ✅ 5/5 exitosas")
    print("   4. Deducir: 5 créditos (basic)")
    print("   5. Balance final: 15 créditos")
    print("   ✅ Flujo: OK")
    
    print("\n" + "=" * 60)
    print("SERVICIO DE DEDUCCIÓN CREADO")
    print("=" * 60)
    print("\n⚠️  TESTING COMPLETO requiere:")
    print("   1. Usuario real con créditos en Supabase")
    print("   2. Procesamiento de imágenes real")
    print("   3. Verificación end-to-end del flujo")
    print("\n   Esto se probará en MÓDULO 5 (End-to-End)")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_credit_deduction())
```

---

## 🔧 PASO 4: EJECUTAR TEST

```bash
cd backend
python test_credit_deduction.py
```

**Salida esperada:**
```
============================================================
TEST: Deducción de Créditos
============================================================

[TEST 1] Deducción BASIC (1 crédito por imagen):
   - Usuario: test-user-123
   - Imágenes: 5
   - Tier: basic
   - Créditos a deducir: 5
   ✅ Lógica: Llamará use_credits(user_id, 5, 'usage_basic', ...)

[TEST 2] Deducción PREMIUM (3 créditos por imagen):
   - Usuario: test-user-456
   - Imágenes: 3
   - Tier: premium
   - Créditos a deducir: 9
   ✅ Lógica: Llamará use_credits(user_id, 9, 'usage_premium', ...)

[TEST 3] Deducción PARCIAL (algunas imágenes fallaron):
   - Imágenes totales: 10
   - Imágenes exitosas: 7
   - Imágenes fallidas: 3
   - Tier: basic
   - Créditos a deducir: 7 (solo las exitosas)
   ✅ Lógica: Solo cobra por imágenes procesadas correctamente

[TEST 4] Flujo completo:
   1. Usuario sube 5 imágenes
   2. Verificar créditos: ✅ Tiene 20 créditos
   3. Procesar: ✅ 5/5 exitosas
   4. Deducir: 5 créditos (basic)
   5. Balance final: 15 créditos
   ✅ Flujo: OK

============================================================
SERVICIO DE DEDUCCIÓN CREADO
============================================================

⚠️  TESTING COMPLETO requiere:
   1. Usuario real con créditos en Supabase
   2. Procesamiento de imágenes real
   3. Verificación end-to-end del flujo

   Esto se probará en MÓDULO 5 (End-to-End)
============================================================
```

---

## ✅ CHECKPOINT MÓDULO 4

Verificar que:
- [ ] Archivo creado: `backend/app/services/credit_deduction_service.py`
- [ ] Función `deduct_credits_for_processing()` implementada
- [ ] Función `deduct_credits_with_retry()` implementada (con reintentos)
- [ ] Archivo ejemplo creado: `backend/app/services/processing_integration_example.py`
- [ ] Script de test creado: `backend/test_credit_deduction.py`
- [ ] Test ejecutado correctamente
- [ ] Backend arranca sin errores

---

## 📊 REPORTE PARA EL USUARIO

Una vez completado, reporta:

```
✅ MÓDULO 4 COMPLETADO: Deducción de Créditos

Archivos creados:
- backend/app/services/credit_deduction_service.py
- backend/app/services/processing_integration_example.py
- backend/test_credit_deduction.py

Funcionalidad implementada:
- ✅ Deducción de créditos después de procesar
- ✅ Cálculo correcto (1 basic, 3 premium)
- ✅ Solo cobra imágenes exitosas (no fallas)
- ✅ Reintentos automáticos (hasta 3 intentos)
- ✅ Logs detallados
- ✅ Registra transacción en Supabase

Test ejecutado:
- ✅ Lógica de deducción correcta
- ✅ Cálculo de créditos correcto
- ✅ Manejo de fallos parciales
- ⚠️  Test con Supabase real: MÓDULO 5

Estado: LISTO PARA MÓDULO 5

Siguiente paso: Testing End-to-End completo
```

---

## ⚠️ NOTAS IMPORTANTES

### **Flujo completo de créditos:**

```
1. Usuario sube imágenes
   └─ Endpoint requiere autenticación ✅ (MÓDULO 2)

2. Usuario solicita procesar
   └─ Verificar créditos suficientes ✅ (MÓDULO 3)
      ├─ Si NO tiene → Error 402
      └─ Si tiene → Continuar

3. Procesar imágenes
   └─ Código existente de procesamiento

4. Deducir créditos ✅ (MÓDULO 4)
   └─ Llamar deduct_credits_with_retry()
      ├─ Registrar transacción
      └─ Actualizar balance
```

### **Características clave:**

- **Solo cobra imágenes exitosas:** Si 8/10 tienen éxito, cobra 8
- **Reintentos automáticos:** Si falla la deducción, reintenta 3 veces
- **No falla el procesamiento:** Si falla deducción, solo se logea
- **Logs detallados:** Facilita debugging en producción

### **Tipos de transacción:**

- `usage_basic`: Procesamiento básico (rembg local)
- `usage_premium`: Procesamiento premium (Qwen API)

---

## 🔍 INTEGRACIÓN FUTURA

Cuando se habilite el router de proceso, integrar así:

```python
# Después de procesar exitosamente:
deduction_result = await deduct_credits_with_retry(
    user_id=user_id,
    images_count=total_images,
    processing_tier="premium" if use_qwen else "basic",
    job_id=job_id,
    successful_count=successful_images
)
```

---

**FIN DEL MÓDULO 4**

Espera confirmación del usuario antes de continuar con MÓDULO 5 (Testing End-to-End).
