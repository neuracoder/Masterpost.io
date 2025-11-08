from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Masterpost.io API"
    VERSION: str = "1.0.0"

    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://masterpost.io",
        "https://*.masterpost.io"
    ]

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Supabase Configuration
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # File Upload Configuration
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    MAX_FILES_PER_JOB: int = 500
    UPLOAD_DIR: str = "uploads"
    PROCESSED_DIR: str = "processed"

    # Redis Configuration (for Celery)
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Image Processing Configuration
    DEFAULT_AMAZON_SIZE: tuple = (1000, 1000)
    DEFAULT_INSTAGRAM_SIZE: tuple = (1080, 1080)
    DEFAULT_EBAY_SIZE: tuple = (1600, 1600)
    JPEG_QUALITY: int = 95
    PNG_COMPRESSION: int = 6

    # AI APIs (Optional for future features)
    CLAUDE_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    DASHSCOPE_API_KEY: str = ""

    # Payment Configuration
    MERCADOPAGO_ACCESS_TOKEN: str = ""
    MERCADOPAGO_PUBLIC_KEY: str = ""
    MERCADOPAGO_SANDBOX: bool = True

    # Stripe Configuration
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # Frontend/Backend URLs
    FRONTEND_URL: str = "http://localhost:3002"
    BACKEND_URL: str = "http://127.0.0.1:8002"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
        # Priorizar .env sobre variables de entorno del sistema
        env_prefix = ""

def get_settings() -> Settings:
    """
    Cargar settings con manejo de errores
    """
    try:
        return Settings(_env_file=".env", _env_file_encoding="utf-8")
    except Exception as e:
        print(f"Warning: Error cargando settings: {e}")
        print("Usando valores por defecto...")
        # Si falla, usar valores por defecto seguros
        return Settings(
            PORT=8002,
            ENVIRONMENT="development",
            DEBUG=True,
            LOG_LEVEL="INFO"
        )

# Instancia global
settings = get_settings()