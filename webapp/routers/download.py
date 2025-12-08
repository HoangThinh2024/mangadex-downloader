import asyncio
import uuid
from fastapi import APIRouter
from pydantic import BaseModel

from mangadex_downloader.cli import main as cli_main


class DownloadRequest(BaseModel):
    url: str


router = APIRouter(prefix="/api", tags=["download"])


_jobs: dict[str, dict] = {}


async def _run_download(job_id: str, url: str):
    _jobs[job_id]["status"] = "running"
    try:
        # Run full CLI main with constructed argv (URL only)
        loop = asyncio.get_running_loop()
        def _run():
            # Pass argv with only the URL; CLI will parse defaults
            return cli_main([url])
        await loop.run_in_executor(None, _run)
        _jobs[job_id]["status"] = "done"
        _jobs[job_id]["message"] = "Completed"
    except Exception as exc:
        _jobs[job_id]["status"] = "error"
        _jobs[job_id]["message"] = str(exc)


@router.post("/download")
async def start_download(req: DownloadRequest):
    job_id = uuid.uuid4().hex
    _jobs[job_id] = {"status": "queued", "message": None}
    asyncio.create_task(_run_download(job_id, req.url))
    return {"job_id": job_id, "status": "queued"}


@router.get("/jobs/{job_id}")
def job_status(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        return {"status": "not-found"}
    return {"job_id": job_id, **job}
