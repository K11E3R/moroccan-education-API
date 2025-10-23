#!/bin/bash

# Initialize Private Git Repository for Development
# This script sets up the private repo for data collection development

echo "============================================================================"
echo "🔒 Initializing PRIVATE Development Repository"
echo "============================================================================"
echo ""

# Step 1: Initialize Git
echo "📝 Step 1: Initializing Git..."
git init
echo "✅ Git initialized"
echo ""

# Step 2: Create .gitignore
echo "📝 Step 2: Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
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
EOF

echo "✅ .gitignore created"
echo ""

# Step 3: Create data directories
echo "📝 Step 3: Creating data directories..."
mkdir -p data/raw
mkdir -p data/cleaned
mkdir -p data/final
echo "✅ Data directories created"
echo ""

# Step 4: Add all files
echo "📝 Step 4: Adding files to Git..."
git add .
echo "✅ Files added"
echo ""

# Step 5: First commit
echo "📝 Step 5: Creating first commit..."
git commit -m "Initial commit: Smart collector with validation and deduplication

Features:
- Smart level detection from URLs and breadcrumbs
- Content type detection (cours, exercice, exam, etc.)
- Automatic deduplication
- Data validation and quality scoring
- Hierarchical data organization
- Complete collection pipeline

Target: Quality score >= 0.95 before public release"

echo "✅ First commit created"
echo ""

# Step 6: Instructions for remote
echo "============================================================================"
echo "📋 NEXT STEPS"
echo "============================================================================"
echo ""
echo "1. Create PRIVATE repository on GitHub:"
echo "   - Go to: https://github.com/new"
echo "   - Name: moroccan-education-data-collector"
echo "   - Description: Private development repo for data collection"
echo "   - Visibility: ✅ Private"
echo "   - Click 'Create repository'"
echo ""
echo "2. Add remote and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/moroccan-education-data-collector.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Verify it's private:"
echo "   - Go to repository settings"
echo "   - Check: Repository visibility = Private ✅"
echo ""
echo "============================================================================"
echo "🔒 Repository initialized! Ready for development."
echo "============================================================================"

