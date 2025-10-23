# Initialize Private Git Repository for Development (PowerShell)
# This script sets up the private repo for data collection development

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🔒 Initializing PRIVATE Development Repository" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Initialize Git
Write-Host "Step 1: Initializing Git..." -ForegroundColor Cyan
git init
Write-Host "Done: Git initialized" -ForegroundColor Green
Write-Host ""

# Step 2: Create .gitignore
Write-Host "Step 2: Creating .gitignore..." -ForegroundColor Cyan
@"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Data files (large files)
data/raw/*.json
data/raw/*.csv
data/cleaned/*.json
data/cleaned/*.csv
*.json.bak
*.csv.bak

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Secrets
.env
.env.local
secrets.json
config/private.json

# Temporary files
tmp/
temp/
*.tmp

# Old/deprecated files
collectors/fast_collector.py
collectors/generic_collector.py
run_fast_test.py
test_single_branch.py
"@ | Out-File -FilePath .gitignore -Encoding UTF8

Write-Host "Done: .gitignore created" -ForegroundColor Green
Write-Host ""

# Step 3: Create data directories
Write-Host "Step 3: Creating data directories..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path data/raw | Out-Null
New-Item -ItemType Directory -Force -Path data/cleaned | Out-Null
New-Item -ItemType Directory -Force -Path data/final | Out-Null
Write-Host "Done: Data directories created" -ForegroundColor Green
Write-Host ""

# Step 4: Add all files
Write-Host "Step 4: Adding files to Git..." -ForegroundColor Cyan
git add .
Write-Host "Done: Files added" -ForegroundColor Green
Write-Host ""

# Step 5: First commit
Write-Host "Step 5: Creating first commit..." -ForegroundColor Cyan
git commit -m @"
Initial commit: Smart collector with validation and deduplication

Features:
- Smart level detection from URLs and breadcrumbs
- Content type detection (cours, exercice, exam, etc.)
- Automatic deduplication
- Data validation and quality scoring
- Hierarchical data organization
- Complete collection pipeline

Target: Quality score >= 0.95 before public release
"@

Write-Host "Done: First commit created" -ForegroundColor Green
Write-Host ""

# Step 6: Instructions for remote
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create PRIVATE repository on GitHub:" -ForegroundColor White
Write-Host "   - Go to: https://github.com/new" -ForegroundColor Gray
Write-Host "   - Name: moroccan-education-data-collector" -ForegroundColor Gray
Write-Host "   - Description: Private development repo for data collection" -ForegroundColor Gray
Write-Host "   - Visibility: Private (IMPORTANT!)" -ForegroundColor Yellow
Write-Host "   - Click 'Create repository'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Add remote and push:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/moroccan-education-data-collector.git" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Verify it's private:" -ForegroundColor White
Write-Host "   - Go to repository settings" -ForegroundColor Gray
Write-Host "   - Check: Repository visibility = Private" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Repository initialized! Ready for development." -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan

