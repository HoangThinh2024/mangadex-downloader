from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
from .routers.download import router as download_router
from .routers.config import router as config_router
from .routers.url import router as url_router
from .routers.search import router as search_router
from .routers.search_advanced import router as search_advanced_router
from .routers.manga import router as manga_router
from .routers.cover import router as cover_router
from .routers.groups import router as groups_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="MangaDex Downloader Web",
        description="A complete web interface for MangaDex Downloader",
        version="1.0.0"
    )

    # Session middleware for storing OAuth tokens
    secret_key = os.getenv("WEBAPP_SESSION_SECRET", "dev-secret-change-me")
    app.add_middleware(SessionMiddleware, secret_key=secret_key)

    app.mount("/static", StaticFiles(directory="webapp/static"), name="static")
    templates = Jinja2Templates(directory="webapp/templates")

    # Core Routers
    app.include_router(download_router)
    app.include_router(config_router)
    app.include_router(url_router)
    
    # Search Routers
    app.include_router(search_router)
    app.include_router(search_advanced_router)
    
    # Manga Detail Routers
    app.include_router(manga_router)
    app.include_router(cover_router)
    
    # Group/Author/Artist Routers
    app.include_router(groups_router)

    @app.get("/health", response_class=HTMLResponse)
    async def health(_: Request):
        return HTMLResponse("OK")

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    return app


app = create_app()
