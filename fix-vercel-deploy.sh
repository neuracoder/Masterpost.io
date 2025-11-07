#!/bin/bash

# ================================================================
# Script de Auto-Fix para Despliegue en Vercel
# ================================================================
# 
# Este script automatiza la solución del problema de dependencias
# faltantes que está causando el fallo en Vercel.
#
# Uso: 
#   bash fix-vercel-deploy.sh
#
# ================================================================

echo "=================================================="
echo "🔧 MASTERPOST.IO - Fix Vercel Deployment"
echo "=================================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar que estamos en la raíz del proyecto
if [ ! -f "package.json" ]; then
    print_error "No se encontró package.json en el directorio actual"
    print_info "Por favor, ejecuta este script desde la raíz del proyecto Masterpost-SaaS"
    exit 1
fi

print_success "Directorio correcto detectado"
echo ""

# Paso 1: Backup del package.json actual
echo "=================================================="
echo "📦 Paso 1: Backup de package.json actual"
echo "=================================================="

if [ -f "package.json" ]; then
    cp package.json package.json.backup
    print_success "Backup creado: package.json.backup"
else
    print_warning "No se encontró package.json existente"
fi
echo ""

# Paso 2: Crear nuevo package.json con todas las dependencias
echo "=================================================="
echo "📝 Paso 2: Actualizando package.json"
echo "=================================================="

cat > package.json << 'EOF'
{
  "name": "masterpost-saas",
  "version": "2.1.0",
  "description": "Professional Image Processing SaaS for E-commerce",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "dependencies": {
    "next": "14.2.32",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "typescript": "^5.3.0",
    "@types/node": "^20.10.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "@radix-ui/react-slider": "^1.2.0",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-switch": "^1.0.3",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-toast": "^1.1.5",
    "@radix-ui/react-tooltip": "^1.0.7",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-progress": "^1.0.3",
    "lucide-react": "^0.263.1",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "geist": "^1.2.0",
    "@vercel/analytics": "^1.1.0",
    "axios": "^1.6.0",
    "stripe": "^14.9.0",
    "zustand": "^4.4.0"
  },
  "devDependencies": {
    "@types/eslint": "^8.56.0",
    "eslint": "^8.57.1",
    "eslint-config-next": "14.2.32",
    "@typescript-eslint/parser": "^6.13.0",
    "@typescript-eslint/eslint-plugin": "^6.13.0",
    "prettier": "^3.1.0",
    "prettier-plugin-tailwindcss": "^0.5.9"
  }
}
EOF

print_success "package.json actualizado con todas las dependencias"
echo ""

# Paso 3: Mostrar diferencias
echo "=================================================="
echo "🔍 Paso 3: Dependencias agregadas"
echo "=================================================="

print_info "Las siguientes dependencias han sido agregadas:"
echo ""
echo "  • @radix-ui/react-slider (UI components)"
echo "  • geist (Vercel fonts)"
echo "  • @vercel/analytics (Analytics)"
echo "  • Otras dependencias de Radix UI"
echo ""

# Paso 4: Verificar Git
echo "=================================================="
echo "🔧 Paso 4: Verificación de Git"
echo "=================================================="

if ! command -v git &> /dev/null; then
    print_error "Git no está instalado"
    print_info "Instala Git y vuelve a ejecutar este script"
    exit 1
fi

print_success "Git detectado"

# Verificar que estamos en un repositorio Git
if [ ! -d ".git" ]; then
    print_error "Este directorio no es un repositorio Git"
    print_info "Inicializa Git con: git init"
    exit 1
fi

print_success "Repositorio Git detectado"
echo ""

# Paso 5: Verificar estado de Git
echo "=================================================="
echo "📊 Paso 5: Estado actual de Git"
echo "=================================================="

git status --short
echo ""

# Paso 6: Commit y Push
echo "=================================================="
echo "💾 Paso 6: Commit y Push"
echo "=================================================="

read -p "¿Deseas hacer commit y push de los cambios? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    print_info "Agregando cambios..."
    git add package.json
    
    print_info "Creando commit..."
    git commit -m "fix: Add missing dependencies for Vercel deployment

- Added @radix-ui/react-slider
- Added geist fonts
- Added @vercel/analytics
- Fixed build errors in Vercel deployment"
    
    if [ $? -eq 0 ]; then
        print_success "Commit creado exitosamente"
        
        print_info "Pusheando a repositorio remoto..."
        git push
        
        if [ $? -eq 0 ]; then
            print_success "Push exitoso!"
            echo ""
            print_success "✨ Vercel detectará automáticamente el cambio y volverá a deployar"
        else
            print_error "Error al hacer push"
            print_info "Intenta manualmente: git push"
        fi
    else
        print_error "Error al crear commit"
        print_info "Verifica los cambios con: git status"
    fi
else
    print_warning "Commit cancelado"
    print_info "Puedes hacer el commit manualmente:"
    echo ""
    echo "  git add package.json"
    echo "  git commit -m \"fix: Add missing dependencies for Vercel\""
    echo "  git push"
fi

echo ""

# Paso 7: Verificación local (opcional)
echo "=================================================="
echo "🧪 Paso 7: Verificación local (opcional)"
echo "=================================================="

read -p "¿Deseas verificar el build localmente? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    print_info "Instalando dependencias..."
    npm install
    
    if [ $? -eq 0 ]; then
        print_success "Dependencias instaladas"
        
        print_info "Ejecutando build..."
        npm run build
        
        if [ $? -eq 0 ]; then
            print_success "Build local exitoso! ✨"
            echo ""
            print_success "El proyecto debería deployarse correctamente en Vercel"
        else
            print_error "Build local falló"
            print_info "Revisa los errores arriba"
        fi
    else
        print_error "Error al instalar dependencias"
    fi
else
    print_info "Verificación local omitida"
fi

echo ""

# Resumen final
echo "=================================================="
echo "📋 Resumen"
echo "=================================================="
echo ""
print_info "Archivos modificados:"
echo "  • package.json (backup en package.json.backup)"
echo ""
print_info "Próximos pasos:"
echo "  1. Espera 2-3 minutos a que Vercel complete el deploy"
echo "  2. Verifica en: https://vercel.com/tu-usuario/masterpost-io"
echo "  3. Revisa que el build termine exitosamente (✅ verde)"
echo ""
print_info "Monitoreo en tiempo real:"
echo "  vercel logs --follow"
echo ""

# Enlaces útiles
echo "=================================================="
echo "🔗 Enlaces Útiles"
echo "=================================================="
echo ""
echo "  📊 Dashboard Vercel:"
echo "     https://vercel.com/dashboard"
echo ""
echo "  📝 Logs de Deployment:"
echo "     https://vercel.com/tu-usuario/masterpost-io/deployments"
echo ""
echo "  📖 Documentación:"
echo "     https://nextjs.org/docs"
echo ""

print_success "Script completado! 🎉"
echo ""
