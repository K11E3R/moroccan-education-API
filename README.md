# 🇲🇦 Moroccan Education API

A comprehensive public API providing access to educational resources for the Moroccan education system.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com)

## ✨ Features

- 📚 **12 Education Levels** - From Primary School to Baccalaureate
- 📖 **117 Subjects** - Mathematics, Sciences, Languages, and more
- 📝 **2000+ Educational Contents** - Courses, Exercises, Exams, Corrections
- 🌐 **Bilingual Support** - French and Arabic
- 🔍 **Powerful Search** - Search across all resources
- 📊 **Rich Statistics** - Detailed API analytics

## 🎓 Education Levels

| Category | Levels | Age Range |
|----------|--------|-----------|
| **Primaire** | 1ère - 6ème Année | 6-12 years |
| **Collège** | 1ère - 3ème Année | 12-15 years |
| **Lycée** | Tronc Commun, 1ère & 2ème Bac | 15-18 years |

## 📚 Content Types

| Type | French | Arabic | Description |
|------|--------|--------|-------------|
| `cours` | Cours | الدروس | Course materials and lessons |
| `exercice` | Exercices | التمارين | Practice exercises |
| `examen` | Examens | الامتحانات | Examination papers |
| `controle` | Contrôles | الفروض | Continuous assessment tests |
| `correction` | Corrections | التصحيحات | Solutions and corrections |
| `resume` | Résumés | الملخصات | Summary sheets |

## 🚀 Quick Start

### API Endpoints

```bash
# Get all education levels
curl "https://your-api-url/api/v1/levels"

# Get subjects for a specific level
curl "https://your-api-url/api/v1/subjects?level_id=lycee-2bac"

# Get mathematics content
curl "https://your-api-url/api/v1/content?subject_id=mathematiques-lycee-2bac"

# Search for content
curl "https://your-api-url/api/v1/search?q=mathematiques"
```

### JavaScript Example

```javascript
// Fetch all subjects for 2nd year Baccalaureate
const response = await fetch('https://your-api-url/api/v1/subjects?level_id=lycee-2bac');
const data = await response.json();
console.log(data.data); // Array of subjects
```

### Python Example

```python
import requests

# Get all exams for mathematics
response = requests.get(
    "https://your-api-url/api/v1/content",
    params={
        "subject_id": "mathematiques-lycee-2bac",
        "content_type": "examen"
    }
)
exams = response.json()["data"]
for exam in exams:
    print(f"{exam['title']} - {exam['title_ar']}")
```

## 📖 API Documentation

- **Swagger UI**: `/docs` - Interactive API documentation
- **ReDoc**: `/redoc` - Alternative documentation view
- **OpenAPI**: `/openapi.json` - OpenAPI specification

## 🛠️ Local Development

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/K11E3R/moroccan-education-API.git
cd moroccan-education-API

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate data (optional - data is included)
python collectors/generate_quality_data.py

# Run the API
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure

```
moroccan-education-data-collector/
├── api/
│   ├── main.py          # FastAPI application
│   ├── data.json        # Education data
│   └── requirements.txt
├── collectors/
│   ├── moroccan_edu_scraper.py      # Web scraper
│   └── generate_quality_data.py     # Data generator
├── data/
│   └── moroccan_education_data.json
├── Dockerfile
├── railway.toml
├── Procfile
└── requirements.txt
```

## 🚢 Deployment

### Railway (Recommended)

1. Fork this repository
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repository
4. Deploy!

### Docker

```bash
# Build the image
docker build -t moroccan-education-api .

# Run the container
docker run -p 8000:8000 moroccan-education-api
```

### Heroku

```bash
heroku create your-app-name
git push heroku main
```

## 📊 API Response Format

All endpoints return responses in this format:

```json
{
  "success": true,
  "count": 10,
  "total": 100,
  "data": [...]
}
```

## 🔗 Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page with API overview |
| GET | `/api/v1/levels` | Get all education levels |
| GET | `/api/v1/levels/{id}` | Get specific level |
| GET | `/api/v1/subjects` | Get all subjects |
| GET | `/api/v1/subjects/{id}` | Get specific subject |
| GET | `/api/v1/content` | Get educational content |
| GET | `/api/v1/content/{id}` | Get specific content |
| GET | `/api/v1/search` | Search across all resources |
| GET | `/api/v1/stats` | Get API statistics |
| GET | `/health` | Health check |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

- **Email**: prs.online.00@gmail.com
- **Issues**: [GitHub Issues](https://github.com/K11E3R/moroccan-education-API/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Moroccan Ministry of Education for the educational framework
- All contributors and users of this API

---

Made with ❤️ for Morocco 🇲🇦
