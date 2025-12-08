from fastapi import APIRouter, Query
from mangadex_downloader.network import Net, base_url
from typing import Optional

router = APIRouter(prefix="/api/search", tags=["search"])

# All MangaDex language codes
LANGUAGE_MAP = {
    "en": "English",
    "ja": "Japanese", 
    "zh": "Chinese (Simplified)",
    "zh-hk": "Chinese (Traditional)",
    "ko": "Korean",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "pt-br": "Portuguese (Brazilian)",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "th": "Thai",
    "vi": "Vietnamese",
    "pl": "Polish",
    "uk": "Ukrainian",
    "id": "Indonesian",
    "tr": "Turkish",
    "bn": "Bengali",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "nl": "Dutch",
    "et": "Estonian",
    "fa": "Farsi",
    "fi": "Finnish",
    "el": "Greek",
    "he": "Hebrew",
    "hu": "Hungarian",
    "ja-ro": "Japanese (Romanized)",
    "jv": "Javanese",
    "kk": "Kazakh",
    "km": "Khmer",
    "lo": "Lao",
    "lt": "Lithuanian",
    "mk": "Macedonian",
    "mn": "Mongolian",
    "ms": "Malay",
    "my": "Burmese",
    "nb": "Norwegian (Bokmål)",
    "ne": "Nepali",
    "no": "Norwegian",
    "or": "Odia",
    "pa": "Punjabi",
    "ro": "Romanian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "sr": "Serbian",
    "sv": "Swedish",
    "ta": "Tamil",
    "te": "Telugu",
    "tl": "Filipino",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "zh-ro": "Chinese (Romanized)",
}

@router.get("/manga")
def search_manga(
    title: str = Query(None),
    authors: str = Query(None),
    artists: str = Query(None),
    status: str = Query(None),
    languages: str = Query(None),
    content_rating: str = Query(None),
    tags: str = Query(None),  # Comma-separated tag IDs to include
    excludedTags: str = Query(None),  # Comma-separated tag IDs to exclude
    limit: int = 12,
    offset: int = 0,
):
    """
    Search manga with pagination support
    - title: Manga title (optional)
    - authors: Author name search (optional)
    - artists: Artist name search (optional)
    - status: ongoing, completed, hiatus, cancelled
    - languages: Original language code
    - content_rating: safe, suggestive, erotica, pornographic
    - limit: Results per page (1-100)
    - offset: Pagination offset
    
    Note: If no title is provided, searches will use author/artist endpoints
    """
    
    # If no search criteria provided
    if not title and not authors and not artists:
        return {
            "results": [],
            "total": 0,
            "limit": limit,
            "offset": offset,
        }
    
    # If searching only by author or artist without title
    if not title and (authors or artists):
        data = []  # Initialize data
        total = 0
        
        # Strategy: Get recent popular manga and filter by author/artist name
        # MangaDex API doesn't support filtering manga by author ID directly
        if authors or artists:
            try:
                search_name = (authors or artists).lower()
                
                # Get popular/recent manga to filter from
                manga_params = {
                    "limit": 100,  # Fetch more manga to increase chances of finding matches
                    "offset": 0,
                    "includes[]": ["author", "artist", "cover_art"],
                    "order[followedCount]": "desc",  # Get popular manga first
                }
                
                if status:
                    manga_params["status[]"] = status
                if languages:
                    manga_params["originalLanguage[]"] = languages
                if content_rating:
                    manga_params["contentRating[]"] = content_rating
                else:
                    manga_params["contentRating[]"] = ["safe", "suggestive", "erotica", "pornographic"]
                
                manga_url = f"{base_url}/manga"
                manga_res = Net.mangadex.get(manga_url, params=manga_params)
                manga_response = manga_res.json()
                
                all_manga = manga_response.get("data", [])
                
                # Filter manga where author/artist name matches
                filtered_manga = []
                for manga in all_manga:
                    relationships = manga.get("relationships", [])
                    
                    # Check if any author or artist matches
                    match_found = False
                    for rel in relationships:
                        if rel.get("type") in ["author", "artist"]:
                            person_name = rel.get("attributes", {}).get("name", "").lower()
                            # Match if search name is in person name or vice versa
                            if search_name in person_name or person_name in search_name:
                                match_found = True
                                break
                    
                    if match_found:
                        filtered_manga.append(manga)
                
                # Apply pagination
                start_idx = min(max(offset, 0), len(filtered_manga))
                end_idx = start_idx + min(max(limit, 1), 100)
                data = filtered_manga[start_idx:end_idx]
                total = len(filtered_manga)
                    
            except Exception as e:
                # Fallback to empty results
                log.error(f"Author/Artist search error: {e}")
                data = []
                total = 0
    else:
        # Normal search with title
        params = {
            "limit": min(max(limit, 1), 100),
            "offset": max(offset, 0),
            "includes[]": ["author", "artist", "cover_art"],
            "order[latestUploadedChapter]": "desc",
        }
        
        if title:
            params["title"] = title
        if authors:
            params["authors[]"] = authors
        if artists:
            params["artists[]"] = artists
        if status:
            params["status[]"] = status
        if languages:
            params["originalLanguage[]"] = languages
        if content_rating:
            params["contentRating[]"] = content_rating
        else:
            params["contentRating[]"] = ["safe", "suggestive", "erotica", "pornographic"]
        
        # Add tag filtering
        if tags:
            tag_ids = [t.strip() for t in tags.split(",") if t.strip()]
            if tag_ids:
                params["includedTags[]"] = tag_ids
        
        # Add excluded tags filtering
        if excludedTags:
            excluded_tag_ids = [t.strip() for t in excludedTags.split(",") if t.strip()]
            if excluded_tag_ids:
                params["excludedTags[]"] = excluded_tag_ids
        
        url = f"{base_url}/manga"
        if tags:
            tag_ids = [t.strip() for t in tags.split(",") if t.strip()]
            if tag_ids:
                params["includedTags[]"] = tag_ids
        
        url = f"{base_url}/manga"
        r = Net.mangadex.get(url, params=params)
        response_data = r.json()
        data = response_data.get("data", [])
        total = response_data.get("total", len(data))
    
    results = []
    for item in data:
        attr = item.get("attributes", {})
        relationships = item.get("relationships", [])
        
        # Get title (with fallback to any available language)
        title_obj = attr.get("title", {})
        en_title = title_obj.get("en") or next(iter(title_obj.values()), "Unknown")
        
        # Get cover URL
        cover_url = None
        for rel in relationships:
            if rel.get("type") == "cover_art":
                cover_filename = rel.get("attributes", {}).get("fileName")
                if cover_filename:
                    cover_url = f"https://uploads.mangadex.org/covers/{item.get('id')}/{cover_filename}"
                break
        
        results.append({
            "id": item.get("id"),
            "title": en_title,
            "status": attr.get("status"),
            "originalLanguage": attr.get("originalLanguage"),
            "year": attr.get("year"),
            "cover": cover_url,
        })
    
    return {
        "results": results,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/languages")
def get_languages():
    """Get all available MangaDex languages"""
    return {
        "languages": [
            {"code": code, "name": name}
            for code, name in sorted(LANGUAGE_MAP.items())
        ]
    }


@router.get("/suggestions")
def get_suggestions(q: str = Query(..., min_length=2), type: str = Query("manga")):
    """Get autocomplete suggestions for manga titles or authors
    
    Args:
        q: Query string (min 2 characters)
        type: 'manga' for titles, 'author' for authors/artists
    """
    try:
        if type == "manga":
            # Search manga titles
            params = {
                "title": q,
                "limit": 10,
                "order[relevance]": "desc",
            }
            r = Net.mangadex.get(f"{base_url}/manga", params=params)
            data = r.json().get("data", [])
            
            suggestions = []
            for item in data:
                title_obj = item.get("attributes", {}).get("title", {})
                title = title_obj.get("en") or next(iter(title_obj.values()), "")
                if title:
                    suggestions.append({
                        "id": item.get("id"),
                        "title": title
                    })
            
            return {"suggestions": suggestions}
            
        elif type == "author":
            # Search authors/artists
            params = {"limit": 10, "name": q}
            r = Net.mangadex.get(f"{base_url}/author", params=params)
            data = r.json().get("data", [])
            
            suggestions = []
            for item in data:
                name = item.get("attributes", {}).get("name", "")
                if name:
                    suggestions.append({
                        "id": item.get("id"),
                        "name": name
                    })
            
            return {"suggestions": suggestions}
        
        return {"suggestions": []}
        
    except Exception as e:
        log.error(f"Suggestions error: {e}")
        return {"suggestions": []}


@router.get("/tags")
def get_tags():
    """Get all available MangaDex tags/genres"""
    try:
        r = Net.mangadex.get(f"{base_url}/manga/tag")
        data = r.json().get("data", [])
        
        tags = []
        for tag in data:
            tag_id = tag.get("id")
            attributes = tag.get("attributes", {})
            name = attributes.get("name", {}).get("en", "")
            group = attributes.get("group", "theme")
            
            if name:
                tags.append({
                    "id": tag_id,
                    "name": name,
                    "group": group
                })
        
        return {"tags": tags}
        
    except Exception as e:
        log.error(f"Get tags error: {e}")
        return {"tags": []}


@router.get("/authors")
def get_suggestions(q: str = Query(..., min_length=2), type: str = Query("manga")):
    """Get autocomplete suggestions for manga titles or authors
    
    Args:
        q: Query string (min 2 characters)
        type: 'manga' for titles, 'author' for authors/artists
    """
    try:
        if type == "manga":
            # Search manga titles
            params = {
                "title": q,
                "limit": 10,
                "order[relevance]": "desc",
            }
            r = Net.mangadex.get(f"{base_url}/manga", params=params)
            data = r.json().get("data", [])
            
            suggestions = []
            for item in data:
                title_obj = item.get("attributes", {}).get("title", {})
                title = title_obj.get("en") or next(iter(title_obj.values()), "")
                if title:
                    suggestions.append({
                        "id": item.get("id"),
                        "title": title
                    })
            
            return {"suggestions": suggestions}
            
        elif type == "author":
            # Search authors/artists
            params = {"limit": 10, "name": q}
            r = Net.mangadex.get(f"{base_url}/author", params=params)
            data = r.json().get("data", [])
            
            suggestions = []
            for item in data:
                name = item.get("attributes", {}).get("name", "")
                if name:
                    suggestions.append({
                        "id": item.get("id"),
                        "name": name
                    })
            
            return {"suggestions": suggestions}
        
        return {"suggestions": []}
        
    except Exception as e:
        log.error(f"Suggestions error: {e}")
        return {"suggestions": []}


@router.get("/tags")
def get_tags():
    """Get all available MangaDex tags/genres"""
    try:
        r = Net.mangadex.get(f"{base_url}/manga/tag")
        data = r.json().get("data", [])
        
        tags = []
        for tag in data:
            tag_id = tag.get("id")
            attributes = tag.get("attributes", {})
            name = attributes.get("name", {}).get("en", "")
            group = attributes.get("group", "theme")
            
            if name:
                tags.append({
                    "id": tag_id,
                    "name": name,
                    "group": group
                })
        
        return {"tags": tags}
        
    except Exception as e:
        log.error(f"Get tags error: {e}")
        return {"tags": []}


@router.get("/suggestions")
def get_suggestions(q: str = Query(..., min_length=2), type: str = Query("manga")):
    """Get autocomplete suggestions for manga titles or authors
    
    Args:
        q: Query string (min 2 characters)
        type: 'manga' for titles, 'author' for authors/artists
    """
    try:
        if type == "manga":
            # Search manga titles
            params = {
                "title": q,
                "limit": 10,
                "order[relevance]": "desc",
            }
            r = Net.mangadex.get(f"{base_url}/manga", params=params)
            data = r.json().get("data", [])
            
            suggestions = []
            for item in data:
                title_obj = item.get("attributes", {}).get("title", {})
                title = title_obj.get("en") or next(iter(title_obj.values()), "")
                if title:
                    suggestions.append({
                        "id": item.get("id"),
                        "title": title
                    })
            
            return {"suggestions": suggestions}
            
        elif type == "author":
            # Search authors/artists
            params = {"limit": 10, "name": q}
            r = Net.mangadex.get(f"{base_url}/author", params=params)
            data = r.json().get("data", [])
            
            suggestions = []
            for item in data:
                name = item.get("attributes", {}).get("name", "")
                if name:
                    suggestions.append({
                        "id": item.get("id"),
                        "name": name
                    })
            
            return {"suggestions": suggestions}
        
        return {"suggestions": []}
        
    except Exception as e:
        log.error(f"Suggestions error: {e}")
        return {"suggestions": []}


@router.get("/tags")
def get_tags():
    """Get all available MangaDex tags/genres"""
    try:
        r = Net.mangadex.get(f"{base_url}/manga/tag")
        data = r.json().get("data", [])
        
        tags = []
        for tag in data:
            tag_id = tag.get("id")
            attributes = tag.get("attributes", {})
            name = attributes.get("name", {}).get("en", "")
            group = attributes.get("group", "theme")
            
            if name:
                tags.append({
                    "id": tag_id,
                    "name": name,
                    "group": group
                })
        
        return {"tags": tags}
        
    except Exception as e:
        log.error(f"Get tags error: {e}")
        return {"tags": []}


@router.get("/authors")
def search_authors(query: str = Query(...)):
    """Search authors by name"""
    try:
        params = {
            "limit": 20,
            "includes[]": "manga",
        }
        
        # MangaDex uses author search through manga endpoint with name filter
        # For now, return a simplified response
        url = f"{base_url}/author"
        r = Net.mangadex.get(url, params={"limit": 20})
        authors = r.json().get("data", [])
        
        # Filter by query
        filtered = [
            {
                "id": a.get("id"),
                "name": a.get("attributes", {}).get("name")
            }
            for a in authors
            if query.lower() in a.get("attributes", {}).get("name", "").lower()
        ]
        
        return {"authors": filtered[:20]}
    except:
        return {"authors": []}


@router.get("/artists")
def search_artists(query: str = Query(...)):
    """Search artists by name"""
    try:
        params = {
            "limit": 20,
        }
        
        # Similar to authors
        url = f"{base_url}/author"
        r = Net.mangadex.get(url, params=params)
        artists = r.json().get("data", [])
        
        # Filter by query
        filtered = [
            {
                "id": a.get("id"),
                "name": a.get("attributes", {}).get("name")
            }
            for a in artists
            if query.lower() in a.get("attributes", {}).get("name", "").lower()
        ]
        
        return {"artists": filtered[:20]}
    except:
        return {"artists": []}
