#!/usr/bin/env python3
"""
Script para verificar que todas las variables de entorno esten configuradas correctamente
"""
import os
from pathlib import Path

def check_env_file(filepath, required_vars):
    """Verifica que un archivo .env contenga las variables requeridas"""
    print(f"\n{'='*70}")
    print(f"Verificando: {filepath}")
    print('='*70)
    
    if not os.path.exists(filepath):
        print(f"❌ ERROR: Archivo no encontrado: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing = []
    placeholder = []
    configured = []
    
    for var in required_vars:
        if var not in content:
            missing.append(var)
        else:
            # Extraer valor
            for line in content.split('\n'):
                if line.startswith(var):
                    value = line.split('=', 1)[1].strip() if '=' in line else ''
                    
                    # Verificar si es placeholder
                    if any(x in value.lower() for x in ['pendiente', 'tu_', 'your_', 'aqui', 'xxxxx']):
                        placeholder.append(var)
                    elif value:
                        configured.append(var)
                    else:
                        placeholder.append(var)
                    break
    
    print(f"\n✅ Configuradas: {len(configured)}/{len(required_vars)}")
    for var in configured:
        print(f"   ✓ {var}")
    
    if placeholder:
        print(f"\n⚠️  Pendientes de configurar: {len(placeholder)}")
        for var in placeholder:
            print(f"   ! {var}")
    
    if missing:
        print(f"\n❌ Faltantes: {len(missing)}")
        for var in missing:
            print(f"   ✗ {var}")
    
    return len(missing) == 0 and len(placeholder) == 0

# Variables requeridas por archivo
BACKEND_REQUIRED = [
    'PORT',
    'ENVIRONMENT',
    'SUPABASE_URL',
    'SUPABASE_ANON_KEY',
    'SUPABASE_SERVICE_ROLE_KEY',
    'JWT_SECRET',
    'STRIPE_SECRET_KEY',
    'STRIPE_PUBLISHABLE_KEY',
    'STRIPE_PRICE_PRO',
    'STRIPE_PRICE_BUSINESS',
    'QWEN_API_KEY',
    'DASHSCOPE_API_KEY',
    'FRONTEND_URL',
    'BACKEND_URL',
]

FRONTEND_REQUIRED = [
    'NEXT_PUBLIC_API_URL',
    'NEXT_PUBLIC_SUPABASE_URL',
    'NEXT_PUBLIC_SUPABASE_ANON_KEY',
    'NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY',
]

print("\n" + "="*70)
print("  VERIFICACION DE CONFIGURACION - MASTERPOST.IO")
print("="*70)

# Verificar backend
backend_ok = check_env_file('backend/.env', BACKEND_REQUIRED)

# Verificar frontend development
frontend_dev_ok = check_env_file('.env.development', FRONTEND_REQUIRED)

# Verificar frontend local
frontend_local_ok = check_env_file('.env.local', FRONTEND_REQUIRED)

# Resumen final
print("\n" + "="*70)
print("  RESUMEN FINAL")
print("="*70)

all_ok = backend_ok and frontend_dev_ok and frontend_local_ok

if all_ok:
    print("\n🎉 ¡EXCELENTE! Todas las configuraciones estan completas.")
    print("   Puedes iniciar el sistema con:")
    print("   - Backend: cd backend && python app/main.py")
    print("   - Frontend: npm run dev")
else:
    print("\n⚠️  HAY CLAVES PENDIENTES DE CONFIGURAR")
    print("   Lee el archivo: CONFIGURAR_CLAVES_PENDIENTES.md")
    print("   Para instrucciones detalladas.")

print("\n" + "="*70 + "\n")
