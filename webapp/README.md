================================================================================
                      WEBAPP - Web Interface & API
================================================================================

This is the FastAPI web application for MangaDex Downloader.


================================================================================
DIRECTORY STRUCTURE
================================================================================

webapp/
├── __init__.py
├── app.py                      # FastAPI application (main entry)
│
├── routers/                    # API endpoints
│   ├── __init__.py
│   ├── search.py              # Basic search endpoint
│   ├── search_advanced.py     # Advanced search with filters
│   ├── manga.py               # Manga details & chapters
│   ├── cover.py               # Cover images
│   ├── groups.py              # Groups, authors, artists
│   ├── download.py            # Simple download
│   ├── url.py                 # Download with job queue
│   ├── config.py              # Configuration
│   └── auth.py                # OAuth (not used)
│
├── schemas/                    # Pydantic models for validation
│   ├── __init__.py
│   ├── manga.py               # Manga, Chapter, Author, Artist models
│   ├── search.py              # Search request/response models
│   ├── download.py            # Download models
│   └── config.py              # Config model
│
├── utils/                      # Helper functions
│   └── __init__.py            # API response formatters
│
├── models/                     # Database models (reserved for future)
│   └── __init__.py
│
├── templates/                  # HTML templates
│   └── index.html             # Web UI (single page app)
│
└── static/                     # Static assets
    └── styles.css             # CSS styling


================================================================================
INSTALLATION & SETUP
================================================================================

__Requirements:__

- Python 3.11+
- uv (Astral's package manager)

__Installation Steps:__

1. __Install dependencies with uv:__

   ```bash
   uv sync
   ```

2. __Run the web app:__

   ```bash
   uv run python .\run_web.py
   ```

3. __Open browser:__

   - Navigate to: `http://localhost:8000`

__Note:__ The `pyproject.toml` has been configured to work with uv. The `lxml`
dependency was removed as it's not required for the basic web interface.


================================================================================
QUICK START
================================================================================

1. Install dependencies:
   .\install-uv.ps1
   or
   uv sync

2. Run the server:
   python ..\run_web.py

3. Open browser:
   http://localhost:8000

4. Use the web interface:
   - Search for manga with advanced filters
   - View manga details and chapters
   - Download with options
   - Track download progress

5. Access API documentation:
   http://localhost:8000/docs (Swagger UI)
   http://localhost:8000/redoc (ReDoc)


================================================================================
API ENDPOINTS
================================================================================

SEARCH (6 endpoints):
  GET /api/search/manga          - Advanced search with filters
  GET /api/search/authors        - Search authors
  GET /api/search/artists        - Search artists

MANGA (3 endpoints):
  GET /api/manga/{id}            - Get manga details
  GET /api/manga/{id}/chapters   - Get chapters list
  GET /api/manga/{id}/feed       - Get latest chapters

COVERS (2 endpoints):
  GET /api/covers/manga/{id}     - Get manga covers
  GET /api/covers/{id}/image     - Get specific cover

GROUPS (5 endpoints):
  GET /api/groups/{id}           - Get group info
  GET /api/groups                - List groups
  GET /api/authors/{id}          - Get author info
  GET /api/artists/{id}          - Get artist info
  GET /api/manga/{id}/groups     - Get manga groups

DOWNLOAD (2 endpoints):
  POST /api/url/download         - Start download
  GET /api/url/jobs/{id}         - Get job status

CONFIG (2 endpoints):
  GET /api/config                - Get configuration
  PUT /api/config                - Update configuration

UTILITY (1 endpoint):
  GET /health                    - Health check


See WEBAPP_API_FULL.md for complete documentation


================================================================================
ROUTERS
================================================================================

Each router file contains related endpoints:

search.py / search_advanced.py
  - GET /api/search/manga       (with 8+ filters)
  - GET /api/search/authors
  - GET /api/search/artists

manga.py
  - GET /api/manga/{id}
  - GET /api/manga/{id}/chapters
  - GET /api/manga/{id}/feed

cover.py
  - GET /api/covers/manga/{id}
  - GET /api/covers/{id}/image

groups.py
  - GET /api/groups/{id}
  - GET /api/groups
  - GET /api/authors/{id}
  - GET /api/artists/{id}
  - GET /api/manga/{id}/groups

download.py / url.py
  - POST /api/download
  - POST /api/url/download
  - GET /api/url/jobs/{id}

config.py
  - GET /api/config
  - PUT /api/config

auth.py
  - OAuth endpoints (not used)


================================================================================
SCHEMAS (Validation Models)
================================================================================

All schemas use Pydantic for type validation and documentation.

manga.py:
  - MangaSchema              - Basic manga info
  - MangaDetailSchema        - Full manga with relationships
  - ChapterSchema            - Chapter information
  - AuthorSchema             - Author data
  - ArtistSchema             - Artist data
  - TagSchema                - Tag data
  - CoverArtSchema           - Cover image data

search.py:
  - SearchRequestSchema      - Search parameters
  - SearchResponseSchema     - Search results

download.py:
  - DownloadRequestSchema    - Download parameters
  - JobStatusSchema          - Job status info

config.py:
  - ConfigSchema             - Configuration data


================================================================================
UTILITIES
================================================================================

webapp/utils/__init__.py provides helper functions:

parse_search_params()          - Convert UI params to API format
format_manga_response()        - Format raw API response
format_chapter_response()      - Format chapter data
build_cli_args()               - Build CLI arguments for downloads


================================================================================
WEB INTERFACE
================================================================================

The web UI (index.html) is a single-page application with 3 tabs:

TAB 1 - SEARCH:
  - Enter title and use filters
  - View results in grid
  - Click to download any manga

TAB 2 - DOWNLOAD:
  - Paste manga URL
  - Choose download options
  - Track progress in real-time

TAB 3 - DETAILS:
  - Enter manga ID or URL
  - View full information
  - See latest chapters

Features:
  - Responsive design (mobile-friendly)
  - Real-time status updates
  - Interactive forms
  - Beautiful card layouts
  - Smooth animations


================================================================================
CSS STYLING
================================================================================

styles.css provides:
  - Color scheme (blue primary, gray secondary)
  - Typography hierarchy
  - Responsive grid layout
  - Button & form styling
  - Animation effects
  - Mobile optimization

Color variables:
  --primary: #0066cc        (Button, links)
  --secondary: #666         (Text, borders)
  --border: #ddd            (Borders)
  --bg-light: #f8f9fa       (Backgrounds)
  --text: #333              (Text color)


================================================================================
ADDING NEW FEATURES
================================================================================

To add a new endpoint:

1. Create a router file in routers/
   - Use FastAPI's @app.get/@app.post decorators
   - Add proper error handling
   - Include docstrings

2. Create schemas in schemas/ if needed
   - Use Pydantic BaseModel
   - Add validation rules

3. Register router in app.py
   - Import the router
   - Add app.include_router()

4. Add to UI (optional)
   - Update index.html
   - Add form or display logic

5. Document in WEBAPP_API_FULL.md
   - Add endpoint description
   - Include parameters
   - Show response example

Example:

  routers/example.py:
  ─────────────────────
  from fastapi import APIRouter
  
  router = APIRouter(prefix="/api/example", tags=["example"])
  
  @router.get("/")
  async def example():
      """Example endpoint"""
      return {"message": "Hello"}
  

  app.py:
  ────────
  from .routers.example import router as example_router
  app.include_router(example_router)


================================================================================
DEPENDENCIES
================================================================================

See requirements-uv.txt for full list:

Web Framework:
  - fastapi
  - uvicorn
  - python-multipart
  - itsdangerous

Templating:
  - Jinja2

Data:
  - pydantic

Core:
  - mangadex_downloader (main library)
  + all its dependencies


================================================================================
ENVIRONMENT VARIABLES
================================================================================

WEBAPP_SESSION_SECRET    - Session encryption key (default: dev-secret-change-me)

Set in your environment or .env file:
  $env:WEBAPP_SESSION_SECRET = "your-secret-key"


================================================================================
TROUBLESHOOTING
================================================================================

If endpoints return 404:
  - Check router is imported in app.py
  - Check router prefix matches
  - Check method (GET/POST) is correct

If validation fails:
  - Check request body matches schema
  - Check parameter types
  - Check required vs optional fields

If UI doesn't load:
  - Check templates/ folder exists
  - Check index.html is in templates/
  - Check static/ folder exists
  - Check styles.css is in static/

If API fails:
  - Check MangaDex is accessible
  - Check parameters are valid
  - Check rate limiting not hit
  - Check internet connection


================================================================================
DOCUMENTATION
================================================================================

See also:
  - WEBAPP_API_FULL.md       - Complete API reference
  - DOCS_INDEX.txt           - Documentation index
  - START_HERE.txt           - Getting started guide
  - /docs                    - Interactive Swagger UI


================================================================================
