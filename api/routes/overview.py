"""Overview and health endpoints"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from datetime import datetime

router = APIRouter(tags=["Overview"])

data_service = None
stats_service = None
_landing_page_html = None


def init(ds, ss, landing_html):
    global data_service, stats_service, _landing_page_html
    data_service = ds
    stats_service = ss
    _landing_page_html = landing_html


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Landing page with API overview and documentation links."""
    stats = data_service.statistics
    html = _landing_page_html

    html = html.replace(
        "{{LEVELS_COUNT}}",
        str(stats.get("total_levels", len(data_service.levels))),
    )
    html = html.replace(
        "{{SUBJECTS_COUNT}}",
        str(stats.get("total_subjects", len(data_service.subjects))),
    )
    html = html.replace(
        "{{CONTENT_COUNT}}",
        str(stats.get("total_content", len(data_service.content))),
    )
    html = html.replace(
        "{{SOURCES_COUNT}}",
        str(len(data_service.metadata.get("data_sources", [])) or 6),
    )
    base_url = str(request.base_url).rstrip("/")
    html = html.replace("{{BASE_URL}}", base_url)
    html = html.replace(
        "{{QUALITY_SCORE}}",
        str(round(data_service.metadata.get("quality_score", 0) * 100)),
    )

    return HTMLResponse(content=html)


@router.get("/api")
async def api_info():
    """API information and available endpoints."""
    return {
        "name": "Moroccan Education API",
        "version": "1.0.0",
        "description": "Comprehensive public API for Moroccan education data",
        "endpoints": {
            "levels": "/api/v1/levels",
            "subjects": "/api/v1/subjects",
            "content": "/api/v1/content",
            "search": "/api/v1/search",
            "stats": "/api/v1/stats",
            "sources": "/api/v1/sources",
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
        },
        "data_highlights": {
            "total_levels": len(data_service.levels),
            "total_subjects": len(data_service.subjects),
            "total_content": len(data_service.content),
            "languages": ["fr", "ar"],
        },
    }


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring and deployment platforms."""
    levels_count = len(data_service.levels)
    subjects_count = len(data_service.subjects)
    content_count = len(data_service.content)

    is_healthy = levels_count > 0 and subjects_count > 0 and content_count > 0
    quality = data_service.metadata.get("quality_score", 0)

    return {
        "status": "healthy" if is_healthy else "degraded",
        "timestamp": datetime.now().isoformat(),
        "data_loaded": is_healthy,
        "counts": {
            "levels": levels_count,
            "subjects": subjects_count,
            "content": content_count,
        },
        "uptime_seconds": round(stats_service.uptime_seconds, 2),
        "version": "1.0.0",
        "data_quality": {
            "score": quality,
            "last_updated": data_service.data.get("collection_date", "N/A"),
        },
    }
