#!/usr/bin/env python3
"""
Moroccan Education Public API v1.0
A comprehensive, production-ready API for Moroccan education data.
"""

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from api.config import settings
from api.services.data_service import DataService
from api.services.search_service import SearchService
from api.services.stats_service import StatsService
from api.services.cache_service import CacheService
from api.middleware.request_tracking import RequestTrackingMiddleware
from api.middleware.rate_limiter import RateLimiter
from api.routes import (
    levels_router,
    subjects_router,
    content_router,
    search_router,
    stats_router,
    overview_router,
)
from api.routes import levels, subjects, content, search, stats, overview

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title="Moroccan Education API",
        version="1.0.0",
        description="""
# Moroccan Education Data API v1.0

A comprehensive, free, public API providing access to educational resources
for the entire Moroccan education system.

## Highlights

- **12 Education Levels** — Primary (Primaire) through Baccalaureate
- **100+ Subjects** — Mathematics, Sciences, Languages, Philosophy, and more
- **2000+ Content Items** — Courses, Exercises, Exams, Corrections
- **Bilingual** — Full French and Arabic support
- **Quality Pipeline** — Automated daily validation and monitoring
- **Multiple Sources** — Aggregated from 6+ trusted Moroccan education platforms

## Content Types

| Type | Description |
|------|-------------|
| `cours` | Course materials and lessons |
| `exercice` | Practice exercises with solutions |
| `examen` | National and regional examination papers |
| `controle` | Continuous assessment tests |
| `correction` | Detailed solutions and corrections |
| `resume` | Summary and revision sheets |

## Rate Limits

- **60 requests/minute** per IP address
- No authentication required

## Links

- **GitHub**: [moroccan-education-API](https://github.com/K11E3R/moroccan-education-API)
- **Contact**: prs.online.00@gmail.com
        """,
        routes=app.routes,
        tags=[
            {"name": "Overview", "description": "API information, health checks, and landing page"},
            {"name": "Levels", "description": "Education levels — Primary, Middle School, High School"},
            {"name": "Subjects", "description": "Academic subjects per level"},
            {"name": "Content", "description": "Educational content — courses, exercises, exams, corrections"},
            {"name": "Search", "description": "Full-text search across all resources"},
            {"name": "Statistics", "description": "API statistics, data analytics, and quality metrics"},
        ],
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "/favicon.png",
        "altText": "Moroccan Education API",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# --- Initialize services ---
data_service = DataService()
search_service = SearchService()
stats_service = StatsService()
cache_service = CacheService(default_ttl=settings.CACHE_TTL)

# --- Create FastAPI app ---
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url=None,
    redoc_url=None,
)
app.openapi = custom_openapi

# --- Middleware stack (order matters: outermost first) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Response-Time", "X-API-Version", "X-RateLimit-Limit", "X-RateLimit-Remaining"],
)
app.add_middleware(RateLimiter, requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)
app.add_middleware(RequestTrackingMiddleware, stats_service=stats_service)

# --- Load data ---
data_service.load(settings.DATA_FALLBACK_PATHS)

# --- Load landing page template ---
_template_path = Path(__file__).parent / "templates" / "landing.html"
_landing_html = _template_path.read_text(encoding="utf-8") if _template_path.exists() else "<h1>Moroccan Education API</h1>"

# --- Initialize route modules with services ---
levels.init(data_service)
subjects.init(data_service)
content.init(data_service)
search.init(data_service, search_service)
stats.init(data_service, stats_service)
overview.init(data_service, stats_service, _landing_html)

# --- Register routers ---
app.include_router(overview_router)
app.include_router(levels_router)
app.include_router(subjects_router)
app.include_router(content_router)
app.include_router(search_router)
app.include_router(stats_router)


# --- Custom docs ---
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Moroccan Education API — Docs",
        swagger_favicon_url="/favicon.png",
        swagger_ui_parameters={
            "deepLinking": True,
            "displayRequestDuration": True,
            "docExpansion": "list",
            "operationsSorter": "alpha",
            "filter": True,
            "tagsSorter": "alpha",
            "syntaxHighlight.theme": "monokai",
        },
    )


@app.get("/redoc", include_in_schema=False)
async def custom_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Moroccan Education API — Reference",
        redoc_favicon_url="/favicon.png",
        redoc_js_url="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js",
    )


@app.get("/favicon.png", include_in_schema=False)
async def favicon():
    path = Path(__file__).parent / "favicon.png"
    if path.exists():
        return FileResponse(path)
    raise HTTPException(status_code=404)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon_ico():
    path = Path(__file__).parent / "favicon.png"
    if path.exists():
        return FileResponse(path, media_type="image/png")
    raise HTTPException(status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
