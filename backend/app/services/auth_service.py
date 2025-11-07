from supabase import Client
from app.database.supabase_client import supabase
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import os

JWT_SECRET = os.getenv('JWT_SECRET', 'change-this-in-production')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.supabase = supabase
    
    async def signup(self, email: str, password: str) -> Dict[str, Any]:
        """Registrar nuevo usuario"""
        try:
            # Crear usuario en Supabase Auth
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                # El trigger grant_initial_credits ya dio los 10 créditos gratis
                return {
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email
                    },
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "expires_in": response.session.expires_in
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Signup failed"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login de usuario"""
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                return {
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email
                    },
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "expires_in": response.session.expires_in
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    
    async def verify_token(self, token: str) -> Optional[str]:
        """Verificar JWT y retornar user_id"""
        try:
            response = self.supabase.auth.get_user(token)
            if response.user:
                return response.user.id
            return None
        except Exception:
            return None

auth_service = AuthService()
