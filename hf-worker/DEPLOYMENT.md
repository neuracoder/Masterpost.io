# Deployment Guide - Hugging Face Spaces

## Pre-requisitos

- Cuenta en https://huggingface.co
- Git instalado localmente
- Variables de entorno listas (ver ENV_SETUP.md)

## Paso 1: Crear Space en Hugging Face

1. Ir a https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Configurar:
   - **Name**: `masterpost-worker`
   - **License**: `other` (o el que prefieras)
   - **SDK**: `Docker`
   - **Hardware**: `CPU basic` (16GB RAM) - **FREE**
   - **Visibility**: `Private` (recomendado)
4. Click **"Create Space"**

## Paso 2: Configurar Variables de Entorno

1. En el Space creado, ir a **Settings**
2. Scroll down a **"Repository secrets"**
3. Agregar las siguientes variables (una por una):

```bash
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...
ALLOWED_ORIGINS=https://masterpost-io.netlify.app
```

4. Click **"Save"** después de cada una

## Paso 3: Deploy Local → HF

Desde la carpeta `hf-worker/`:

```bash
# 1. Inicializar git (si no existe)
git init

# 2. Agregar todos los archivos
git add .

# 3. Commit inicial
git commit -m "Initial commit: Masterpost Worker"

# 4. Agregar remote de HF (reemplaza USERNAME con tu usuario)
git remote add hf https://huggingface.co/spaces/USERNAME/masterpost-worker

# 5. Push a HF
git push hf main
```

Si te pide credenciales:
- Username: tu usuario de HuggingFace
- Password: usa un **Access Token** (Settings > Access Tokens)

## Paso 4: Monitorear el Build

1. En la página del Space, verás **"Building..."**
2. Click en **"Show build logs"** para ver el progreso
3. El build tomará **3-5 minutos**:
   - Descarga Python 3.11
   - Instala dependencias (rembg, FastAPI, etc)
   - Descarga modelo U2-Net (~180MB)
   - Inicia el servidor

## Paso 5: Verificar Deployment

Una vez que el build termine:

```bash
# 1. Test health endpoint
curl https://USERNAME-masterpost-worker.hf.space/health

# Debe retornar:
{
  "status": "healthy",
  "local_processing": true,
  "manual_editor": "available",
  "timestamp": 1699380000
}

# 2. Test API docs
# Abrir en navegador:
https://USERNAME-masterpost-worker.hf.space/docs
```

## Paso 6: Integrar con Frontend

En tu frontend (Netlify), actualiza la API URL:

```javascript
// Antes:
const API_URL = "http://localhost:8002"

// Después:
const API_URL = "https://USERNAME-masterpost-worker.hf.space"
```

## Updates Futuros

Para actualizar el worker:

```bash
# 1. Hacer cambios locales
# 2. Commit
git add .
git commit -m "Update: descripción de los cambios"

# 3. Push a HF
git push hf main

# HF rebuildeará automáticamente (~3-5 min)
```

## Troubleshooting

### Build failed: "Permission denied"
- Verifica que el Dockerfile use `USER user`
- Verifica que todos los COPY tengan `--chown=user:user`

### Build failed: "Port 7860 already in use"
- No modificar el puerto en el código
- HF Spaces requiere puerto 7860

### Runtime error: "Cannot write to /app"
- Verifica que todos los paths usen `/tmp`
- Ejemplo: `/tmp/uploads`, `/tmp/processed`

### CORS error en frontend
- Verifica variable `ALLOWED_ORIGINS` en HF Settings
- Debe incluir el dominio de tu frontend Netlify

### Model download timeout
- Es normal en el primer build (~5 min)
- El modelo U2-Net es ~180MB
- Se cachea en `/tmp/.u2net` para siguientes reiniciós

## Logs y Debugging

Ver logs en tiempo real:

1. En el Space, click **"Logs"**
2. Filtra por nivel: `INFO`, `ERROR`, etc
3. Busca por job_id para debuggear jobs específicos

## Recursos del Space

**Free Tier (CPU basic):**
- RAM: 16GB
- vCPU: 2 cores
- Disk: 50GB
- GPU: No

**Upgrades disponibles:**
- CPU upgrade: +8GB RAM
- T4 GPU: Para procesamiento más rápido (si usas GPU en rembg)

## Seguridad

- ✅ Space en modo `Private`
- ✅ Service key en Repository secrets (no en código)
- ✅ CORS configurado para dominios específicos
- ✅ Usuario no-root en Docker
- ⚠️ No exponer logs con información sensible

## Costo

**HF Spaces Free Tier:**
- CPU basic: **GRATIS** indefinidamente
- Sin límite de requests
- Sin límite de almacenamiento (50GB disk)

**Pro Tier (si necesitas):**
- $9/mes: GPU T4 + más recursos
- $69/mes: GPU A10 + recursos premium
