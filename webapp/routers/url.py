from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
import uuid
from mangadex_downloader.cli import main as cli_main


router = APIRouter(prefix="/api/url", tags=["url"])


class UrlDownloadRequest(BaseModel):
    url: str
    save_as: str | None = None
    path: str | None = None
    log_level: str | None = None
    no_track: bool | None = None


_jobs: dict[str, dict] = {}


async def _run(job_id: str, req: UrlDownloadRequest):
    _jobs[job_id]["status"] = "running"
    argv = []
    if req.save_as:
        argv += ["--save-as", req.save_as]
    if req.path:
        # Always use chapter title to create separate manga folders
        argv += ["--path", req.path]
        argv += ["--use-chapter-title"]  # Auto create manga folder
    if req.log_level:
        argv += ["--log-level", req.log_level]
    if req.no_track:
        argv += ["--no-track"]
    argv += [req.url]

    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, cli_main, argv)
        _jobs[job_id]["status"] = "done"
        _jobs[job_id]["message"] = "Download completed! Files saved in separate manga folder."
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
