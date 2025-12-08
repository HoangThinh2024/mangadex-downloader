"""Group, author and artist router"""

import logging
from fastapi import APIRouter, Query
from typing import Optional, List

from mangadex_downloader.network import Net

router = APIRouter(prefix="/api", tags=["groups"])
log = logging.getLogger(__name__)


@router.get("/groups/{group_id}")
async def get_group_info(
    group_id: str,
):
    """Get scanlation group information"""
    
    try:
        result = Net.mangadex.get(f"/group/{group_id}")
        data = result.json().get("data", {})
        
        if not data:
            return {"error": "Group not found"}
        
        attributes = data.get("attributes", {})
        
        return {
            "id": data.get("id"),
            "name": attributes.get("name"),
            "alt_names": attributes.get("altNames", []),
            "description": attributes.get("description"),
            "members": attributes.get("members"),
            "language": attributes.get("language"),
            "official": attributes.get("official"),
            "verified": attributes.get("verified"),
        }
    
    except Exception as e:
        log.error(f"Get group info error: {e}")
        return {"error": str(e)}


@router.get("/groups")
async def list_groups(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List scanlation groups"""
    
    try:
        params = {
            "limit": limit,
            "offset": offset,
        }
        
        result = Net.mangadex.get("/group", params=params)
        data = result.json()
        
        groups = []
        for item in data.get("data", []):
            attributes = item.get("attributes", {})
            groups.append({
                "id": item.get("id"),
                "name": attributes.get("name"),
                "alt_names": attributes.get("altNames", []),
                "language": attributes.get("language"),
                "verified": attributes.get("verified"),
            })
        
        return {
            "total": data.get("total", 0),
            "groups": groups,
        }
    
    except Exception as e:
        log.error(f"List groups error: {e}")
        return {"error": str(e), "groups": []}


@router.get("/authors/{author_id}")
async def get_author_info(
    author_id: str,
):
    """Get author information"""
    
    try:
        result = Net.mangadex.get(f"/author/{author_id}")
        data = result.json().get("data", {})
        
        if not data:
            return {"error": "Author not found"}
        
        attributes = data.get("attributes", {})
        
        return {
            "id": data.get("id"),
            "name": attributes.get("name"),
            "biography": attributes.get("biography", {}).get("en"),
            "image_url": attributes.get("imageUrl"),
            "twitter": attributes.get("twitter"),
            "pixiv": attributes.get("pixiv"),
            "melon_book": attributes.get("melonBook"),
            "fan_box": attributes.get("fanBox"),
            "booth": attributes.get("booth"),
            "nico_video": attributes.get("nicoVideo"),
            "amazon_url": attributes.get("amazonUrl"),
        }
    
    except Exception as e:
        log.error(f"Get author info error: {e}")
        return {"error": str(e)}


@router.get("/artists/{artist_id}")
async def get_artist_info(
    artist_id: str,
):
    """Get artist information"""
    
    try:
        result = Net.mangadex.get(f"/artist/{artist_id}")
        data = result.json().get("data", {})
        
        if not data:
            return {"error": "Artist not found"}
        
        attributes = data.get("attributes", {})
        
        return {
            "id": data.get("id"),
            "name": attributes.get("name"),
            "biography": attributes.get("biography", {}).get("en"),
            "image_url": attributes.get("imageUrl"),
            "twitter": attributes.get("twitter"),
            "pixiv": attributes.get("pixiv"),
            "melon_book": attributes.get("melonBook"),
            "fan_box": attributes.get("fanBox"),
            "booth": attributes.get("booth"),
            "nico_video": attributes.get("nicoVideo"),
            "amazon_url": attributes.get("amazonUrl"),
        }
    
    except Exception as e:
        log.error(f"Get artist info error: {e}")
        return {"error": str(e)}


@router.get("/manga/{manga_id}/groups")
async def get_manga_groups(
    manga_id: str,
):
    """Get scanlation groups that have chapters for a manga"""
    
    try:
        # Get chapters with groups included
        params = {
            "limit": 500,
            "includes[]": ["scanlation_group"],
        }
        
        result = Net.mangadex.get(f"/manga/{manga_id}/feed", params=params)
        data = result.json()
        
        # Collect unique groups
        groups_dict = {}
        for chapter in data.get("data", []):
            relationships = chapter.get("relationships", [])
            for rel in relationships:
                if rel.get("type") == "scanlation_group":
                    group_id = rel.get("id")
                    group_name = rel.get("attributes", {}).get("name", "Unknown")
                    if group_id not in groups_dict:
                        groups_dict[group_id] = group_name
        
        groups = [
            {"id": gid, "name": gname}
            for gid, gname in groups_dict.items()
        ]
        
        return {
            "manga_id": manga_id,
            "total": len(groups),
            "groups": groups,
        }
    
    except Exception as e:
        log.error(f"Get manga groups error: {e}")
        return {"error": str(e), "groups": []}
