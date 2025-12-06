# 🚀 PostgreSQL Production Deployment Guide

## ✅ What You Just Configured

The backend is now **production-ready** with PostgreSQL support!

### Files Updated:
- ✅ `requirements.txt` - Added `asyncpg>=0.29.0` (PostgreSQL driver)
- ✅ `src/config.py` - Updated CORS origins to include GitHub Pages
- ✅ `src/models/base.py` - Auto-converts `postgresql://` to `postgresql+asyncpg://`
- ✅ `scripts/migrate_to_postgres.py` - Migration script created

---

## 📋 Render Form Configuration

### **1. Create PostgreSQL Database on Render**

Fill out the form with these values:

```yaml
Name: truestate-retail-db
Database: truestate_prod
User: [Leave empty - auto-generated]
Region: Virginia (US East)
PostgreSQL Version: 18
Datadog API Key: [Leave empty]
```

### **2. After Database Created**

Render will show you connection details. **Copy the Internal Database URL** (looks like):
```
postgresql://truestate_prod_user:LONG_PASSWORD_HERE@dpg-xxxxx-a.virginia-postgres.render.com/truestate_prod
```

---

## 🌐 Deploy Backend to Render

### **Step 1: Create Web Service**

1. Go to Render Dashboard → **New +** → **Web Service**
2. Connect your GitHub repo: `samay2504/retail-sales-management-system`
3. Configure:

```yaml
Name: truestate-backend
Region: Virginia (US East)
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn src.index:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

### **Step 2: Add Environment Variables**

In **Environment** tab, add these:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | *(Paste Internal Database URL from Render PostgreSQL)* |
| `APP_ENV` | `production` |
| `DEBUG` | `false` |
| `CORS_ORIGINS` | `https://samay2504.github.io` |
| `LOG_LEVEL` | `WARNING` |

### **Step 3: Deploy**

Click **Create Web Service** → Wait for deployment (3-5 minutes)

---

## 🗄️ Seed Production Database

After backend is deployed, seed the database:

### **Option 1: Run from Render Shell**

1. Go to your web service → **Shell** tab
2. Run:
```bash
python scripts/migrate_to_postgres.py
```

### **Option 2: Run Locally (Connect to Render DB)**

```powershell
# Set Render's DATABASE_URL
$env:DATABASE_URL = "postgresql://USER:PASS@HOST:5432/truestate_prod"

# Run migration
python backend/scripts/migrate_to_postgres.py
```

When prompted:
- **Drop existing tables?** → Type `yes`
- **How many records?** → Type `1000` (or more)

---

## 🔗 Update Frontend API URL

After backend is deployed, you'll get a URL like:
```
https://truestate-backend.onrender.com
```

### Update Frontend:

**File: `frontend/src/services/api.ts`**

Change:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

To:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://truestate-backend.onrender.com';
```

### Redeploy Frontend:

```powershell
cd frontend
npm run build
git add .
git commit -m "Update API URL to Render backend"
git push origin main
```

GitHub Actions will auto-deploy to GitHub Pages in ~2 minutes.

---

## ✅ Verification Checklist

After everything is deployed:

- [ ] PostgreSQL database created on Render
- [ ] Backend web service deployed with DATABASE_URL set
- [ ] Database seeded with sample data
- [ ] Frontend updated with backend URL
- [ ] Frontend redeployed to GitHub Pages
- [ ] Test live site: https://samay2504.github.io/retail-sales-management-system

---

## 🧪 Test Your Production App

Visit: **https://samay2504.github.io/retail-sales-management-system**

Try:
1. ✅ Search for customer names
2. ✅ Navigate to page 2, 3, 4 (no snap-back!)
3. ✅ Apply filters (region, category, payment method)
4. ✅ Sort by different columns
5. ✅ Check responsive design (no horizontal scroll)

---

## 🎉 You're Done!

Your full-stack retail sales management system is now live with:
- ✅ PostgreSQL production database
- ✅ FastAPI backend on Render
- ✅ React frontend on GitHub Pages
- ✅ Pagination bug fixed
- ✅ Production-ready architecture

---

## 🆘 Troubleshooting

### Backend 500 Error
```powershell
# Check Render logs
Go to Web Service → Logs tab
```

### CORS Error in Browser
```
Add your backend URL to frontend API config
Check CORS_ORIGINS env var on Render
```

### Database Connection Failed
```
Verify DATABASE_URL in Render environment variables
Check PostgreSQL database is running (Render dashboard)
```

### Frontend Shows No Data
```
Check Network tab → API calls should go to Render URL
Verify backend health: https://your-backend.onrender.com/health
```

---

## 📞 Need Help?

Check deployment status:
- **Backend:** https://dashboard.render.com
- **Frontend:** https://github.com/samay2504/retail-sales-management-system/actions
- **Database:** Render Dashboard → PostgreSQL service
