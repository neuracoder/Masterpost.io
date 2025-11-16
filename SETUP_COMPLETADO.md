# ✅ SETUP COMPLETADO - Backend Simplificado

## 🎉 LO QUE SE HA HECHO:

### 1. ✅ Estructura Minimalista Creada
```
api/
├── main.py              # Backend completo (350 líneas)
├── requirements.txt     # 9 dependencias
├── venv/               # Entorno virtual (creado)
├── .env                # Variables (necesita configuración)
├── start.bat           # Inicio Windows
├── start.sh            # Inicio Linux/Mac
└── README.md          # Documentación técnica
```

### 2. ✅ Dependencias Instaladas
Todas las dependencias están instaladas en el entorno virtual `api/venv/`:
- ✅ fastapi
- ✅ uvicorn  
- ✅ supabase
- ✅ stripe
- ✅ dashscope (Qwen API)
- ✅ requests
- ✅ python-dotenv

### 3. ✅ Scripts de Inicio Creados
- `api/start.bat` - Para Windows
- `api/start.sh` - Para Linux/Mac

---

## 🎯 SIGUIENTE PASO: CONFIGURAR Y TESTEAR (5 minutos)

### Paso 1: Configurar variables de entorno

Edita `api/.env` con tus keys:

```bash
cd api
notepad .env   # Windows
# o
nano .env      # Linux/Mac
```

**Variables REQUERIDAS para test:**
```env
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Variables OPCIONALES (para testing local):**
```env
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxx
STRIPE_PRICE_STARTER=price_xxxxxxxxxxxxx
STRIPE_PRICE_PRO=price_xxxxxxxxxxxxx
STRIPE_PRICE_BUSINESS=price_xxxxxxxxxxxxx
FRONTEND_URL=http://localhost:3000
```

### Paso 2: Iniciar servidor

**Windows:**
```cmd
cd api
start.bat
```

**Linux/Mac:**
```bash
cd api
./start.sh
```

**O manualmente:**
```bash
cd api
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Paso 3: Verificar que funciona

Abrir en navegador o curl:
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "qwen_configured": true,
  "supabase_configured": true,
  "stripe_configured": true
}
```

---

## 🧪 TESTING COMPLETO (10 minutos)

### 1. Health Check ✅
```bash
curl http://localhost:8000/health
```

### 2. Pricing ✅
```bash
curl http://localhost:8000/api/pricing
```

### 3. Register User ✅
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@masterpost.io","password":"Test123456!"}'
```

### 4. Login ✅
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@masterpost.io","password":"Test123456!"}'
```

Guardar el `access_token` de la respuesta.

### 5. Check Credits ✅
```bash
curl http://localhost:8000/api/credits/balance \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Process Image ✅
**IMPORTANTE:** Necesitas agregar créditos manualmente en Supabase primero:

```sql
-- En Supabase SQL Editor
SELECT add_credits(
  'USER_ID_DEL_PASO_4',
  100,
  'test',
  'Test credits',
  '{}'::jsonb
);
```

Luego procesar:
```bash
curl -X POST http://localhost:8000/api/process \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@test_image.jpg" \
  -F "pipeline=amazon" \
  --output result.png
```

Si funciona, tendrás `result.png` con fondo blanco! 🎉

---

## 📋 CHECKLIST DE VERIFICACIÓN

- [ ] ✅ Dependencias instaladas (en venv)
- [ ] ⏳ Variables en `.env` configuradas
- [ ] ⏳ Servidor inicia sin errores
- [ ] ⏳ Health check responde OK
- [ ] ⏳ Registro de usuario funciona
- [ ] ⏳ Login funciona
- [ ] ⏳ Procesamiento con Qwen funciona

---

## 🚀 SIGUIENTE: DEPLOY A VERCEL (15 minutos)

Una vez que el test local funciona:

### 1. Instalar Vercel CLI
```bash
npm install -g vercel
```

### 2. Login
```bash
vercel login
```

### 3. Deploy
```bash
# En la raíz del proyecto (no en api/)
cd ..
vercel
```

Responder:
- Link to existing project? **N**
- Project name? **masterpost-api**
- Directory? **./**
- Override settings? **N**

### 4. Configurar secrets
```bash
vercel env add DASHSCOPE_API_KEY
vercel env add SUPABASE_URL
vercel env add SUPABASE_ANON_KEY
vercel env add STRIPE_SECRET_KEY
vercel env add STRIPE_WEBHOOK_SECRET
vercel env add STRIPE_PRICE_STARTER
vercel env add STRIPE_PRICE_PRO
vercel env add STRIPE_PRICE_BUSINESS
```

### 5. Deploy a producción
```bash
vercel --prod
```

Tu API estará en: `https://masterpost-api-xxx.vercel.app`

### 6. Verificar deployment
```bash
curl https://masterpost-api-xxx.vercel.app/health
```

---

## 💰 RESULTADO FINAL

Después de estos pasos tendrás:

✅ **Backend local funcionando** (puerto 8000)
✅ **Procesamiento con Qwen API** (premium quality)
✅ **Auth con Supabase** (JWT tokens)
✅ **Sistema de créditos** (verificación automática)
✅ **Listo para deploy** en Vercel ($0/mes)

---

## 🆘 TROUBLESHOOTING

### Error: "DASHSCOPE_API_KEY not configured"
**Solución:** Editar `api/.env` y agregar tu key de Qwen.

### Error: "Qwen API error"
**Solución:** 
1. Verificar que la key sea correcta
2. Verificar cuota en Alibaba Cloud console
3. Región correcta: Singapore

### Error: "Auth failed"
**Solución:** Verificar `SUPABASE_URL` y `SUPABASE_ANON_KEY` en `.env`.

### Error: "Insufficient credits"
**Solución:** Agregar créditos manualmente en Supabase:
```sql
SELECT add_credits('USER_ID', 100, 'test', 'Test credits', '{}'::jsonb);
```

---

## 📚 DOCUMENTACIÓN

- [QUICK_START.md](QUICK_START.md) - Guía completa de deployment
- [api/README.md](api/README.md) - Documentación técnica
- [RESUMEN_MIGRACION.md](RESUMEN_MIGRACION.md) - Overview de cambios
- [INFORME_EJECUTIVO_MIGRACION_QWEN.md](INFORME_EJECUTIVO_MIGRACION_QWEN.md) - Análisis completo

---

## ✅ SIGUIENTE ACCIÓN

**AHORA:** 
1. Editar `api/.env` con tus keys
2. Correr `cd api && start.bat` (Windows) o `./start.sh` (Linux)
3. Verificar http://localhost:8000/health

**DESPUÉS:**
1. Test completo (ver sección Testing)
2. Deploy a Vercel
3. Actualizar frontend

---

🎉 **¡El backend simplificado está listo para usar!**
