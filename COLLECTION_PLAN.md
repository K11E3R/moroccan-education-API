# 🎯 Moroccan Education Data - Complete Collection Plan

## 🚨 Current Problems

### Data Quality Issues:
- ❌ **48 subjects but 40+ are duplicates** (same subject repeated)
- ❌ **All levels show "unknown"** - no proper level detection
- ❌ **Not sorted or organized** - chaotic data structure
- ❌ **Missing 90% of content** - no exercises, exams, corrections
- ❌ **Poor collection strategy** - surface scraping only

### What We're Missing:
- 📚 **Courses** (Cours) - Lessons and theory
- 📝 **Exercises** (Exercices) - Practice problems
- 📋 **Controls** (Contrôles) - Tests and quizzes
- 📄 **Exams** (Examens) - Final exams
- ✅ **Corrections** (Corrections) - Solutions and answers
- 🎥 **Videos** - Educational videos
- 📊 **Summaries** (Résumés) - Quick reviews

## 🎯 NEW COLLECTION STRATEGY

### Phase 1: Proper Structure Analysis
**Goal**: Understand AlloSchool's complete structure

```
AlloSchool Structure:
├── Levels (Niveaux)
│   ├── Primaire (6 years: 1-6)
│   ├── Collège (3 years: 1-3)
│   ├── Lycée (3 years: Tronc Commun, 1ère Bac, 2ème Bac)
│   ├── Baccalauréat (Multiple branches)
│   └── Supérieur (CPGE, University)
│
├── Subjects per Level (Matières)
│   ├── Math, Physics, Chemistry, SVT
│   ├── French, Arabic, English
│   ├── History, Geography, Philosophy
│   └── Islamic Education, Informatics
│
└── Content per Subject
    ├── 📚 Cours (Lessons)
    ├── 📝 Exercices (Exercises)
    ├── 📋 Contrôles (Tests)
    ├── 📄 Examens (Exams)
    ├── ✅ Corrections (Solutions)
    ├── 🎥 Vidéos (Videos)
    └── 📊 Résumés (Summaries)
```

### Phase 2: Smart Collection Algorithm

**Step 1: Discover All Levels**
```python
# Extract from sitemap and navigation
- Get all level URLs
- Parse level names (FR + AR)
- Identify level hierarchy
- Map level IDs properly
```

**Step 2: Discover All Subjects per Level**
```python
# For each level, get all subjects
- Navigate to level page
- Extract subject list
- Get subject metadata (color, icon, name)
- Link subject to correct level
```

**Step 3: Collect All Content per Subject**
```python
# For each subject, collect:
- Cours (lessons)
- Exercices (with solutions)
- Contrôles (tests)
- Examens (past exams)
- Corrections (answer keys)
- Vidéos (educational videos)
- Résumés (summaries)
```

### Phase 3: Data Organization

**Hierarchical Structure**:
```json
{
  "levels": [
    {
      "id": "primaire-1",
      "name": "1ère Année Primaire",
      "name_ar": "السنة الأولى ابتدائي",
      "order": 1,
      "subjects": ["math", "french", "arabic", "sciences"]
    }
  ],
  "subjects": [
    {
      "id": "math-primaire-1",
      "name": "Mathématiques",
      "level_id": "primaire-1",
      "content_types": ["cours", "exercices", "controles"]
    }
  ],
  "content": [
    {
      "id": "cours-math-p1-001",
      "subject_id": "math-primaire-1",
      "type": "cours",
      "title": "Les nombres de 0 à 100",
      "title_ar": "الأعداد من 0 إلى 100"
    }
  ]
}
```

### Phase 4: Data Cleaning & Deduplication

**Cleaning Rules**:
1. Remove exact duplicates (same ID)
2. Merge similar entries (same name + level)
3. Standardize naming conventions
4. Validate all relationships (level → subject → content)
5. Sort by: level order → subject name → content type

## 🛠️ Implementation Plan

### New Collector Features:

1. **Level Detection**
   - Parse URL patterns: `/course/math-1ere-annee-primaire`
   - Extract level from breadcrumbs
   - Match against known level patterns
   - Fallback to manual mapping

2. **Content Type Detection**
   - Identify: Cours, Exercices, Contrôles, Examens, Corrections
   - Parse section headers
   - Extract metadata (difficulty, duration, points)

3. **Relationship Mapping**
   - Link subjects to correct levels
   - Link content to correct subjects
   - Maintain referential integrity

4. **Deduplication**
   - Hash-based duplicate detection
   - Merge similar entries
   - Keep most complete version

5. **Data Validation**
   - Verify all required fields
   - Check data consistency
   - Validate relationships
   - Quality score per item

## 📊  Results

### State:
```
✅ ~15 unique levels (properly identified)
✅ ~100 unique subjects (deduplicated, sorted)
✅ ~5,000+ courses
✅ ~10,000+ exercises
✅ ~2,000+ exams
✅ ~1,000+ corrections
✅ ~500+ videos
```

## 🚀 Action Items

### Immediate (Week 1):
1. ✅ Analyze AlloSchool complete structure
2. ✅ Map all levels and subjects
3. ✅ Design new data schema
4. ✅ Build smart level detector
5. ✅ Implement deduplication logic

### Short-term (Week 2-3):
1. ✅ Collect all courses
2. ✅ Collect all exercises
3. ✅ Collect all exams
4. ✅ Clean and organize data
5. ✅ Validate data quality

### Medium-term (Week 4):
1. ✅ Deploy cleaned API
2. ✅ Add search and filters
3. ✅ Add statistics
4. ✅ Documentation
5. ✅ Community testing

## 🎯 Success Criteria

- ✅ **Zero duplicates** in final dataset
- ✅ **100% level detection** accuracy
- ✅ **All content types** collected
- ✅ **Properly sorted** and organized
- ✅ **High quality** data (score > 0.95)
- ✅ **Complete coverage** of Moroccan education system

## 🤝 Community Involvement

We need help with:
- 🔍 **Data Validation** - Verify accuracy
- 🧹 **Data Cleaning** - Manual review
- 📝 **Content Review** - Check completeness
- 🌍 **Translation** - Improve FR/AR quality
- 🐛 **Bug Reports** - Find issues

---

**Let's build the BEST Moroccan education data API! 🇲🇦**

