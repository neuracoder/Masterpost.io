"""
Masterpost Worker - Image Processing Logic
Handles background removal and shadow effects using rembg
"""

import os
import tempfile
import logging
from pathlib import Path
from rembg import remove, new_session
from PIL import Image
import httpx
from typing import Optional

# Supabase client
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# Import shadow effects
from services.shadow_effects import apply_simple_drop_shadow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if SUPABASE_AVAILABLE and SUPABASE_URL and SUPABASE_SERVICE_KEY:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        logger.info("✓ Supabase client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        supabase = None
else:
    logger.warning("⚠ Supabase not configured - storage features disabled")
    supabase = None

# Pre-load rembg model for better performance
logger.info("Pre-loading U2-Net model for rembg...")
try:
    REMBG_SESSION = new_session("u2net")
    logger.info("✓ U2-Net model loaded successfully")
except Exception as e:
    logger.error(f"Failed to pre-load model: {e}")
    REMBG_SESSION = None

async def process_image_job(
    job_id: str,
    image_url: str,
    pipeline: str,
    shadow_type: Optional[str],
    enable_shadows: bool,
    shadow_intensity: float = 0.5
):
    """
    Process an image job: download, remove background, apply effects, upload result

    Args:
        job_id: Unique job identifier
        image_url: URL of the image to process
        pipeline: Processing pipeline (amazon/ebay/instagram/none)
        shadow_type: Type of shadow effect (drop/reflection/natural/none)
        enable_shadows: Whether to apply shadow effects
        shadow_intensity: Shadow intensity (0.0-1.0)
    """
    try:
        logger.info("=" * 80)
        logger.info(f"Starting job {job_id}")
        logger.info(f"  Image URL: {image_url}")
        logger.info(f"  Pipeline: {pipeline}")
        logger.info(f"  Shadow: {shadow_type if enable_shadows else 'disabled'}")
        logger.info(f"  Intensity: {shadow_intensity}")
        logger.info("=" * 80)

        # Update job status to "processing"
        update_job_status(job_id, "processing", 10)

        # 1. Download image from URL
        logger.info(f"[1/5] Downloading image from {image_url}")
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(image_url)
            response.raise_for_status()
            image_data = response.content
            logger.info(f"✓ Downloaded {len(image_data)} bytes")

        update_job_status(job_id, "processing", 30)

        # 2. Save to temporary file (HF Spaces only allows writing to /tmp)
        logger.info("[2/5] Saving to temporary file")
        with tempfile.NamedTemporaryFile(suffix=".jpg", dir="/tmp", delete=False) as tmp_input:
            tmp_input.write(image_data)
            tmp_input.flush()
            input_path = tmp_input.name
            logger.info(f"✓ Saved to {input_path}")

        try:
            # 3. Remove background with rembg
            logger.info("[3/5] Removing background with rembg")
            with Image.open(input_path) as img:
                logger.info(f"  Original size: {img.size}")

                # Remove background
                if REMBG_SESSION:
                    output = remove(img, session=REMBG_SESSION)
                    logger.info("  Using pre-loaded session")
                else:
                    output = remove(img)
                    logger.info("  Using default session")

                # Ensure RGBA mode
                if output.mode != 'RGBA':
                    output = output.convert('RGBA')

                logger.info(f"✓ Background removed, output mode: {output.mode}")

            update_job_status(job_id, "processing", 60)

            # 4. Apply shadow effects if enabled
            if enable_shadows and shadow_type and shadow_type != "none":
                logger.info(f"[4/5] Applying {shadow_type} shadow (intensity: {shadow_intensity})")

                try:
                    output = apply_simple_drop_shadow(
                        image=output,
                        intensity=shadow_intensity
                    )
                    logger.info(f"✓ Shadow applied successfully")
                except Exception as shadow_error:
                    logger.error(f"Shadow application failed: {shadow_error}")
                    logger.info("  Falling back to white background without shadow")
                    # Create white background as fallback
                    white_bg = Image.new('RGB', output.size, (255, 255, 255))
                    white_bg.paste(output, (0, 0), output)
                    output = white_bg
            else:
                logger.info("[4/5] No shadow - creating white background")
                # Create white background
                white_bg = Image.new('RGB', output.size, (255, 255, 255))
                white_bg.paste(output, (0, 0), output)
                output = white_bg

            update_job_status(job_id, "processing", 80)

            # 5. Save result
            logger.info("[5/5] Saving processed result")
            result_path = f"/tmp/{job_id}_result.jpg"
            output.save(result_path, "JPEG", quality=95)
            logger.info(f"✓ Result saved to {result_path}")

            # 6. Upload to Supabase Storage (if available)
            result_url = None
            if supabase:
                logger.info("Uploading result to Supabase Storage")
                try:
                    with open(result_path, "rb") as f:
                        file_data = f.read()

                    # Upload to 'processed' bucket
                    filename = f"{job_id}_result.jpg"
                    upload_result = supabase.storage.from_("processed").upload(
                        filename,
                        file_data,
                        {"content-type": "image/jpeg", "upsert": "true"}
                    )

                    # Get public URL
                    result_url = supabase.storage.from_("processed").get_public_url(filename)
                    logger.info(f"✓ Uploaded to: {result_url}")

                except Exception as upload_error:
                    logger.error(f"Upload to Supabase failed: {upload_error}")
                    logger.info("  Job will complete without storage URL")
            else:
                logger.warning("⚠ Supabase not available, cannot upload result")

            # 7. Update job status to completed
            update_job_status(job_id, "completed", 100, result_url)

            # 8. Cleanup temporary files
            logger.info("Cleaning up temporary files")
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(result_path):
                os.remove(result_path)

            logger.info("=" * 80)
            logger.info(f"✓ Job {job_id} completed successfully")
            logger.info("=" * 80)

        finally:
            # Ensure temp input file is always cleaned up
            if os.path.exists(input_path):
                os.remove(input_path)

    except httpx.HTTPError as http_error:
        logger.error(f"HTTP error downloading image: {http_error}")
        update_job_status(job_id, "failed", 0, error=f"Download failed: {str(http_error)}")
    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}", exc_info=True)
        update_job_status(job_id, "failed", 0, error=str(e))

def update_job_status(
    job_id: str,
    status: str,
    progress: int,
    result_url: Optional[str] = None,
    error: Optional[str] = None
):
    """
    Update job status in Supabase database

    Args:
        job_id: Job identifier
        status: Job status (processing/completed/failed)
        progress: Progress percentage (0-100)
        result_url: URL of processed result (optional)
        error: Error message if failed (optional)
    """
    if not supabase:
        logger.warning(f"Cannot update job {job_id}: Supabase not configured")
        logger.info(f"  Status: {status}, Progress: {progress}%")
        return

    try:
        # Prepare update data
        data = {
            "status": status,
            "progress": progress
        }

        if result_url:
            data["result_url"] = result_url

        if error:
            data["error"] = error

        # Update job in database
        result = supabase.table("jobs").update(data).eq("id", job_id).execute()

        logger.info(f"Job {job_id} status updated: {status} ({progress}%)")

        if result_url:
            logger.info(f"  Result URL: {result_url}")

        if error:
            logger.error(f"  Error: {error}")

    except Exception as e:
        logger.error(f"Failed to update job {job_id} in database: {str(e)}")
