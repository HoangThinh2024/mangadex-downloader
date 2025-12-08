"""Manga related schemas"""

from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class ContentRating(str, Enum):
    safe = "safe"
    suggestive = "suggestive"
    erotica = "erotica"
    pornographic = "pornographic"


class AuthorSchema(BaseModel):
    id: str
    name: str
    biography: Optional[str] = None


class ArtistSchema(BaseModel):
    id: str
    name: str
    biography: Optional[str] = None


class TagSchema(BaseModel):
    id: str
    name: str
    group: str


class CoverArtSchema(BaseModel):
    id: str
    url: Optional[str] = None
    file_name: Optional[str] = None
    volume: Optional[str] = None


class MangaSchema(BaseModel):
    """Lightweight manga info for search results"""
    id: str
    title: str
    description: Optional[str] = None
    year: Optional[int] = None
    status: Optional[str] = None
    cover: Optional[str] = None
    content_rating: Optional[str] = None
    last_volume: Optional[str] = None
    last_chapter: Optional[str] = None

    class Config:
        from_attributes = True


class ChapterSchema(BaseModel):
    """Chapter information"""
    id: str
    manga_id: str
    volume: Optional[str] = None
    chapter: str
    title: Optional[str] = None
    language: str
    pages: Optional[int] = None
    groups: Optional[List[str]] = None
    scanlators: Optional[List[str]] = None


class MangaDetailSchema(MangaSchema):
    """Full manga information with details"""
    authors: Optional[List[AuthorSchema]] = None
    artists: Optional[List[ArtistSchema]] = None
    tags: Optional[List[TagSchema]] = None
    alt_titles: Optional[dict] = None
    links: Optional[dict] = None
    rating: Optional[float] = None
    followers: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    original_language: Optional[str] = None
    chapters: Optional[List[ChapterSchema]] = None
    total_chapters: Optional[int] = None

    class Config:
        from_attributes = True
