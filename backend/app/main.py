from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import time
import asyncio
import logging
import zipfile
import tempfile
import threading
import io
import uuid
from pathlib import Path
from typing import List, Dict, Any

from .routers import upload, process, download, test_routes, simple_auth, image_editor, manual_editor
try:
    from .routers import hybrid_routes, auth_routes
    v2_available = True
except ImportError as e:
    print(f"V2 routes not available: {e}")
    v2_available = False

# Credit system API routes
try:
    from .api import auth as credit_auth, credits, payments
    credit_system_available = True
except ImportError as e:
    print(f"Credit system routes not available: {e}")
    credit_system_available = False

from .core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory progress tracking
JOB_PROGRESS = {}
progress_lock = threading.Lock()

def update_progress(job_id: str, current: int, total: int, status: str = "processing"):
    """Update job progress in memory"""
    with progress_lock:
        JOB_PROGRESS[job_id] = {
            "current": current,
            "total": total,
            "percentage": int((current / total * 100)) if total > 0 else 0,
            "status": status,
            "updated_at": time.time()
        }

app = FastAPI(
    title="Masterpost.io API - Unified",
    description="Unified backend for image processing, authentication, and payment processing",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8002",
        "https://masterpost.io",
        "https://www.masterpost.io",
        "https://*.masterpost.io",
        "https://*.railway.app",
        "https://*.up.railway.app",
        "https://*.vercel.app",
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta base del proyecto
BASE_DIR = Path(__file__).parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Montar carpetas estáticas del frontend
try:
    if (FRONTEND_DIR / "css").exists():
        app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
    if (FRONTEND_DIR / "js").exists():
        app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")
    if (FRONTEND_DIR / "assets").exists():
        app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")

    # Montar imágenes del backend para la galería
    IMG_ORIGINAL = BASE_DIR / "backend" / "img_original"
    IMG_PROCESADA = BASE_DIR / "backend" / "img_procesada"

    if IMG_ORIGINAL.exists():
        app.mount("/img_original", StaticFiles(directory=str(IMG_ORIGINAL)), name="img_original")
    if IMG_PROCESADA.exists():
        app.mount("/img_procesada", StaticFiles(directory=str(IMG_PROCESADA)), name="img_procesada")
except Exception as e:
    print(f"Warning: Could not mount some static files: {e}")

# Montar carpetas de procesamiento (uploads, processed, static)
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

processed_dir = Path("processed")
processed_dir.mkdir(exist_ok=True)
app.mount("/processed", StaticFiles(directory="processed"), name="processed")

static_dir = Path("static")
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Additional directories for manual editor and temp files
TEMP_DIR = Path("temp")
MANUAL_EDITOR_TEMP_DIR = TEMP_DIR
MANUAL_EDITOR_EDITED_DIR = MANUAL_EDITOR_TEMP_DIR / "edited"
TEMP_DIR.mkdir(exist_ok=True)
MANUAL_EDITOR_EDITED_DIR.mkdir(exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z"}

def validate_upload_file(file: UploadFile) -> bool:
    """Validate uploaded file (image or archive)"""
    if not file.filename:
        return False

    is_image = any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)
    is_archive = any(file.filename.lower().endswith(ext) for ext in ALLOWED_ARCHIVE_EXTENSIONS)

    if not (is_image or is_archive):
        return False

    if is_archive:
        max_size = 500 * 1024 * 1024  # 500MB for archives
    else:
        max_size = 50 * 1024 * 1024   # 50MB for images

    if file.size and file.size > max_size:
        return False

    return True

def is_archive_file(filename: str) -> bool:
    """Check if file is an archive"""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_ARCHIVE_EXTENSIONS)

def format_time(seconds: int) -> str:
    """Format seconds to mm:ss"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"

app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(process.router, prefix="/api/v1", tags=["process"])
app.include_router(download.router, prefix="/api/v1", tags=["download"])
app.include_router(test_routes.router, prefix="/api/v1", tags=["testing"])
app.include_router(simple_auth.router, prefix="/api/v1/auth", tags=["simple-auth"])
app.include_router(image_editor.router, tags=["image-editor"])
app.include_router(manual_editor.router, tags=["manual-editor"])

# Include V2 routes if available
if v2_available:
    app.include_router(auth_routes.router, prefix="/api/v2/auth", tags=["authentication"])
    app.include_router(hybrid_routes.router, prefix="/api/v2", tags=["hybrid"])

# Include Credit System routes
if credit_system_available:
    app.include_router(credit_auth.router, tags=["credit-auth"])
    app.include_router(credits.router, tags=["credits"])
    app.include_router(payments.router, tags=["payments"])

# API Info endpoints
@app.get("/api")
async def api_root():
    return {
        "message": "Masterpost.io API - Unified",
        "version": "2.1.0",
        "docs": "/docs",
        "status": "online"
    }

@app.get("/api/health")
async def api_health_check():
    return {"status": "ok", "service": "masterpost.io", "version": "2.1.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint with service diagnostics"""
    try:
        from rembg import remove
        rembg_available = True
    except ImportError:
        rembg_available = False

    return {
        "status": "healthy",
        "service": "masterpost-api-unified",
        "version": "2.1.0",
        "local_processing": rembg_available,
        "manual_editor": "available",
        "timestamp": time.time()
    }

# Frontend routes - Serve HTML pages
@app.get("/")
async def root():
    """Servir la landing page o info de la API"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    # Fallback al static si existe
    static_index = Path("static/index.html")
    if static_index.exists():
        return FileResponse(str(static_index))
    # API info fallback
    return {
        "message": "Masterpost.io API is running",
        "status": "online",
        "version": "2.1.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/login")
async def login_page():
    """Servir página de login"""
    login_path = FRONTEND_DIR / "login.html"
    if login_path.exists():
        return FileResponse(str(login_path))
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/signup")
async def signup_page():
    """Servir página de registro"""
    signup_path = FRONTEND_DIR / "signup.html"
    if signup_path.exists():
        return FileResponse(str(signup_path))
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/dashboard")
async def dashboard_page():
    """Servir página de dashboard"""
    dashboard_path = FRONTEND_DIR / "dashboard.html"
    if dashboard_path.exists():
        return FileResponse(str(dashboard_path))
    return FileResponse(str(FRONTEND_DIR / "index.html"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    print(f">> Starting Masterpost.io Unified Backend on port {port}...")
    print(f">> API Docs: http://localhost:{port}/docs")
    print(f">> Health: http://localhost:{port}/health")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )