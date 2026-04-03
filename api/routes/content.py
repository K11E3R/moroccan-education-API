"""Content endpoints"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["Content"])

data_service = None


def init(ds):
    global data_service
    data_service = ds


@router.get("/content")
async def get_content(
    level_id: Optional[str] = Query(None, description="Filter by level ID"),
    subject_id: Optional[str] = Query(None, description="Filter by subject ID"),
    content_type: Optional[str] = Query(
        None, description="Filter by type: cours, exercice, examen, controle, correction, resume"
    ),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty: easy, medium, hard"),
    year: Optional[str] = Query(None, description="Filter by year (e.g. 2024, 2025)"),
    limit: int = Query(50, ge=1, le=500, description="Limit results (default 50)"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    """
    Get educational content with flexible filtering and pagination.

    Content types:
    - **cours**: Course materials and lessons
    - **exercice**: Practice exercises
    - **examen**: Examination papers (national/regional)
    - **controle**: Continuous assessment tests
    - **correction**: Solutions and corrections
    - **resume**: Summary and revision sheets
    """
    items, total = data_service.get_content(
        level_id=level_id,
        subject_id=subject_id,
        content_type=content_type,
        difficulty=difficulty,
        year=year,
        limit=limit,
        offset=offset,
    )
    return {
        "success": True,
        "count": len(items),
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(items) < total,
        "data": items,
    }


@router.get("/content/{content_id}")
async def get_content_item(content_id: str):
    """Get a specific content item by ID."""
    item = data_service.get_content_item(content_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Content '{content_id}' not found")
    return {"success": True, "data": item}


@router.get("/courses", include_in_schema=False)
async def get_courses_legacy(
    level_id: Optional[str] = None,
    subject_id: Optional[str] = None,
    content_type: Optional[str] = None,
    limit: int = 50,
):
    """Legacy endpoint - redirects to /api/v1/content"""
    return await get_content(level_id, subject_id, content_type, None, None, limit, 0)
