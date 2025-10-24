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
import os
import httpx
import asyncio
from pathlib import Path
from datetime import datetime, timedelta

app = FastAPI(
    title="Moroccan Education API",
    description="Complete public API for Moroccan education data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "email": "prs.online.00@gmail.com",
        "url": "https://github.com/K11E3R/moroccan-education-API (private repository)"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
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

# Railway API configuration
RAILWAY_API_TOKEN = os.getenv("RAILWAY_API_TOKEN", "")
RAILWAY_PROJECT_ID = os.getenv("RAILWAY_PROJECT_ID", "")
RAILWAY_API_BASE = "https://backboard.railway.app/v1"

# Cache for Railway consumption data
railway_consumption_cache = {
    "data": None,
    "last_updated": None,
    "cache_duration": 300  # 5 minutes
}

# Simple uptime tracking
uptime_tracker = {
    "start_time": datetime.now(),
    "total_requests": 0,
    "successful_requests": 0
}

def calculate_real_uptime():
    """Calculate real-time uptime based on successful requests"""
    global uptime_tracker
    
    if uptime_tracker["total_requests"] == 0:
        return "100.00%"
    
    success_rate = (uptime_tracker["successful_requests"] / uptime_tracker["total_requests"]) * 100
    return f"{success_rate:.2f}%"

async def get_railway_consumption():
    """Get Railway consumption data from API"""
    global railway_consumption_cache, uptime_tracker
    
    # Track request
    uptime_tracker["total_requests"] += 1
    
    # Check cache first
    if (railway_consumption_cache["data"] and 
        railway_consumption_cache["last_updated"] and 
        datetime.now() - railway_consumption_cache["last_updated"] < timedelta(seconds=railway_consumption_cache["cache_duration"])):
        uptime_tracker["successful_requests"] += 1
        return railway_consumption_cache["data"]
    
    if not RAILWAY_API_TOKEN or not RAILWAY_PROJECT_ID:
        return {
            "error": "Railway API credentials not configured",
            "status": "not_configured"
        }
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {RAILWAY_API_TOKEN}"}
            
            # Try different Railway API endpoints
            endpoints_to_try = [
                f"{RAILWAY_API_BASE}/projects/{RAILWAY_PROJECT_ID}/usage",
                f"{RAILWAY_API_BASE}/projects/{RAILWAY_PROJECT_ID}",
                f"https://api.railway.app/v1/projects/{RAILWAY_PROJECT_ID}/usage",
                f"https://api.railway.app/v1/projects/{RAILWAY_PROJECT_ID}"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    response = await client.get(endpoint, headers=headers, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        railway_consumption_cache["data"] = data
                        railway_consumption_cache["last_updated"] = datetime.now()
                        uptime_tracker["successful_requests"] += 1
                        return data
                    elif response.status_code == 401:
                        return {"error": "Railway API authentication failed - check your token"}
                    elif response.status_code == 404:
                        continue  # Try next endpoint
                    else:
                        return {"error": f"Railway API error: {response.status_code} - {response.text}"}
                except Exception as e:
                    continue  # Try next endpoint
            
            # If all endpoints fail, return minimal real data only
            return {
                "error": "Railway API endpoints not accessible",
                "status": "api_unavailable",
                "message": "Real Railway API data not available - check API credentials and endpoints",
                "last_attempt": datetime.now().isoformat(),
                "endpoints_tried": len(endpoints_to_try)
            }
                
    except Exception as e:
        return {"error": f"Railway API error: {str(e)}"}

async def get_dynamic_hosting_info():
    """Get dynamic hosting information with real-time uptime"""
    railway_data = await get_railway_consumption()
    real_uptime = calculate_real_uptime()
    
    # Determine status based on real uptime
    uptime_percent = float(real_uptime.replace("%", ""))
    if uptime_percent < 95:
        status = "degraded"
    elif uptime_percent < 99:
        status = "moderate_load"
    else:
        status = "operational"
    
    # Only show real data - no fake information
    hosting_info = {
        "platform": "Railway",
        "status": status,
        "uptime": real_uptime,
        "account_linked": True,
        "metrics": {
            "real_uptime": real_uptime,
            "total_requests": uptime_tracker["total_requests"],
            "successful_requests": uptime_tracker["successful_requests"],
            "tracking_since": uptime_tracker["start_time"].isoformat()
        }
    }
    
    # Only add consumption if Railway API is accessible
    if "error" not in railway_data:
        hosting_info["consumption"] = railway_data
        hosting_info["region"] = railway_data.get("region", "Unknown")
    else:
        hosting_info["consumption"] = {
            "status": "unavailable",
            "error": railway_data["error"],
            "message": "Railway API not accessible"
        }
        hosting_info["region"] = "Unknown"
    
    return hosting_info

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
        
        print(f"[OK] Loaded data from: {data_file.name}")
        print(f"[INFO] Data contains: {len(education_data.get('levels', []))} levels, {len(education_data.get('subjects', []))} subjects, {len(education_data.get('content', []))} content items")
        
        return education_data
        
    except Exception as e:
        print(f"[ERROR] Error loading data: {e}")
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
    """API information and welcome message with dynamic Railway consumption data"""
    try:
        stats = education_data.get("statistics", {})
        
        # Get comprehensive hosting and monitoring data
        consumption_data = await get_railway_consumption()
        real_uptime = calculate_real_uptime()
        
        # Calculate real metrics
        total_requests = uptime_tracker["total_requests"]
        successful_requests = uptime_tracker["successful_requests"]
        failed_requests = total_requests - successful_requests
        success_rate = (successful_requests / max(1, total_requests)) * 100
        
        # Calculate request rate
        duration_minutes = (datetime.now() - uptime_tracker["start_time"]).total_seconds() / 60
        requests_per_minute = total_requests / max(1, duration_minutes)
        
        # Determine health status
        if success_rate >= 99:
            health_status = "excellent"
            health_color = "green"
        elif success_rate >= 95:
            health_status = "good"
            health_color = "yellow"
        elif success_rate >= 90:
            health_status = "warning"
            health_color = "orange"
        else:
            health_status = "critical"
            health_color = "red"
        
        # Essential hosting information only
        hosting_details = {
            "platform": "Railway",
            "status": "operational" if success_rate >= 95 else "degraded",
            "uptime": real_uptime,
            "region": "Global CDN",
            "account_linked": True,
            
            # Essential performance metrics
            "performance": {
                "uptime": real_uptime,
                "health_status": health_status,
                "total_requests": total_requests,
                "success_rate": f"{success_rate:.2f}%",
                "last_request_time": datetime.now().isoformat()
            },
            
            # Railway API Status
            "railway_api": {
                "status": "unavailable" if "error" in consumption_data else "available",
                "authentication": "configured" if RAILWAY_API_TOKEN else "missing"
            }
        }
        
        return {
            "message": "🇲🇦 Moroccan Education Public API - UNDER MAINTENANCE & DATA IMPROVEMENT",
            "description": "API for Moroccan education data - Currently under maintenance, data cleaning and improvement in progress",
            "version": "1.0.0",
            
            "hosting": hosting_details,
            
            "support": {
                "email": "prs.online.00@gmail.com",
                "github_issues": "https://github.com/K11E3R/moroccan-education-API/issues",
                "response_time": "8-12 hours",
                "documentation": "/docs",
                "api_status": "/health"
            },
            
            "endpoints": {
                "levels": "/api/v1/levels",
                "subjects": "/api/v1/subjects", 
                "courses": "/api/v1/courses",
                "stats": "/api/v1/stats",
                "search": "/api/v1/search"
            },
            
            "docs": "/docs",
            "status": hosting_details.get("status", "operational"),
            "data_source": "Moroccan Education Data",
            "last_update": education_data.get("collection_date", "N/A"),
            "total_items": stats.get("total_content", len(education_data.get("content", []))),
            "levels_count": stats.get("total_levels", len(education_data.get("levels", []))),
            "subjects_count": stats.get("total_subjects", len(education_data.get("subjects", []))),
            "github": "https://github.com/K11E3R/moroccan-education-API",
            "email": "prs.online.00@gmail.com",
            "license": "MIT License",
            "project_status": "Under Maintenance - Data Cleaning & Improvement"
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
