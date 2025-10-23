#!/usr/bin/env python3
"""
Moroccan Education Public API

Free, open API for Moroccan education data.
No authentication required - built for the Moroccan developer community.
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
import json
from pathlib import Path
from datetime import datetime

app = FastAPI(
    title="Moroccan Education API",
    description="Free public API for Moroccan education data - Levels, Subjects, Courses",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for all origins (public API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
DATA_FILE = Path(__file__).parent / "data.json"
if not DATA_FILE.exists():
    # Try alternative paths
    DATA_FILE = Path(__file__).parent.parent / "data" / "fast_collected_data_20251022_233523.json"
    if not DATA_FILE.exists():
        DATA_FILE = Path(__file__).parent / ".." / "data" / "fast_collected_data_20251022_233523.json"
        DATA_FILE = DATA_FILE.resolve()

def load_data():
    """Load education data from JSON file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "levels": [],
            "subjects": [],
            "courses": [],
            "metadata": {}
        }

# Load data on startup
education_data = load_data()

@app.get("/")
async def root():
    """API information and welcome message"""
    return {
        "message": "🇲🇦 Moroccan Education Public API",
        "description": "Free API for Moroccan education data",
        "version": "1.0.0",
        "endpoints": {
            "levels": "/api/v1/levels",
            "subjects": "/api/v1/subjects",
            "courses": "/api/v1/courses",
            "stats": "/api/v1/stats",
            "search": "/api/v1/search"
        },
        "docs": "/docs",
        "status": "operational",
        "data_source": "Public Moroccan Education Websites",
        "last_update": education_data.get("collection_date", "N/A"),
        "total_items": education_data.get("metadata", {}).get("total_items", 0),
        "made_by": "Moroccan Developers Community",
        "github": {
            "repository": "https://github.com/K11E3R/moroccan-education-API",
            "issues": "https://github.com/K11E3R/moroccan-education-API/issues",
            "contribute": "https://github.com/K11E3R/moroccan-education-API#contributing"
        },
        "support": {
            "report_issue": "https://github.com/K11E3R/moroccan-education-API/issues/new",
            "contribute": "Fork the repo and submit a PR",
            "contact": "Open an issue on GitHub"
        }
    }

@app.get("/api/v1/levels")
async def get_levels(
    language: Optional[str] = Query(None, description="Filter by language (fr/ar)"),
    limit: Optional[int] = Query(None, description="Limit results")
):
    """
    Get all education levels
    
    Returns: List of education levels (Primaire, Collège, Lycée, etc.)
    """
    levels = education_data.get("levels", [])
    
    if limit:
        levels = levels[:limit]
    
    return {
        "success": True,
        "count": len(levels),
        "data": levels
    }

@app.get("/api/v1/levels/{level_id}")
async def get_level(level_id: str):
    """Get specific level by ID"""
    levels = education_data.get("levels", [])
    level = next((l for l in levels if l["id"] == level_id), None)
    
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")
    
    return {
        "success": True,
        "data": level
    }

@app.get("/api/v1/subjects")
async def get_subjects(
    level_id: Optional[str] = Query(None, description="Filter by level ID"),
    language: Optional[str] = Query(None, description="Filter by language (fr/ar)"),
    limit: Optional[int] = Query(None, description="Limit results")
):
    """
    Get all subjects
    
    Returns: List of subjects (Math, French, Arabic, Sciences, etc.)
    """
    subjects = education_data.get("subjects", [])
    
    # Filter by level
    if level_id:
        subjects = [s for s in subjects if s.get("level_id") == level_id]
    
    if limit:
        subjects = subjects[:limit]
    
    return {
        "success": True,
        "count": len(subjects),
        "data": subjects
    }

@app.get("/api/v1/subjects/{subject_id}")
async def get_subject(subject_id: str):
    """Get specific subject by ID"""
    subjects = education_data.get("subjects", [])
    subject = next((s for s in subjects if s["id"] == subject_id), None)
    
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    return {
        "success": True,
        "data": subject
    }

@app.get("/api/v1/courses")
async def get_courses(
    level_id: Optional[str] = Query(None, description="Filter by level ID"),
    subject_id: Optional[str] = Query(None, description="Filter by subject ID"),
    content_type: Optional[str] = Query(None, description="Filter by type (course/exercise/exam)"),
    limit: Optional[int] = Query(None, description="Limit results")
):
    """
    Get all courses and educational content
    
    Returns: List of courses, exercises, exams, etc.
    """
    courses = education_data.get("courses", [])
    
    # Filter by level
    if level_id:
        courses = [c for c in courses if c.get("level_id") == level_id]
    
    # Filter by subject
    if subject_id:
        courses = [c for c in courses if c.get("subject_id") == subject_id]
    
    # Filter by content type
    if content_type:
        courses = [c for c in courses if c.get("content_type") == content_type]
    
    if limit:
        courses = courses[:limit]
    
    return {
        "success": True,
        "count": len(courses),
        "data": courses
    }

@app.get("/api/v1/search")
async def search(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Search in (levels/subjects/courses/all)"),
    language: Optional[str] = Query("fr", description="Search language (fr/ar)")
):
    """
    Search across all education data
    
    Returns: Matching levels, subjects, and courses
    """
    q_lower = q.lower()
    results = {
        "levels": [],
        "subjects": [],
        "courses": []
    }
    
    # Search levels
    if not type or type in ["levels", "all"]:
        for level in education_data.get("levels", []):
            name_field = "name" if language == "fr" else "name_ar"
            if q_lower in level.get(name_field, "").lower() or q_lower in level.get("id", "").lower():
                results["levels"].append(level)
    
    # Search subjects
    if not type or type in ["subjects", "all"]:
        for subject in education_data.get("subjects", []):
            name_field = "name" if language == "fr" else "name_ar"
            if q_lower in subject.get(name_field, "").lower() or q_lower in subject.get("id", "").lower():
                results["subjects"].append(subject)
    
    # Search courses
    if not type or type in ["courses", "all"]:
        for course in education_data.get("courses", []):
            title_field = "title" if language == "fr" else "title_ar"
            if q_lower in course.get(title_field, "").lower():
                results["courses"].append(course)
    
    total = len(results["levels"]) + len(results["subjects"]) + len(results["courses"])
    
    return {
        "success": True,
        "query": q,
        "total_results": total,
        "results": results
    }

@app.get("/api/v1/stats")
async def get_stats():
    """
    Get API statistics and metadata
    
    Returns: Collection stats, data quality, and availability
    """
    metadata = education_data.get("metadata", {})
    
    return {
        "success": True,
        "data": {
            "total_items": metadata.get("total_items", 0),
            "levels_count": metadata.get("levels_count", 0),
            "subjects_count": metadata.get("subjects_count", 0),
            "courses_count": metadata.get("courses_count", 0),
            "exercises_count": metadata.get("exercises_count", 0),
            "controls_count": metadata.get("controls_count", 0),
            "exams_count": metadata.get("exams_count", 0),
            "languages": metadata.get("languages", ["fr", "ar"]),
            "quality_score": metadata.get("quality_score", 0),
            "last_update": education_data.get("collection_date", "N/A"),
            "data_source": "Public Moroccan Education Websites",
            "api_version": "1.0.0",
            "status": "operational"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_loaded": len(education_data.get("levels", [])) > 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

