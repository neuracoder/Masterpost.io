from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from .config.supabase_config import get_supabase
from .routers import upload, auth_routes, credit_routes, payment_routes
# Temporalmente deshabilitados por falta de schemas:
# from .routers import process, download, test_routes, simple_auth, image_editor, manual_editor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Masterpost.io API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
# Temporalmente deshabilitados:
# app.include_router(process.router)
# app.include_router(download.router)
# app.include_router(test_routes.router)
# app.include_router(simple_auth.router)
# app.include_router(image_editor.router)
# app.include_router(manual_editor.router)

# Include Stripe payment routers
app.include_router(auth_routes.router)
app.include_router(credit_routes.router)
app.include_router(payment_routes.router)

@app.get("/")
async def root():
    return {"message": "Masterpost.io API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    supabase = get_supabase()
    supabase_status = "connected" if supabase else "disconnected"
    
    return {
        "status": "healthy",
        "supabase": supabase_status,
        "version": "1.0.0"
    }

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Masterpost.io API")
    
    supabase = get_supabase()
    if supabase:
        logger.info("✅ Supabase connection initialized successfully")
    else:
        logger.warning("❌ Supabase connection failed - running in limited mode")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
