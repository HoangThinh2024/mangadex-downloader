"""Cover and image router"""

import logging
from fastapi import APIRouter, Query
from typing import Optional

from mangadex_downloader.network import Net

router = APIRouter(prefix="/api/covers", tags=["covers"])
log = logging.getLogger(__name__)


@router.get("/manga/{manga_id}")
async def get_manga_covers(
    manga_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Get cover images for a manga"""
    
    try:
        params = {
            "limit": limit,
            "offset": offset,
            "manga[]": [manga_id],
        }
        
        result = Net.mangadex.get("/cover", params=params)
        data = result.json()
        
        covers = []
        for item in data.get("data", []):
            attributes = item.get("attributes", {})
            file_name = attributes.get("fileName")
            
            cover_url = None
            if file_name:
                cover_url = f"https://uploads.mangadex.org/covers/{manga_id}/{file_name}"
            
            covers.append({
                "id": item.get("id"),
                "file_name": file_name,
                "volume": attributes.get("volume"),
                "version": attributes.get("version"),
                "cover_url": cover_url,
            })
        
        return {
            "manga_id": manga_id,
            "total": data.get("total", 0),
            "covers": covers,
        }
    
    except Exception as e:
        log.error(f"Get covers error: {e}")
        return {"error": str(e), "covers": []}


@router.get("/{cover_id}/image")
async def get_cover_image(
    cover_id: str,
    size: Optional[str] = Query("256", description="Image size: 256, 512"),
):
    """Get cover image by ID"""
    
    try:
        # Get cover metadata first
        result = Net.mangadex.get(f"/cover/{cover_id}")
        data = result.json().get("data", {})
        
        if not data:
            return {"error": "Cover not found"}
        
        attributes = data.get("attributes", {})
        relationships = data.get("relationships", [])
        
        file_name = attributes.get("fileName")
        if not file_name:
            return {"error": "File name not found"}
        
        # Get manga ID from relationships
        manga_id = None
        for rel in relationships:
            if rel.get("type") == "manga":
                manga_id = rel.get("id")
                break
        
        if not manga_id:
            return {"error": "Manga ID not found"}
        
        cover_url = f"https://uploads.mangadex.org/covers/{manga_id}/{file_name}"
        
        return {
            "id": cover_id,
            "manga_id": manga_id,
            "file_name": file_name,
            "url": cover_url,
            "256px": f"{cover_url}.256.jpg",
            "512px": f"{cover_url}.512.jpg",
        }
    
    except Exception as e:
        log.error(f"Get cover image error: {e}")
        return {"error": str(e)}
