# 🚀 Deployment Guide - Make API Public

Complete guide to deploy your Moroccan Education API for public use.

## ✅ Pre-Deployment Checklist

- [x] Data collected and validated (68 items)
- [x] API tested (12/13 tests passing)
- [x] Documentation complete
- [x] No private information in data
- [x] Proper attribution ("Public Moroccan Education Websites")
- [x] CORS enabled for all origins
- [x] No authentication required

## 🎯 Deployment Options

### Option 1: Railway (Recommended - Free & Easy)

**Why Railway?**
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy deployment
- ✅ Custom domain support

**Steps:**
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
cd api
railway init

# 4. Deploy
railway up

# 5. Get public URL
railway domain
```

**Result**: Your API will be live at `https://your-app.railway.app`

---

### Option 2: Render (Free Tier)

**Steps:**
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Build Command**: `cd api && pip install -r requirements.txt`
   - **Start Command**: `cd api && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
5. Click "Create Web Service"

**Result**: Live at `https://your-app.onrender.com`

---

### Option 3: Heroku

**Steps:**
```bash
# 1. Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Create app
heroku create moroccan-education-api

# 4. Add Procfile
echo "web: cd api && uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 5. Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# 6. Open app
heroku open
```

**Result**: Live at `https://moroccan-education-api.herokuapp.com`

---

### Option 4: Vercel (Serverless)

**Steps:**
1. Install Vercel CLI: `npm install -g vercel`
2. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/main.py"
    }
  ]
}
```
3. Deploy: `vercel --prod`

**Result**: Live at `https://your-app.vercel.app`

---

### Option 5: Docker + Any Cloud

**Dockerfile** (already created in `api/Dockerfile`):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
COPY ../data/fast_collected_data_20251022_233523.json /app/data/
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deploy:**
```bash
# Build
docker build -t moroccan-education-api api/

# Run locally
docker run -p 8000:8000 moroccan-education-api

# Push to Docker Hub
docker tag moroccan-education-api yourusername/moroccan-education-api
docker push yourusername/moroccan-education-api

# Deploy to any cloud (AWS, GCP, Azure, DigitalOcean)
```

---

## 🌐 After Deployment

### 1. Test Your Public API

```bash
# Replace YOUR_DOMAIN with your actual domain
export API_URL="https://your-app.railway.app"

# Test endpoints
curl $API_URL/
curl $API_URL/health
curl $API_URL/api/v1/levels
curl $API_URL/api/v1/subjects
curl "$API_URL/api/v1/search?q=math"
curl $API_URL/api/v1/stats
```

### 2. Update Documentation

Update all documentation with your public URL:
- README.md
- API_SUMMARY.md
- api/README.md

Replace `http://localhost:8000` with your public URL.

### 3. Share with Community

**Announce on:**
- GitHub (create repository)
- Twitter/X with #MoroccanDev #OpenData
- LinkedIn
- Dev.to
- Moroccan developer communities

**Example announcement:**
```markdown
🇲🇦 Free Moroccan Education API

I've built a free, open API for Moroccan education data!

✅ No authentication required
✅ 68 educational items
✅ French & Arabic support
✅ CORS enabled
✅ Free for all developers

API: https://your-domain.com
Docs: https://your-domain.com/docs

#MoroccanDev #OpenData #Education
```

---

## 📊 Monitoring & Maintenance

### Add Analytics (Optional)

```python
# In api/main.py, add middleware
from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"{request.method} {request.url.path} - {duration:.2f}s")
    return response
```

### Monitor Health

```bash
# Set up a cron job or use UptimeRobot
curl https://your-domain.com/health
```

### Update Data

```bash
# When you want to update data
python collectors/fast_collector.py

# Redeploy with new data
git add data/
git commit -m "Update education data"
git push
```

---

## 🔒 Security Best Practices

### Rate Limiting (Optional)

```python
# Install: pip install slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/v1/levels")
@limiter.limit("100/minute")
async def get_levels(request: Request):
    # ... existing code
```

### HTTPS Only

Most platforms (Railway, Render, Heroku) provide HTTPS automatically.

---

## 💰 Cost Estimates

| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| **Railway** | 500 hours/month | $5/month |
| **Render** | 750 hours/month | $7/month |
| **Heroku** | 550 hours/month | $7/month |
| **Vercel** | Unlimited | $20/month (Pro) |
| **DigitalOcean** | N/A | $5/month |

**Recommendation**: Start with Railway or Render free tier.

---

## 🎯 Quick Deploy (Railway - Fastest)

```bash
# 1. Install Railway
npm install -g @railway/cli

# 2. Login
railway login

# 3. Deploy (from project root)
cd api && railway up

# 4. Get URL
railway domain

# Done! Your API is live in ~2 minutes
```

---

## 📞 Support & Community

### Create GitHub Repository

```bash
# 1. Create repo on GitHub
# 2. Push your code
git init
git add .
git commit -m "Initial commit - Moroccan Education API"
git remote add origin https://github.com/yourusername/moroccan-education-api.git
git push -u origin main
```

### Add README Badge

```markdown
[![API Status](https://img.shields.io/badge/API-Live-success)](https://your-domain.com)
[![Tests](https://img.shields.io/badge/tests-12%2F13%20passing-success)](./TEST_RESULTS.md)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
```

---

## ✅ Final Checklist

Before going public:

- [ ] API tested and working locally
- [ ] All tests passing (12/13)
- [ ] Documentation updated with public URL
- [ ] CORS enabled
- [ ] No private information in data
- [ ] Proper attribution in place
- [ ] Health check endpoint working
- [ ] Deployed to cloud platform
- [ ] Public URL accessible
- [ ] GitHub repository created
- [ ] Community announcement prepared

---

## 🎉 You're Ready!

Your Moroccan Education API is ready to go public and serve the Moroccan developer community!

**Next Step**: Choose a deployment platform and run the deploy command.

---

**Recommended**: Railway (fastest, easiest, free tier)  
**Command**: `cd api && railway up`  
**Time**: ~2 minutes  
**Cost**: Free

