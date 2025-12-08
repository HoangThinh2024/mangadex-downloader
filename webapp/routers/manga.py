"""Manga detail and chapter router"""

import logging
from fastapi import APIRouter, Query
from typing import Optional

from mangadex_downloader.network import Net

router = APIRouter(prefix="/api/manga", tags=["manga"])
log = logging.getLogger(__name__)


@router.get("/{manga_id}")
async def get_manga_detail(
    manga_id: str,
    includes: Optional[str] = Query("author,artist,cover_art", description="Include relationships"),
):
    """Get detailed manga information"""
    
    try:
        includes_list = [i.strip() for i in includes.split(",")]
        params = {"includes[]": includes_list}
        
        result = Net.mangadex.get(f"https://api.mangadex.org/manga/{manga_id}", params=params)
        data = result.json().get("data", {})
        
        if not data:
            return {"error": "Manga not found"}
        
        attributes = data.get("attributes", {})
        relationships = data.get("relationships", [])
        
        # Format response
        cover_url = None
        authors = []
        artists = []
        
        for rel in relationships:
            if rel.get("type") == "cover_art":
                file_name = rel.get("attributes", {}).get("fileName")
                if file_name:
                    cover_url = f"https://uploads.mangadex.org/covers/{manga_id}/{file_name}"
            
            if rel.get("type") == "author":
                authors.append({
                    "id": rel.get("id"),
                    "name": rel.get("attributes", {}).get("name"),
                })
            
            if rel.get("type") == "artist":
                artists.append({
                    "id": rel.get("id"),
                    "name": rel.get("attributes", {}).get("name"),
                })
        
        # Get title
        title_obj = attributes.get("title", {})
        if isinstance(title_obj, dict):
            title_str = title_obj.get("en") or next(iter(title_obj.values()), "Unknown")
        else:
            title_str = str(title_obj)
        
        # Get tags
        tags = []
        for tag_data in attributes.get("tags", []):
            tag_name = tag_data.get("attributes", {}).get("name", {}).get("en")
            if tag_name:
                tags.append(tag_name)
        
        return {
            "id": data.get("id"),
            "title": title_str,
            "description": attributes.get("description", {}).get("en"),
            "year": attributes.get("year"),
            "status": attributes.get("status"),
            "coverUrl": cover_url,
            "contentRating": attributes.get("contentRating"),
            "lastVolume": attributes.get("lastVolume"),
            "lastChapter": attributes.get("lastChapter"),
            "authors": authors,
            "artists": artists,
            "tags": tags,
            "originalLanguage": attributes.get("originalLanguage"),
            "altTitles": attributes.get("altTitles"),
        }
    
    except Exception as e:
        log.error(f"Get manga detail error: {e}")
        return {"error": str(e)}


@router.get("/{manga_id}/chapters")
async def get_manga_chapters(
    manga_id: str,
    language: Optional[str] = Query(None, description="Filter by language"),
    limit: int = Query(500, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """Get chapters of a manga"""
    
    try:
        params = {
            "limit": limit,
            "offset": offset,
            "includes[]": ["scanlation_group"],
            "order[chapter]": "desc",  # Sort by chapter descending
            "contentRating[]": ["safe", "suggestive", "erotica", "pornographic"],  # Include all ratings
        }
        
        if language:
            params["translatedLanguage[]"] = [language]
        
        log.info(f"Fetching chapters for manga {manga_id} with params: {params}")
        
        result = Net.mangadex.get(f"https://api.mangadex.org/manga/{manga_id}/feed", params=params)
        data = result.json()
        
        log.info(f"Got {len(data.get('data', []))} chapters, total: {data.get('total', 0)}")
        
        formatted_chapters = []
        for item in data.get("data", []):
            attributes = item.get("attributes", {})
            relationships = item.get("relationships", [])
            
            groups = []
            for rel in relationships:
                if rel.get("type") == "scanlation_group":
                    groups.append({
                        "id": rel.get("id"),
                        "name": rel.get("attributes", {}).get("name"),
                    })
            
            formatted_chapters.append({
                "id": item.get("id"),
                "volume": attributes.get("volume"),
                "chapter": attributes.get("chapter"),
                "title": attributes.get("title"),
                "language": attributes.get("translatedLanguage"),
                "pages": attributes.get("pages"),
                "groups": groups,
            })
        
        return {
            "manga_id": manga_id,
            "total": data.get("total", 0),
            "limit": limit,
            "offset": offset,
            "chapters": formatted_chapters,
        }
    
    except Exception as e:
        log.error(f"Get chapters error: {e}")
        return {"error": str(e), "chapters": []}


@router.get("/{manga_id}/feed")
async def get_manga_feed(
    manga_id: str,
    language: Optional[str] = Query("en", description="Filter by language"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Get latest chapters feed for a manga"""
    
    try:
        params = {
            "limit": limit,
            "offset": offset,
            "translatedLanguage": [language] if language else [],
            "includes[]": ["scanlation_group"],
        }
        
        result = Net.mangadex.get(f"https://api.mangadex.org/manga/{manga_id}/feed", params=params)
        data = result.json()
        
        chapters = []
        for item in data.get("data", []):
            attributes = item.get("attributes", {})
            chapters.append({
                "id": item.get("id"),
                "volume": attributes.get("volume"),
                "chapter": attributes.get("chapter"),
                "title": attributes.get("title"),
                "language": attributes.get("translatedLanguage"),
                "published_at": attributes.get("publishAt"),
            })
        
        return {
            "manga_id": manga_id,
            "total": data.get("total", 0),
            "chapters": chapters,
        }
    
    except Exception as e:
        log.error(f"Get feed error: {e}")
        return {"error": str(e), "chapters": []}
