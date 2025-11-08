from app.database.supabase_client import supabase
from typing import Dict, List, Any
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def get_balance(user_id: str) -> Dict[str, Any]:
    """Obtener balance de créditos"""
    try:
        logger.info(f"Getting balance for user {user_id}")
        result = supabase.rpc('get_user_credits', {'p_user_id': user_id}).execute()

        if result.data and len(result.data) > 0:
            logger.info(f"Balance retrieved: {result.data[0]['credits']} credits")
            return {
                "credits": result.data[0]['credits'],
                "updated_at": result.data[0]['updated_at']
            }
        else:
            logger.warning(f"No balance found for user {user_id}, returning 0")
            return {"credits": 0, "updated_at": None}
    except Exception as e:
        logger.error(f"Error getting balance for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting balance: {str(e)}")

async def use_credits(
    user_id: str,
    credits_needed: int,
    transaction_type: str = "usage_basic",
    description: str = None
) -> Dict[str, Any]:
    """Usar créditos"""
    try:
        result = supabase.rpc('use_credits', {
            'p_user_id': user_id,
            'p_credits': credits_needed,
            'p_transaction_type': transaction_type,
            'p_description': description
        }).execute()
        
        if result.data and len(result.data) > 0:
            data = result.data[0]
            if data['success']:
                return {
                    "success": True,
                    "credits_used": credits_needed,
                    "credits_remaining": data['credits_remaining'],
                    "message": data['message']
                }
            else:
                raise HTTPException(status_code=400, detail=data['message'])
        else:
            raise HTTPException(status_code=500, detail="Function returned no data")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error using credits: {str(e)}")

async def add_credits(
    user_id: str,
    credits_amount: int,
    transaction_type: str = "purchase_pro",
    description: str = None,
    metadata: dict = None
) -> Dict[str, Any]:
    """Agregar créditos"""
    try:
        result = supabase.rpc('add_credits', {
            'p_user_id': user_id,
            'p_credits': credits_amount,
            'p_transaction_type': transaction_type,
            'p_description': description,
            'p_metadata': metadata or {}
        }).execute()
        
        if result.data and len(result.data) > 0:
            data = result.data[0]
            if data['success']:
                return {
                    "success": True,
                    "credits_added": credits_amount,
                    "credits_total": data['credits_total'],
                    "message": data['message']
                }
            else:
                raise HTTPException(status_code=400, detail=data['message'])
        else:
            raise HTTPException(status_code=500, detail="Function returned no data")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding credits: {str(e)}")

async def get_transaction_history(
    user_id: str,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """Obtener historial de transacciones"""
    try:
        result = supabase.table('transactions')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .offset(offset)\
            .execute()
        
        return {
            "transactions": result.data,
            "total": len(result.data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting history: {str(e)}")
