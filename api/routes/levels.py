"""Level endpoints"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["Levels"])

data_service = None


def init(ds):
    global data_service
    data_service = ds


@router.get("/levels")
async def get_levels(
    category: Optional[str] = Query(None, description="Filter by category (primaire/college/lycee)"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    """
    Get all education levels.

    Returns the complete list of Moroccan education levels from Primary (Primaire)
    through Middle School (College) to High School (Lycee/Baccalaureate).
    """
    levels, total = data_service.get_levels(category=category, limit=limit, offset=offset)
    return {
        "success": True,
        "count": len(levels),
        "total": total,
        "offset": offset,
        "has_more": offset + len(levels) < total,
        "data": levels,
    }


@router.get("/levels/{level_id}")
async def get_level(level_id: str):
    """
    Get a specific education level by ID with related statistics.

    Example IDs: primaire-1, college-3, lycee-2bac
    """
    level = data_service.get_level(level_id)
    if not level:
        raise HTTPException(status_code=404, detail=f"Level '{level_id}' not found")

    subjects = data_service.get_subjects_for_level(level_id)
    content = data_service.get_content_for_level(level_id)
    content_types = data_service.get_content_type_counts(content)

    return {
        "success": True,
        "data": {
            **level,
            "subjects_count": len(subjects),
            "content_count": len(content),
            "content_types": content_types,
            "subjects": [{"id": s["id"], "name": s["name"], "name_ar": s.get("name_ar")} for s in subjects],
        },
    }
