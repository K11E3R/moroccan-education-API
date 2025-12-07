# 🇲🇦 Moroccan Education Data Collector & API

A comprehensive data collection and API system for Moroccan education data, providing clean, validated educational content for developers and educators.


## 🚀 Features

- **Data Collection**: Automated scraping from Moroccan education websites
- **Data Validation**: Comprehensive validation and quality monitoring
- **Data Cleaning**: Removal of broken links and unnecessary content
- **REST API**: Complete v1 API with all endpoints
- **Quality Assurance**: 100% validated data with quality reports

## 📊 Data Statistics

- **Education Levels**: 12 levels (Primary, College, High School)
- **Subjects**: 96 subjects across all levels
- **Content Items**: 89 verified educational content items
- **Languages**: French and Arabic support
- **Quality Score**: 100% validated and cleaned

## 🔧 API Endpoints

### Core Endpoints
- `GET /api/v1/levels` - Get all education levels
- `GET /api/v1/subjects` - Get all subjects
- `GET /api/v1/courses` - Get all educational content
- `GET /api/v1/search` - Search across all data
- `GET /api/v1/stats` - Get API statistics

### Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 🛠️ Installation & Setup

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

## 📧 Contact

- **Email**: prs.online.00@gmail.com
- **GitHub**: [K11E3R/moroccan-education-API](https://github.com/K11E3R/moroccan-education-API)

## 🎯 Status

**PRODUCTION READY** ✅

The Moroccan Education API v1 is ready for public use with:
- Complete v1 endpoints
- 100% validated data
- Sub-second response times
- Comprehensive error handling
- Real-time monitoring
- Complete documentation

---


Made with ❤️ for the Moroccan Developer Community 🇲🇦
