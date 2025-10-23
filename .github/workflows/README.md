# GitHub Actions CI/CD Pipeline

This repository uses GitHub Actions to automatically test and validate the API before deployment to Railway.

## Pipeline Steps

### 1. **Test Job** (Runs on every push and PR)

✅ **Data Validation**
- Verifies `api/data.json` exists
- Validates JSON format
- Checks data quality (source, levels, subjects)
- Ensures source is "public_website" (generic)

✅ **API Testing**
- Starts API server locally
- Tests all endpoints:
  - `/health` - Health check
  - `/` - API info
  - `/api/v1/levels` - Get levels
  - `/api/v1/subjects` - Get subjects
  - `/api/v1/stats` - Get statistics
  - `/api/v1/search` - Search functionality
- Runs full API test suite

✅ **Privacy Check**
- Scans for email addresses
- Scans for phone numbers
- Verifies no private data

### 2. **Deploy Job** (Runs only on main branch)

🚂 **Railway Deployment**
- Triggered after all tests pass
- Railway auto-deploys from GitHub
- No manual intervention needed

## Workflow Triggers

- **Push to `main`**: Runs tests + deploys
- **Pull Request**: Runs tests only
- **Manual**: Can be triggered from Actions tab

## Status Badge

Add this to your README:

```markdown
![CI/CD](https://github.com/K11E3R/moroccan-education-API/actions/workflows/test-and-deploy.yml/badge.svg)
```

## Local Testing

Before pushing, you can run tests locally:

```bash
# Install dependencies
pip install -r requirements.txt
pip install pytest httpx

# Run API tests
cd api
python test_api.py

# Start API locally
python -m uvicorn main:app --reload
```

## What Gets Checked

| Check | Description | Failure Action |
|-------|-------------|----------------|
| Data file exists | `api/data.json` must exist | ❌ Build fails |
| Valid JSON | Data file must be valid JSON | ❌ Build fails |
| Data quality | Must have levels & subjects | ❌ Build fails |
| Source field | Must be "public_website" | ❌ Build fails |
| API endpoints | All endpoints must respond | ❌ Build fails |
| Privacy | No email/phone numbers | ❌ Build fails |
| API tests | Full test suite must pass | ❌ Build fails |

## Benefits

✅ **Quality Assurance** - Every change is tested
✅ **Privacy Protection** - Automatic privacy checks
✅ **Fast Feedback** - Know immediately if something breaks
✅ **Safe Deployments** - Only tested code reaches production
✅ **Documentation** - Test results visible in GitHub

## Viewing Results

1. Go to the **Actions** tab in GitHub
2. Click on the latest workflow run
3. View detailed logs for each step
4. Green checkmark = All tests passed ✅
5. Red X = Tests failed ❌

---

**Made with ❤️ for Moroccan Developers**

