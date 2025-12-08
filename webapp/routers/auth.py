import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from mangadex_downloader.auth.oauth2 import OAuth2


router = APIRouter(prefix="/auth", tags=["auth"])


def _get_oauth():
    client_id = os.getenv("MANGADEX_CLIENT_ID")
    client_secret = os.getenv("MANGADEX_CLIENT_SECRET")
    redirect_uri = os.getenv("MANGADEX_REDIRECT_URI", "http://localhost:8000/auth/callback")
    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="Missing MangaDex OAuth env vars")
    return OAuth2(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)


@router.get("/login")
def login(_: Request):
    oauth = _get_oauth()
    url = oauth.get_authorize_url()
    return RedirectResponse(url)


@router.get("/callback")
def callback(request: Request, code: str | None = None, state: str | None = None):
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")
    oauth = _get_oauth()
    token = oauth.get_access_token(code)
    # Store token in session via signed cookie
    request.session["md_token"] = token
    return RedirectResponse("/")
