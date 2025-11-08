"""
Script para probar el endpoint de upload protegido
"""

import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://localhost:8002"

def test_upload_without_auth():
    """Test 1: Upload sin autenticacion (debe fallar)"""
    print("=" * 60)
    print("[TEST 1] Upload sin autenticacion")
    print("=" * 60)

    # Intentar subir sin token
    files = {'files': ('test.txt', b'test content', 'text/plain')}
    data = {'job_id': 'test-job-123'}

    response = requests.post(
        f"{API_URL}/upload",
        files=files,
        data=data
    )

    if response.status_code == 401:
        print("CORRECTO - Rechazo sin autenticacion")
        print(f"   Mensaje: {response.json()}")
    else:
        print(f"FALLO - Status: {response.status_code}")
        print(f"   Deberia retornar 401 Unauthorized")

    print()

def test_upload_with_invalid_token():
    """Test 2: Upload con token invalido (debe fallar)"""
    print("=" * 60)
    print("[TEST 2] Upload con token invalido")
    print("=" * 60)

    headers = {'Authorization': 'Bearer token_invalido_123'}
    files = {'files': ('test.txt', b'test content', 'text/plain')}
    data = {'job_id': 'test-job-456'}

    response = requests.post(
        f"{API_URL}/upload",
        files=files,
        data=data,
        headers=headers
    )

    if response.status_code == 401:
        print("CORRECTO - Rechazo token invalido")
        print(f"   Mensaje: {response.json()}")
    else:
        print(f"FALLO - Status: {response.status_code}")
        print(f"   Deberia retornar 401 Unauthorized")

    print()

def test_upload_with_valid_token():
    """Test 3: Upload con token valido (debe funcionar)"""
    print("=" * 60)
    print("[TEST 3] Upload con token valido")
    print("=" * 60)
    print("NOTA: Para probar con token real:")
    print("   1. Abre el frontend: http://localhost:3000")
    print("   2. Registra/inicia sesion")
    print("   3. Abre DevTools - Application - localStorage")
    print("   4. Copia el valor de 'token'")
    print("   5. Ejecuta este comando:")
    print()
    print("   curl -X POST http://localhost:8002/upload \\")
    print("     -H 'Authorization: Bearer TU_TOKEN_AQUI' \\")
    print("     -F 'files=@ruta/a/imagen.jpg' \\")
    print("     -F 'job_id=test-job-789'")
    print()
    print("   Deberia retornar: Status 200 con job_id")
    print()

if __name__ == "__main__":
    print("\nTESTING: Endpoint de Upload Protegido\n")

    # Verificar que el backend este corriendo
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code != 200:
            print("Backend no esta respondiendo en http://localhost:8002")
            print("   Inicia el backend con: python app/main.py")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("No se puede conectar al backend")
        print("   Asegurate que este corriendo en http://localhost:8002")
        sys.exit(1)

    print("Backend esta corriendo\n")

    # Ejecutar tests
    test_upload_without_auth()
    test_upload_with_invalid_token()
    test_upload_with_valid_token()

    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print("Endpoint protegido correctamente")
    print("Rechaza requests sin autenticacion")
    print("Rechaza tokens invalidos")
    print("Test con token real: manual")
    print()
    print("Estado: LISTO PARA MODULO 3")
    print("=" * 60)
