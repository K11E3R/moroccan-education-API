"""Data loading and management service"""

import json
import glob as glob_module
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataService:
    """Manages education data loading, indexing, and retrieval"""

    def __init__(self):
        self.data: Dict[str, Any] = {}
        self._levels_index: Dict[str, Dict] = {}
        self._subjects_index: Dict[str, Dict] = {}
        self._content_index: Dict[str, Dict] = {}
        self._subjects_by_level: Dict[str, List[Dict]] = {}
        self._content_by_level: Dict[str, List[Dict]] = {}
        self._content_by_subject: Dict[str, List[Dict]] = {}
        self._content_by_type: Dict[str, List[Dict]] = {}
        self.loaded_at: Optional[datetime] = None
        self.data_file_path: Optional[str] = None

    def load(self, data_paths: List[Path]) -> Dict[str, Any]:
        """Load education data from JSON with fallback paths"""
        for path in data_paths:
            if "*" in str(path):
                matches = sorted(glob_module.glob(str(path)), reverse=True)
                if matches:
                    path = Path(matches[0])
                else:
                    continue

            if path.exists():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        self.data = json.load(f)
                    self.data_file_path = str(path)
                    self.loaded_at = datetime.now()
                    self._build_indexes()
                    logger.info(f"Loaded data from: {path}")
                    logger.info(
                        f"  Levels: {len(self.levels)} | "
                        f"Subjects: {len(self.subjects)} | "
                        f"Content: {len(self.content)}"
                    )
                    return self.data
                except Exception as e:
                    logger.error(f"Error loading {path}: {e}")

        logger.warning("No data file found, using empty dataset")
        self.data = {"levels": [], "subjects": [], "content": [], "statistics": {}}
        self._build_indexes()
        return self.data

    def _build_indexes(self):
        """Build lookup indexes for fast retrieval"""
        self._levels_index = {l["id"]: l for l in self.levels}
        self._subjects_index = {s["id"]: s for s in self.subjects}
        self._content_index = {c["id"]: c for c in self.content}

        self._subjects_by_level = {}
        for s in self.subjects:
            lid = s.get("level_id", "")
            self._subjects_by_level.setdefault(lid, []).append(s)

        self._content_by_level = {}
        self._content_by_subject = {}
        self._content_by_type = {}
        for c in self.content:
            lid = c.get("level_id", "")
            sid = c.get("subject_id", "")
            ctype = c.get("content_type", "")
            self._content_by_level.setdefault(lid, []).append(c)
            self._content_by_subject.setdefault(sid, []).append(c)
            self._content_by_type.setdefault(ctype, []).append(c)

    @property
    def levels(self) -> List[Dict]:
        return self.data.get("levels", [])

    @property
    def subjects(self) -> List[Dict]:
        return self.data.get("subjects", [])

    @property
    def content(self) -> List[Dict]:
        return self.data.get("content", [])

    @property
    def statistics(self) -> Dict:
        return self.data.get("statistics", {})

    @property
    def metadata(self) -> Dict:
        return self.data.get("metadata", {})

    def get_level(self, level_id: str) -> Optional[Dict]:
        return self._levels_index.get(level_id)

    def get_subject(self, subject_id: str) -> Optional[Dict]:
        return self._subjects_index.get(subject_id)

    def get_content_item(self, content_id: str) -> Optional[Dict]:
        return self._content_index.get(content_id)

    def get_levels(
        self, category: Optional[str] = None, limit: Optional[int] = None, offset: int = 0
    ) -> Tuple[List[Dict], int]:
        """Get levels with optional filtering and pagination"""
        levels = self.levels
        if category:
            levels = [l for l in levels if l.get("category") == category]
        total = len(levels)
        levels = levels[offset:]
        if limit:
            levels = levels[:limit]
        return levels, total

    def get_subjects(
        self,
        level_id: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Tuple[List[Dict], int]:
        """Get subjects with filtering"""
        if level_id:
            subjects = self._subjects_by_level.get(level_id, [])
        else:
            subjects = self.subjects

        if category:
            subjects = [s for s in subjects if s.get("category") == category]

        total = len(subjects)
        subjects = subjects[offset:]
        if limit:
            subjects = subjects[:limit]
        return subjects, total

    def get_content(
        self,
        level_id: Optional[str] = None,
        subject_id: Optional[str] = None,
        content_type: Optional[str] = None,
        difficulty: Optional[str] = None,
        year: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Dict], int]:
        """Get content with flexible filtering"""
        if subject_id:
            result = self._content_by_subject.get(subject_id, [])
        elif level_id:
            result = self._content_by_level.get(level_id, [])
        elif content_type:
            result = self._content_by_type.get(content_type, [])
        else:
            result = self.content

        if level_id and subject_id:
            result = [c for c in result if c.get("level_id") == level_id]
        if content_type and not (not subject_id and not level_id):
            result = [c for c in result if c.get("content_type") == content_type]
        if difficulty:
            result = [c for c in result if c.get("difficulty") == difficulty]
        if year:
            result = [c for c in result if c.get("year") == year]

        total = len(result)
        result = result[offset : offset + limit]
        return result, total

    def get_subjects_for_level(self, level_id: str) -> List[Dict]:
        return self._subjects_by_level.get(level_id, [])

    def get_content_for_subject(self, subject_id: str) -> List[Dict]:
        return self._content_by_subject.get(subject_id, [])

    def get_content_for_level(self, level_id: str) -> List[Dict]:
        return self._content_by_level.get(level_id, [])

    def get_content_type_counts(self, items: Optional[List[Dict]] = None) -> Dict[str, int]:
        """Count content by type for given items or all content"""
        if items is None:
            return {k: len(v) for k, v in self._content_by_type.items()}
        counts: Dict[str, int] = {}
        for c in items:
            ctype = c.get("content_type", "other")
            counts[ctype] = counts.get(ctype, 0) + 1
        return counts
