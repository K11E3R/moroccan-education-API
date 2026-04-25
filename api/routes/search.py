"""Search endpoints"""

from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["Search"])

data_service = None
search_service = None


def init(ds, ss):
    global data_service, search_service
    data_service = ds
    search_service = ss


@router.get("/search")
async def search(
    q: str = Query(..., min_length=2, max_length=200, description="Search query (min 2 characters)"),
    type: Optional[str] = Query(None, description="Search scope: levels, subjects, content, or all"),
    limit: int = Query(50, ge=1, le=200, description="Limit results per category"),
):
    """
    Search across all educational resources with relevance scoring.

    Searches in titles, descriptions, names, chapters, and tags in both French and Arabic.
    Results are ranked by relevance.
    """
    result = search_service.search(data_service, query=q, search_type=type, limit=limit)
    return {"success": True, **result}
