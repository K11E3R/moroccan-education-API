#!/usr/bin/env python3
"""
Moroccan Education Public API v1.0
Complete v1 API with all endpoints for comprehensive testing
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
import json
from pathlib import Path
from datetime import datetime

app = FastAPI(
    title="Moroccan Education API",
    description="Complete public API for Moroccan education data",
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

# Global variables for data
education_data = {}

def load_data():
    """Load education data from JSON file"""
    global education_data
    
    # Try multiple paths for data file
    possible_paths = [
        Path(__file__).parent / "data.json",
        Path(__file__).parent.parent / "data" / "cleaned_data_20251023_173829.json",
        Path(__file__).parent.parent / "data" / "corrected_data_20251023_173332.json"
    ]
    
    data_file = None
    for path in possible_paths:
        if path.exists():
            data_file = path
            break
    
    if not data_file:
        print("❌ No data file found!")
        return {
            "levels": [],
            "subjects": [],
            "content": [],
            "statistics": {"total_levels": 0, "total_subjects": 0, "total_content": 0},
            "error": "No data file found"
        }
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            education_data = json.load(f)
        
        print(f"✅ Loaded data from: {data_file.name}")
        print(f"📊 Data contains: {len(education_data.get('levels', []))} levels, {len(education_data.get('subjects', []))} subjects, {len(education_data.get('content', []))} content items")
        
        return education_data
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return {
            "levels": [],
            "subjects": [],
            "content": [],
            "statistics": {"total_levels": 0, "total_subjects": 0, "total_content": 0},
            "error": f"Error loading data: {str(e)}"
        }

# Load data on startup
education_data = load_data()

@app.get("/")
async def root():
    """API information and welcome message"""
    try:
        stats = education_data.get("statistics", {})
        
        return {
            "message": "🇲🇦 Moroccan Education Public API",
            "description": "Complete API for Moroccan education data",
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
            "data_source": "Moroccan Education Data",
            "last_update": education_data.get("collection_date", "N/A"),
            "total_items": stats.get("total_content", len(education_data.get("content", []))),
            "levels_count": stats.get("total_levels", len(education_data.get("levels", []))),
            "subjects_count": stats.get("total_subjects", len(education_data.get("subjects", []))),
            "made_by": "Moroccan Developers Community",
            "github": "https://github.com/K11E3R/moroccan-education-API",
            "email": "prs.online.00@gmail.com"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )

@app.get("/api/v1/levels")
async def get_levels(
    language: Optional[str] = Query(None, description="Filter by language (fr/ar)"),
    limit: Optional[int] = Query(None, description="Limit results")
):
    """Get all education levels"""
    try:
        levels = education_data.get("levels", [])
        
        if limit:
            levels = levels[:limit]
        
        return {
            "success": True,
            "count": len(levels),
            "data": levels
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving levels: {str(e)}")

@app.get("/api/v1/levels/{level_id}")
async def get_level(level_id: str):
    """Get specific level by ID"""
    try:
        levels = education_data.get("levels", [])
        level = next((l for l in levels if l["id"] == level_id), None)
        
        if not level:
            raise HTTPException(status_code=404, detail="Level not found")
        
        return {
            "success": True,
            "data": level
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving level: {str(e)}")

@app.get("/api/v1/subjects")
async def get_subjects(
    level_id: Optional[str] = Query(None, description="Filter by level ID"),
    language: Optional[str] = Query(None, description="Filter by language (fr/ar)"),
    limit: Optional[int] = Query(None, description="Limit results")
):
    """Get all subjects"""
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving subjects: {str(e)}")

@app.get("/api/v1/subjects/{subject_id}")
async def get_subject(subject_id: str):
    """Get specific subject by ID"""
    try:
        subjects = education_data.get("subjects", [])
        subject = next((s for s in subjects if s["id"] == subject_id), None)
        
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        
        return {
            "success": True,
            "data": subject
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving subject: {str(e)}")

@app.get("/api/v1/courses")
async def get_courses(
    level_id: Optional[str] = Query(None, description="Filter by level ID"),
    subject_id: Optional[str] = Query(None, description="Filter by subject ID"),
    content_type: Optional[str] = Query(None, description="Filter by type (course/exercise/exam)"),
    limit: Optional[int] = Query(None, description="Limit results")
):
    """Get all courses and educational content"""
    try:
        courses = education_data.get("content", education_data.get("courses", []))
        
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving courses: {str(e)}")

@app.get("/api/v1/search")
async def search(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Search in (levels/subjects/courses/all)"),
    language: Optional[str] = Query("fr", description="Search language (fr/ar)")
):
    """Search across all education data"""
    try:
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
            for course in education_data.get("content", education_data.get("courses", [])):
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching: {str(e)}")

@app.get("/api/v1/stats")
async def get_stats():
    """Get API statistics and metadata"""
    try:
        stats = education_data.get("statistics", {})
        levels_count = len(education_data.get("levels", []))
        subjects_count = len(education_data.get("subjects", []))
        courses_count = len(education_data.get("content", []))
        
        return {
            "success": True,
            "data": {
                "total_items": stats.get("total_content", courses_count),
                "levels_count": stats.get("total_levels", levels_count),
                "subjects_count": stats.get("total_subjects", subjects_count),
                "courses_count": stats.get("total_content", courses_count),
                "content_count": stats.get("total_content", courses_count),
                "languages": ["fr", "ar"],
                "last_update": education_data.get("collection_date", "N/A"),
                "data_source": "Moroccan Education Data",
                "api_version": "1.0.0",
                "status": "operational"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        levels_count = len(education_data.get("levels", []))
        subjects_count = len(education_data.get("subjects", []))
        content_count = len(education_data.get("content", []))
        
        health_status = "healthy"
        issues = []
        
        if not education_data or education_data.get("error"):
            health_status = "unhealthy"
            issues.append("Data not loaded")
        
        if levels_count == 0:
            health_status = "degraded"
            issues.append("No levels found")
        
        if subjects_count == 0:
            health_status = "degraded"
            issues.append("No subjects found")
        
        return {
            "status": health_status,
            "timestamp": datetime.now().isoformat(),
            "data_loaded": levels_count > 0,
            "levels_count": levels_count,
            "subjects_count": subjects_count,
            "content_count": content_count,
            "issues": issues,
            "api_version": "1.0.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
