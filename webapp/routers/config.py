from fastapi import APIRouter
from pydantic import BaseModel
from mangadex_downloader.cli.config import build_config
from mangadex_downloader.cli.args_parser import get_args


router = APIRouter(prefix="/api/config", tags=["config"])


class ConfigUpdate(BaseModel):
    # Accept minimal common options; extend as needed
    save_as: str | None = None
    path: str | None = None
    no_track: bool | None = None
    log_level: str | None = None


@router.get("")
def get_current():
    # Build args with no argv to load defaults and env/user config
    parser, args = get_args([])
    build_config(parser, args)
    return {
        "save_as": args.save_as,
        "path": args.path,
        "no_track": args.no_track,
        "log_level": args.log_level,
    }


@router.put("")
def update_config(update: ConfigUpdate):
    # Translate provided fields into argv flags and let CLI write config
    argv: list[str] = []
    if update.save_as:
        argv += ["--save-as", update.save_as]
    if update.path:
        argv += ["--path", update.path]
    if update.no_track is True:
        argv += ["--no-track"]
    if update.log_level:
        argv += ["--log-level", update.log_level]

    parser, args = get_args(argv)
    build_config(parser, args)
    return {"status": "ok"}
