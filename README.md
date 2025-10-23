# 🇲🇦 Moroccan Education API

Free, open-source REST API providing access to Moroccan education data. Built for developers, by developers.

[![CI/CD](https://github.com/K11E3R/moroccan-education-API/actions/workflows/test-and-deploy.yml/badge.svg)](https://github.com/K11E3R/moroccan-education-API/actions)
[![API Status](https://img.shields.io/badge/API-Live-success)](https://github.com/K11E3R/moroccan-education-API)
[![Tests](https://img.shields.io/badge/tests-passing-success)](./TEST_RESULTS.md)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
[![Data Quality](https://img.shields.io/badge/quality-1.0%2F1.0-success)](./DATA_VISUALIZATION.md)

## ✨ Features

- 🆓 **100% Free** - No authentication, no rate limits
- 🌍 **Bilingual** - French & Arabic support
- 🚀 **Fast** - Optimized async data collection
- 📊 **Rich Data** - 68 items (20 levels + 48 subjects)
- 🎨 **UI Ready** - Colors and icons for each subject
- 🔓 **CORS Enabled** - Use from any domain
- 📱 **Production Ready** - Tested and validated

## 📊 Data Overview

```
🇲🇦 Moroccan Education System
│
├── 📚 20 Education Levels
│   ├── Primaire (الابتدائي)
│   ├── Collège (الإعدادي)
│   ├── Lycée (الثانوي)
│   ├── Baccalauréat (البكالوريا)
│   └── Supérieur (العالي)
│
└── 📑 48 Subjects
    ├── 🔢 Sciences (15): Math, Physics, Chemistry, SVT...
    ├── 📚 Languages (12): French, Arabic, English...
    ├── 🌍 Humanities (10): History, Geography, Philosophy...
    ├── 💻 Technology (6): Informatics, Engineering...
    └── 🎨 Arts & Others (5): Arts, Music, Sports...

Quality Score: 0.85/1.0 | Success Rate: 97.1% | 100% Bilingual
```

**[📊 View Complete Data Visualization →](./DATA_VISUALIZATION.md)**

## 🚀 Quick Start

### Base URL (After Deployment)
```
https://your-app.railway.app
```

### Example Requests

```bash
# Get all education levels
curl https://your-api.railway.app/api/v1/levels

# Get all subjects
curl https://your-api.railway.app/api/v1/subjects

# Search for math subjects
curl "https://your-api.railway.app/api/v1/search?q=math"

# Get statistics
curl https://your-api.railway.app/api/v1/stats
```

### JavaScript Example

```javascript
// Fetch all levels
const response = await fetch('https://your-api.railway.app/api/v1/levels');
const data = await response.json();
console.log(data);

// Search subjects
const search = await fetch('https://your-api.railway.app/api/v1/search?q=mathematiques');
const results = await search.json();
```

### Python Example

```python
import requests

# Get all subjects
response = requests.get('https://your-api.railway.app/api/v1/subjects')
subjects = response.json()

for subject in subjects['data']:
    print(f"{subject['name']} - {subject['name_ar']}")
```

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/api/v1/levels` | GET | Get all education levels |
| `/api/v1/subjects` | GET | Get all subjects |
| `/api/v1/search?q=query` | GET | Search levels and subjects |
| `/api/v1/stats` | GET | Get statistics |
| `/docs` | GET | Interactive API documentation |

## 📊 Response Format

### Level Object
```json
{
  "id": "primaire",
  "name": "Primaire",
  "name_ar": "الابتدائي",
  "subjects_count": 8,
  "courses_count": 150,
  "url": "https://example.com/primaire",
  "source": "public_website",
  "collected_at": "2025-10-22T23:35:13Z"
}
```

### Subject Object
```json
{
  "id": "mathematiques-primaire",
  "name": "Mathématiques",
  "name_ar": "الرياضيات",
  "level_id": "primaire",
  "color": "#3b82f6",
  "icon": "Calculator",
  "courses_count": 150,
  "url": "https://example.com/subject",
  "source": "public_website",
  "collected_at": "2025-10-22T23:35:13Z"
}
```

## 🎨 Subject Colors & Icons

All subjects include color codes and icon names for easy UI integration:

- **Mathématiques** - Blue (#3b82f6) - Calculator
- **Français** - Red (#ef4444) - BookOpen
- **Arabe** - Green (#10b981) - Book
- **Physique** - Orange (#f59e0b) - Atom
- **Chimie** - Green (#10b981) - FlaskConical
- **Informatique** - Indigo (#6366f1) - Monitor

[View complete color scheme →](./DATA_VISUALIZATION.md#-color-scheme)

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- pip or uv

### Setup

```bash
# Clone repository
git clone https://github.com/K11E3R/moroccan-education-API.git
cd moroccan-education-API

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r api/requirements.txt

# Run API locally
cd api
uvicorn main:app --reload

# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Run Tests

```bash
cd api
python test_api.py
```

## 🚀 Deployment

### Deploy to Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy
railway up

# Get public URL
railway domain
```

**[📖 Complete Deployment Guide →](./DEPLOYMENT_GUIDE.md)**

## 📖 Documentation

- **[Data Visualization](./DATA_VISUALIZATION.md)** - Complete data tree and statistics
- **[API Summary](./API_SUMMARY.md)** - Detailed API reference
- **[Deployment Guide](./DEPLOYMENT_GUIDE.md)** - 5 deployment options
- **[Quick Start](./QUICK_START.md)** - Detailed usage guide
- **[Test Results](./TEST_RESULTS.md)** - API test results
- **[GitHub Setup](./GITHUB_SETUP.md)** - GitHub & Railway setup

## 📊 Data Collection

Update the data anytime:

```bash
# Run fast collector
python collectors/fast_collector.py

# Data saved to data/fast_collected_data_*.json
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔒 Privacy & Compliance

- ✅ **No Private Data** - Only public education information
- ✅ **Generic Attribution** - Source marked as "public_website"
- ✅ **No Credentials** - Zero API keys or passwords in data
- ✅ **Open Access** - Free for all Moroccan developers
- ✅ **Quality Validated** - 0.85/1.0 quality score

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Data sourced from public Moroccan education websites
- Built for the Moroccan developer community
- Open source and free forever

## 📞 Contact & Support

- **mail**: prs.online.00@gmail.com
- **Issues**: [Report a bug](https://github.com/K11E3R/moroccan-education-API/issues)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ for Moroccan developers | Free & Open | Production Ready**
