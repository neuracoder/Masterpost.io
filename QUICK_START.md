# 🚀 QUICK START - Masterpost.io Simplified Backend

## ✅ LO QUE ACABAS DE CREAR

Backend ultra-simplificado con **1 solo archivo** (api/main.py):

```
api/
├── main.py              # TODO el backend (350 líneas)
├── requirements.txt     # 7 dependencias (vs 50+ anterior)
└── README.md           # Guía de deployment
```

**SIN:**
- ❌ rembg (eliminado)
- ❌ onnxruntime (eliminado)
- ❌ BiRefNet (eliminado)
- ❌ Múltiples routers
- ❌ Servicios separados
- ❌ Complejidad innecesaria

**CON:**
- ✅ Qwen API (SOLO)
- ✅ Auth (Supabase)
- ✅ Créditos (Supabase RPC)
- ✅ Pagos (Stripe)
- ✅ 1 archivo, fácil de mantener

---

## 📋 SIGUIENTE PASO: TEST LOCAL (5 minutos)

### 1. Instalar dependencias
```bash
cd api
pip install -r requirements.txt
```

### 2. Copiar variables de entorno
```bash
# Copiar el template
cp ../.env.example .env

# Editar con tus keys
nano .env
```

Necesitas:
- `DASHSCOPE_API_KEY` (Qwen API)
- `SUPABASE_URL` y `SUPABASE_ANON_KEY`
- `STRIPE_SECRET_KEY` (opcional para testing)

### 3. Correr servidor
```bash
uvicorn main:app --reload
```

### 4. Test básico
```bash
# En otra terminal
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "qwen_configured": true,
  "supabase_configured": true
}
```

---

## 🧪 TEST COMPLETO (10 minutos)

### 1. Registrar usuario
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@masterpost.io","password":"Test123!"}'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@masterpost.io","password":"Test123!"}'
```

Guardar el `access_token` que te devuelve.

### 3. Ver balance
```bash
curl http://localhost:8000/api/credits/balance \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Procesar imagen (IMPORTANTE: necesitas créditos)

Primero, agregar créditos manualmente en Supabase:
```sql
-- En Supabase SQL Editor
SELECT add_credits(
  'USER_ID_AQUI',
  100,
  'test',
  'Test credits',
  '{}'::jsonb
);
```

Luego procesar:
```bash
curl -X POST http://localhost:8000/api/process \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test_image.jpg" \
  -F "pipeline=amazon" \
  --output result.png
```

Si funciona, verás:
- Headers: `X-Credits-Used: 3`
- Archivo: `result.png` con fondo blanco

---

## 🚀 DEPLOYMENT A VERCEL (15 minutos)

### Paso 1: Instalar Vercel CLI
```bash
npm install -g vercel
```

### Paso 2: Login
```bash
vercel login
```

### Paso 3: Link proyecto
```bash
# En la raíz del proyecto
vercel
```

Responder:
- Set up and deploy? **Y**
- Which scope? (tu cuenta)
- Link to existing project? **N**
- Project name? **masterpost-api**
- Directory? **./** (raíz)
- Override settings? **N**

### Paso 4: Configurar secrets
```bash
# Qwen API
vercel env add DASHSCOPE_API_KEY
# Pegar tu key cuando pregunte
# Environment: Production
# Add to other envs? Y

# Supabase
vercel env add SUPABASE_URL
vercel env add SUPABASE_ANON_KEY

# Stripe
vercel env add STRIPE_SECRET_KEY
vercel env add STRIPE_WEBHOOK_SECRET
vercel env add STRIPE_PRICE_STARTER
vercel env add STRIPE_PRICE_PRO
vercel env add STRIPE_PRICE_BUSINESS
```

### Paso 5: Deploy a producción
```bash
vercel --prod
```

Tu API estará en: `https://masterpost-api.vercel.app`

### Paso 6: Verificar deployment
```bash
curl https://masterpost-api.vercel.app/health
```

---

## 🎯 CONFIGURAR STRIPE (20 minutos)

### 1. Crear productos en Stripe Dashboard

Ir a: https://dashboard.stripe.com/products

**Producto 1: Starter Pack**
- Name: `Starter Pack`
- Description: `30 créditos para procesar ~10 imágenes`
- Add pricing:
  - Model: `One time`
  - Price: `$9.99 USD`
- Add metadata:
  - Key: `credits`
  - Value: `30`
- Save

Copiar el **Price ID** (empieza con `price_...`) → `STRIPE_PRICE_STARTER`

**Producto 2: Pro Pack**
- Name: `Pro Pack`
- Description: `100 créditos para procesar ~33 imágenes`
- Price: `$29.99 USD`
- Metadata: `credits = 100`

Copiar Price ID → `STRIPE_PRICE_PRO`

**Producto 3: Business Pack**
- Name: `Business Pack`
- Description: `300 créditos para procesar ~100 imágenes`
- Price: `$79.99 USD`
- Metadata: `credits = 300`

Copiar Price ID → `STRIPE_PRICE_BUSINESS`

### 2. Actualizar Vercel con Price IDs
```bash
vercel env add STRIPE_PRICE_STARTER
# Pegar el price_xxx

vercel env add STRIPE_PRICE_PRO
# Pegar el price_xxx

vercel env add STRIPE_PRICE_BUSINESS
# Pegar el price_xxx
```

### 3. Crear Webhook

Ir a: https://dashboard.stripe.com/webhooks

- Click **Add endpoint**
- Endpoint URL: `https://masterpost-api.vercel.app/webhook/stripe`
- Events to send: Seleccionar `checkout.session.completed`
- Add endpoint

Copiar el **Signing secret** (empieza con `whsec_...`)

```bash
vercel env add STRIPE_WEBHOOK_SECRET
# Pegar whsec_xxx
```

### 4. Redeploy
```bash
vercel --prod
```

---

## 🧪 TEST DE PAYMENT (Stripe Test Mode)

### 1. Crear checkout session
```bash
curl -X POST https://masterpost-api.vercel.app/api/create-checkout \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price_id":"price_xxx"}'
```

Response:
```json
{
  "session_id": "cs_xxx",
  "url": "https://checkout.stripe.com/c/pay/cs_xxx..."
}
```

### 2. Abrir URL en browser

Usar tarjeta de test:
- Card: `4242 4242 4242 4242`
- Expiry: cualquier fecha futura
- CVC: cualquier 3 dígitos

### 3. Verificar créditos agregados
```bash
curl https://masterpost-api.vercel.app/api/credits/balance \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Deberías ver los créditos sumados.

---

## 📱 ACTUALIZAR FRONTEND

### 1. Cambiar API URL

En tu frontend (`.env.local` de Next.js):
```env
NEXT_PUBLIC_API_URL=https://masterpost-api.vercel.app
```

### 2. Simplificar UI

**ANTES (código viejo con tiers):**
```jsx
<select>
  <option value="basic">Basic (1 crédito)</option>
  <option value="premium">Premium (3 créditos)</option>
</select>
```

**DESPUÉS (solo Qwen):**
```jsx
<p className="text-sm text-gray-600">
  Costo: 3 créditos por imagen (Premium AI)
</p>
```

### 3. Actualizar pricing display

```jsx
const CREDITS_PER_IMAGE = 3; // SIEMPRE

function calculateCost(imageCount: number) {
  return imageCount * CREDITS_PER_IMAGE;
}
```

### 4. Actualizar API calls

```tsx
// Procesar imagen
const formData = new FormData();
formData.append('file', file);
formData.append('pipeline', 'amazon');

const response = await fetch(`${API_URL}/api/process`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});

const blob = await response.blob();
const processedImageUrl = URL.createObjectURL(blob);
```

---

## 🎉 DEPLOYMENT COMPLETO

Después de estos pasos tendrás:

✅ **Backend en Vercel** (gratis)
- URL: `https://masterpost-api.vercel.app`
- Costo: $0/mes

✅ **Procesamiento con Qwen API**
- Calidad premium
- Costo: $0.045 por imagen
- Margen: $0.255 por imagen

✅ **Pagos con Stripe**
- 3 paquetes de créditos
- Webhook funcionando
- Test mode para desarrollo

✅ **Frontend actualizado**
- Apuntando a nueva API
- Solo tier premium (3 créditos)

---

## 💰 COSTOS FINALES

```
Hosting:           $0/mes (Vercel Hobby)
Qwen API:          $0.045 por imagen
Stripe fees:       2.9% + $0.30 por transacción
Supabase:          $0/mes (hasta 500MB)

TOTAL FIJO:        $0/mes
TOTAL VARIABLE:    $0.045 por imagen procesada

Precio al usuario: $0.30 por imagen (3 créditos)
Margen:            $0.255 por imagen (85% margen)
```

---

## 📊 MONITOREO

### Vercel Logs
```bash
vercel logs https://masterpost-api.vercel.app --follow
```

### Métricas en Vercel Dashboard
- https://vercel.com/dashboard
- Ver:
  - Request count
  - Response time
  - Error rate
  - Bandwidth

### Qwen API Usage
- https://dashscope.console.aliyun.com
- Monitorear costos diarios

### Stripe Dashboard
- https://dashboard.stripe.com
- Ver:
  - Payments
  - Webhooks (verificar que lleguen)

---

## ⚠️ DESACTIVAR BACKEND ANTERIOR

Una vez que el nuevo backend funciona:

### 1. Desactivar Railway (ahorrar $20/mes)
- Ir a Railway dashboard
- Stop service
- Delete project
- ✅ Ahorro: $20/mes

### 2. Eliminar archivos obsoletos (opcional)
```bash
# Backup primero
git checkout -b backup-old-backend

# Luego eliminar
rm -rf backend/
rm -rf services/
rm -rf hf-worker/
rm server.py
rm main.py
```

---

## 🎯 CHECKLIST FINAL

- [ ] Backend en Vercel funcionando
- [ ] Health check OK
- [ ] Qwen API configurado
- [ ] Supabase conectado
- [ ] Stripe productos creados
- [ ] Stripe webhook configurado
- [ ] Frontend actualizado
- [ ] Test de procesamiento OK
- [ ] Test de payment OK
- [ ] Railway desactivado

---

## 🆘 AYUDA

### Error común: "Qwen API error"
**Solución:** Verificar que `DASHSCOPE_API_KEY` sea correcto y tenga cuota.

### Error común: "Insufficient credits"
**Solución:** Agregar créditos manualmente en Supabase o comprar vía Stripe.

### Error común: "Auth failed"
**Solución:** Token expirado, hacer login nuevamente.

### Error común: "Stripe webhook failed"
**Solución:** Verificar URL del webhook y signing secret.

---

**¿Listo para empezar?**

```bash
cd api
pip install -r requirements.txt
cp ../.env.example .env
# Editar .env
uvicorn main:app --reload
```

🚀 Let's go!
