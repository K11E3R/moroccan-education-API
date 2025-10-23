# 🚀 GitHub & Railway Setup Guide

Complete guide to push your project to GitHub and deploy to Railway.

## 📋 Prerequisites

- ✅ Railway CLI installed (`npm install -g @railway/cli`)
- ✅ Railway account logged in (`railway login`)
- ✅ Git installed
- ✅ GitHub account

## 🔗 GitHub Repository

**Repository URL**: https://github.com/K11E3R/-moroccan-education-API

## 📤 Push to GitHub

### Step 1: Initialize Git (if not already done)

```bash
# Navigate to project directory
cd /mnt/c/Users/YassineNAANANI/Desktop/project_education/project_education/moroccan-education-data-collector

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Moroccan Education API"
```

### Step 2: Connect to GitHub

```bash
# Add remote repository
git remote add origin https://github.com/K11E3R/-moroccan-education-API.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

If you get an error about branch name, try:
```bash
git branch -M main
git push -u origin main
```

## 🚂 Railway Deployment

### Step 1: Link Railway Project

```bash
# In your project directory
railway link

# Select your project or create new one
```

### Step 2: Deploy

```bash
# Deploy from current directory
railway up

# Or deploy API specifically
cd api && railway up
```

### Step 3: Set Environment Variables (if needed)

```bash
# Set PORT (Railway sets this automatically)
railway variables set PORT=8000

# View all variables
railway variables
```

### Step 4: Get Your Public URL

```bash
# Get deployment URL
railway domain

# Or add custom domain
railway domain add your-domain.com
```

## 🔧 Railway Configuration

The project includes:
- ✅ `railway.json` - Railway build configuration
- ✅ `Procfile` - Start command
- ✅ `api/requirements.txt` - Python dependencies

Railway will automatically:
1. Detect Python project
2. Install dependencies from `api/requirements.txt`
3. Run the start command from `Procfile`
4. Expose your API on a public URL

## 📊 Verify Deployment

After deployment, test your API:

```bash
# Replace YOUR_URL with your Railway URL
export API_URL="https://your-app.railway.app"

# Test health
curl $API_URL/health

# Test endpoints
curl $API_URL/api/v1/levels
curl $API_URL/api/v1/subjects
curl "$API_URL/api/v1/search?q=math"
curl $API_URL/api/v1/stats
```

## 🔄 Update Deployment

When you make changes:

```bash
# Commit changes
git add .
git commit -m "Update: description of changes"

# Push to GitHub
git push origin main

# Redeploy to Railway
railway up

# Or let Railway auto-deploy from GitHub (recommended)
```

## 🔗 Connect Railway to GitHub (Auto-Deploy)

1. Go to Railway dashboard: https://railway.app/dashboard
2. Select your project
3. Click "Settings"
4. Under "Source", click "Connect GitHub"
5. Select repository: `K11E3R/-moroccan-education-API`
6. Select branch: `main`
7. Enable "Auto-deploy"

Now every push to GitHub will automatically deploy to Railway! 🎉

## 📝 Update README with Live URL

After deployment, update `README.md` with your live URL:

```bash
# Get your Railway URL
railway domain

# Example output: https://moroccan-education-api.railway.app
```

Then update all instances of `https://your-api.railway.app` in:
- `README.md`
- `API_SUMMARY.md`
- `QUICK_START.md`
- `api/README.md`

## 🎯 Quick Commands Reference

```bash
# Git commands
git status                    # Check status
git add .                     # Stage all changes
git commit -m "message"       # Commit changes
git push origin main          # Push to GitHub

# Railway commands
railway login                 # Login to Railway
railway link                  # Link project
railway up                    # Deploy
railway domain                # Get URL
railway logs                  # View logs
railway status                # Check status
railway variables             # View env variables
```

## 🐛 Troubleshooting

### Issue: "No linked project found"
```bash
# Solution: Link your project
railway link
# Then select or create project
```

### Issue: "Build failed"
```bash
# Check logs
railway logs

# Verify requirements.txt exists
ls api/requirements.txt

# Test locally first
cd api && uvicorn main:app --reload
```

### Issue: "Port already in use"
```bash
# Railway sets PORT automatically
# Make sure your app uses: --port $PORT
```

### Issue: "Data file not found"
```bash
# Verify data file exists
ls data/fast_collected_data_20251022_233523.json

# Check path in api/main.py
```

## ✅ Final Checklist

Before going live:

- [ ] Code pushed to GitHub
- [ ] Railway project linked
- [ ] API deployed successfully
- [ ] Public URL obtained
- [ ] All endpoints tested
- [ ] README updated with live URL
- [ ] Documentation updated
- [ ] GitHub repository description set
- [ ] Repository topics added (api, morocco, education, fastapi)

## 🎉 You're Live!

Once deployed, share your API:

```markdown
🇲🇦 Free Moroccan Education API is now live!

🔗 API: https://your-app.railway.app
📚 Docs: https://your-app.railway.app/docs
💻 GitHub: https://github.com/K11E3R/-moroccan-education-API

✅ No auth required
✅ CORS enabled
✅ Free forever

#MoroccanDev #OpenData #Education
```

---

**Need help?** Check Railway docs: https://docs.railway.app

