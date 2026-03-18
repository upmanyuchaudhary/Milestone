# Milestone — Autonomous Portfolio Manager

Three-layer autonomous portfolio manager for retail investors in India.

---

## Sprint 0 — Infrastructure Setup

Complete these steps in order before writing any application code.

### Step 1 — GitHub
```bash
git init
git add .
git commit -m "Sprint 0: initial scaffold"
gh repo create milestone --private
git remote add origin https://github.com/YOUR_USERNAME/milestone.git
git push -u origin main
```

### Step 2 — Supabase
1. Go to supabase.com → New project
2. Note your DATABASE_URL from Settings → Database → Connection string (URI)
3. It will look like: `postgresql://postgres:Milestone_Atul@1234@db.ramnoumsvxvydjsloqjr.supabase.co:5432/postgres`(actual URL)

### Step 3 — Railway (Backend)
1. Go to railway.app → New project → Deploy from GitHub repo
2. Select your `milestone` repo
3. Add environment variables (Settings → Variables):
   ```
   KITE_API_KEY=your_key
   KITE_API_SECRET=your_secret
   DATABASE_URL=your_supabase_url
   ENVIRONMENT=production
   ```
4. Railway will auto-deploy on every push to main

### Step 4 — Vercel (Frontend)
1. Go to vercel.com → New project → Import from GitHub
2. Set root directory to `frontend/`
3. Add environment variable:
   ```
   VITE_API_BASE_URL=https://your-app.railway.app
   ```
4. Vercel will auto-deploy on every push to main

### Step 5 — Run Database Migrations
```bash
# From project root, with DATABASE_URL set in .env
cd backend
pip install -r requirements.txt
alembic upgrade head
```

### Step 6 — Verify End to End
```bash
# Check backend is live
curl https://your-app.railway.app/health
# Expected: {"status":"ok","service":"milestone-api"}

# Check frontend is live
# Open https://your-app.vercel.app in browser
```

### Step 7 — First Login (Kite token)
```bash
# Get login URL
curl https://your-app.railway.app/auth/login-url

# Open the URL in browser → login → you'll be redirected to a URL like:
# https://your-app.railway.app/auth/callback?request_token=xxxxx

# Exchange for access token
curl -X POST "https://your-app.railway.app/auth/callback?request_token=YOUR_TOKEN"
```

---

## Daily Operation

**Every trading day before 3:45 PM:**
1. Open `https://your-app.railway.app/auth/login-url`
2. Login to Kite
3. Token is stored — jobs run automatically

**Scheduled jobs:**
- 3:45 PM — Layer 1 sync (data + scores)
- 4:15 PM — Layer 2 decisions (recommendations)
- 9:00 AM — Outcome computation

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite → Vercel |
| Backend | Python + FastAPI → Railway |
| Database | PostgreSQL → Supabase |
| Scheduling | APScheduler (inside FastAPI) |
| Data | Zerodha Kite Connect API |

---

## Sprint Plan

| Sprint | Focus | Status |
|--------|-------|--------|
| 0 | Infrastructure | ← You are here |
| 1 | Layer 1 — Data + Scoring | Pending |
| 2 | Layer 2 — Decision Engine | Pending |
| 3 | Backend API | Pending |
| 4 | Frontend Screens | Pending |
| 5 | Signal Impact | Pending |
| 6 | Hardening | Pending |
