# Masterpost.io Backend - Qwen Only

## 🎯 Arquitectura Ultra-Simplificada

Backend serverless de **1 solo archivo** con procesamiento 100% en Qwen API.

```
api/
├── main.py              # Todo el backend (350 líneas)
├── requirements.txt     # 7 dependencias
└── README.md           # Esta guía
```

## 🚀 Quick Start (Local)

### 1. Instalar dependencias
```bash
cd api
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
cp ../.env.example .env
```

Editar `.env` con tus keys:
```env
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_STARTER=price_xxx
STRIPE_PRICE_PRO=price_xxx
STRIPE_PRICE_BUSINESS=price_xxx
FRONTEND_URL=http://localhost:3000
```

### 3. Correr servidor
```bash
uvicorn main:app --reload
```

Servidor corriendo en: http://localhost:8000

## 🧪 Testing

### Health check
```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "qwen_configured": true,
  "supabase_configured": true,
  "stripe_configured": true
}
```

### Registro de usuario
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

Response:
```json
{
  "access_token": "eyJhbGci...",
  "user": {...}
}
```

### Procesar imagen
```bash
curl -X POST http://localhost:8000/api/process \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test.jpg" \
  -F "pipeline=amazon" \
  --output result.png
```

## 📦 Deploy a Vercel

### 1. Instalar Vercel CLI
```bash
npm i -g vercel
```

### 2. Login
```bash
vercel login
```

### 3. Configurar secrets
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

### 4. Deploy
```bash
# Deploy a staging
vercel

# Deploy a producción
vercel --prod
```

Tu API estará en: `https://your-app.vercel.app`

## 🔗 Endpoints

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Login

### Créditos
- `GET /api/credits/balance` - Ver balance (requiere auth)

### Procesamiento
- `POST /api/process` - Procesar imagen con Qwen (requiere auth)
  - Headers: `Authorization: Bearer TOKEN`
  - Body: `file` (multipart/form-data)
  - Query: `pipeline` (amazon/ebay/instagram)
  - Costo: **3 créditos por imagen**

### Pagos
- `GET /api/pricing` - Ver paquetes disponibles
- `POST /api/create-checkout` - Crear sesión de pago (requiere auth)
- `POST /webhook/stripe` - Webhook de Stripe

### Health
- `GET /` - Status del servicio
- `GET /health` - Health check

## 💰 Pricing

| Pack | Créditos | Precio | Imágenes |
|------|----------|--------|----------|
| Starter | 30 | $9.99 | ~10 |
| Pro | 100 | $29.99 | ~33 |
| Business | 300 | $79.99 | ~100 |

**Costo por imagen:** 3 créditos = $0.30

## 🔧 Configuración de Stripe

### Crear productos en Stripe Dashboard

1. **Starter Pack**
   - Name: Starter Pack
   - Price: $9.99
   - Metadata: `credits=30`
   - Guardar Price ID en `STRIPE_PRICE_STARTER`

2. **Pro Pack**
   - Name: Pro Pack
   - Price: $29.99
   - Metadata: `credits=100`
   - Guardar Price ID en `STRIPE_PRICE_PRO`

3. **Business Pack**
   - Name: Business Pack
   - Price: $79.99
   - Metadata: `credits=300`
   - Guardar Price ID en `STRIPE_PRICE_BUSINESS`

### Configurar Webhook

URL: `https://your-api.vercel.app/webhook/stripe`

Eventos a escuchar:
- `checkout.session.completed`

Copiar Webhook Secret a `STRIPE_WEBHOOK_SECRET`

## 📊 Monitoreo

### Logs en Vercel
```bash
vercel logs https://your-app.vercel.app
```

### Metrics en Vercel Dashboard
- Request count
- Response time
- Error rate
- Bandwidth

### Qwen API Usage
- Dashboard: https://dashscope.console.aliyun.com
- Monitorear:
  - API calls/día
  - Costos ($0.045 por imagen)
  - Error rate

## ⚡ Optimizaciones

### Cache de imágenes (opcional)
Si procesas la misma imagen múltiples veces, puedes cachear en Supabase Storage:

```python
# Hash de la imagen
import hashlib
hash_key = hashlib.md5(image_bytes).hexdigest()

# Check cache
cached = supabase.storage.from_('processed').download(f'{hash_key}.png')
if cached:
    return cached
```

### Rate limiting (recomendado)
Agregar rate limiting por usuario:

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/process")
@limiter.limit("10/minute")
async def process_image(...):
    ...
```

## 🐛 Troubleshooting

### Error: "Qwen API error"
- Verificar `DASHSCOPE_API_KEY`
- Verificar cuota en Alibaba Cloud
- Check region: debe ser Singapore

### Error: "Insufficient credits"
- Verificar balance: `GET /api/credits/balance`
- Comprar más créditos

### Error: "Auth failed"
- Token expirado, hacer login nuevamente
- Verificar formato: `Bearer TOKEN`

### Error: "Stripe webhook failed"
- Verificar `STRIPE_WEBHOOK_SECRET`
- Test con Stripe CLI: `stripe listen --forward-to localhost:8000/webhook/stripe`

## 📝 Notas

- **Sin rembg local:** Todo el procesamiento en Qwen API
- **Sin storage local:** Imágenes en memoria, devueltas directamente
- **Stateless:** Serverless-ready, sin sesiones en servidor
- **Escalable:** Auto-scaling de Vercel

## 💡 Tips

1. **Desarrollo local:** Usa ngrok para testear webhooks de Stripe
   ```bash
   ngrok http 8000
   ```

2. **Testing de Qwen:** Usa imágenes pequeñas (< 1MB) para tests

3. **Logs:** Usa `print()` para debug, se ven en `vercel logs`

4. **Errores:** Todos los errores devuelven créditos automáticamente

## 📞 Support

- Issues: GitHub Issues
- Docs de Qwen: https://help.aliyun.com/zh/model-studio/
- Docs de Vercel: https://vercel.com/docs
