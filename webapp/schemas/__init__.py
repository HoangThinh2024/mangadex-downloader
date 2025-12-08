"""Pydantic schemas for request/response validation"""

from .manga import MangaSchema, MangaDetailSchema, ChapterSchema, AuthorSchema, ArtistSchema
from .search import SearchRequestSchema, SearchResponseSchema
from .download import DownloadRequestSchema, JobStatusSchema
from .config import ConfigSchema

__all__ = [
    "MangaSchema",
    "MangaDetailSchema",
    "ChapterSchema",
    "AuthorSchema",
    "ArtistSchema",
    "SearchRequestSchema",
    "SearchResponseSchema",
    "DownloadRequestSchema",
    "JobStatusSchema",
    "ConfigSchema",
]
