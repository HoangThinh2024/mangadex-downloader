"""Search related schemas"""

from pydantic import BaseModel
from typing import Optional, List


class SearchRequestSchema(BaseModel):
    """Search request parameters"""
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    artists: Optional[List[str]] = None
    year: Optional[int] = None
    status: Optional[str] = None
    languages: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    content_rating: Optional[List[str]] = None
    limit: int = 10
    offset: int = 0
    includes: Optional[List[str]] = None

    class Config:
        from_attributes = True


class SearchResponseSchema(BaseModel):
    """Search response"""
    total: int
    limit: int
    offset: int
    data: List[dict]

    class Config:
        from_attributes = True
