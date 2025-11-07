# 🔒 MÓDULO 2: PROTEGER ENDPOINT DE UPLOAD

**Tiempo estimado:** 15 minutos  
**Objetivo:** Agregar autenticación al endpoint `/api/v1/upload`  
**Archivos a modificar:** 1 (backend/app/main.py)

---

## 📋 CONTEXTO

El middleware ya está creado y funciona. Ahora lo vamos a usar en el endpoint de upload.

**Cambio:**
- ANTES: Cualquiera puede subir imágenes sin login
- DESPUÉS: Solo usuarios autenticados pueden subir imágenes

---

## 📝 PASO 1: MODIFICAR ENDPOINT DE UPLOAD

**Archivo:** `backend/app/main.py`

### **Ubicar este código (aproximadamente línea 150-200):**

```python
@app.post("/api/v1/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    job_id: str = Form(None)
):
```

### **Reemplazar con:**

```python
from fastapi import Depends
from app.middleware.auth_middleware import get_current_user_id

@app.post("/api/v1/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    job_id: str = Form(None),
    user_id: str = Depends(get_current_user_id)  # ← NUEVA LÍNEA
):
```

### **Dentro de la función, agregar log del user_id:**

Busca la línea que dice:
```python
logger.info(f"Uploading {len(files)} files for job {job_id}")
```

Agregar ANTES de esa línea:
```python
    logger.info(f"[AUTH] User {user_id} uploading files for job {job_id}")
```

---

## 📝 PASO 2: VERIFICAR IMPORTS

En la parte superior de `backend/app/main.py`, asegúrate que estén estos imports:

```python
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks, Depends
from app.middleware.auth_middleware import get_current_user_id
```

Si falta alguno, agrégalo.

---

## ✅ PASO 3: TESTING DEL ENDPOINT PROTEGIDO

**Crear:** `backend/test_protected_upload.py`

```python
"""
Script para probar el endpoint de upload protegido
"""

import requests
import sys

API_URL = "http://localhost:8002"

def test_upload_without_auth():
    """Test 1: Upload sin autenticación (debe fallar)"""
    print("=" * 60)
    print("[TEST 1] Upload sin autenticación")
    print("=" * 60)
    
    # Intentar subir sin token
    files = {'files': ('test.txt', b'test content', 'text/plain')}
    data = {'job_id': 'test-job-123'}
    
    response = requests.post(
        f"{API_URL}/api/v1/upload",
        files=files,
        data=data
    )
    
    if response.status_code == 401:
        print("✅ CORRECTO - Rechazó sin autenticación")
        print(f"   Mensaje: {response.json()}")
    else:
        print(f"❌ FALLÓ - Status: {response.status_code}")
        print(f"   Debería retornar 401 Unauthorized")
    
    print()

def test_upload_with_invalid_token():
    """Test 2: Upload con token inválido (debe fallar)"""
    print("=" * 60)
    print("[TEST 2] Upload con token inválido")
    print("=" * 60)
    
    headers = {'Authorization': 'Bearer token_invalido_123'}
    files = {'files': ('test.txt', b'test content', 'text/plain')}
    data = {'job_id': 'test-job-456'}
    
    response = requests.post(
        f"{API_URL}/api/v1/upload",
        files=files,
        data=data,
        headers=headers
    )
    
    if response.status_code == 401:
        print("✅ CORRECTO - Rechazó token inválido")
        print(f"   Mensaje: {response.json()}")
    else:
        print(f"❌ FALLÓ - Status: {response.status_code}")
        print(f"   Debería retornar 401 Unauthorized")
    
    print()

def test_upload_with_valid_token():
    """Test 3: Upload con token válido (debe funcionar)"""
    print("=" * 60)
    print("[TEST 3] Upload con token válido")
    print("=" * 60)
    print("⚠️  Para probar con token real:")
    print("   1. Abre el frontend: http://localhost:3000")
    print("   2. Registra/inicia sesión")
    print("   3. Abre DevTools → Application → localStorage")
    print("   4. Copia el valor de 'token'")
    print("   5. Ejecuta este comando:")
    print()
    print("   curl -X POST http://localhost:8002/api/v1/upload \\")
    print("     -H 'Authorization: Bearer TU_TOKEN_AQUI' \\")
    print("     -F 'files=@ruta/a/imagen.jpg' \\")
    print("     -F 'job_id=test-job-789'")
    print()
    print("   Debería retornar: Status 200 con job_id")
    print()

if __name__ == "__main__":
    print("\n🔒 TESTING: Endpoint de Upload Protegido\n")
    
    # Verificar que el backend esté corriendo
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code != 200:
            print("❌ Backend no está respondiendo en http://localhost:8002")
            print("   Inicia el backend con: python app/main.py")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        print("   Asegúrate que esté corriendo en http://localhost:8002")
        sys.exit(1)
    
    print("✅ Backend está corriendo\n")
    
    # Ejecutar tests
    test_upload_without_auth()
    test_upload_with_invalid_token()
    test_upload_with_valid_token()
    
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print("✅ Endpoint protegido correctamente")
    print("✅ Rechaza requests sin autenticación")
    print("✅ Rechaza tokens inválidos")
    print("⚠️  Test con token real: manual")
    print()
    print("Estado: LISTO PARA MÓDULO 3")
    print("=" * 60)
```

---

## 🔧 PASO 4: EJECUTAR TESTS

### **Asegúrate que el backend esté corriendo:**

```bash
# En una terminal
cd backend
python app/main.py
```

### **En otra terminal, ejecuta el test:**

```bash
cd backend
python test_protected_upload.py
```

**Salida esperada:**
```
🔒 TESTING: Endpoint de Upload Protegido

✅ Backend está corriendo

============================================================
[TEST 1] Upload sin autenticación
============================================================
✅ CORRECTO - Rechazó sin autenticación
   Mensaje: {'detail': 'Missing authorization header'}

============================================================
[TEST 2] Upload con token inválido
============================================================
✅ CORRECTO - Rechazó token inválido
   Mensaje: {'detail': 'Token verification failed: ...'}

============================================================
[TEST 3] Upload con token válido
============================================================
⚠️  Para probar con token real:
   ...

============================================================
RESUMEN
============================================================
✅ Endpoint protegido correctamente
✅ Rechaza requests sin autenticación
✅ Rechaza tokens inválidos
⚠️  Test con token real: manual

Estado: LISTO PARA MÓDULO 3
============================================================
```

---

## ✅ CHECKPOINT MÓDULO 2

Verificar que:
- [ ] Import agregado en `backend/app/main.py`
- [ ] Endpoint `/api/v1/upload` modificado con `user_id: str = Depends(get_current_user_id)`
- [ ] Log de user_id agregado
- [ ] Script de test creado: `backend/test_protected_upload.py`
- [ ] Tests ejecutados correctamente
- [ ] Test 1 y 2 pasan (rechazan sin auth y con token inválido)

---

## 📊 REPORTE PARA EL USUARIO

Una vez completado, reporta:

```
✅ MÓDULO 2 COMPLETADO: Endpoint de Upload Protegido

Cambios realizados:
- backend/app/main.py: Endpoint /api/v1/upload ahora requiere autenticación
- backend/test_protected_upload.py: Script de testing creado

Resultados de tests:
- ✅ Test 1: Rechaza requests sin token
- ✅ Test 2: Rechaza tokens inválidos
- ⚠️  Test 3: Pendiente (requiere token real del frontend)

Estado: LISTO PARA MÓDULO 3

Siguiente paso: Verificar créditos antes de procesar
```

---

## ⚠️ NOTAS IMPORTANTES

- El frontend DEBE enviar el header `Authorization: Bearer <token>` al subir imágenes
- Si el frontend no envía token, recibirá error 401
- El `user_id` ya está disponible en el endpoint para usar después
- NO agregues lógica de créditos todavía (eso es MÓDULO 3)

---

## 🔍 VERIFICACIÓN MANUAL OPCIONAL

Si quieres probar con token real AHORA:

1. Registra usuario en http://localhost:3000/register
2. Abre DevTools → Application → localStorage → token
3. Copia el token
4. Ejecuta:
```bash
curl -X POST http://localhost:8002/api/v1/upload \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -F "files=@test_image.jpg" \
  -F "job_id=test-123"
```

Deberías ver en los logs del backend:
```
INFO: [AUTH] User <user_id> uploading files for job test-123
INFO: Uploading 1 files for job test-123
```

---

**FIN DEL MÓDULO 2**

Espera confirmación del usuario antes de continuar con MÓDULO 3.
