# 🚀 DEPLOYMENT OPTIONS - Choose Your Path

You have **3 excellent options** to deploy. Choose based on your preference:

| Option | Best For | Time | Difficulty | Cost |
|--------|----------|------|------------|------|
| **Docker** | Full control, professional | 15 min | Medium | Free |
| **Railway** | Easiest, fastest | 10 min | Easy | Free |
| **Hugging Face** | AI community showcase | 20 min | Medium | Free |

---

## 🐳 OPTION 1: DOCKER DEPLOYMENT (RECOMMENDED)

### Why Docker?
- ✅ Professional deployment
- ✅ Works locally and in cloud
- ✅ Easy to replicate
- ✅ Can deploy to any cloud provider

### STEP 1: Test Locally with Docker

```bash
# Make sure Docker Desktop is running
# Check: docker --version

# Navigate to project root
cd C:\Users\Asad\.claude-worktrees\physical-ai-textbook\nostalgic-elbakyan

# Build and run with docker-compose
docker-compose up --build
```

**Expected output:**
```
backend_1   | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend_1  | Ready in 2.1s
```

**Test it:**
- Backend: http://localhost:8000/api/health
- Frontend: http://localhost:3000

**If it works locally, it'll work in production!**

### STEP 2: Deploy Docker to Railway

Railway supports Docker deployments automatically!

1. **Push your code to GitHub:**
```bash
git add .
git commit -m "Add Docker configuration"
git push origin main
```

2. **Go to Railway:**
   - Visit: https://railway.app
   - Login with GitHub
   - New Project → Deploy from GitHub
   - Select: `asadullah48/physical-ai-textbook`

3. **Railway auto-detects Dockerfile!**
   - It will find `backend/Dockerfile`
   - Set root directory: `backend`
   - Add environment variables (same as before)
   - Deploy!

4. **Get your URL:**
   - Copy the Railway-provided URL
   - Example: `https://physical-ai-backend-production.up.railway.app`

### STEP 3: Deploy Frontend to Vercel

```bash
# Update frontend environment
# Go to Vercel dashboard
# Settings → Environment Variables
# Add: NEXT_PUBLIC_API_URL = https://YOUR-RAILWAY-URL.railway.app
# Redeploy
```

**Done! Docker + Railway + Vercel = Professional stack 🎉**

---

## 🚂 OPTION 2: RAILWAY (NO DOCKER - EASIEST)

### STEP-BY-STEP Walkthrough

#### 1. Go to Railway
- Open: https://railway.app
- Click "Login"
- Select "Login with GitHub"
- Authorize Railway

#### 2. Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Find and click: `asadullah48/physical-ai-textbook`

#### 3. Configure Service
- Railway will ask: "Which directory?"
- Select: `backend`
- Click "Add variables"

#### 4. Add Environment Variables

Click "+ Variable" for EACH of these:

**Variable 1:**
```
Name: GEMINI_API_KEY
Value: AIzaSyDgQcQri6JQN_A-w56ONvec4w1h9S3a7Co
```

**Variable 2:**
```
Name: QDRANT_URL
Value: https://110c8859-6a7d-4a49-bb57-b23873fc2d41.us-east-1-1.aws.cloud.qdrant.io:6333
```

**Variable 3:**
```
Name: QDRANT_API_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.3EC__AzL82x8fhTmR1NmnXB1HG69IN_PeaIqyAD4YA0
```

**Variable 4:**
```
Name: AI_PROVIDER
Value: gemini
```

**Variable 5:**
```
Name: ANTHROPIC_API_KEY
Value: your_anthropic_key_here
```

**Variable 6:**
```
Name: COHERE_API_KEY
Value: VIQ6iZD9rDU7IqIiqyixXSwEcMr7WBJSrbyNqH90
```

#### 5. Deploy
- Click "Deploy"
- Wait 3-5 minutes
- Watch the build logs (they'll appear on screen)

#### 6. Get Your URL
- Once deployed, click "Settings"
- Under "Domains", you'll see a URL like:
  `physical-ai-textbook-production.up.railway.app`
- **COPY THIS URL!**

#### 7. Test Backend
Open in browser:
```
https://YOUR-URL.railway.app/api/health
```

Should see:
```json
{
  "status": "healthy",
  "rag_ready": true,
  "socratic_ready": true,
  "embodiment_ready": true
}
```

#### 8. Update Vercel
- Go to: https://vercel.com/dashboard
- Click your project
- Settings → Environment Variables
- Add new variable:
  - Name: `NEXT_PUBLIC_API_URL`
  - Value: `https://YOUR-URL.railway.app`
- Save
- Deployments → Redeploy

**Test frontend:** Your Vercel URL should now work!

---

## 🤗 OPTION 3: HUGGING FACE SPACES

### Why Hugging Face?
- ✅ AI/ML community platform
- ✅ Free GPU available
- ✅ Great for showcasing AI projects
- ✅ Easy sharing in AI community

### STEP 1: Create Hugging Face Space

1. **Sign up/Login:**
   - Go to: https://huggingface.co
   - Create account or login

2. **Create New Space:**
   - Click your profile → "Spaces"
   - Click "Create new Space"
   - Name: `physical-ai-textbook`
   - License: MIT
   - SDK: **Gradio** or **Docker**
   - Click "Create Space"

3. **Choose Deployment Method:**

#### Method A: Using Gradio (Easier)

Create `app.py` in your backend:

```python
import gradio as gr
from src.rag.rag_engine import RAGEngine
import os

# Initialize
rag = RAGEngine(
    openai_api_key=os.getenv("GEMINI_API_KEY"),
    qdrant_url=os.getenv("QDRANT_URL")
)

async def chat_interface(message, mode):
    chunks = await rag.retrieve(message)
    result = await rag.generate_answer(message, chunks, mode=mode)
    return result['answer']

# Create Gradio interface
demo = gr.Interface(
    fn=chat_interface,
    inputs=[
        gr.Textbox(label="Your Question"),
        gr.Radio(["helpful", "socratic", "embodiment"], label="AI Mode")
    ],
    outputs=gr.Textbox(label="AI Response"),
    title="Physical AI Textbook - Interactive AI Tutor",
    description="Ask questions about Physical AI, Robotics, and ROS 2!"
)

if __name__ == "__main__":
    demo.launch()
```

#### Method B: Using Docker

Upload your `Dockerfile` to the Space repository.

4. **Add Secrets:**
   - In your Space, go to Settings
   - Add secrets:
     - `GEMINI_API_KEY`
     - `QDRANT_URL`
     - `QDRANT_API_KEY`
     - etc.

5. **Deploy:**
   - Push code to Space
   - HuggingFace builds automatically
   - You get a URL like: `https://huggingface.co/spaces/YOUR-USERNAME/physical-ai-textbook`

---

## 📊 DEPLOYMENT COMPARISON

### Docker (Local → Railway)
**Pros:**
- Professional approach
- Works anywhere
- Easy to debug locally first
- Industry standard

**Cons:**
- Need to learn basic Docker
- Slightly more setup

**Verdict:** ⭐⭐⭐⭐⭐ Best for hackathon judges

### Railway (Direct)
**Pros:**
- Fastest deployment
- No Docker knowledge needed
- Great free tier
- Auto HTTPS

**Cons:**
- Less control
- Tied to Railway platform

**Verdict:** ⭐⭐⭐⭐⭐ Best for speed

### Hugging Face Spaces
**Pros:**
- AI community exposure
- Free GPU option
- Great for portfolio
- Built for ML apps

**Cons:**
- More complex setup
- Gradio UI different from yours
- Slower cold starts

**Verdict:** ⭐⭐⭐⭐ Best for AI showcase

---

## 🎯 MY RECOMMENDATION

**For your hackathon submission:**

### Use Railway (Option 2) - HERE'S WHY:

1. **Speed:** Deploy in 10 minutes
2. **Reliability:** Railway has excellent uptime
3. **Free tier:** Generous for demos
4. **HTTPS:** Automatic secure connection
5. **Logs:** Easy debugging
6. **Scale:** Can handle judge traffic

### Deployment Order:

1. **Backend → Railway** (10 min)
   - Follow Option 2 step-by-step above
   - Get backend URL

2. **Frontend → Vercel** (5 min)
   - Already deployed
   - Just add environment variable
   - Redeploy

3. **Test** (2 min)
   - Open Vercel URL
   - Test chat
   - Done!

**Total time: 17 minutes to production! 🚀**

---

## 🐳 BONUS: Docker Commands Reference

If you choose Docker option:

```bash
# Build backend image
cd backend
docker build -t physical-ai-backend .

# Run backend container
docker run -p 8000:8000 --env-file .env physical-ai-backend

# Or use docker-compose (easier)
cd ..
docker-compose up --build

# Stop containers
docker-compose down

# View logs
docker-compose logs -f backend

# Rebuild after code changes
docker-compose up --build --force-recreate
```

---

## ✅ FINAL CHECKLIST

Before you start deployment:

- [ ] Docker Desktop is running (if using Docker)
- [ ] You have your API keys ready (in `.env`)
- [ ] GitHub repo is up to date
- [ ] You know which option you're choosing

After deployment:

- [ ] Backend health check works
- [ ] Frontend loads
- [ ] Chat sends messages
- [ ] AI responds with real answers
- [ ] Sources are cited
- [ ] No console errors

---

## 🚀 LET'S START!

**Which option do you want to try?**

**Option A:** "Let's use Railway - fastest!" → Follow Option 2 above
**Option B:** "I want to learn Docker first!" → Test locally with docker-compose
**Option C:** "Show me on Hugging Face!" → Create Gradio interface

**I recommend starting with Railway (Option 2) - it's the fastest path to a working demo!**

**Ready? Go to https://railway.app and let's deploy! Tell me when you're on the Railway dashboard and I'll guide you through each click! 🚂**
