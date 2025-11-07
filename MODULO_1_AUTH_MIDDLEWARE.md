# 🔐 MÓDULO 1: MIDDLEWARE DE AUTENTICACIÓN

**Tiempo estimado:** 30 minutos  
**Objetivo:** Crear función para verificar tokens JWT y extraer user_id  
**Archivos a modificar:** 1

---

## 📋 CONTEXTO

Actualmente el endpoint `/api/v1/process` permite procesar imágenes sin autenticación.
Necesitamos crear un middleware que:
1. Verifique que haya token en el header `Authorization`
2. Valide el token con Supabase
3. Extraiga el `user_id` del token
4. Lo pase al endpoint

---

## 📝 PASO 1: CREAR ARCHIVO DE MIDDLEWARE

**Crear:** `backend/app/middleware/auth_middleware.py`

```python
"""
Middleware de autenticación para endpoints protegidos
"""

from fastapi import Header, HTTPException, status
from typing import Optional
import os
from app.database.supabase_client import supabase

async def verify_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Verifica el token JWT y retorna el user_id
    
    Args:
        authorization: Header Authorization con formato "Bearer <token>"
        
    Returns:
        user_id: ID del usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o falta
    """
    
    # 1. Verificar que existe el header
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    # 2. Extraer token (formato: "Bearer <token>")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    # 3. Verificar token con Supabase
    try:
        response = supabase.auth.get_user(token)
        
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        # 4. Retornar user_id
        return response.user.id
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}"
        )


async def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Dependency para obtener user_id en endpoints
    Alias de verify_token para usar con Depends()
    """
    return await verify_token(authorization)
```

---

## 📝 PASO 2: CREAR __init__.py

**Crear:** `backend/app/middleware/__init__.py`

```python
from .auth_middleware import verify_token, get_current_user_id

__all__ = ['verify_token', 'get_current_user_id']
```

---

## ✅ PASO 3: TESTING DEL MIDDLEWARE

**Crear:** `backend/test_auth_middleware.py`

```python
"""
Script para probar el middleware de autenticación
"""

import asyncio
import sys
sys.path.insert(0, '.')

from app.middleware.auth_middleware import verify_token

async def test_middleware():
    print("=" * 60)
    print("TEST: Middleware de Autenticación")
    print("=" * 60)
    
    # Test 1: Sin token
    print("\n[TEST 1] Sin token:")
    try:
        await verify_token(None)
        print("❌ FALLÓ - Debería rechazar sin token")
    except Exception as e:
        print(f"✅ CORRECTO - Rechazó: {e.detail}")
    
    # Test 2: Token inválido
    print("\n[TEST 2] Token inválido:")
    try:
        await verify_token("Bearer token_falso_123")
        print("❌ FALLÓ - Debería rechazar token inválido")
    except Exception as e:
        print(f"✅ CORRECTO - Rechazó: {e.detail}")
    
    # Test 3: Token real (necesitas obtener uno)
    print("\n[TEST 3] Token real:")
    print("⚠️  Para probar con token real:")
    print("   1. Registra un usuario en http://localhost:3000/register")
    print("   2. Copia el token de localStorage")
    print("   3. Ejecuta: await verify_token('Bearer <tu_token>')")
    print("   4. Debería retornar el user_id")
    
    print("\n" + "=" * 60)
    print("MIDDLEWARE CREADO - Listo para usar")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_middleware())
```

---

## 🔧 PASO 4: EJECUTAR TEST

```bash
cd backend
python test_auth_middleware.py
```

**Salida esperada:**
```
============================================================
TEST: Middleware de Autenticación
============================================================

[TEST 1] Sin token:
✅ CORRECTO - Rechazó: Missing authorization header

[TEST 2] Token inválido:
✅ CORRECTO - Rechazó: Token verification failed: ...

[TEST 3] Token real:
⚠️  Para probar con token real:
   1. Registra un usuario en http://localhost:3000/register
   2. Copia el token de localStorage
   3. Ejecuta: await verify_token('Bearer <tu_token>')
   4. Debería retornar el user_id

============================================================
MIDDLEWARE CREADO - Listo para usar
============================================================
```

---

## ✅ CHECKPOINT MÓDULO 1

Verificar que:
- [ ] Archivo `backend/app/middleware/auth_middleware.py` creado
- [ ] Archivo `backend/app/middleware/__init__.py` creado
- [ ] Script de test ejecutado sin errores
- [ ] Test 1 y 2 pasan correctamente (rechazan sin token y con token inválido)

---

## 📊 REPORTE PARA EL USUARIO

Una vez completado, reporta:

```
✅ MÓDULO 1 COMPLETADO: Middleware de Autenticación

Archivos creados:
- backend/app/middleware/auth_middleware.py
- backend/app/middleware/__init__.py
- backend/test_auth_middleware.py

Funciones disponibles:
- verify_token() - Verifica token y retorna user_id
- get_current_user_id() - Dependency para FastAPI

Estado: LISTO PARA USAR EN MÓDULO 2

Siguiente paso: Proteger endpoint de upload
```

---

## ⚠️ NOTAS IMPORTANTES

- NO modifiques otros archivos en este módulo
- NO agregues el middleware a ningún endpoint todavía
- Solo crea las funciones y prueba que funcionan
- El test completo con token real se hará en MÓDULO 5

---

**FIN DEL MÓDULO 1**

Espera confirmación del usuario antes de continuar con MÓDULO 2.
