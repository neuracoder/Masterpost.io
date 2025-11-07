from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.schemas import CheckoutRequest
from app.services.stripe_service import create_checkout_session, handle_successful_payment
from app.routers.auth_routes import get_current_user_id
from app.services.auth_service import auth_service
import stripe
import os

router = APIRouter(prefix="/api/payments", tags=["Payments"])

@router.post("/create-checkout")
async def create_checkout(
    request: CheckoutRequest,
    user_id: str = Depends(get_current_user_id)
):
    """Crear sesión de Stripe Checkout"""
    # Obtener email del usuario
    user = await auth_service.supabase.auth.admin.get_user_by_id(user_id)
    user_email = user.user.email
    
    return await create_checkout_session(
        user_id=user_id,
        pack_type=request.pack_type,
        user_email=user_email
    )

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Webhook de Stripe para eventos de pago"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Manejar evento de pago exitoso
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Procesar pago
        await handle_successful_payment(
            payment_intent_id=session.get('payment_intent'),
            metadata=session.get('metadata', {})
        )
        
        return {"status": "success"}
    
    return {"status": "ignored"}
