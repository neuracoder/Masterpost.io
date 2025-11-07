from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Optional

from ..models.schemas import ProcessRequest, ProcessResponse, JobStatus, PipelineType
from ..database.memory_client import memory_db
from ..processing.batch_handler import start_batch_processing
from ..core.security import get_current_user

router = APIRouter()

@router.post("/process", response_model=ProcessResponse)
async def process_images(
    request: ProcessRequest,
    background_tasks: BackgroundTasks
):
    job = memory_db.get_job(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # If no pipeline is provided, default to 'amazon' for testing
    if not request.pipeline:
        request.pipeline = PipelineType.AMAZON

    # Skip user validation for testing
    # if job.get("user_id") != user_id:
    #     raise HTTPException(status_code=403, detail="Access denied")

    if job.get("status") != "uploaded":
        raise HTTPException(
            status_code=400,
            detail=f"Job cannot be processed. Current status: {job.get('status')}"
        )

    valid_pipelines = [p.value for p in PipelineType]
    if request.pipeline not in valid_pipelines:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid pipeline. Available: {', '.join(valid_pipelines)}"
        )

    memory_db.update_job(request.job_id, {
        "status": "processing",
        "pipeline": request.pipeline,
        "settings": request.settings
    })

    background_tasks.add_task(
        start_batch_processing,
        job_id=request.job_id,
        pipeline=request.pipeline,
        settings=request.settings
    )

    return ProcessResponse(
        job_id=request.job_id,
        message="Processing started",
        pipeline=request.pipeline,
        status="processing",
        estimated_time_minutes=job.get("total_files", 0) * 2  # 2 seconds per image estimate
    )

@router.get("/status/{job_id}", response_model=JobStatus)
async def get_job_status(
    job_id: str
):
    job = memory_db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Skip user validation for testing
    # if job.get("user_id") != user_id:
    #     raise HTTPException(status_code=403, detail="Access denied")

    total_files = job.get("total_files", 0)
    processed_files = job.get("processed_files", 0)

    return JobStatus(
        job_id=job.get("job_id"),
        status=job.get("status"),
        total_files=total_files,
        processed_files=processed_files,
        failed_files=job.get("failed_files", 0),
        progress_percentage=round(processed_files / total_files * 100, 2) if total_files > 0 else 0,
        created_at=job.get("created_at"),
        updated_at=job.get("updated_at"),
        pipeline=job.get("pipeline"),
        error_message=job.get("error_message")
    )

@router.get("/pipelines")
async def get_available_pipelines():
    return {
        "pipelines": [
            {
                "id": "amazon",
                "name": "Amazon Compliant",
                "description": "White background, 1000x1000px, 85% product coverage",
                "features": ["White background removal", "Square format", "Product centering", "Quality optimization"]
            },
            {
                "id": "instagram",
                "name": "Instagram Ready",
                "description": "1080x1080px square format with color enhancement",
                "features": ["Square crop", "Color boost", "Contrast enhancement", "Social media optimization"]
            },
            {
                "id": "ebay",
                "name": "eBay Optimized",
                "description": "1600x1600px high resolution for detailed product view",
                "features": ["High resolution", "Detail enhancement", "Multiple angle support", "Zoom optimization"]
            }
        ]
    }

@router.post("/process-test", response_model=ProcessResponse)
async def process_images_test(
    request: ProcessRequest,
    background_tasks: BackgroundTasks
):
    """Testing endpoint without authentication for development"""
    job = memory_db.get_job(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Skip user validation for testing

    if job.get("status") != "uploaded":
        raise HTTPException(
            status_code=400,
            detail=f"Job cannot be processed. Current status: {job.get('status')}"
        )

    valid_pipelines = ["amazon", "instagram", "ebay"]
    if request.pipeline not in valid_pipelines:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid pipeline. Available: {', '.join(valid_pipelines)}"
        )

    memory_db.update_job(request.job_id, {
        "status": "processing",
        "pipeline": request.pipeline,
        "settings": request.settings
    })

    background_tasks.add_task(
        start_batch_processing,
        job_id=request.job_id,
        pipeline=request.pipeline,
        settings=request.settings
    )

    return ProcessResponse(
        job_id=request.job_id,
        message="Processing started",
        pipeline=request.pipeline,
        status="processing",
        estimated_time_minutes=job.get("total_files", 0) * 2  # 2 seconds per image estimate
    )

@router.get("/status-test/{job_id}", response_model=JobStatus)
async def get_job_status_test(
    job_id: str
):
    """Testing endpoint without authentication for development"""
    job = memory_db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Skip user validation for testing

    total_files = job.get("total_files", 0)
    processed_files = job.get("processed_files", 0)

    return JobStatus(
        job_id=job.get("job_id"),
        status=job.get("status"),
        total_files=total_files,
        processed_files=processed_files,
        failed_files=job.get("failed_files", 0),
        progress_percentage=round(processed_files / total_files * 100, 2) if total_files > 0 else 0,
        created_at=job.get("created_at"),
        updated_at=job.get("updated_at"),
        pipeline=job.get("pipeline"),
        error_message=job.get("error_message")
    )

@router.post("/cancel/{job_id}")
async def cancel_job(
    job_id: str
):
    job = memory_db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Skip user validation for testing
    # if job.get("user_id") != user_id:
    #     raise HTTPException(status_code=403, detail="Access denied")

    if job.get("status") not in ["uploaded", "processing"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job with status: {job.get('status')}"
        )

    memory_db.update_job(job_id, {"status": "cancelled"})

    return {"message": "Job cancelled successfully", "job_id": job_id}