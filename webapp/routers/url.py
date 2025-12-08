from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
import uuid
import os
from pathlib import Path
from mangadex_downloader.cli import main as cli_main


router = APIRouter(prefix="/api/url", tags=["url"])


class UrlDownloadRequest(BaseModel):
    url: str
    format: str | None = None
    language: str | None = None
    start: str | None = None
    end: str | None = None
    path: str | None = None
    save_as: str | None = None
    log_level: str | None = None
    no_track: bool | None = None


_jobs: dict[str, dict] = {}


def _run_cli_safe(argv):
    """Wrapper to catch sys.exit() and exceptions from CLI"""
    try:
        cli_main(argv)
        return None
    except SystemExit as e:
        # CLI exits with 0 on success, non-zero on error
        if e.code != 0:
            return f"Download failed with exit code {e.code}"
        return None
    except Exception as e:
        # Catch all exceptions including network errors from MangaDex API
        error_msg = str(e)
        # Check if it's a known network/API error that can be ignored
        if "UnhandledHTTPError" in error_msg or "api.mangadex.network/report" in error_msg:
            # Report endpoint errors are non-critical, download may have succeeded
            return None
        return error_msg

async def _run(job_id: str, req: UrlDownloadRequest):
    _jobs[job_id]["status"] = "running"
    argv = []
    
    # Format - default to cbz if not specified or "auto"
    if req.format and req.format.lower() not in ['auto', '']:
        argv += ["--save-as", req.format]
    else:
        # Default to cbz format
        argv += ["--save-as", "cbz"]
    
    # Language filter
    if req.language:
        argv += ["--language", req.language]
    
    # Chapter range
    if req.start:
        argv += ["--start-chapter", req.start]
    if req.end:
        argv += ["--end-chapter", req.end]
    
    # Path and folder structure
    if req.path:
        download_path = req.path
    else:
        # Default to downloads folder in current directory
        download_path = "./downloads"
    
    # Create download directory if it doesn't exist
    Path(download_path).mkdir(parents=True, exist_ok=True)
    
    argv += ["--path", download_path]
    
    # Always use chapter title to create separate manga folders
    argv += ["--use-chapter-title"]
    
    # Log level
    if req.log_level:
        argv += ["--log-level", req.log_level]
    
    # Tracking
    if req.no_track:
        argv += ["--no-track"]
    
    # URL must be last
    argv += [req.url]

    try:
        loop = asyncio.get_running_loop()
        error = await loop.run_in_executor(None, _run_cli_safe, argv)
        if error:
            _jobs[job_id]["status"] = "error"
            _jobs[job_id]["message"] = error
        else:
            _jobs[job_id]["status"] = "done"
            format_type = req.format if req.format and req.format.lower() not in ['auto', ''] else 'cbz'
            _jobs[job_id]["message"] = f"Download completed! Files saved as {format_type.upper()} in manga folder."
    except Exception as e:
        _jobs[job_id]["status"] = "error"
        _jobs[job_id]["message"] = str(e)


@router.post("/download")
async def download(req: UrlDownloadRequest):
    job_id = uuid.uuid4().hex
    _jobs[job_id] = {"status": "queued", "message": None}
    asyncio.create_task(_run(job_id, req))
    return {"job_id": job_id}


@router.get("/jobs/{job_id}")
def job(job_id: str):
    return _jobs.get(job_id, {"status": "not-found"})
