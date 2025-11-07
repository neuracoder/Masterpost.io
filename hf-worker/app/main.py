"""
Masterpost Worker - FastAPI Server
Background removal and shadow effects service for Masterpost.io
Optimized for Hugging Face Spaces deployment
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import logging
from typing import Optional
from worker import process_image_job

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Masterpost Worker",
    description="Image processing worker for Masterpost.io - Background removal and shadow effects",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
logger.info(f"CORS allowed origins: {ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Pydantic models
class JobRequest(BaseModel):
    """Image processing job request"""
    job_id: str = Field(..., description="Unique job identifier")
    image_url: str = Field(..., description="URL of image in Supabase Storage")
    pipeline: str = Field(default="amazon", description="Processing pipeline: amazon, ebay, instagram, none")
    shadow_type: Optional[str] = Field(default="drop", description="Shadow type: drop, reflection, natural, none")
    enable_shadows: bool = Field(default=True, description="Enable shadow effects")
    shadow_intensity: Optional[float] = Field(default=0.5, description="Shadow intensity (0.0-1.0)")

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "550e8400-e29b-41d4-a716-446655440000",
                "image_url": "https://your-project.supabase.co/storage/v1/object/public/uploads/image.jpg",
                "pipeline": "amazon",
                "shadow_type": "drop",
                "enable_shadows": True,
                "shadow_intensity": 0.5
            }
        }

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    rembg_available: bool

class JobResponse(BaseModel):
    """Job acceptance response"""
    status: str
    job_id: str
    message: str

# API Endpoints

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Masterpost Worker",
        "version": "1.0.0",
        "status": "running",
        "description": "Background removal and shadow effects service",
        "endpoints": {
            "health": "GET /health",
            "process": "POST /process",
            "docs": "GET /docs"
        },
        "pipelines": ["amazon", "ebay", "instagram", "none"],
        "shadow_types": ["drop", "reflection", "natural", "none"]
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring

    Returns:
        Health status including rembg availability
    """
    # Check if rembg is available
    try:
        from rembg import remove
        rembg_available = True
        logger.info("Health check: rembg is available")
    except ImportError as e:
        rembg_available = False
        logger.error(f"Health check: rembg not available - {e}")

    return {
        "status": "healthy" if rembg_available else "degraded",
        "service": "masterpost-worker",
        "version": "1.0.0",
        "rembg_available": rembg_available
    }

@app.post("/process", response_model=JobResponse, tags=["Processing"])
async def process_job(
    job: JobRequest,
    background_tasks: BackgroundTasks
):
    """
    Accept an image processing job and execute it in the background

    Args:
        job: Job request with image URL and processing parameters
        background_tasks: FastAPI background tasks manager

    Returns:
        Job acceptance confirmation

    Raises:
        HTTPException: If job parameters are invalid
    """
    try:
        # Validate job parameters
        if not job.job_id or not job.image_url:
            raise HTTPException(
                status_code=400,
                detail="Missing required fields: job_id and image_url are required"
            )

        # Validate pipeline
        valid_pipelines = ["amazon", "ebay", "instagram", "none"]
        if job.pipeline not in valid_pipelines:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid pipeline '{job.pipeline}'. Must be one of: {valid_pipelines}"
            )

        # Validate shadow type
        valid_shadow_types = ["drop", "reflection", "natural", "none"]
        if job.shadow_type and job.shadow_type not in valid_shadow_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid shadow_type '{job.shadow_type}'. Must be one of: {valid_shadow_types}"
            )

        # Validate shadow intensity
        if job.shadow_intensity is not None and not (0.0 <= job.shadow_intensity <= 1.0):
            raise HTTPException(
                status_code=400,
                detail="shadow_intensity must be between 0.0 and 1.0"
            )

        logger.info(f"Accepting job {job.job_id} for processing")
        logger.info(f"  Pipeline: {job.pipeline}")
        logger.info(f"  Shadow: {job.shadow_type if job.enable_shadows else 'disabled'}")
        logger.info(f"  Intensity: {job.shadow_intensity}")

        # Add job to background tasks queue
        background_tasks.add_task(
            process_image_job,
            job.job_id,
            job.image_url,
            job.pipeline,
            job.shadow_type,
            job.enable_shadows,
            job.shadow_intensity
        )

        return {
            "status": "accepted",
            "job_id": job.job_id,
            "message": f"Job queued for processing with {job.pipeline} pipeline"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error accepting job {job.job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to queue job: {str(e)}"
        )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 60)
    logger.info("Masterpost Worker starting up...")
    logger.info(f"Port: {os.getenv('PORT', 7860)}")
    logger.info(f"Allowed origins: {ALLOWED_ORIGINS}")

    # Check Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

    if supabase_url and supabase_key:
        logger.info("✓ Supabase credentials configured")
    else:
        logger.warning("⚠ Supabase credentials not configured")

    # Check rembg availability
    try:
        from rembg import new_session
        logger.info("✓ rembg library available")
        logger.info("Pre-loading U2-Net model...")
        # Pre-load model at startup (this will be cached in worker.py)
    except ImportError as e:
        logger.error(f"✗ rembg not available: {e}")

    logger.info("Masterpost Worker ready!")
    logger.info("=" * 60)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Masterpost Worker shutting down...")

# Run with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))

    logger.info(f"Starting server on port {port}...")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False
    )
