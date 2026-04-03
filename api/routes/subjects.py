"""Subject endpoints"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["Subjects"])

data_service = None


def init(ds):
    global data_service
    data_service = ds


@router.get("/subjects")
async def get_subjects(
    level_id: Optional[str] = Query(None, description="Filter by level ID"),
    category: Optional[str] = Query(None, description="Filter by category (primaire/college/lycee)"),
    limit: Optional[int] = Query(None, ge=1, le=200, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
):
    """
    Get all subjects with optional filtering.

    Subjects include Mathematics, French, Arabic, Physics, SVT, Philosophy, etc.
    Filter by level_id or category for targeted results.
    """
    subjects, total = data_service.get_subjects(
        level_id=level_id, category=category, limit=limit, offset=offset
    )
    return {
        "success": True,
        "count": len(subjects),
        "total": total,
        "offset": offset,
        "has_more": offset + len(subjects) < total,
        "data": subjects,
    }


@router.get("/subjects/{subject_id}")
async def get_subject(subject_id: str):
    """
    Get a specific subject by ID with content breakdown.

    Example ID: mathematiques-lycee-2bac
    """
    subject = data_service.get_subject(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject '{subject_id}' not found")

    content = data_service.get_content_for_subject(subject_id)
    content_types = data_service.get_content_type_counts(content)

    return {
        "success": True,
        "data": {
            **subject,
            "content_count": len(content),
            "content_types": content_types,
        },
    }
