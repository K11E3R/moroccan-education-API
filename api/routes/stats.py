"""Statistics endpoints"""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["Statistics"])

data_service = None
stats_service = None


def init(ds, ss):
    global data_service, stats_service
    data_service = ds
    stats_service = ss


@router.get("/stats")
async def get_stats():
    """
    Get comprehensive API statistics, data analytics, and quality metrics.
    """
    stats = stats_service.get_api_stats(data_service)
    return {"success": True, "data": stats}


@router.get("/sources")
async def get_data_sources():
    """
    Get information about data sources used by the API.
    """
    from api.config import settings

    return {
        "success": True,
        "data": {
            "sources": settings.DATA_SOURCES,
            "total_sources": len(settings.DATA_SOURCES),
            "collection_method": "Automated collection and verification pipeline",
        },
    }
