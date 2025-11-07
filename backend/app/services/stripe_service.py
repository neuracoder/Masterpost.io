import stripe
import os
from datetime import datetime, timedelta
import secrets
from app.database.supabase_client import supabase
from typing import Dict, Any
from fastapi import HTTPException

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Packs de créditos
CREDIT_PACKS = {
    'PRO': {
        'credits': 200,
        'price_id': os.getenv('STRIPE_PRICE_PRO'),
        'name': 'Pro Pack - 200 Credits',
        'price': 1799  # $17.99
    },
    'BUSINESS': {
        'credits': 500,
        'price_id': os.getenv('STRIPE_PRICE_BUSINESS'),
        'name': 'Business Pack - 500 Credits',
        'price': 3999  # $39.99
    }
}

def generate_credit_code() -> str:
    """Generar código único de créditos"""
    return f"MP-{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}"

async def create_checkout_session(
    user_id: str,
    pack_type: str,
    user_email: str
) -> Dict[str, Any]:
    """Crear sesión de Stripe Checkout"""
    
    if pack_type not in CREDIT_PACKS:
        raise HTTPException(status_code=400, detail="Invalid pack type")
    
    pack = CREDIT_PACKS[pack_type]
    
    if not pack['price_id']:
        raise HTTPException(
            status_code=500,
            detail=f"Stripe Price ID not configured for {pack_type}"
        )
    
    try:
        # Crear o recuperar Stripe Customer
        customer_result = supabase.table('stripe_customers')\
            .select('stripe_customer_id')\
            .eq('user_id', user_id)\
            .execute()
        
        if customer_result.data and len(customer_result.data) > 0:
            customer_id = customer_result.data[0]['stripe_customer_id']
        else:
            # Crear nuevo customer
            customer = stripe.Customer.create(
                email=user_email,
                metadata={'user_id': user_id}
            )
            customer_id = customer.id
            
            # Guardar en DB
            supabase.table('stripe_customers').insert({
                'user_id': user_id,
                'stripe_customer_id': customer_id,
                'email': user_email
            }).execute()
        
        # Crear sesión de checkout
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': pack['price_id'],
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/pricing?canceled=true",
            metadata={
                'user_id': user_id,
                'pack_type': pack_type,
                'credits': pack['credits']
            }
        )
        
        return {
            "checkout_url": session.url,
            "session_id": session.id
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def handle_successful_payment(payment_intent_id: str, metadata: dict):
    """Manejar pago exitoso desde webhook"""
    
    user_id = metadata.get('user_id')
    pack_type = metadata.get('pack_type')
    credits = int(metadata.get('credits', 0))
    
    if not user_id or not pack_type:
        raise ValueError("Missing metadata in payment")
    
    # Generar código de créditos
    code = generate_credit_code()
    
    # Guardar código en DB
    supabase.table('credit_codes').insert({
        'code': code,
        'user_id': user_id,
        'credits_total': credits,
        'pack_type': pack_type,
        'stripe_payment_intent_id': payment_intent_id,
        'redeemed': True,
        'redeemed_at': datetime.utcnow().isoformat()
    }).execute()
    
    # Agregar créditos al usuario usando la función SQL
    supabase.rpc('add_credits', {
        'p_user_id': user_id,
        'p_credits': credits,
        'p_transaction_type': f'purchase_{pack_type.lower()}',
        'p_description': f'Purchased {pack_type} pack - Code: {code}',
        'p_metadata': {'code': code, 'payment_intent': payment_intent_id}
    }).execute()
    
    return {"code": code, "credits": credits}
