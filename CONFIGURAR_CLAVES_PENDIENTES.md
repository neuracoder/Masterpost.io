# INSTRUCCIONES: Configurar Claves Pendientes

## 1. SUPABASE - Obtener Claves

### Paso a paso:
1. Ve a: https://app.supabase.com
2. Selecciona tu proyecto: **cvytoscpsmfagiuglopy**
3. Click en **Settings** (engranaje abajo a la izquierda)
4. Click en **API**
5. Copia las siguientes claves:

**Project URL:**
```
https://cvytoscpsmfagiuglopy.supabase.co
```

**anon public (clave publica):**
```
eyJhbGc...
```

**service_role (clave secreta):**
```
eyJhbGc...
```

---

## 2. STRIPE - Obtener Clave Publica

### Paso a paso:
1. Ve a: https://dashboard.stripe.com/test/apikeys
2. Asegurate de estar en modo **TEST**
3. Busca **Publishable key**
4. Click en **Reveal test key**
5. Copia la clave que empieza con: `pk_test_...`

---

## 3. ACTUALIZAR ARCHIVOS

### Backend: backend/.env

Abre el archivo y busca estas lineas, reemplaza con tus claves:

```env
# Linea ~44
SUPABASE_ANON_KEY=AQUI_TU_CLAVE_ANON_DE_SUPABASE

# Linea ~45
SUPABASE_SERVICE_ROLE_KEY=AQUI_TU_CLAVE_SERVICE_ROLE_DE_SUPABASE

# Linea ~53
STRIPE_PUBLISHABLE_KEY=AQUI_TU_pk_test_DE_STRIPE
```

### Frontend: .env.development

Abre el archivo y busca estas lineas:

```env
# Linea ~36
NEXT_PUBLIC_SUPABASE_ANON_KEY=AQUI_TU_CLAVE_ANON_DE_SUPABASE

# Linea ~43
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=AQUI_TU_pk_test_DE_STRIPE
```

### Frontend: .env.local

Abre el archivo y busca estas lineas:

```env
# Linea ~15
NEXT_PUBLIC_SUPABASE_ANON_KEY=AQUI_TU_CLAVE_ANON_DE_SUPABASE

# Linea ~18
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=AQUI_TU_pk_test_DE_STRIPE
```

---

## 4. VERIFICAR

Despues de configurar, ejecuta:

```bash
# Terminal 1 - Backend
cd backend
python app/main.py

# Deberia ver:
# - Supabase connection initialized successfully
# - Server running on port 8002
```

```bash
# Terminal 2 - Frontend  
npm run dev

# Deberia ver:
# - Ready on http://localhost:3000
# - Sin errores de Supabase o Stripe
```

---

## 5. PROBAR REGISTRO

1. Ve a: http://localhost:3000/register
2. Crea una cuenta con tu email
3. Si todo funciona:
   - Te redirige a /dashboard
   - Ves 10 creditos gratis
   - No hay errores en consola

---

## NOTAS IMPORTANTES

- La clave **anon public** es segura para el frontend
- La clave **service_role** NUNCA debe ir en el frontend
- Usa claves de TEST de Stripe (pk_test_, sk_test_)
- Para produccion necesitaras claves LIVE diferentes

---

## RESUMEN DE CLAVES NECESARIAS

| Clave | Donde obtenerla | Donde va |
|-------|----------------|----------|
| SUPABASE_ANON_KEY | Supabase → API | Backend + Frontend |
| SUPABASE_SERVICE_ROLE_KEY | Supabase → API | Solo Backend |
| STRIPE_PUBLISHABLE_KEY | Stripe Dashboard | Backend + Frontend |

---

**Una vez configuradas estas 3 claves, tu sistema estara 100% funcional!**

