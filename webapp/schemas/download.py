"""Download related schemas"""

from pydantic import BaseModel
from typing import Optional


class DownloadRequestSchema(BaseModel):
    """Download request parameters"""
    url: str
    save_as: Optional[str] = None
    path: Optional[str] = None
    manga_title: Optional[str] = None
    chapters: Optional[str] = None
    start_chapter: Optional[str] = None
    end_chapter: Optional[str] = None
    start_page: Optional[int] = None
    end_page: Optional[int] = None
    start_volume: Optional[str] = None
    end_volume: Optional[str] = None
    language: Optional[str] = None
    groups: Optional[str] = None
    no_track: bool = False
    log_level: Optional[str] = None


class JobStatusSchema(BaseModel):
    """Job status information"""
    job_id: str
    status: str
    manga_title: Optional[str] = None
    url: Optional[str] = None
    progress: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
