# 🚀 DEPLOY TO PRODUCTION NOW

## Current Status
- ❌ Frontend: 401 Error (not configured properly)
- ❌ Backend: Not deployed yet
- ✅ GitHub: Code is ready

## Fix Plan (15 Minutes Total)

---

## STEP 1: Deploy Backend to Railway (10 min)

### Option A: Railway Dashboard (EASIEST - RECOMMENDED)

1. **Go to Railway:**
   - Visit: https://railway.app
   - Click "Login" → Sign in with GitHub
   - Authorize Railway to access your repos

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose: `asadullah48/physical-ai-textbook`
   - Click "Add variables" before deploying

3. **Add Environment Variables:**

   Click "+ New Variable" and add these **ONE BY ONE**:

   ```
   GEMINI_API_KEY=AIzaSyDgQcQri6JQN_A-w56ONvec4w1h9S3a7Co
   ```

   ```
   QDRANT_URL=https://110c8859-6a7d-4a49-bb57-b23873fc2d41.us-east-1-1.aws.cloud.qdrant.io:6333
   ```

   ```
   QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.3EC__AzL82x8fhTmR1NmnXB1HG69IN_PeaIqyAD4YA0
   ```

   ```
   AI_PROVIDER=gemini
   ```

   ```
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

   ```
   COHERE_API_KEY=VIQ6iZD9rDU7IqIiqyixXSwEcMr7WBJSrbyNqH90
   ```

4. **Configure Build:**
   - Root Directory: `backend`
   - Build Command: (leave empty, Railway auto-detects)
   - Start Command: (leave empty, uses Procfile)

5. **Deploy:**
   - Click "Deploy"
   - Wait 3-5 minutes
   - You'll get a URL like: `https://physical-ai-textbook-production.up.railway.app`

6. **Get Your Backend URL:**
   - Click "Settings"
   - Under "Domains", copy the Railway-provided URL
   - **SAVE THIS URL** - you need it for frontend!

7. **Test Backend:**
   ```bash
   curl https://YOUR-RAILWAY-URL.railway.app/api/health
   ```

   Should return:
   ```json
   {
     "status": "healthy",
     "rag_ready": true,
     "socratic_ready": true,
     "embodiment_ready": true
   }
   ```

---

## STEP 2: Fix Frontend on Vercel (5 min)

### Go to Vercel Dashboard

1. Visit: https://vercel.com/dashboard
2. Find your project (or import from GitHub if needed)

### Add Environment Variable

1. Click on your project
2. Go to "Settings" tab
3. Click "Environment Variables" in left sidebar
4. Add new variable:
   - **Name:** `NEXT_PUBLIC_API_URL`
   - **Value:** `https://YOUR-RAILWAY-URL.railway.app` (from Step 1)
   - **Environment:** Production, Preview, Development (check all)
5. Click "Save"

### Redeploy

1. Go to "Deployments" tab
2. Click "..." on latest deployment
3. Click "Redeploy"
4. **OR** just push to GitHub and it auto-deploys

---

## STEP 3: Test Everything (2 min)

### Test Backend Endpoints

```bash
# Health check
curl https://YOUR-RAILWAY-URL.railway.app/api/health

# List modules
curl https://YOUR-RAILWAY-URL.railway.app/api/v1/modules

# Test chat
curl -X POST https://YOUR-RAILWAY-URL.railway.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?", "mode": "helpful"}'
```

### Test Frontend

1. Open your Vercel URL: `https://physical-ai-textbook.vercel.app`
2. Should see homepage with 5 modules
3. Click chat button (bottom right 💬)
4. Type: "What is Physical AI?"
5. Should get AI response!

---

## 🎉 SUCCESS CHECKLIST

After deployment, verify:

- [ ] Backend URL accessible
- [ ] `/api/health` returns healthy
- [ ] Frontend loads without errors
- [ ] Homepage shows 5 modules
- [ ] Chat button visible
- [ ] Can send message and get AI response
- [ ] Voice mode works (optional)

---

## 🔧 TROUBLESHOOTING

### Backend Deploy Failed

**Check Railway Logs:**
1. Go to Railway dashboard
2. Click on your service
3. Click "Logs" tab
4. Look for errors

**Common issues:**
- Missing `Procfile` → I created it for you
- Missing `runtime.txt` → I created it for you
- Missing dependencies → Check `requirements.txt`

**Fix:** Push the new files to GitHub:
```bash
cd backend
git add Procfile runtime.txt
git commit -m "Add deployment files"
git push
```

Then redeploy in Railway dashboard.

### Frontend Still 401

**Check Environment Variables:**
1. Vercel Dashboard → Your Project → Settings → Environment Variables
2. Make sure `NEXT_PUBLIC_API_URL` is set
3. Value should start with `https://` (not `http://`)

**Force Rebuild:**
1. Deployments tab
2. Click "..." → "Redeploy"
3. Wait for build to complete

### Chat Not Working

**Check CORS:**

If backend deploys but chat fails, update `backend/src/api/main.py`:

```python
# Line 27-32, update to:
allow_origins=[
    "https://physical-ai-textbook.vercel.app",
    "https://frontend-7bu6ugdjh-asadullah-shafiques-projects.vercel.app",
    "https://*.vercel.app",  # Allow all Vercel deployments
    "http://localhost:3000"
]
```

Push to GitHub, redeploy Railway.

---

## 📝 UPDATE SUBMISSION.MD

After successful deployment, update your submission:

```markdown
## Live Demo

- **Live Demo:** https://physical-ai-textbook.vercel.app
- **Backend API:** https://YOUR-RAILWAY-URL.railway.app
- **API Documentation:** https://YOUR-RAILWAY-URL.railway.app/docs
- **GitHub Repository:** https://github.com/asadullah48/physical-ai-textbook
- **Demo Video:** [To be updated with new recording]

## Test the Features

### Try the AI Chatbot:
1. Visit the live demo
2. Click the chat button (💬 bottom right)
3. Ask: "What is Physical AI?"
4. Get intelligent responses with sources!

### Test Different AI Modes:
- Helpful Mode: Direct answers
- Socratic Mode: AI asks YOU questions
- Embodiment Mode: RAIA robot persona

### API Endpoints:
- Health: `GET /api/health`
- Modules: `GET /api/v1/modules`
- Chat: `POST /api/v1/chat`
```

---

## ⚡ ALTERNATIVE: Quick Demo with Ngrok

If Railway is taking too long, use this hack for immediate demo:

```bash
# Terminal 1: Start local backend
cd backend
python -m uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Expose with ngrok
ngrok http 8000
# Copy the https:// URL it gives you

# Go to Vercel dashboard
# Settings → Environment Variables
# Set NEXT_PUBLIC_API_URL to your ngrok URL
# Redeploy

# Now your Vercel frontend talks to your local backend!
```

**⚠️ Note:** Ngrok URL changes every restart. Good for demo, not permanent.

---

## 🎯 DEPLOYMENT SUMMARY

| Service | Platform | Cost | Time | Status |
|---------|----------|------|------|--------|
| Backend | Railway | FREE | 10 min | ⏳ Pending |
| Frontend | Vercel | FREE | 5 min | ⏳ Needs fix |
| Database | Qdrant Cloud | FREE | ✅ Done | ✅ Ready |

**Total: $0, ~15 minutes, Production-ready!**

---

Ready to deploy? Start with Railway backend deployment now!

Let me know when you have your Railway backend URL and I'll help you test it!
