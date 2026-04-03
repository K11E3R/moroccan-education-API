# Moroccan Education API v1.0

A comprehensive, free, public REST API providing access to educational resources for the entire Moroccan education system. From Primary (Primaire) through Baccalaureate — courses, exercises, exams, corrections — all bilingual (French/Arabic).

**Live API** · **Railway Hosted** · **MIT Licensed**

---

## Highlights

| Metric | Value |
|--------|-------|
| Education Levels | 12 (Primary, Middle, High School) |
| Subjects | 117 across all levels |
| Content Items | 2,275+ (courses, exercises, exams, corrections) |
| Languages | French and Arabic |
| Data Sources | AlloSchool, 9rayti, Dyrassa, men.gov.ma, Telmidtice |
| Quality Score | 96%+ (automated daily validation) |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/api/v1/levels` | All education levels with category filtering |
| GET | `/api/v1/levels/{id}` | Specific level with subjects and content stats |
| GET | `/api/v1/subjects` | All subjects with level/category filtering |
| GET | `/api/v1/subjects/{id}` | Specific subject with content breakdown |
| GET | `/api/v1/content` | Educational content with type/level/difficulty/year filters |
| GET | `/api/v1/content/{id}` | Specific content item |
| GET | `/api/v1/search?q=` | Full-text search with relevance scoring |
| GET | `/api/v1/stats` | Comprehensive statistics and analytics |
| GET | `/api/v1/sources` | Data source information |
| GET | `/health` | Health check (used by Railway) |
| GET | `/docs` | Interactive Swagger UI |
| GET | `/redoc` | ReDoc API reference |

### Query Parameters

**Content endpoint** (`/api/v1/content`):
- `level_id` — Filter by level (e.g. `lycee-2bac`)
- `subject_id` — Filter by subject (e.g. `mathematiques-lycee-2bac`)
- `content_type` — Filter by type: `cours`, `exercice`, `examen`, `controle`, `correction`, `resume`
- `difficulty` — Filter by difficulty: `easy`, `medium`, `hard`
- `year` — Filter by year (e.g. `2024`)
- `limit` / `offset` — Pagination (default limit: 50, max: 500)

### Response Format

```json
{
  "success": true,
  "count": 10,
  "total": 150,
  "limit": 50,
  "offset": 0,
  "has_more": true,
  "data": [...]
}
```

## Quick Start

```bash
# Get all education levels
curl "https://your-api.railway.app/api/v1/levels"

# Search for math content
curl "https://your-api.railway.app/api/v1/search?q=mathematiques"

# Get Baccalaureate exams
curl "https://your-api.railway.app/api/v1/content?content_type=examen&level_id=lycee-2bac"
```

## Architecture

```
moroccan-education-API/
├── api/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py             # Settings and configuration
│   ├── models.py             # Pydantic models and schemas
│   ├── data.json             # Education dataset (committed)
│   ├── start.sh              # Startup script
│   ├── test_api.py           # Test suite
│   ├── routes/
│   │   ├── overview.py       # Landing page, /api, /health
│   │   ├── levels.py         # /api/v1/levels endpoints
│   │   ├── subjects.py       # /api/v1/subjects endpoints
│   │   ├── content.py        # /api/v1/content endpoints
│   │   ├── search.py         # /api/v1/search endpoint
│   │   └── stats.py          # /api/v1/stats, /api/v1/sources
│   ├── services/
│   │   ├── data_service.py   # Data loading, indexing, retrieval
│   │   ├── search_service.py # Full-text search with scoring
│   │   ├── stats_service.py  # Analytics and request tracking
│   │   └── cache_service.py  # In-memory TTL cache
│   ├── middleware/
│   │   ├── request_tracking.py  # Request timing and analytics
│   │   └── rate_limiter.py      # Per-IP rate limiting
│   └── templates/
│       └── landing.html      # Landing page template
├── collectors/
│   └── generate_quality_data.py  # Data generator with real sources
├── pipelines/
│   └── validate_data.py      # Data quality validation pipeline
├── config/
│   └── moroccan_education_config.json  # API and scraping config
├── .github/workflows/
│   ├── test-and-deploy.yml       # CI: tests + smoke tests on push/PR
│   └── data-quality-check.yml    # Daily automated quality checks
├── Dockerfile
├── railway.toml
├── Procfile
└── requirements.txt
```

## Local Development

```bash
# Clone
git clone https://github.com/K11E3R/moroccan-education-API.git
cd moroccan-education-API

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt

# (Optional) Regenerate data
python collectors/generate_quality_data.py

# Run validation pipeline
python pipelines/validate_data.py api/data.json

# Start dev server
PYTHONPATH=. uvicorn api.main:app --reload --port 8000
```

Open http://localhost:8000 for the landing page, http://localhost:8000/docs for Swagger UI.

## Deployment

### Railway (Recommended)

1. Fork this repository
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repository
4. Railway auto-deploys from `main` using the `Dockerfile`

### Docker

```bash
docker build -t moroccan-education-api .
docker run -p 8000:8000 moroccan-education-api
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `DEBUG` | `false` | Enable debug mode |
| `RATE_LIMIT_PER_MINUTE` | `60` | Rate limit per IP |
| `CACHE_TTL` | `300` | Cache TTL in seconds |
| `LOG_LEVEL` | `INFO` | Logging level |
| `ENVIRONMENT` | `production` | Environment name |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |

## Data Pipeline

The project includes automated data quality checks:

- **Daily GitHub Actions cron** runs `pipelines/validate_data.py` at 06:00 UTC
- **38 validation checks** covering structure, integrity, bilingual coverage, statistics
- **Quality scoring** with detailed breakdown per dimension
- **Reports** archived as GitHub Actions artifacts

Run manually:

```bash
python pipelines/validate_data.py api/data.json
```

## Rate Limits

- **60 requests per minute** per IP address
- No authentication required
- Response headers include `X-RateLimit-Limit` and `X-RateLimit-Remaining`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Run tests: `python api/test_api.py && python pipelines/validate_data.py api/data.json`
4. Commit and push
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE).

## Contact

- **Email**: prs.online.00@gmail.com
- **GitHub**: [K11E3R/moroccan-education-API](https://github.com/K11E3R/moroccan-education-API)

---

Made for the Moroccan Developer Community
