"""Advanced search router with filters"""

import logging
from fastapi import APIRouter, Query
from typing import Optional, List

from mangadex_downloader.network import Net

router = APIRouter(prefix="/api/search", tags=["search"])
log = logging.getLogger(__name__)


@router.get("/manga")
async def search_manga(
    title: Optional[str] = Query(None, description="Manga title"),
    authors: Optional[List[str]] = Query(None, description="Author IDs"),
    artists: Optional[List[str]] = Query(None, description="Artist IDs"),
    year: Optional[int] = Query(None, description="Year published"),
    status: Optional[str] = Query(None, description="Publication status"),
    languages: Optional[List[str]] = Query(None, description="Languages"),
    tags: Optional[List[str]] = Query(None, description="Include tags"),
    excluded_tags: Optional[List[str]] = Query(None, description="Exclude tags"),
    content_rating: Optional[List[str]] = Query(None, description="Content rating"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Search manga with advanced filters"""
    
    try:
        params = {
            "title": title,
            "limit": limit,
            "offset": offset,
        }
        
        if year:
            params["year"] = year
        
        if status:
            params["status"] = status
        
        if languages:
            params["translatedLanguage"] = languages
        
        if content_rating:
            params["contentRating"] = content_rating
        
        # Multiple includes for relationships
        includes = ["author", "artist", "cover_art", "manga"]
        params["includes[]"] = includes
        
        # Handle tag filters
        if tags:
            params["includedTags[]"] = tags
        if excluded_tags:
            params["excludedTags[]"] = excluded_tags
        
        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}
        
        result = Net.mangadex.get("/manga", params=params)
        data = result.json()
        
        # Format response
        formatted_data = []
        for item in data.get("data", []):
            attributes = item.get("attributes", {})
            relationships = item.get("relationships", [])
            
            # Get cover image
            cover_url = None
            for rel in relationships:
                if rel.get("type") == "cover_art":
                    file_name = rel.get("attributes", {}).get("fileName")
                    if file_name:
                        cover_url = f"https://uploads.mangadex.org/covers/{item.get('id')}/{file_name}.256.jpg"
                    break
            
            # Get title (prefer English, fallback to first available)
            title_obj = attributes.get("title", {})
            if isinstance(title_obj, dict):
                title_str = title_obj.get("en") or next(iter(title_obj.values()), "Unknown")
            else:
                title_str = str(title_obj)
            
            formatted_data.append({
                "id": item.get("id"),
                "title": title_str,
                "description": attributes.get("description", {}).get("en"),
                "status": attributes.get("status"),
                "year": attributes.get("year"),
                "content_rating": attributes.get("contentRating"),
                "cover": cover_url,
                "last_volume": attributes.get("lastVolume"),
                "last_chapter": attributes.get("lastChapter"),
            })
        
        return {
            "total": data.get("total", 0),
            "limit": limit,
            "offset": offset,
            "data": formatted_data,
        }
    
    except Exception as e:
        log.error(f"Search error: {e}")
        return {
            "total": 0,
            "limit": limit,
            "offset": offset,
            "data": [],
            "error": str(e),
        }


@router.get("/authors")
async def search_authors(
    name: Optional[str] = Query(None, description="Author name"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Search authors by name"""
    
    try:
        params = {"limit": limit, "offset": offset}
        
        if name:
            params["name"] = name
        
        result = Net.mangadex.get("/author", params=params)
        data = result.json()
        
        formatted_data = [
            {
                "id": item.get("id"),
                "name": item.get("attributes", {}).get("name"),
                "biography": item.get("attributes", {}).get("biography", {}).get("en"),
            }
            for item in data.get("data", [])
        ]
        
        return {
            "total": data.get("total", 0),
            "limit": limit,
            "offset": offset,
            "data": formatted_data,
        }
    
    except Exception as e:
        log.error(f"Author search error: {e}")
        return {"total": 0, "limit": limit, "offset": offset, "data": [], "error": str(e)}


@router.get("/artists")
async def search_artists(
    name: Optional[str] = Query(None, description="Artist name"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Search artists by name"""
    
    try:
        params = {"limit": limit, "offset": offset}
        
        if name:
            params["name"] = name
        
        result = Net.mangadex.get("/artist", params=params)
        data = result.json()
        
        formatted_data = [
            {
                "id": item.get("id"),
                "name": item.get("attributes", {}).get("name"),
                "biography": item.get("attributes", {}).get("biography", {}).get("en"),
            }
            for item in data.get("data", [])
        ]
        
        return {
            "total": data.get("total", 0),
            "limit": limit,
            "offset": offset,
            "data": formatted_data,
        }
    
    except Exception as e:
        log.error(f"Artist search error: {e}")
        return {"total": 0, "limit": limit, "offset": offset, "data": [], "error": str(e)}
