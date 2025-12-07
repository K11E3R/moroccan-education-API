#!/usr/bin/env python3
"""
Moroccan Education Public API v2.0
Professional API with beautiful documentation
"""

from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from typing import Optional, List, Dict, Any
import json
from pathlib import Path
from datetime import datetime

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title="🇲🇦 Moroccan Education API",
        version="2.0.0",
        description="""
# Moroccan Education Data API

A comprehensive public API providing access to educational resources for the Moroccan education system.

## Features

- 📚 **12 Education Levels** - From Primary to Baccalaureate
- 📖 **100+ Subjects** - Mathematics, Sciences, Languages, and more
- 📝 **1000+ Educational Contents** - Courses, Exercises, Exams
- 🌐 **Bilingual Support** - French and Arabic

## Content Types

| Type | Description |
|------|-------------|
| `cours` | Course materials and lessons |
| `exercice` | Practice exercises |
| `examen` | Examination papers |
| `controle` | Continuous assessment tests |
| `correction` | Solutions and corrections |
| `resume` | Summary sheets |

## Rate Limits

- **Free tier**: 1000 requests/day
- No authentication required for public endpoints

## Support

- 📧 Email: prs.online.00@gmail.com
- 🐙 GitHub: [moroccan-education-API](https://github.com/K11E3R/moroccan-education-API)
        """,
        routes=app.routes,
        tags=[
            {"name": "Overview", "description": "API information and health checks"},
            {"name": "Levels", "description": "Education levels (Primary, Middle, High School)"},
            {"name": "Subjects", "description": "Academic subjects per level"},
            {"name": "Content", "description": "Educational content (courses, exercises, exams)"},
            {"name": "Search", "description": "Search across all resources"},
            {"name": "Statistics", "description": "API usage and data statistics"},
        ]
    )
    
    # Custom logo
    openapi_schema["info"]["x-logo"] = {
        "url": "/favicon.png",
        "altText": "Moroccan Education API"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(
    title="Moroccan Education API",
    description="Comprehensive API for Moroccan education data",
    version="2.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable default redoc
)

app.openapi = custom_openapi

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage
education_data: Dict[str, Any] = {}
api_stats = {
    "start_time": datetime.now(),
    "requests": 0,
    "endpoints_hit": {}
}


def load_data() -> Dict[str, Any]:
    """Load education data from JSON"""
    global education_data
    
    data_paths = [
        Path(__file__).parent / "data.json",
        Path(__file__).parent.parent / "data" / "moroccan_education_data_*.json",
        Path(__file__).parent.parent / "data.json",
    ]
    
    for path in data_paths:
        if "*" in str(path):
            import glob
            matches = sorted(glob.glob(str(path)), reverse=True)
            if matches:
                path = Path(matches[0])
            else:
                continue
        
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    education_data = json.load(f)
                print(f"✅ Loaded data from: {path}")
                print(f"   Levels: {len(education_data.get('levels', []))}")
                print(f"   Subjects: {len(education_data.get('subjects', []))}")
                print(f"   Content: {len(education_data.get('content', []))}")
                return education_data
            except Exception as e:
                print(f"❌ Error loading {path}: {e}")
    
    print("⚠️ No data file found, using empty dataset")
    return {"levels": [], "subjects": [], "content": [], "statistics": {}}


# Load data on startup
education_data = load_data()


# Landing page HTML
LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇲🇦 Moroccan Education API</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a24;
            --accent-primary: #c41e3a;
            --accent-secondary: #006233;
            --accent-gold: #c5a572;
            --text-primary: #ffffff;
            --text-secondary: #a0a0b0;
            --border-color: #2a2a3a;
            --gradient-morocco: linear-gradient(135deg, #c41e3a 0%, #006233 100%);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Space Grotesk', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Animated background */
        .bg-pattern {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            opacity: 0.03;
            background-image: 
                linear-gradient(30deg, var(--accent-primary) 12%, transparent 12.5%, transparent 87%, var(--accent-primary) 87.5%, var(--accent-primary)),
                linear-gradient(150deg, var(--accent-primary) 12%, transparent 12.5%, transparent 87%, var(--accent-primary) 87.5%, var(--accent-primary)),
                linear-gradient(30deg, var(--accent-primary) 12%, transparent 12.5%, transparent 87%, var(--accent-primary) 87.5%, var(--accent-primary)),
                linear-gradient(150deg, var(--accent-primary) 12%, transparent 12.5%, transparent 87%, var(--accent-primary) 87.5%, var(--accent-primary)),
                linear-gradient(60deg, var(--accent-secondary) 25%, transparent 25.5%, transparent 75%, var(--accent-secondary) 75%, var(--accent-secondary)),
                linear-gradient(60deg, var(--accent-secondary) 25%, transparent 25.5%, transparent 75%, var(--accent-secondary) 75%, var(--accent-secondary));
            background-size: 80px 140px;
            background-position: 0 0, 0 0, 40px 70px, 40px 70px, 0 0, 40px 70px;
            animation: patternMove 20s linear infinite;
        }
        
        @keyframes patternMove {
            0% { transform: translateY(0); }
            100% { transform: translateY(-140px); }
        }
        
        .container {
            position: relative;
            z-index: 1;
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        /* Header */
        header {
            text-align: center;
            padding: 4rem 0;
        }
        
        .logo {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        h1 {
            font-size: 3.5rem;
            font-weight: 700;
            background: var(--gradient-morocco);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        }
        
        .subtitle {
            font-size: 1.25rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto;
        }
        
        .version-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: var(--bg-card);
            border: 1px solid var(--accent-gold);
            border-radius: 50px;
            color: var(--accent-gold);
            font-size: 0.9rem;
            margin-top: 1rem;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 3rem 0;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--gradient-morocco);
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent-primary);
            box-shadow: 0 20px 40px rgba(196, 30, 58, 0.1);
        }
        
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: var(--gradient-morocco);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-top: 0.5rem;
        }
        
        /* Endpoints Section */
        .endpoints-section {
            margin: 4rem 0;
        }
        
        .section-title {
            font-size: 2rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .section-title .material-icons {
            color: var(--accent-primary);
        }
        
        .endpoints-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
        }
        
        .endpoint-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .endpoint-card:hover {
            border-color: var(--accent-secondary);
        }
        
        .endpoint-method {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: #10b981;
            color: white;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .endpoint-path {
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent-gold);
            margin: 0.75rem 0;
            font-size: 1rem;
        }
        
        .endpoint-desc {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        /* Quick Start */
        .quickstart {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            margin: 3rem 0;
        }
        
        .code-block {
            background: var(--bg-primary);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            overflow-x: auto;
            position: relative;
        }
        
        .code-block code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #e0e0e0;
        }
        
        .code-block .comment { color: #6a9955; }
        .code-block .keyword { color: #569cd6; }
        .code-block .string { color: #ce9178; }
        .code-block .function { color: #dcdcaa; }
        
        .copy-btn {
            position: absolute;
            top: 0.75rem;
            right: 0.75rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.5rem;
            cursor: pointer;
            color: var(--text-secondary);
            transition: all 0.2s;
        }
        
        .copy-btn:hover {
            color: var(--accent-gold);
            border-color: var(--accent-gold);
        }
        
        /* CTA Buttons */
        .cta-section {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 3rem 0;
            flex-wrap: wrap;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            cursor: pointer;
            border: none;
        }
        
        .btn-primary {
            background: var(--gradient-morocco);
            color: white;
        }
        
        .btn-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(196, 30, 58, 0.3);
        }
        
        .btn-secondary {
            background: transparent;
            border: 2px solid var(--accent-secondary);
            color: var(--accent-secondary);
        }
        
        .btn-secondary:hover {
            background: var(--accent-secondary);
            color: white;
        }
        
        /* Footer */
        footer {
            text-align: center;
            padding: 3rem 0;
            border-top: 1px solid var(--border-color);
            margin-top: 4rem;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }
        
        .footer-links a {
            color: var(--text-secondary);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: color 0.2s;
        }
        
        .footer-links a:hover {
            color: var(--accent-gold);
        }
        
        .copyright {
            color: var(--text-secondary);
            font-size: 0.875rem;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            h1 { font-size: 2.5rem; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .endpoints-grid { grid-template-columns: 1fr; }
        }
        
        /* Live indicator */
        .live-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid #10b981;
            border-radius: 50px;
            color: #10b981;
            font-size: 0.85rem;
            margin-left: 1rem;
        }
        
        .live-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    
    <div class="container">
        <header>
            <div class="logo">🇲🇦</div>
            <h1>Moroccan Education API</h1>
            <p class="subtitle">
                A comprehensive public API providing access to educational resources 
                for the entire Moroccan education system - from Primary to Baccalaureate
            </p>
            <span class="version-badge">v2.0.0</span>
            <span class="live-indicator">
                <span class="live-dot"></span>
                API Online
            </span>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <span class="material-icons stat-icon">school</span>
                <div class="stat-value" id="levels-count">{{LEVELS_COUNT}}</div>
                <div class="stat-label">Education Levels</div>
            </div>
            <div class="stat-card">
                <span class="material-icons stat-icon">menu_book</span>
                <div class="stat-value" id="subjects-count">{{SUBJECTS_COUNT}}</div>
                <div class="stat-label">Subjects</div>
            </div>
            <div class="stat-card">
                <span class="material-icons stat-icon">description</span>
                <div class="stat-value" id="content-count">{{CONTENT_COUNT}}</div>
                <div class="stat-label">Educational Contents</div>
            </div>
            <div class="stat-card">
                <span class="material-icons stat-icon">language</span>
                <div class="stat-value">2</div>
                <div class="stat-label">Languages (FR/AR)</div>
            </div>
        </div>
        
        <div class="cta-section">
            <a href="/docs" class="btn btn-primary">
                <span class="material-icons">api</span>
                Interactive Docs
            </a>
            <a href="/redoc" class="btn btn-secondary">
                <span class="material-icons">description</span>
                API Reference
            </a>
        </div>
        
        <section class="endpoints-section">
            <h2 class="section-title">
                <span class="material-icons">bolt</span>
                Quick Endpoints
            </h2>
            
            <div class="endpoints-grid">
                <div class="endpoint-card">
                    <span class="endpoint-method">GET</span>
                    <div class="endpoint-path">/api/v1/levels</div>
                    <p class="endpoint-desc">Get all education levels (Primary, Middle School, High School)</p>
                </div>
                <div class="endpoint-card">
                    <span class="endpoint-method">GET</span>
                    <div class="endpoint-path">/api/v1/subjects</div>
                    <p class="endpoint-desc">Get all subjects with optional level filtering</p>
                </div>
                <div class="endpoint-card">
                    <span class="endpoint-method">GET</span>
                    <div class="endpoint-path">/api/v1/content</div>
                    <p class="endpoint-desc">Get educational content (courses, exercises, exams)</p>
                </div>
                <div class="endpoint-card">
                    <span class="endpoint-method">GET</span>
                    <div class="endpoint-path">/api/v1/search?q={query}</div>
                    <p class="endpoint-desc">Search across all educational resources</p>
                </div>
                <div class="endpoint-card">
                    <span class="endpoint-method">GET</span>
                    <div class="endpoint-path">/api/v1/stats</div>
                    <p class="endpoint-desc">Get API statistics and metadata</p>
                </div>
                <div class="endpoint-card">
                    <span class="endpoint-method">GET</span>
                    <div class="endpoint-path">/health</div>
                    <p class="endpoint-desc">API health check endpoint</p>
                </div>
            </div>
        </section>
        
        <section class="quickstart">
            <h2 class="section-title">
                <span class="material-icons">code</span>
                Quick Start
            </h2>
            
            <div class="code-block">
                <button class="copy-btn" onclick="copyCode(this)">
                    <span class="material-icons">content_copy</span>
                </button>
                <code><span class="comment"># Fetch all education levels</span>
<span class="keyword">curl</span> <span class="string">"{{BASE_URL}}/api/v1/levels"</span>

<span class="comment"># Get subjects for a specific level</span>
<span class="keyword">curl</span> <span class="string">"{{BASE_URL}}/api/v1/subjects?level_id=lycee-2bac"</span>

<span class="comment"># Search for mathematics content</span>
<span class="keyword">curl</span> <span class="string">"{{BASE_URL}}/api/v1/search?q=mathematiques"</span></code>
            </div>
            
            <h3 style="margin-top: 2rem; color: var(--text-secondary);">JavaScript Example</h3>
            <div class="code-block">
                <button class="copy-btn" onclick="copyCode(this)">
                    <span class="material-icons">content_copy</span>
                </button>
                <code><span class="comment">// Fetch mathematics courses for Baccalaureate</span>
<span class="keyword">const</span> response = <span class="keyword">await</span> <span class="function">fetch</span>(<span class="string">'{{BASE_URL}}/api/v1/content?subject_id=mathematiques-lycee-2bac'</span>);
<span class="keyword">const</span> data = <span class="keyword">await</span> response.<span class="function">json</span>();
console.<span class="function">log</span>(data.data); <span class="comment">// Array of educational content</span></code>
            </div>
            
            <h3 style="margin-top: 2rem; color: var(--text-secondary);">Python Example</h3>
            <div class="code-block">
                <button class="copy-btn" onclick="copyCode(this)">
                    <span class="function">import</span> requests

<span class="comment"># Get all subjects for middle school</span>
response = requests.get(<span class="string">"{{BASE_URL}}/api/v1/subjects"</span>, params={<span class="string">"level_id"</span>: <span class="string">"college-3"</span>})
subjects = response.json()[<span class="string">"data"</span>]

<span class="keyword">for</span> subject <span class="keyword">in</span> subjects:
    print(f<span class="string">"{subject['name']} - {subject['name_ar']}"</span>)</code>
            </div>
        </section>
        
        <footer>
            <div class="footer-links">
                <a href="https://github.com/K11E3R/moroccan-education-API" target="_blank">
                    <span class="material-icons">code</span>
                    GitHub
                </a>
                <a href="mailto:prs.online.00@gmail.com">
                    <span class="material-icons">email</span>
                    Contact
                </a>
                <a href="/docs">
                    <span class="material-icons">api</span>
                    API Docs
                </a>
            </div>
            <p class="copyright">
                © 2025 Moroccan Education API • MIT License • Made with ❤️ for Morocco
            </p>
        </footer>
    </div>
    
    <script>
        function copyCode(btn) {
            const codeBlock = btn.parentElement.querySelector('code');
            const text = codeBlock.textContent;
            navigator.clipboard.writeText(text);
            btn.innerHTML = '<span class="material-icons">check</span>';
            setTimeout(() => {
                btn.innerHTML = '<span class="material-icons">content_copy</span>';
            }, 2000);
        }
    </script>
</body>
</html>
"""


# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Moroccan Education API - Docs",
        swagger_favicon_url="/favicon.png",
        swagger_ui_parameters={
            "deepLinking": True,
            "displayRequestDuration": True,
            "docExpansion": "list",
            "operationsSorter": "alpha",
            "filter": True,
            "tagsSorter": "alpha",
            "syntaxHighlight.theme": "monokai",
        }
    )


@app.get("/redoc", include_in_schema=False)
async def custom_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Moroccan Education API - Reference",
        redoc_favicon_url="/favicon.png",
    )


@app.get("/", response_class=HTMLResponse, tags=["Overview"])
async def root(request: Request):
    """
    Landing page with API overview and documentation links.
    """
    stats = education_data.get("statistics", {})
    
    html = LANDING_PAGE.replace("{{LEVELS_COUNT}}", str(stats.get("total_levels", len(education_data.get("levels", [])))))
    html = html.replace("{{SUBJECTS_COUNT}}", str(stats.get("total_subjects", len(education_data.get("subjects", [])))))
    html = html.replace("{{CONTENT_COUNT}}", str(stats.get("total_content", len(education_data.get("content", [])))))
    
    # Get base URL
    base_url = str(request.base_url).rstrip("/")
    html = html.replace("{{BASE_URL}}", base_url)
    
    return HTMLResponse(content=html)


@app.get("/api", tags=["Overview"])
async def api_info():
    """
    API information and available endpoints.
    """
    return {
        "name": "Moroccan Education API",
        "version": "2.0.0",
        "description": "Comprehensive API for Moroccan education data",
        "endpoints": {
            "levels": "/api/v1/levels",
            "subjects": "/api/v1/subjects",
            "content": "/api/v1/content",
            "search": "/api/v1/search",
            "stats": "/api/v1/stats",
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    }


@app.get("/health", tags=["Overview"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    levels_count = len(education_data.get("levels", []))
    subjects_count = len(education_data.get("subjects", []))
    content_count = len(education_data.get("content", []))
    
    return {
        "status": "healthy" if levels_count > 0 else "degraded",
        "timestamp": datetime.now().isoformat(),
        "data_loaded": levels_count > 0,
        "counts": {
            "levels": levels_count,
            "subjects": subjects_count,
            "content": content_count
        },
        "uptime_seconds": (datetime.now() - api_stats["start_time"]).total_seconds(),
        "version": "2.0.0"
    }


# ==================== LEVELS ENDPOINTS ====================

@app.get("/api/v1/levels", tags=["Levels"])
async def get_levels(
    category: Optional[str] = Query(None, description="Filter by category (primaire/college/lycee)"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit results"),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination")
):
    """
    Get all education levels.
    
    Returns the complete list of Moroccan education levels from Primary (Primaire)
    through Middle School (Collège) to High School (Lycée/Baccalaureate).
    """
    levels = education_data.get("levels", [])
    
    if category:
        levels = [l for l in levels if l.get("category") == category]
    
    total = len(levels)
    levels = levels[offset:]
    
    if limit:
        levels = levels[:limit]
    
    return {
        "success": True,
        "count": len(levels),
        "total": total,
        "data": levels
    }


@app.get("/api/v1/levels/{level_id}", tags=["Levels"])
async def get_level(level_id: str):
    """
    Get a specific education level by ID.
    
    Example IDs: primaire-1, college-3, lycee-2bac
    """
    levels = education_data.get("levels", [])
    level = next((l for l in levels if l["id"] == level_id), None)
    
    if not level:
        raise HTTPException(status_code=404, detail=f"Level '{level_id}' not found")
    
    # Get subject count for this level
    subjects = [s for s in education_data.get("subjects", []) if s.get("level_id") == level_id]
    content = [c for c in education_data.get("content", []) if c.get("level_id") == level_id]
    
    return {
        "success": True,
        "data": {
            **level,
            "subjects_count": len(subjects),
            "content_count": len(content)
        }
    }


# ==================== SUBJECTS ENDPOINTS ====================

@app.get("/api/v1/subjects", tags=["Subjects"])
async def get_subjects(
    level_id: Optional[str] = Query(None, description="Filter by level ID"),
    limit: Optional[int] = Query(None, ge=1, le=200, description="Limit results"),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination")
):
    """
    Get all subjects with optional filtering.
    
    Subjects include Mathematics, French, Arabic, Physics, SVT, etc.
    """
    subjects = education_data.get("subjects", [])
    
    if level_id:
        subjects = [s for s in subjects if s.get("level_id") == level_id]
    
    total = len(subjects)
    subjects = subjects[offset:]
    
    if limit:
        subjects = subjects[:limit]
    
    return {
        "success": True,
        "count": len(subjects),
        "total": total,
        "data": subjects
    }


@app.get("/api/v1/subjects/{subject_id}", tags=["Subjects"])
async def get_subject(subject_id: str):
    """
    Get a specific subject by ID.
    
    Example ID: mathematiques-lycee-2bac
    """
    subjects = education_data.get("subjects", [])
    subject = next((s for s in subjects if s["id"] == subject_id), None)
    
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject '{subject_id}' not found")
    
    # Get content for this subject
    content = [c for c in education_data.get("content", []) if c.get("subject_id") == subject_id]
    content_types = {}
    for c in content:
        ctype = c.get("content_type", "other")
        content_types[ctype] = content_types.get(ctype, 0) + 1
    
    return {
        "success": True,
        "data": {
            **subject,
            "content_count": len(content),
            "content_types": content_types
        }
    }


# ==================== CONTENT ENDPOINTS ====================

@app.get("/api/v1/content", tags=["Content"])
async def get_content(
    level_id: Optional[str] = Query(None, description="Filter by level ID"),
    subject_id: Optional[str] = Query(None, description="Filter by subject ID"),
    content_type: Optional[str] = Query(None, description="Filter by type (cours/exercice/examen/controle/correction/resume)"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty (easy/medium/hard)"),
    limit: Optional[int] = Query(50, ge=1, le=500, description="Limit results"),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination")
):
    """
    Get educational content with flexible filtering.
    
    Content types:
    - **cours**: Course materials and lessons
    - **exercice**: Practice exercises
    - **examen**: Examination papers
    - **controle**: Continuous assessment tests
    - **correction**: Solutions and corrections
    - **resume**: Summary sheets
    """
    content = education_data.get("content", [])
    
    if level_id:
        content = [c for c in content if c.get("level_id") == level_id]
    
    if subject_id:
        content = [c for c in content if c.get("subject_id") == subject_id]
    
    if content_type:
        content = [c for c in content if c.get("content_type") == content_type]
    
    if difficulty:
        content = [c for c in content if c.get("difficulty") == difficulty]
    
    total = len(content)
    content = content[offset:offset + limit]
    
    return {
        "success": True,
        "count": len(content),
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": content
    }


@app.get("/api/v1/content/{content_id}", tags=["Content"])
async def get_content_item(content_id: str):
    """
    Get a specific content item by ID.
    """
    content = education_data.get("content", [])
    item = next((c for c in content if c["id"] == content_id), None)
    
    if not item:
        raise HTTPException(status_code=404, detail=f"Content '{content_id}' not found")
    
    return {
        "success": True,
        "data": item
    }


# Legacy endpoint for compatibility
@app.get("/api/v1/courses", tags=["Content"], include_in_schema=False)
async def get_courses_legacy(
    level_id: Optional[str] = None,
    subject_id: Optional[str] = None,
    content_type: Optional[str] = None,
    limit: Optional[int] = 50
):
    """Legacy endpoint - redirects to /api/v1/content"""
    return await get_content(level_id, subject_id, content_type, None, limit, 0)


# ==================== SEARCH ENDPOINT ====================

@app.get("/api/v1/search", tags=["Search"])
async def search(
    q: str = Query(..., min_length=2, description="Search query (min 2 characters)"),
    type: Optional[str] = Query(None, description="Search in specific type (levels/subjects/content/all)"),
    language: Optional[str] = Query("fr", description="Search language (fr/ar)"),
    limit: Optional[int] = Query(50, ge=1, le=200, description="Limit results per category")
):
    """
    Search across all educational resources.
    
    Searches in titles, descriptions, and names in both French and Arabic.
    """
    q_lower = q.lower()
    results = {
        "levels": [],
        "subjects": [],
        "content": []
    }
    
    # Search levels
    if not type or type in ["levels", "all"]:
        for level in education_data.get("levels", []):
            searchable = f"{level.get('name', '')} {level.get('name_ar', '')} {level.get('id', '')}".lower()
            if q_lower in searchable:
                results["levels"].append(level)
    
    # Search subjects
    if not type or type in ["subjects", "all"]:
        for subject in education_data.get("subjects", []):
            searchable = f"{subject.get('name', '')} {subject.get('name_ar', '')} {subject.get('id', '')}".lower()
            if q_lower in searchable:
                results["subjects"].append(subject)
    
    # Search content
    if not type or type in ["content", "all"]:
        for content in education_data.get("content", []):
            searchable = f"{content.get('title', '')} {content.get('title_ar', '')} {content.get('description', '')}".lower()
            if q_lower in searchable:
                results["content"].append(content)
    
    # Apply limits
    results["levels"] = results["levels"][:limit]
    results["subjects"] = results["subjects"][:limit]
    results["content"] = results["content"][:limit]
    
    total = len(results["levels"]) + len(results["subjects"]) + len(results["content"])
    
    return {
        "success": True,
        "query": q,
        "total_results": total,
        "results": results
    }


# ==================== STATISTICS ENDPOINT ====================

@app.get("/api/v1/stats", tags=["Statistics"])
async def get_stats():
    """
    Get comprehensive API statistics and metadata.
    """
    stats = education_data.get("statistics", {})
    
    # Calculate content type distribution
    content_types = {}
    for c in education_data.get("content", []):
        ctype = c.get("content_type", "other")
        content_types[ctype] = content_types.get(ctype, 0) + 1
    
    # Calculate level distribution
    level_distribution = {}
    for c in education_data.get("content", []):
        level_id = c.get("level_id", "unknown")
        level_distribution[level_id] = level_distribution.get(level_id, 0) + 1
    
    return {
        "success": True,
        "data": {
            "total_levels": stats.get("total_levels", len(education_data.get("levels", []))),
            "total_subjects": stats.get("total_subjects", len(education_data.get("subjects", []))),
            "total_content": stats.get("total_content", len(education_data.get("content", []))),
            "content_types": content_types,
            "level_distribution": level_distribution,
            "languages": ["fr", "ar"],
            "collection_date": education_data.get("collection_date", "N/A"),
            "api_version": "2.0.0",
            "data_source": "Moroccan Education Websites"
        }
    }


# ==================== FAVICON ====================

@app.get("/favicon.png", include_in_schema=False)
async def favicon():
    """Serve favicon"""
    favicon_path = Path(__file__).parent / "favicon.png"
    if favicon_path.exists():
        from fastapi.responses import FileResponse
        return FileResponse(favicon_path)
    raise HTTPException(status_code=404)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
