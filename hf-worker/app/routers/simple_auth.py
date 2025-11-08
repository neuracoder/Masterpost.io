"""
Simple authentication endpoints for V1 compatibility
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime, timedelta

router = APIRouter()

# Simple token store for demo purposes
DEMO_TOKENS = {}

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str

class UserRegistration(BaseModel):
    email: str
    password: str
    full_name: str

@router.post("/login", response_model=LoginResponse)
async def login_demo(request: LoginRequest):
    """Demo login endpoint that accepts any credentials"""

    # For demo purposes, accept any email/password
    if not request.email or not request.password:
        raise HTTPException(status_code=400, detail="Email and password required")

    # Generate demo token
    token = f"demo_token_{uuid.uuid4().hex[:16]}"
    user_id = f"user_{uuid.uuid4().hex[:8]}"

    # Store token (in production, use proper JWT)
    DEMO_TOKENS[token] = {
        "user_id": user_id,
        "email": request.email,
        "expires": datetime.now() + timedelta(hours=24)
    }

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user_id=user_id,
        email=request.email
    )

@router.post("/register", response_model=LoginResponse)
async def register_demo(request: UserRegistration):
    """Demo registration endpoint"""

    if not request.email or not request.password:
        raise HTTPException(status_code=400, detail="Email and password required")

    # Generate demo token
    token = f"demo_token_{uuid.uuid4().hex[:16]}"
    user_id = f"user_{uuid.uuid4().hex[:8]}"

    # Store token
    DEMO_TOKENS[token] = {
        "user_id": user_id,
        "email": request.email,
        "full_name": request.full_name,
        "expires": datetime.now() + timedelta(hours=24)
    }

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user_id=user_id,
        email=request.email
    )

@router.get("/me")
async def get_current_user_info():
    """Get current user info"""
    return {
        "user_id": "demo_user",
        "email": "demo@masterpost.io",
        "plan": "free",
        "status": "active"
    }

def validate_demo_token(token: str) -> dict:
    """Validate demo token"""
    if not token:
        return None

    # Remove 'Bearer ' prefix if present
    if token.startswith('Bearer '):
        token = token[7:]

    # For demo purposes, accept any token that starts with 'demo'
    if token.startswith('demo'):
        return {
            "user_id": "demo_user",
            "email": "demo@masterpost.io",
            "plan": "free"
        }

    # Check stored tokens
    token_data = DEMO_TOKENS.get(token)
    if token_data and token_data["expires"] > datetime.now():
        return token_data

    return None