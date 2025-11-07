# Variables de Entorno para HF Space

## Variables OBLIGATORIAS

Configura estas variables en **Settings > Repository secrets** del Space:

```bash
# Supabase Configuration
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...

# CORS Origins (comma-separated)
ALLOWED_ORIGINS=https://masterpost-io.netlify.app,http://localhost:3000
```

## Variables OPCIONALES

```bash
# Premium processing (Qwen API)
QWEN_API_KEY=sk-xxx

# Custom frontend URL (legacy, use ALLOWED_ORIGINS instead)
FRONTEND_URL=https://masterpost-io.netlify.app
```

## Ejemplo completo

```env
SUPABASE_URL=https://abcdefg.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
ALLOWED_ORIGINS=https://masterpost-io.netlify.app,https://masterpost.io,http://localhost:3000
```

## Verificación

Una vez deployado, verifica que las variables se cargaron correctamente:

```bash
# Check health endpoint
curl https://USERNAME-masterpost-worker.hf.space/health

# Should return:
{
  "status": "healthy",
  "local_processing": true,
  "manual_editor": "available",
  "timestamp": 1699380000
}
```

## Troubleshooting

### Error: CORS blocked
- Verifica que `ALLOWED_ORIGINS` incluya tu dominio frontend
- Formato: `https://domain1.com,https://domain2.com` (sin espacios)

### Error: Supabase connection failed
- Verifica que `SUPABASE_URL` y `SUPABASE_SERVICE_KEY` sean correctos
- El key debe ser el **service_role** key (no anon key)

### Error: Port 7860 not available
- No modificar el puerto, HF Spaces requiere 7860
- Variable `PORT` se configura automáticamente
