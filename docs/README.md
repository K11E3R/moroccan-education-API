# 📚 Documentation

Complete documentation for the Moroccan Education Data Collector.

## 🎯 Overview

This system collects structured educational data from public Moroccan education websites using ethical web scraping practices.

## 🏗️ Architecture

### Components

1. **Fast Collector** (`collectors/fast_collector.py`)
   - Async/await for high concurrency
   - 50 concurrent requests
   - 12,000 URLs/sec parsing speed
   - Connection pooling

2. **Generic Collector** (`collectors/generic_collector.py`)
   - Respectful crawling mode
   - 3 concurrent requests
   - 2 second delays
   - Production-ready

3. **Website Analyzer** (`analysis/website_analyzer.py`)
   - Discovers sitemaps
   - Analyzes structure
   - Maps URL patterns
   - Identifies content types

4. **Configuration** (`config/moroccan_education_config.json`)
   - URL patterns
   - Content selectors
   - Extraction rules
   - Quality checks

## 📊 Data Structure

### Levels
```json
    {
      "id": "primaire",
  "slug": "primaire",
      "name": "Primaire",
      "name_ar": "الابتدائي",
  "description": "Primary education",
  "description_ar": "التعليم الابتدائي المغربي",
      "subjects_count": 8,
      "courses_count": 1200,
  "url": "https://...",
  "source": "public_website",
  "collected_at": "2025-10-22T23:27:16Z"
}
```

### Subjects
```json
    {
      "id": "primaire-math",
  "slug": "primaire-math",
      "name": "Mathématiques",
      "name_ar": "الرياضيات",
  "description": "Cours de mathématiques",
  "description_ar": "دروس الرياضيات",
      "level_id": "primaire",
  "level_name": "Primaire",
  "level_name_ar": "الابتدائي",
  "color": "#3b82f6",
  "icon": "Calculator",
      "courses_count": 150,
  "url": "https://...",
  "source": "public_website",
  "collected_at": "2025-10-22T23:27:22Z"
}
```

### Courses
```json
    {
      "id": "math-primaire-1",
  "slug": "addition",
      "title": "L'addition",
      "title_ar": "الجمع",
  "description": "Apprendre l'addition",
  "description_ar": "تعلم الجمع",
      "content_type": "course",
      "subject_id": "primaire-math",
  "subject_name": "Mathématiques",
  "subject_name_ar": "الرياضيات",
      "level_id": "primaire",
  "level_name": "Primaire",
  "level_name_ar": "الابتدائي",
  "url": "https://...",
  "language": "fr",
  "confidence": 0.8,
  "source": "public_website",
  "collected_at": "2025-10-22T23:27:22Z"
}
```

## 🔧 Configuration

### Collection Settings
```json
{
  "collection_config": {
    "base_url": "https://www.alloschool.com",
    "source_name": "public_website",
    "country": "morocco",
    "respect_robots": true,
    "delay_between_requests": 2.0,
    "max_concurrent_requests": 3,
    "timeout": 30
  }
}
```

### URL Patterns
```json
{
  "url_patterns": {
    "levels": ["/category/primaire", "/category/college", "/category/lycee"],
    "subjects": ["/category/mathematiques", "/category/francais"],
    "courses": ["/cours/", "/lesson/", "/lecon/"],
    "exercises": ["/exercice/", "/exercise/"],
    "controls": ["/controle/", "/control/"],
    "exams": ["/examen/", "/exam/"],
    "corrections": ["/correction/", "/solution/"]
  }
}
```

### Content Selectors
```json
{
  "content_selectors": {
    "title": "h1, .title, .page-title",
    "description": ".description, .content, .summary",
    "level": ".level, .niveau, .grade",
    "subject": ".subject, .matiere, .discipline"
  }
}
```

## 🚀 Usage

### Basic Collection
```python
from collectors.fast_collector import FastEducationalCollector, FastCollectionConfig

config = FastCollectionConfig(
    base_url="https://www.alloschool.com",
    source_name="public_website",
    country="morocco"
)

collector = FastEducationalCollector(config)
data = await collector.collect_all_data()
collector.save_data()
```

### Custom Collection
```python
# Filter specific URLs
categorized_urls = collector._categorize_urls(all_urls)
level_urls = categorized_urls['levels'][:10]  # First 10 only

# Collect specific category
await collector._collect_batch_async(level_urls, 'level', collector._extract_level_data)
```

## 📈 Performance

### Speed Comparison
| Mode | Concurrent | Delay | URLs/sec | Items/sec |
|------|-----------|-------|----------|-----------|
| Fast | 50 | 0.05s | 12,000 | 6-7 |
| Balanced | 20 | 0.2s | 5,000 | 3-4 |
| Respectful | 3 | 2.0s | 1,000 | 0.5-1 |

### Optimization Tips
1. Increase `max_concurrent_requests` (50-100)
2. Decrease `delay_between_requests` (0.01-0.1s)
3. Use connection pooling (already implemented)
4. Filter URLs early
5. Process in batches

## 🔒 Ethical Guidelines

### Respectful Crawling
- ✅ Check robots.txt
- ✅ Implement delays (2s default)
- ✅ Use proper User-Agent
- ✅ Limit concurrent requests (3 default)
- ✅ Only collect metadata

### Legal Compliance
- ✅ Public data only
- ✅ No authentication bypass
- ✅ Proper attribution
- ✅ Educational purpose
- ✅ No content copying

## 🐛 Troubleshooting

### Common Issues

**No Data Collected**
- Check internet connection
- Verify sitemap accessibility
- Check URL patterns
- Review extraction rules

**Low Quality Score**
- Review content selectors
- Check URL categorization
- Validate extraction logic
- Improve pattern matching

**Rate Limiting**
- Increase delays
- Reduce concurrency
- Check robots.txt
- Respect crawl-delay

**Memory Issues**
- Process in smaller batches
- Clear visited_urls periodically
- Save data incrementally
- Use generators

## 📊 Quality Metrics

### Data Quality
- **Completeness**: All required fields present
- **Accuracy**: Validated against source
- **Consistency**: Standardized format
- **Freshness**: Timestamp included
- **Attribution**: Source tracked

### Collection Metrics
- **Success Rate**: % of successful requests
- **Quality Score**: Overall data quality (0-1)
- **Coverage**: % of available content
- **Speed**: Items collected per second
- **Efficiency**: Success/total ratio

## 🔄 Integration

### API Format
```json
{
  "success": true,
  "data": {
    "levels": [...],
    "subjects": [...],
    "courses": [...]
  },
  "meta": {
    "source": "public_website",
    "country": "morocco",
    "collection_date": "2025-10-22T23:27:22Z",
    "total_items": 68,
    "quality_score": 0.85
  }
}
```

### Export Formats
- **JSON**: Complete structured data
- **CSV**: Individual category files
- **Excel**: Multi-sheet workbook
- **SQL**: Database import scripts

## 📝 Development

### Adding New Content Type
1. Add URL pattern to config
2. Create extraction function
3. Add to categorization logic
4. Update data structure
5. Add validation rules

### Custom Extractor
```python
def _extract_custom_data(self, soup, url, data_type):
    """Extract custom content type"""
    try:
        title = soup.find('h1').get_text(strip=True)
        # Custom extraction logic
        return {
            'id': slugify(title),
            'title': title,
            # ... more fields
        }
    except:
        return None
```

## 🧪 Testing

### Run Tests
```bash
# Single branch test
python run_fast_test.py primaire

# Full test suite
python tests/test_collection.py

# Website analysis
python analysis/website_analyzer.py
```

### Validation
```python
# Check data quality
assert data['metadata']['quality_score'] > 0.8
assert data['metadata']['total_items'] > 0

# Check required fields
for level in data['levels']:
    assert 'id' in level
    assert 'name' in level
    assert 'name_ar' in level
```

---

**Last Updated**: 2025-10-22 23:33
**Version**: 1.0
**Status**: ✅ Operational

