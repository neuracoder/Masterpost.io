from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Auth
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Credits
class UseCreditsRequest(BaseModel):
    credits: int
    transaction_type: str = "usage_basic"
    description: Optional[str] = None

# Payments
class CheckoutRequest(BaseModel):
    pack_type: str  # 'PRO' o 'BUSINESS'

# Upload
class UploadResponse(BaseModel):
    job_id: str
    message: str
    files_uploaded: int
    job_status: str

class JobCreate(BaseModel):
    user_id: str
    pipeline: str
    total_files: int
    is_zip_upload: bool
    original_filename: str
    files: List[Dict[str, Any]]

class JobResponse(BaseModel):
    id: str
    user_id: str
    pipeline: str
    total_files: int
    created_at: datetime

# Process
class PipelineType(str, Enum):
    AMAZON = "amazon"
    ETSY = "etsy"
    EBAY = "ebay"
    INSTAGRAM = "instagram"

class ProcessRequest(BaseModel):
    job_id: str
    pipeline: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class ProcessResponse(BaseModel):
    job_id: str
    message: str
    pipeline: str
    status: str
    estimated_time_minutes: int

class JobStatus(BaseModel):
    job_id: str
    status: str
    total_files: int
    processed_files: int
    progress_percentage: float
    current_file: Optional[str] = None
    pipeline: Optional[str] = None

# Download
class DownloadResponse(BaseModel):
    job_id: str
    status: str
    download_ready: bool
    files_count: int
    total_size_mb: float
    download_url: Optional[str] = None
    zip_filename: Optional[str] = None
