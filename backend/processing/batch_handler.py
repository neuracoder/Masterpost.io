import asyncio
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from processing.image_processor import ImageProcessor
from processing.pipelines import PipelineFactory
from app.database.memory_client import memory_db
from services.simple_processing import remove_background_simple

logger = logging.getLogger(__name__)

class BatchProcessor:
    def __init__(self):
        self.processor = ImageProcessor()
        self.active_jobs: Dict[str, bool] = {}

    async def process_job(
        self,
        job_id: str,
        pipeline_type: str,
        settings: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Process a batch job with the specified pipeline"""

        if job_id in self.active_jobs:
            logger.warning(f"Job {job_id} is already being processed")
            return False

        self.active_jobs[job_id] = True

        try:
            # Get job details from database
            job = memory_db.get_job(job_id)
            if not job:
                logger.error(f"Job {job_id} not found")
                return False

            # Create pipeline
            pipeline = PipelineFactory.create_pipeline(pipeline_type, self.processor)

            # Setup directories
            upload_dir = Path("uploads") / job_id
            processed_dir = Path("processed") / job_id
            processed_dir.mkdir(parents=True, exist_ok=True)

            if not upload_dir.exists():
                logger.error(f"Upload directory not found: {upload_dir}")
                memory_db.update_job(job_id, {"status": "failed", "error_message": "Upload directory not found"})
                return False

            # Get all image files
            image_files = [
                f for f in upload_dir.iterdir()
                if f.is_file() and f.suffix.lower() in self.processor.supported_formats
            ]

            if not image_files:
                logger.error(f"No valid image files found in {upload_dir}")
                memory_db.update_job(job_id, {"status": "failed", "error_message": "No valid image files found"})
                return False

            total_files = len(image_files)
            processed_count = 0
            failed_count = 0

            logger.info(f"Starting batch processing for job {job_id}: {total_files} files")

            # Process images one by one
            for image_file in image_files:
                try:
                    # Generate output filename
                    output_filename = f"{pipeline_type}_{image_file.stem}.jpg"
                    output_path = processed_dir / output_filename

                    # Use simple background removal directly
                    success = remove_background_simple(str(image_file), str(output_path))

                    if success:
                        processed_count += 1
                        logger.debug(f"Processed {image_file.name} -> {output_filename}")
                    else:
                        failed_count += 1
                        logger.error(f"Failed to process image: {output_filename}")

                except Exception as e:
                    failed_count += 1
                    logger.error(f"Error processing {image_file.name}: {str(e)}")

                # Update progress
                memory_db.update_job(job_id, {
                    "processed_files": processed_count + failed_count,
                    "failed_files": failed_count
                })

                # Add small delay to prevent system overload
                await asyncio.sleep(0.1)

            # Final status update
            if failed_count == 0:
                memory_db.update_job(job_id, {"status": "completed"})
                logger.info(f"Job {job_id} completed successfully: {processed_count} files processed")
            elif processed_count > 0:
                memory_db.update_job(job_id, {
                    "status": "completed_with_errors",
                    "error_message": f"Processed {processed_count} files, {failed_count} failed"
                })
                logger.warning(f"Job {job_id} completed with errors: {processed_count} success, {failed_count} failed")
            else:
                memory_db.update_job(job_id, {"status": "failed", "error_message": "All files failed to process"})
                logger.error(f"Job {job_id} failed: all files failed to process")

            return processed_count > 0

        except Exception as e:
            logger.error(f"Critical error in job {job_id}: {str(e)}")
            memory_db.update_job(job_id, {"status": "failed", "error_message": str(e)})
            return False

        finally:
            # Remove from active jobs
            self.active_jobs.pop(job_id, None)

class QueueManager:
    def __init__(self):
        self.processor = BatchProcessor()
        self.queue: List[Dict[str, Any]] = []
        self.processing = False

    async def add_job(
        self,
        job_id: str,
        pipeline_type: str,
        settings: Optional[Dict[str, Any]] = None,
        priority: int = 0
    ):
        """Add a job to the processing queue"""
        job_item = {
            'job_id': job_id,
            'pipeline_type': pipeline_type,
            'settings': settings or {},
            'priority': priority,
            'added_at': datetime.utcnow()
        }

        # Insert based on priority (higher priority first)
        inserted = False
        for i, item in enumerate(self.queue):
            if priority > item['priority']:
                self.queue.insert(i, job_item)
                inserted = True
                break

        if not inserted:
            self.queue.append(job_item)

        logger.info(f"Job {job_id} added to queue (priority: {priority}). Queue length: {len(self.queue)}")

        # Start processing if not already running
        if not self.processing:
            asyncio.create_task(self._process_queue())

    async def _process_queue(self):
        """Process jobs in the queue"""
        if self.processing:
            return

        self.processing = True

        try:
            while self.queue:
                job_item = self.queue.pop(0)
                logger.info(f"Processing job {job_item['job_id']} from queue")

                try:
                    success = await self.processor.process_job(
                        job_item['job_id'],
                        job_item['pipeline_type'],
                        job_item['settings']
                    )

                    if success:
                        logger.info(f"Job {job_item['job_id']} processed successfully")
                    else:
                        logger.error(f"Job {job_item['job_id']} processing failed")

                except Exception as e:
                    logger.error(f"Error processing job {job_item['job_id']}: {str(e)}")

        finally:
            self.processing = False

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            'queue_length': len(self.queue),
            'processing': self.processing,
            'active_jobs': list(self.processor.active_jobs.keys()),
            'next_jobs': [item['job_id'] for item in self.queue[:5]]  # Next 5 jobs
        }

# Global queue manager instance
queue_manager = QueueManager()

async def start_batch_processing(
    job_id: str,
    pipeline: str,
    settings: Optional[Dict[str, Any]] = None
):
    """Start batch processing for a job (called from router)"""
    await queue_manager.add_job(job_id, pipeline, settings)

async def get_queue_status():
    """Get current queue status"""
    return queue_manager.get_queue_status()