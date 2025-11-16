"""
Masterpost.io Backend - QWEN ONLY
Ultra-simplified serverless API
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import os
import stripe
import base64
import requests
from typing import Optional
from pydantic import BaseModel
from supabase import create_client, Client
import dashscope
from dashscope import MultiModalConversation
from io import BytesIO

# ============================================================
# CONFIGURACIÓN
# ============================================================

app = FastAPI(title="Masterpost API", version="3.0-QWEN-ONLY")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clientes externos
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Qwen API configuration
QWEN_API_KEY = os.getenv("DASHSCOPE_API_KEY")
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

# ============================================================
# MODELOS PYDANTIC
# ============================================================

class ProcessRequest(BaseModel):
    pipeline: str = "amazon"  # amazon, ebay, instagram

class AuthUser(BaseModel):
    id: str
    email: str

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

async def verify_token(authorization: str) -> AuthUser:
    """Verificar JWT token de Supabase"""
    if not authorization:
        raise HTTPException(401, "Authorization header required")

    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid token format")

    token = authorization.replace("Bearer ", "")

    try:
        # Verificar con Supabase
        response = supabase.auth.get_user(token)
        user = response.user

        if not user:
            raise HTTPException(401, "Invalid token")

        return AuthUser(id=user.id, email=user.email)

    except Exception as e:
        raise HTTPException(401, f"Auth failed: {str(e)}")


async def check_and_use_credits(user_id: str, credits_needed: int = 3) -> bool:
    """Verificar y usar créditos (atómico en Supabase)"""
    try:
        # Llamar función RPC de Supabase
        result = supabase.rpc(
            'use_credits',
            {
                'p_user_id': user_id,
                'p_credits': credits_needed,
                'p_transaction_type': 'image_processing_qwen',
                'p_description': f'Processed 1 image with Qwen API'
            }
        ).execute()

        return result.data is not None

    except Exception as e:
        print(f"Credit check failed: {e}")
        return False


async def call_qwen_api(image_bytes: bytes, pipeline: str) -> bytes:
    """
    Llamar a Qwen Image Edit API usando el SDK oficial

    Returns: bytes de la imagen procesada
    """

    # Prompts optimizados por pipeline
    prompts = {
        "amazon": """Remove the background completely from this product image and replace it with pure white (RGB 255, 255, 255).
Keep ONLY the main product, remove everything else.
Preserve all product details with maximum precision.
Ensure the product covers exactly 85% of the image area.
Remove ALL shadows, reflections, and background elements.""",

        "ebay": """Remove the background completely and replace with pure white (RGB 255, 255, 255).
Preserve MAXIMUM detail quality for zoom inspection.
Keep all fine details: textures, engravings, small text.
Remove all background shadows and elements.""",

        "instagram": """Remove the background completely and replace with pure white (RGB 255, 255, 255).
Create a visually appealing, social-media ready image.
Enhance colors while maintaining natural look.
Remove all background elements."""
    }

    prompt = prompts.get(pipeline, prompts["amazon"])

    # Encode imagen a base64
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')

    # Preparar messages según especificación oficial
    messages = [
        {
            "role": "user",
            "content": [
                {"image": f"data:image/jpeg;base64,{image_b64}"},
                {"text": prompt}
            ]
        }
    ]

    # Llamar a Qwen Image Edit API usando el SDK oficial
    response = MultiModalConversation.call(
        api_key=QWEN_API_KEY,
        model="qwen-image-edit",
        messages=messages,
        stream=False,
        watermark=False,
        negative_prompt="shadows, reflections, background, blur, artifacts, low quality"
    )

    # Verificar respuesta
    if response.status_code != 200:
        raise HTTPException(500, f"Qwen API error: {response.message}")

    # Extraer URL de imagen procesada
    try:
        image_url = response.output.choices[0].message.content[0]['image']
    except (KeyError, IndexError, AttributeError) as e:
        raise HTTPException(500, f"Failed to extract image URL from Qwen response: {str(e)}")

    # Descargar imagen procesada (válida por 24h)
    img_response = requests.get(image_url, timeout=30)

    if img_response.status_code != 200:
        raise HTTPException(500, "Failed to download processed image")

    return img_response.content


# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    return {"status": "ok", "service": "Masterpost API - Qwen Only"}


@app.get("/health")
async def health_check():
    """Health check para Vercel"""
    return {
        "status": "healthy",
        "qwen_configured": bool(QWEN_API_KEY),
        "supabase_configured": bool(os.getenv("SUPABASE_URL")),
        "stripe_configured": bool(stripe.api_key)
    }


@app.post("/api/auth/register")
async def register(email: str, password: str):
    """Registrar usuario nuevo"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        return {
            "success": True,
            "user": response.user.dict() if response.user else None
        }

    except Exception as e:
        raise HTTPException(400, str(e))


@app.post("/api/auth/login")
async def login(email: str, password: str):
    """Login de usuario"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        return {
            "access_token": response.session.access_token,
            "user": response.user.dict()
        }

    except Exception as e:
        raise HTTPException(401, "Invalid credentials")


@app.get("/api/credits/balance")
async def get_balance(authorization: str = Depends(lambda r: r.headers.get("authorization"))):
    """Obtener balance de créditos"""
    user = await verify_token(authorization)

    result = supabase.rpc('get_user_credits', {'p_user_id': user.id}).execute()

    return {
        "user_id": user.id,
        "credits": result.data if result.data else 0
    }


@app.post("/api/process")
async def process_image(
    file: UploadFile = File(...),
    pipeline: str = "amazon",
    authorization: str = Depends(lambda r: r.headers.get("authorization"))
):
    """
    ENDPOINT PRINCIPAL - Procesar imagen con Qwen

    Flujo:
    1. Verificar autenticación
    2. Verificar y deducir créditos (3 créditos)
    3. Procesar con Qwen API
    4. Devolver imagen procesada
    """

    # 1. Verificar auth
    user = await verify_token(authorization)

    # 2. Verificar créditos
    has_credits = await check_and_use_credits(user.id, credits_needed=3)

    if not has_credits:
        raise HTTPException(402, "Insufficient credits")

    try:
        # 3. Leer imagen
        image_bytes = await file.read()

        # 4. Procesar con Qwen
        processed_bytes = await call_qwen_api(image_bytes, pipeline)

        # 5. Devolver imagen procesada
        return StreamingResponse(
            BytesIO(processed_bytes),
            media_type="image/png",
            headers={
                "X-Credits-Used": "3",
                "X-Processing-Method": "qwen-api"
            }
        )

    except HTTPException:
        # Si falla, devolver créditos
        supabase.rpc('add_credits', {
            'p_user_id': user.id,
            'p_credits': 3,
            'p_transaction_type': 'refund',
            'p_description': 'Processing failed - refund'
        }).execute()
        raise

    except Exception as e:
        # Si falla, devolver créditos
        supabase.rpc('add_credits', {
            'p_user_id': user.id,
            'p_credits': 3,
            'p_transaction_type': 'refund',
            'p_description': 'Processing failed - refund'
        }).execute()
        raise HTTPException(500, f"Processing error: {str(e)}")


@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """
    Webhook de Stripe para pagos
    Genera códigos de crédito después de pago exitoso
    """
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv('STRIPE_WEBHOOK_SECRET')
        )
    except Exception as e:
        raise HTTPException(400, str(e))

    # Procesar pago exitoso
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Extraer metadata
        email = session['customer_details']['email']

        # Obtener producto comprado
        line_items = stripe.checkout.Session.list_line_items(session['id'])
        price = stripe.Price.retrieve(line_items.data[0]['price']['id'])
        product = stripe.Product.retrieve(price['product'])

        credits = int(product.metadata.get('credits', 100))

        # Buscar usuario por email
        user_result = supabase.from_('users').select('id').eq('email', email).execute()

        if user_result.data:
            user_id = user_result.data[0]['id']

            # Agregar créditos
            supabase.rpc('add_credits', {
                'p_user_id': user_id,
                'p_credits': credits,
                'p_transaction_type': 'purchase',
                'p_description': f'Purchased {credits} credits via Stripe'
            }).execute()

    return {"status": "success"}


# ============================================================
# PRODUCTOS DE STRIPE (Setup inicial)
# ============================================================

@app.get("/api/pricing")
async def get_pricing():
    """Obtener paquetes de créditos disponibles"""
    return {
        "packs": [
            {
                "id": "starter",
                "name": "Starter Pack",
                "credits": 30,
                "price": "$9.99",
                "price_cents": 999,
                "images": "~10 images",
                "price_id": os.getenv("STRIPE_PRICE_STARTER")
            },
            {
                "id": "pro",
                "name": "Pro Pack",
                "credits": 100,
                "price": "$29.99",
                "price_cents": 2999,
                "images": "~33 images",
                "price_id": os.getenv("STRIPE_PRICE_PRO"),
                "popular": True
            },
            {
                "id": "business",
                "name": "Business Pack",
                "credits": 300,
                "price": "$79.99",
                "price_cents": 7999,
                "images": "~100 images",
                "price_id": os.getenv("STRIPE_PRICE_BUSINESS")
            }
        ]
    }


@app.post("/api/create-checkout")
async def create_checkout(
    price_id: str,
    authorization: str = Depends(lambda r: r.headers.get("authorization"))
):
    """Crear sesión de checkout de Stripe"""
    user = await verify_token(authorization)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{os.getenv('FRONTEND_URL')}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/pricing",
            customer_email=user.email,
        )

        return {"session_id": session.id, "url": session.url}

    except Exception as e:
        raise HTTPException(400, str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
