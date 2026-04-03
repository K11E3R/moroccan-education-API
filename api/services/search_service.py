"""Full-text search service with relevance scoring"""

from typing import Dict, List, Optional, Any
import unicodedata


class SearchService:
    """Provides search across levels, subjects, and content with relevance scoring"""

    @staticmethod
    def normalize(text: str) -> str:
        """Normalize text for search (handle French accents and Arabic)"""
        text = text.lower().strip()
        nfkd = unicodedata.normalize("NFKD", text)
        ascii_text = "".join(c for c in nfkd if not unicodedata.combining(c))
        return ascii_text

    @staticmethod
    def _score_match(query: str, text: str, field_weight: float = 1.0) -> float:
        """Calculate relevance score for a match"""
        q = SearchService.normalize(query)
        t = SearchService.normalize(text)
        if not q or not t:
            return 0.0

        score = 0.0
        if q == t:
            score = 10.0
        elif t.startswith(q):
            score = 8.0
        elif q in t:
            score = 5.0
        else:
            words = q.split()
            matched = sum(1 for w in words if w in t)
            if matched > 0:
                score = (matched / len(words)) * 4.0

        return score * field_weight

    def search(
        self,
        data_service,
        query: str,
        search_type: Optional[str] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Search across all educational resources with relevance scoring"""
        results = {"levels": [], "subjects": [], "content": []}

        if not search_type or search_type in ("levels", "all"):
            scored = []
            for level in data_service.levels:
                score = max(
                    self._score_match(query, level.get("name", ""), 2.0),
                    self._score_match(query, level.get("name_ar", ""), 2.0),
                    self._score_match(query, level.get("id", ""), 1.5),
                    self._score_match(query, level.get("description", ""), 1.0),
                )
                if score > 0:
                    scored.append((score, level))
            scored.sort(key=lambda x: x[0], reverse=True)
            results["levels"] = [item for _, item in scored[:limit]]

        if not search_type or search_type in ("subjects", "all"):
            scored = []
            for subject in data_service.subjects:
                score = max(
                    self._score_match(query, subject.get("name", ""), 2.0),
                    self._score_match(query, subject.get("name_ar", ""), 2.0),
                    self._score_match(query, subject.get("id", ""), 1.5),
                    self._score_match(query, subject.get("description", ""), 1.0),
                )
                if score > 0:
                    scored.append((score, subject))
            scored.sort(key=lambda x: x[0], reverse=True)
            results["subjects"] = [item for _, item in scored[:limit]]

        if not search_type or search_type in ("content", "all"):
            scored = []
            for content in data_service.content:
                score = max(
                    self._score_match(query, content.get("title", ""), 2.0),
                    self._score_match(query, content.get("title_ar", ""), 2.0),
                    self._score_match(query, content.get("description", ""), 1.5),
                    self._score_match(query, content.get("chapter", ""), 1.0),
                    self._score_match(
                        query, " ".join(content.get("tags", [])), 0.8
                    ),
                )
                if score > 0:
                    scored.append((score, content))
            scored.sort(key=lambda x: x[0], reverse=True)
            results["content"] = [item for _, item in scored[:limit]]

        total = sum(len(v) for v in results.values())
        return {
            "query": query,
            "total_results": total,
            "results": results,
        }
