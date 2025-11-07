from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.schemas import SignupRequest, LoginRequest
from app.services.auth_service import auth_service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/signup")
async def signup(request: SignupRequest):
    """Registrar nuevo usuario"""
    return await auth_service.signup(request.email, request.password)

@router.post("/login")
async def login(request: LoginRequest):
    """Login de usuario"""
    return await auth_service.login(request.email, request.password)

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Dependency para obtener user_id del token"""
    user_id = await auth_service.verify_token(credentials.credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user_id
