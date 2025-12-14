# 🚀 DEPLOYMENT FIXES - Make Your Live Demo Work

## 🔴 CURRENT ISSUES

### 1. Frontend (Vercel) - 401 Error
**URL:** https://frontend-7bu6ugdjh-asadullah-shafiques-projects.vercel.app
**Status:** ❌ Not accessible (401 Unauthorized)

**Likely causes:**
- Missing environment variables on Vercel
- Build failure
- Backend URL not configured

### 2. Backend - Not Deployed Yet
**Status:** ❌ No production backend URL
**Impact:** Frontend can't make API calls

---

## ✅ SOLUTION: Deploy Full Stack to Production

### STEP 1: Deploy Backend First (Railway - FREE)

Railway offers free tier perfect for this project.

#### 1.1: Sign Up for Railway
1. Go to: https://railway.app
2. Sign in with GitHub (use your account)
3. Authorize Railway

#### 1.2: Create New Project
```bash
# In your local backend folder
cd backend

# Make sure you have a Procfile
echo "web: uvicorn src.api.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Make sure you have runtime.txt
echo "python-3.11" > runtime.txt
```

#### 1.3: Deploy to Railway

**Option A: Using Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables
railway variables set GEMINI_API_KEY=AIzaSyDgQcQri6JQN_A-w56ONvec4w1h9S3a7Co
railway variables set QDRANT_URL=https://110c8859-6a7d-4a49-bb57-b23873fc2d41.us-east-1-1.aws.cloud.qdrant.io:6333
railway variables set QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.3EC__AzL82x8fhTmR1NmnXB1HG69IN_PeaIqyAD4YA0
railway variables set AI_PROVIDER=gemini
railway variables set ANTHROPIC_API_KEY=your_anthropic_key_here
railway variables set COHERE_API_KEY=VIQ6iZD9rDU7IqIiqyixXSwEcMr7WBJSrbyNqH90

# Deploy
railway up
```

**Option B: Using Railway Dashboard (EASIER)**
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select `asadullah48/physical-ai-textbook`
4. Set root directory: `backend`
5. Add environment variables (copy from your `.env`)
6. Click "Deploy"

**You'll get a URL like:** `https://physical-ai-textbook-production.up.railway.app`

#### 1.4: Test Backend Deployment

Once deployed, test:
```bash
curl https://your-railway-url.railway.app/api/health
```

Expected:
```json
{
  "status": "healthy",
  "rag_ready": true,
  "socratic_ready": true,
  "embodiment_ready": true
}
```

---

### STEP 2: Fix Frontend Deployment (Vercel)

#### 2.1: Update Environment Variables on Vercel

1. Go to: https://vercel.com/dashboard
2. Find your project: `physical-ai-textbook` or similar
3. Go to Settings → Environment Variables
4. Add:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app
   ```
5. Redeploy

#### 2.2: Alternative - Redeploy from GitHub

If above doesn't work:

1. Push latest code to GitHub:
```bash
cd C:\Users\Asad\.claude-worktrees\physical-ai-textbook\nostalgic-elbakyan

# Add all changes
git add .
git commit -m "feat: Add production RAG system with Gemini AI"
git push origin nostalgic-elbakyan
```

2. Go to Vercel dashboard
3. Import fresh from GitHub
4. Select `asadullah48/physical-ai-textbook`
5. Set framework: **Next.js**
6. Set root directory: `frontend`
7. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app
   ```
8. Deploy

---

### STEP 3: Verify Everything Works

#### Test Checklist:

**Backend (Railway):**
- [ ] `/api/health` returns healthy
- [ ] `/api/v1/modules` returns 5 modules
- [ ] `/api/v1/chat` (POST) returns AI response
- [ ] CORS allows your Vercel domain

**Frontend (Vercel):**
- [ ] Homepage loads
- [ ] Shows 5 modules
- [ ] Chat button appears
- [ ] Click chat → can type message
- [ ] Send message → gets AI response

---

## 🔧 ALTERNATIVE: Use Render (If Railway Issues)

### Backend on Render

1. Go to: https://render.com
2. Sign in with GitHub
3. New → Web Service
4. Connect `asadullah48/physical-ai-textbook`
5. Settings:
   - **Name:** physical-ai-backend
   - **Root Directory:** backend
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11
6. Add Environment Variables (same as above)
7. Create Web Service

**Free tier:** 750 hours/month (enough for hackathon!)

---

## 🆘 QUICK FIX: Use Current Local + Ngrok (DEMO HACK)

If deployments are taking too long and you need to demo NOW:

### Use Ngrok to Expose Local Backend

```bash
# Install ngrok
# Windows: Download from https://ngrok.com/download
# Mac: brew install ngrok

# Start your local backend
cd backend
python -m uvicorn src.api.main:app --reload --port 8000

# In new terminal, expose it
ngrok http 8000
```

**You'll get a URL like:** `https://abc123.ngrok.io`

**Update Vercel env:**
```
NEXT_PUBLIC_API_URL=https://abc123.ngrok.io
```

**Redeploy Vercel, now it works with your local backend!**

**⚠️ Note:** Ngrok URL changes each restart. Good for demo, not production.

---

## 📋 DEPLOYMENT CHECKLIST

### Before Deploying:

**Backend:**
- [ ] `Procfile` created
- [ ] `runtime.txt` created
- [ ] All environment variables documented
- [ ] Test locally one more time
- [ ] Push to GitHub

**Frontend:**
- [ ] Update `NEXT_PUBLIC_API_URL` to production backend
- [ ] Test build locally: `npm run build`
- [ ] Push to GitHub
- [ ] Verify Vercel auto-deploys

### After Deploying:

**Backend:**
- [ ] Health check works
- [ ] Chat endpoint works
- [ ] CORS configured for Vercel domain
- [ ] Check Railway/Render logs for errors

**Frontend:**
- [ ] Homepage loads
- [ ] Chat works end-to-end
- [ ] Voice mode functional
- [ ] No console errors (F12)

---

## 🎯 RECOMMENDED DEPLOYMENT STACK

**Best for Hackathon:**
- **Backend:** Railway (easiest, generous free tier)
- **Frontend:** Vercel (already set up)
- **Database:** Qdrant Cloud (already configured!)

**Total cost:** $0
**Setup time:** 15-20 minutes
**Reliability:** High

---

## 💡 UPDATED SUBMISSION LINKS

After deployment, update your SUBMISSION.md:

```markdown
**Live Demo:** https://physical-ai-textbook.vercel.app
**Backend API:** https://physical-ai-backend.up.railway.app
**API Docs:** https://physical-ai-backend.up.railway.app/docs
**GitHub Repository:** https://github.com/asadullah48/physical-ai-textbook
**Demo Video:** [Update with new video showing working features]
```

---

## 🚨 COMMON DEPLOYMENT ERRORS & FIXES

### Error: "Module not found" during build
**Fix:** Make sure `requirements.txt` has all dependencies
```bash
pip freeze > requirements.txt
```

### Error: "CORS policy" in browser
**Fix:** Update `main.py` line 30-32:
```python
allow_origins=[
    "https://physical-ai-textbook.vercel.app",
    "https://*.vercel.app",
    "http://localhost:3000"
]
```

### Error: "API timeout" on Vercel
**Fix:** Add to `vercel.json` in frontend:
```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend.railway.app/api/:path*"
    }
  ]
}
```

### Error: "Build failed" on Railway
**Fix:** Check logs, usually missing Python version or bad Procfile
```bash
# Procfile should be exactly:
web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

---

## ⚡ FASTEST PATH TO WORKING DEMO

1. **Deploy backend to Railway** (10 min)
   - Use dashboard, not CLI
   - Copy/paste environment variables
   - Wait for deploy

2. **Update Vercel env variable** (2 min)
   - Add `NEXT_PUBLIC_API_URL`
   - Trigger redeploy

3. **Test** (2 min)
   - Open Vercel URL
   - Try chat
   - Done!

**Total time: 15 minutes to production! 🚀**

---

Want me to help you deploy step-by-step right now?
