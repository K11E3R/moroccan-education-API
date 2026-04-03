"""Pydantic models for the Moroccan Education API v1.0"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class ContentType(str, Enum):
    COURS = "cours"
    EXERCICE = "exercice"
    EXAMEN = "examen"
    CONTROLE = "controle"
    CORRECTION = "correction"
    RESUME = "resume"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Category(str, Enum):
    PRIMAIRE = "primaire"
    COLLEGE = "college"
    LYCEE = "lycee"


class SearchType(str, Enum):
    LEVELS = "levels"
    SUBJECTS = "subjects"
    CONTENT = "content"
    ALL = "all"


class Language(str, Enum):
    FR = "fr"
    AR = "ar"


class Level(BaseModel):
    id: str
    name: str
    name_ar: str
    order: int
    category: Category
    description: str
    icon: Optional[str] = None
    color: Optional[str] = None
    age_range: Optional[str] = None


class Subject(BaseModel):
    id: str
    name: str
    name_ar: str
    level_id: str
    level_name: Optional[str] = None
    level_name_ar: Optional[str] = None
    category: Category
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    content_count: int = 0


class ContentItem(BaseModel):
    id: str
    title: str
    title_ar: Optional[str] = None
    level_id: str
    subject_id: str
    content_type: ContentType
    description: Optional[str] = None
    description_ar: Optional[str] = None
    chapter: Optional[str] = None
    chapter_ar: Optional[str] = None
    difficulty: Optional[Difficulty] = None
    duration_minutes: Optional[int] = None
    url: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    year: Optional[str] = None
    semester: Optional[str] = None
    semester_ar: Optional[str] = None
    exam_type: Optional[str] = None
    exam_type_ar: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    last_verified: Optional[str] = None


class PaginatedResponse(BaseModel):
    success: bool = True
    count: int
    total: int
    limit: int
    offset: int
    has_more: bool
    data: List[Any]


class SingleResponse(BaseModel):
    success: bool = True
    data: Any


class SearchResponse(BaseModel):
    success: bool = True
    query: str
    total_results: int
    results: Dict[str, List[Any]]


class StatsResponse(BaseModel):
    success: bool = True
    data: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    data_loaded: bool
    counts: Dict[str, int]
    uptime_seconds: float
    version: str
    data_quality: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
    status_code: int


class DataQualityReport(BaseModel):
    overall_score: float
    checks_passed: int
    checks_failed: int
    total_checks: int
    issues: List[Dict[str, Any]]
    timestamp: str
    details: Dict[str, Any]
