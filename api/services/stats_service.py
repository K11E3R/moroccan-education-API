"""Statistics and analytics service"""

from typing import Dict, Any
from datetime import datetime
import threading


class StatsService:
    """Tracks API statistics and computes data analytics"""

    def __init__(self):
        self.start_time = datetime.now()
        self._lock = threading.Lock()
        self.total_requests = 0
        self.endpoint_hits: Dict[str, int] = {}

    def record_request(self, path: str):
        """Thread-safe request counter"""
        with self._lock:
            self.total_requests += 1
            self.endpoint_hits[path] = self.endpoint_hits.get(path, 0) + 1

    @property
    def uptime_seconds(self) -> float:
        return (datetime.now() - self.start_time).total_seconds()

    def get_api_stats(self, data_service) -> Dict[str, Any]:
        """Compute comprehensive statistics about the data and API"""
        stats = data_service.statistics
        content_types = data_service.get_content_type_counts()

        level_distribution = {}
        for c in data_service.content:
            lid = c.get("level_id", "unknown")
            level_distribution[lid] = level_distribution.get(lid, 0) + 1

        category_distribution = {}
        for level in data_service.levels:
            cat = level.get("category", "unknown")
            category_distribution[cat] = category_distribution.get(cat, 0) + 1

        difficulty_distribution = {}
        for c in data_service.content:
            diff = c.get("difficulty", "unrated")
            difficulty_distribution[diff] = difficulty_distribution.get(diff, 0) + 1

        subjects_per_level = {}
        for s in data_service.subjects:
            lid = s.get("level_id", "unknown")
            subjects_per_level[lid] = subjects_per_level.get(lid, 0) + 1

        avg_content = (
            len(data_service.content) / len(data_service.subjects)
            if data_service.subjects
            else 0
        )

        sources_used = set()
        for c in data_service.content:
            src = c.get("source")
            if src:
                sources_used.add(src)

        return {
            "total_levels": len(data_service.levels),
            "total_subjects": len(data_service.subjects),
            "total_content": len(data_service.content),
            "content_types": content_types,
            "level_distribution": level_distribution,
            "category_distribution": category_distribution,
            "difficulty_distribution": difficulty_distribution,
            "subjects_per_level": subjects_per_level,
            "avg_content_per_subject": round(avg_content, 2),
            "languages": ["fr", "ar"],
            "data_sources": list(sources_used) if sources_used else ["generated"],
            "collection_date": data_service.data.get("collection_date", "N/A"),
            "data_version": data_service.data.get("version", "1.0.0"),
            "api_version": "1.0.0",
            "quality_score": data_service.metadata.get("quality_score", 0),
            "api_metrics": {
                "uptime_seconds": round(self.uptime_seconds, 2),
                "total_requests": self.total_requests,
                "top_endpoints": dict(
                    sorted(
                        self.endpoint_hits.items(),
                        key=lambda x: x[1],
                        reverse=True,
                    )[:10]
                ),
            },
        }
