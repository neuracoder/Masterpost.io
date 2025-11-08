"""
Script para probar el middleware de autenticacion
"""

import asyncio
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '.')

from app.middleware.auth_middleware import verify_token

async def test_middleware():
    print("=" * 60)
    print("TEST: Middleware de Autenticacion")
    print("=" * 60)

    # Test 1: Sin token
    print("\n[TEST 1] Sin token:")
    try:
        await verify_token(None)
        print("FALLO - Deberia rechazar sin token")
    except Exception as e:
        print(f"CORRECTO - Rechazo: {e.detail}")

    # Test 2: Token invalido
    print("\n[TEST 2] Token invalido:")
    try:
        await verify_token("Bearer token_falso_123")
        print("FALLO - Deberia rechazar token invalido")
    except Exception as e:
        print(f"CORRECTO - Rechazo: {e.detail}")

    # Test 3: Token real (necesitas obtener uno)
    print("\n[TEST 3] Token real:")
    print("NOTA: Para probar con token real:")
    print("   1. Registra un usuario en http://localhost:3000/register")
    print("   2. Copia el token de localStorage")
    print("   3. Ejecuta: await verify_token('Bearer <tu_token>')")
    print("   4. Deberia retornar el user_id")

    print("\n" + "=" * 60)
    print("MIDDLEWARE CREADO - Listo para usar")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_middleware())
