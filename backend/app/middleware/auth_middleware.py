"""
Middleware de autenticación para endpoints protegidos
"""

from fastapi import Header, HTTPException, status
from typing import Optional
import os
from app.database.supabase_client import supabase

async def verify_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Verifica el token JWT y retorna el user_id

    Args:
        authorization: Header Authorization con formato "Bearer <token>"

    Returns:
        user_id: ID del usuario autenticado

    Raises:
        HTTPException: Si el token es inválido o falta
    """

    # 1. Verificar que existe el header
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )

    # 2. Extraer token (formato: "Bearer <token>")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

    # 3. Verificar token con Supabase
    try:
        response = supabase.auth.get_user(token)

        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        # 4. Retornar user_id
        return response.user.id

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}"
        )


async def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Dependency para obtener user_id en endpoints
    Alias de verify_token para usar con Depends()
    """
    return await verify_token(authorization)
