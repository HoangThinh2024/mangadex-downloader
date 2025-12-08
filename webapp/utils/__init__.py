"""Utility functions for webapp"""

from typing import Optional, List, Dict, Any
import logging

log = logging.getLogger(__name__)


def parse_search_params(
    title: Optional[str] = None,
    authors: Optional[List[str]] = None,
    artists: Optional[List[str]] = None,
    year: Optional[int] = None,
    status: Optional[str] = None,
    languages: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    content_rating: Optional[List[str]] = None,
    limit: int = 10,
    offset: int = 0,
    includes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Parse search parameters into MangaDex API format"""
    
    params = {
        "limit": limit,
        "offset": offset,
    }
    
    if title:
        params["title"] = title
    
    if year:
        params["year"] = year
    
    if status:
        params["status"] = status
    
    if languages:
        params["translatedLanguage"] = languages
    
    if content_rating:
        params["contentRating"] = content_rating
    
    # Multiple includes for relationships
    if includes is None:
        includes = ["author", "artist", "cover_art", "manga"]
    params["includes[]"] = includes
    
    # Handle IDs for advanced filters
    if authors:
        params["authors[]"] = authors
    if artists:
        params["artists[]"] = artists
    if tags:
        params["includedTags[]"] = tags
    
    return params


def format_manga_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format manga data from API response"""
    
    if not data:
        return {}
    
    attributes = data.get("attributes", {})
    relationships = data.get("relationships", [])
    
    cover_url = None
    authors = []
    artists = []
    
    # Extract cover art
    for rel in relationships:
        if rel.get("type") == "cover_art":
            file_name = rel.get("attributes", {}).get("fileName")
            if file_name:
                cover_url = f"https://uploads.mangadex.org/covers/{data.get('id')}/{file_name}.256.jpg"
        
        # Extract author
        if rel.get("type") == "author":
            authors.append({
                "id": rel.get("id"),
                "name": rel.get("attributes", {}).get("name"),
            })
        
        # Extract artist
        if rel.get("type") == "artist":
            artists.append({
                "id": rel.get("id"),
                "name": rel.get("attributes", {}).get("name"),
            })
    
    return {
        "id": data.get("id"),
        "title": attributes.get("title", {}).get("en") or list(attributes.get("title", {}).values())[0] if attributes.get("title") else "Unknown",
        "description": attributes.get("description", {}).get("en"),
        "year": attributes.get("year"),
        "status": attributes.get("status"),
        "cover": cover_url,
        "content_rating": attributes.get("contentRating"),
        "last_volume": attributes.get("lastVolume"),
        "last_chapter": attributes.get("lastChapter"),
        "authors": authors,
        "artists": artists,
    }


def format_chapter_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format chapter data from API response"""
    
    if not data:
        return {}
    
    attributes = data.get("attributes", {})
    relationships = data.get("relationships", [])
    
    groups = []
    scanlators = []
    
    # Extract groups and scanlators
    for rel in relationships:
        if rel.get("type") == "scanlation_group":
            groups.append(rel.get("id"))
        if rel.get("type") == "user":
            scanlators.append(rel.get("attributes", {}).get("username"))
    
    return {
        "id": data.get("id"),
        "manga_id": next((rel.get("id") for rel in relationships if rel.get("type") == "manga"), None),
        "volume": attributes.get("volume"),
        "chapter": attributes.get("chapter"),
        "title": attributes.get("title"),
        "language": attributes.get("translatedLanguage"),
        "pages": attributes.get("pages"),
        "groups": groups,
        "scanlators": scanlators,
    }


def build_cli_args(
    url: str,
    save_as: Optional[str] = None,
    path: Optional[str] = None,
    chapters: Optional[str] = None,
    start_chapter: Optional[str] = None,
    end_chapter: Optional[str] = None,
    start_page: Optional[int] = None,
    end_page: Optional[int] = None,
    start_volume: Optional[str] = None,
    end_volume: Optional[str] = None,
    language: Optional[str] = None,
    groups: Optional[str] = None,
    no_track: bool = False,
    log_level: Optional[str] = None,
) -> List[str]:
    """Build CLI arguments for download command"""
    
    args = [url]
    
    if save_as:
        args.extend(["--save-as", save_as])
    
    if path:
        args.extend(["--path", path])
    
    if chapters:
        args.extend(["--chapters", chapters])
    
    if start_chapter:
        args.extend(["--start-chapter", start_chapter])
    
    if end_chapter:
        args.extend(["--end-chapter", end_chapter])
    
    if start_page:
        args.extend(["--start-page", str(start_page)])
    
    if end_page:
        args.extend(["--end-page", str(end_page)])
    
    if start_volume:
        args.extend(["--start-volume", start_volume])
    
    if end_volume:
        args.extend(["--end-volume", end_volume])
    
    if language:
        args.extend(["--language", language])
    
    if groups:
        args.extend(["--group", groups])
    
    if no_track:
        args.append("--no-track")
    
    if log_level:
        args.extend(["--log-level", log_level])
    
    return args
