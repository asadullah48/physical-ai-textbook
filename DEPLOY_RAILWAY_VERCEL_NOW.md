# 🚀 DEPLOY TO RAILWAY + VERCEL - 15 MINUTE GUIDE

## 🎯 What We're Doing

- **Backend → Railway** (Free tier, production-ready)
- **Frontend → Vercel** (Already set up, just needs fixing)
- **Database → Qdrant Cloud** (Already configured!)

**Total time: 15 minutes | Total cost: $0**

---

## 📋 PART 1: DEPLOY BACKEND TO RAILWAY (10 min)

### Step 1: Open Railway (1 min)

1. Open browser: https://railway.app
2. Click **"Login"**
3. Click **"Login with GitHub"**
4. Authorize Railway to access your GitHub

✅ **You're now on the Railway dashboard!**

---

### Step 2: Create New Project (2 min)

1. Click the big **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. You'll see a list of your repos
4. Find and click: **`asadullah48/physical-ai-textbook`**
5. Railway will ask: "Configure your service"

---

### Step 3: Configure the Service (1 min)

1. **Root Directory:** Type `backend` (important!)
2. Click **"Add variables"** (before deploying)

---

### Step 4: Add Environment Variables (5 min)

**IMPORTANT:** Click **"+ New Variable"** for EACH variable below:

#### Variable 1: Gemini API
```
Name: GEMINI_API_KEY
Value: AIzaSyDgQcQri6JQN_A-w56ONvec4w1h9S3a7Co
```
Click "Add" ✅

#### Variable 2: Qdrant URL
```
Name: QDRANT_URL
Value: https://110c8859-6a7d-4a49-bb57-b23873fc2d41.us-east-1-1.aws.cloud.qdrant.io:6333
```
Click "Add" ✅

#### Variable 3: Qdrant API Key
```
Name: QDRANT_API_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.3EC__AzL82x8fhTmR1NmnXB1HG69IN_PeaIqyAD4YA0
```
Click "Add" ✅

#### Variable 4: AI Provider
```
Name: AI_PROVIDER
Value: gemini
```
Click "Add" ✅

#### Variable 5: Anthropic (Backup)
```
Name: ANTHROPIC_API_KEY
Value: your_anthropic_key_here
```
Click "Add" ✅

#### Variable 6: Cohere
```
Name: COHERE_API_KEY
Value: VIQ6iZD9rDU7IqIiqyixXSwEcMr7WBJSrbyNqH90
```
Click "Add" ✅

---

### Step 5: Deploy! (1 min)

1. After adding all variables, click **"Deploy"**
2. You'll see build logs streaming
3. Wait 3-5 minutes (Railway is installing dependencies and building)

**What you'll see:**
```
Building...
Installing dependencies from requirements.txt...
✓ Build completed
Deploying...
✓ Deployment successful
```

---

### Step 6: Get Your Backend URL (30 sec)

1. Once deployed, click **"Settings"** tab
2. Scroll down to **"Domains"** section
3. You'll see a URL like:
   ```
   physical-ai-textbook-production-xxxx.up.railway.app
   ```
4. **COPY THIS ENTIRE URL** (including https://)
5. Save it in Notepad - you need it for Vercel!

---

### Step 7: Test Your Backend (30 sec)

Open in browser (replace with YOUR URL):
```
https://YOUR-RAILWAY-URL.up.railway.app/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "rag_ready": true,
  "socratic_ready": true,
  "embodiment_ready": true
}
```

✅ **If you see this = Backend is LIVE! 🎉**

---

## 📋 PART 2: FIX FRONTEND ON VERCEL (5 min)

### Step 1: Open Vercel Dashboard (1 min)

1. Go to: https://vercel.com/dashboard
2. You should see your project listed
3. Click on: **`physical-ai-textbook`** or whatever it's named

---

### Step 2: Add Environment Variable (2 min)

1. Click the **"Settings"** tab
2. In the left sidebar, click **"Environment Variables"**
3. You'll see a form to add new variables

**Add this variable:**

**Name:**
```
NEXT_PUBLIC_API_URL
```

**Value:** (paste your Railway URL from Part 1, Step 6)
```
https://YOUR-RAILWAY-URL.up.railway.app
```

**Important:**
- Make sure it starts with `https://`
- NO trailing slash at the end
- Example: `https://physical-ai-backend-production.up.railway.app`

4. **Environments:** Check all boxes:
   - ✅ Production
   - ✅ Preview
   - ✅ Development

5. Click **"Save"**

---

### Step 3: Redeploy Frontend (2 min)

**Option A: Automatic (if you push to GitHub)**
```bash
# In your local project
git add .
git commit -m "Configure production backend URL"
git push origin main
# Vercel auto-deploys!
```

**Option B: Manual Redeploy (faster)**
1. Click **"Deployments"** tab
2. Find the latest deployment
3. Click the **"..."** menu (three dots)
4. Click **"Redeploy"**
5. Confirm **"Redeploy"**
6. Wait 1-2 minutes

---

### Step 4: Get Your Frontend URL (30 sec)

1. Once deployed, click **"Visit"** button (top right)
2. Or copy the URL shown in the deployment
3. Example: `https://physical-ai-textbook.vercel.app`

---

### Step 5: Test Everything! (1 min)

1. **Open your Vercel URL**
2. **Check homepage loads** ✅
3. **See 5 modules displayed** ✅
4. **Click chat button** (💬 bottom right) ✅
5. **Type a question:** "What is Physical AI?"
6. **Get AI response!** ✅

**If all 6 steps work = YOU'RE LIVE! 🚀🎉**

---

## 🧪 FULL TESTING CHECKLIST

### Backend Tests (Railway)

```bash
# Replace YOUR-URL with your actual Railway URL

# Test 1: Health check
curl https://YOUR-URL.railway.app/api/health

# Test 2: List modules
curl https://YOUR-URL.railway.app/api/v1/modules

# Test 3: Chat (Helpful mode)
curl -X POST https://YOUR-URL.railway.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?", "mode": "helpful"}'

# Test 4: Chat (Socratic mode)
curl -X POST https://YOUR-URL.railway.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is inverse kinematics?", "mode": "socratic"}'

# Test 5: Chat (Embodiment mode)
curl -X POST https://YOUR-URL.railway.app/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about sensors", "mode": "embodiment"}'
```

### Frontend Tests (Vercel)

1. ✅ Homepage loads without errors
2. ✅ All 5 modules are visible
3. ✅ Chat button appears (bottom right)
4. ✅ Click chat → Modal opens
5. ✅ Type message → Can send
6. ✅ Response appears (not "Error")
7. ✅ Voice button works (optional)
8. ✅ No red errors in browser console (F12)

---

## 🐛 TROUBLESHOOTING

### Backend Deploy Failed on Railway

**Check Build Logs:**
1. Railway dashboard → Your project
2. Click "Deployments" tab
3. Click failed deployment
4. Read error message

**Common Issues:**

**Error: "Module not found"**
- Solution: Check `requirements.txt` has all packages
- Push updated `requirements.txt` to GitHub
- Redeploy

**Error: "Port binding failed"**
- Solution: Check `Procfile` exists in backend folder
- Content should be: `web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

**Error: "GEMINI_API_KEY not found"**
- Solution: Double-check you added ALL 6 environment variables
- Settings → Variables → Verify each one

---

### Frontend Not Working on Vercel

**Issue: Chat returns errors**

**Check in browser console (F12):**

**Error: "Network request failed"**
- Solution: Check `NEXT_PUBLIC_API_URL` is set correctly
- Must include `https://`
- Must NOT have trailing `/`

**Error: "CORS policy"**
- Solution: Update backend CORS settings
- Edit `backend/src/api/main.py` line 27-32
- Add your Vercel domain to `allow_origins`
- Example:
  ```python
  allow_origins=[
      "https://physical-ai-textbook.vercel.app",
      "https://*.vercel.app",
      "http://localhost:3000"
  ]
  ```
- Push to GitHub, Railway auto-redeploys

**Issue: "401 Unauthorized" when opening frontend**

- Solution: Project might be set to private
- Vercel Dashboard → Settings → General
- Make sure "Private" is OFF

---

### Quick Fix: Force Redeploy Everything

**Backend (Railway):**
1. Settings → Redeploy → Confirm

**Frontend (Vercel):**
1. Deployments → Latest → "..." → Redeploy

---

## 📝 UPDATE YOUR SUBMISSION.MD

After successful deployment:

```markdown
## Live Demo

- **Live Demo:** https://YOUR-VERCEL-URL.vercel.app
- **Backend API:** https://YOUR-RAILWAY-URL.railway.app
- **API Documentation:** https://YOUR-RAILWAY-URL.railway.app/docs
- **API Health Check:** https://YOUR-RAILWAY-URL.railway.app/api/health
- **GitHub Repository:** https://github.com/asadullah48/physical-ai-textbook

## Try It Now!

### Test the AI Chatbot:
1. Visit the live demo link above
2. Click the chat button (💬) at bottom right
3. Ask: "What is Physical AI?"
4. Get AI-powered responses with textbook citations!

### Test Different AI Modes:

**Helpful Mode (Default):**
- Straightforward answers with sources
- Educational explanations

**Socratic Mode:**
- AI asks YOU questions first
- Guides your thinking
- Promotes active learning

**Embodiment Mode (RAIA):**
- AI takes on robot persona
- Shares "experiences" learning Physical AI
- Unique narrative approach

### Backend API Access:
- Health: `GET /api/health`
- Modules: `GET /api/v1/modules`
- Chat: `POST /api/v1/chat`
- Full API docs: https://YOUR-RAILWAY-URL.railway.app/docs

## Technologies Used

**Production Stack:**
- Frontend: Next.js 14 (Vercel)
- Backend: FastAPI (Railway)
- AI: Google Gemini (Free tier)
- Vector DB: Qdrant Cloud
- Features: RAG, Socratic tutoring, Robot embodiment
```

---

## ✅ SUCCESS INDICATORS

You know deployment worked when:

✅ Railway URL shows: `{"status": "healthy"}`
✅ Vercel site loads homepage
✅ Chat button is visible
✅ Can send message
✅ Get intelligent AI response (not error)
✅ Response includes sources from textbook
✅ No console errors (F12)

---

## 🎉 CONGRATULATIONS!

**Once both tests pass, you have:**

✅ Production backend on Railway
✅ Production frontend on Vercel
✅ Real RAG system running
✅ 3 AI modes functional
✅ Cloud vector database
✅ HTTPS secure connections
✅ Auto-scaling enabled
✅ $0 hosting costs

**You're LIVE and ready to demo! 🚀**

---

## 📞 NEXT STEPS

1. **Record new demo video** showing:
   - Working chat with real AI
   - Different AI modes (Helpful/Socratic/Embodiment)
   - Source citations
   - Live deployment

2. **Update SUBMISSION.md** with new URLs

3. **Share with judges!**

---

**START NOW:**
1. Open https://railway.app
2. Login with GitHub
3. Follow Part 1 above
4. Takes 15 minutes total

**Need help? Tell me which step you're on and I'll guide you through it!**
