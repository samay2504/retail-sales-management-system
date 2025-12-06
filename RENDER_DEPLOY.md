# 🚀 Render Backend Deployment Configuration

## ✅ PostgreSQL Database - Already Created!

Your production database is live and seeded with 1000 records:

```
Database Name: truestate_prod
Host: dpg-d4q30nqli9vc739mg5ng-a.virginia-postgres.render.com
Username: truestate_prod_user
Password: 0vjEVitjfpiAxi3VE9ppR5XcFojPRph1
Records: 1000 transactions ✅
```

**Internal URL (for Render services):**
```
postgresql://truestate_prod_user:0vjEVitjfpiAxi3VE9ppR5XcFojPRph1@dpg-d4q30nqli9vc739mg5ng-a/truestate_prod
```

**External URL (for local testing):**
```
postgresql://truestate_prod_user:0vjEVitjfpiAxi3VE9ppR5XcFojPRph1@dpg-d4q30nqli9vc739mg5ng-a.virginia-postgres.render.com/truestate_prod
```

---

## 🌐 Step 1: Create Web Service on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"**
4. Search for: `samay2504/retail-sales-management-system`
5. Click **"Connect"**

---

## ⚙️ Step 2: Configure Web Service

### **Basic Settings:**

| Field | Value |
|-------|-------|
| **Name** | `truestate-backend` |
| **Region** | `Virginia (US East)` |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn src.index:app --host 0.0.0.0 --port $PORT` |

### **Instance Type:**
- Select: **Free** (or Starter if you need guaranteed uptime)

---

## 🔐 Step 3: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** for each:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://truestate_prod_user:0vjEVitjfpiAxi3VE9ppR5XcFojPRph1@dpg-d4q30nqli9vc739mg5ng-a/truestate_prod` |
| `APP_ENV` | `production` |
| `DEBUG` | `false` |
| `CORS_ORIGINS` | `https://samay2504.github.io` |
| `LOG_LEVEL` | `WARNING` |
| `API_HOST` | `0.0.0.0` |
| `API_PORT` | `$PORT` |

**Important:** Use the **Internal Database URL** (without `.virginia-postgres.render.com`) since both services are on Render.

---

## 🚀 Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Once live, you'll get a URL like: `https://truestate-backend.onrender.com`

### Check Deployment Status:
- **Logs tab** → Watch for "Uvicorn running on..." message
- **Events tab** → Verify "Live" status

---

## ✅ Step 5: Test Your Backend

### Health Check:
```
https://truestate-backend.onrender.com/health
```
Expected response: `{"status": "healthy"}`

### Get Transactions:
```
https://truestate-backend.onrender.com/api/transactions?page=1&limit=10
```
Expected: JSON with 10 transactions

---

## 🎨 Step 6: Update Frontend

Once backend is deployed, update the frontend API URL:

### File: `frontend/src/services/api.ts`

Change line ~5:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://truestate-backend.onrender.com';
```

### Redeploy Frontend:
```powershell
cd frontend
npm run build
git add .
git commit -m "Connect to Render backend"
git push origin main
```

GitHub Actions will auto-deploy in ~2 minutes.

---

## 🧪 Final Testing

Visit: **https://samay2504.github.io/retail-sales-management-system**

Test all features:
- ✅ Search customers
- ✅ Navigate pages (no snap-back!)
- ✅ Apply filters
- ✅ Sort columns
- ✅ Responsive design

---

## 🎉 Production Architecture

```
┌─────────────────────────────────────────┐
│  GitHub Pages (Frontend)                │
│  https://samay2504.github.io           │
│  React + Vite + TanStack Query         │
└──────────────┬──────────────────────────┘
               │ HTTPS
               ▼
┌─────────────────────────────────────────┐
│  Render Web Service (Backend)           │
│  https://truestate-backend.onrender.com│
│  FastAPI + Uvicorn                      │
└──────────────┬──────────────────────────┘
               │ Internal Network
               ▼
┌─────────────────────────────────────────┐
│  Render PostgreSQL 18                   │
│  dpg-d4q30nqli9vc739mg5ng-a            │
│  1000 transactions seeded ✅            │
└─────────────────────────────────────────┘
```

---

## 🆘 Troubleshooting

### Backend shows "Application Failed"
**Check Logs:**
- Go to Web Service → **Logs** tab
- Look for Python errors or missing dependencies

**Common Issues:**
- Wrong `DATABASE_URL` format (use internal URL)
- Missing environment variables
- Python version mismatch

### CORS Errors in Browser Console
**Fix:**
- Verify `CORS_ORIGINS=https://samay2504.github.io` in Render env vars
- Check frontend is actually deployed to GitHub Pages
- Open browser DevTools → Network tab to see exact error

### Database Connection Timeout
**Verify:**
- PostgreSQL service is running (Render Dashboard)
- `DATABASE_URL` uses **internal** hostname (no `.virginia-postgres.render.com`)
- Check database status in Render PostgreSQL dashboard

### Frontend Shows No Data
**Debug Steps:**
1. Open browser DevTools → Network tab
2. Check API calls go to Render URL (not localhost)
3. Verify backend health: `https://your-backend.onrender.com/health`
4. Check CORS headers in response

---

## 📊 Monitor Your App

### Render Dashboard:
- **Metrics** → CPU, Memory, Response time
- **Logs** → Real-time application logs
- **Events** → Deployment history

### PostgreSQL Dashboard:
- **Metrics** → Connections, Queries, Storage
- **Connections** → Current active connections
- **Backups** → Automatic daily backups (Pro plan)

---

## 💰 Free Tier Limits

**Render Free Plan:**
- ✅ 750 hours/month (enough for 1 service always-on)
- ✅ Spins down after 15 min inactivity
- ✅ 512 MB RAM
- ⚠️ First request after spin-down takes ~30s

**PostgreSQL Free Plan:**
- ✅ 90 days free, then $7/month
- ✅ 256 MB RAM, 1 GB storage
- ✅ 97 concurrent connections

---

## 🎯 Next Steps (Optional)

### Add Custom Domain:
1. Go to Web Service → **Settings** → **Custom Domain**
2. Add your domain (e.g., `api.yourdomain.com`)
3. Update DNS records as shown

### Enable Auto-Deploy:
- Already enabled by default
- Push to `main` branch → Auto-deploys

### Set Up Monitoring:
- Add Datadog integration (optional)
- Set up Uptime monitoring
- Configure email alerts

---

## ✨ You're Production Ready!

Your full-stack app is now deployed with:
- ✅ **Backend:** FastAPI on Render
- ✅ **Frontend:** React on GitHub Pages  
- ✅ **Database:** PostgreSQL 18 with 1000 records
- ✅ **Features:** Pagination, search, filters, sorting
- ✅ **Performance:** Indexed queries, optimized React Query
- ✅ **Production:** CORS configured, environment variables set

**Live URLs:**
- Frontend: https://samay2504.github.io/retail-sales-management-system
- Backend: https://truestate-backend.onrender.com (after you deploy)
- Database: dpg-d4q30nqli9vc739mg5ng-a (Render-managed)
