# Moroccan Education API - Server

FastAPI server for the Moroccan Education API.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `GET /api/v1/levels` - All levels
- `GET /api/v1/subjects` - All subjects
- `GET /api/v1/search?q=query` - Search
- `GET /api/v1/stats` - Statistics
- `GET /docs` - Interactive docs

## Testing

```bash
python test_api.py
```

