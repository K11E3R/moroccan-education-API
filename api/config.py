"""Configuration for the Moroccan Education API v1.0"""

import os
from pathlib import Path
from typing import List


class Settings:
    APP_NAME: str = "Moroccan Education API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Comprehensive public API for Moroccan education data"

    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    WORKERS: int = int(os.getenv("WORKERS", "1"))

    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "*").split(",")

    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_PER_DAY: int = int(os.getenv("RATE_LIMIT_PER_DAY", "10000"))

    API_BASE_PATH: str = "/api/v1"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))

    BASE_DIR: Path = Path(__file__).parent
    DATA_FILE: Path = BASE_DIR / "data.json"
    DATA_FALLBACK_PATHS: list = [
        BASE_DIR / "data.json",
        BASE_DIR.parent / "data" / "moroccan_education_data.json",
        BASE_DIR.parent / "data.json",
    ]

    CONTACT_EMAIL: str = "prs.online.00@gmail.com"
    GITHUB_URL: str = "https://github.com/K11E3R/moroccan-education-API"

    DATA_SOURCES: list = [
        {
            "name": "men.gov.ma",
            "url": "https://www.men.gov.ma",
            "description": "Ministry of National Education",
            "type": "official",
        },
        {
            "name": "AlloSchool",
            "url": "https://www.alloschool.com",
            "description": "Moroccan educational platform with courses, exercises and exams",
            "type": "educational_platform",
        },
        {
            "name": "9rayti",
            "url": "https://9rayti.com",
            "description": "Moroccan education resources and orientation portal",
            "type": "educational_platform",
        },
        {
            "name": "Dyrassa",
            "url": "https://www.dyrassa.com",
            "description": "Educational content platform for Moroccan students",
            "type": "educational_platform",
        },
        {
            "name": "TaalimPress",
            "url": "https://taalimpress.info",
            "description": "Moroccan education news and resources",
            "type": "news",
        },
        {
            "name": "Telmidtice",
            "url": "https://telmidtice.men.gov.ma",
            "description": "Official e-learning platform by the Ministry",
            "type": "official",
        },
    ]

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")


settings = Settings()
