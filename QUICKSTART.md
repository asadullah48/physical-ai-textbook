# ⚡ Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI API Key

### Step 1: Backend Setup (2 minutes)

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Edit .env and add your API key:
# OPENAI_API_KEY=sk-your-actual-key-here

# Initialize RAG system (this indexes all content)
python initialize_content.py

# Start backend server
python -m uvicorn src.api.main_new:app --reload --port 8000
```

**You should see:**
```
✅ All chunks indexed successfully!
INFO:     Uvicorn running on http://localhost:8000
```

### Step 2: Frontend Setup (2 minutes)

Open a NEW terminal:

```bash
cd frontend

# Install Node dependencies
npm install

# Set API URL
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start dev server
npm run dev
```

**You should see:**
```
✓ Ready in 2.3s
○ Local: http://localhost:3000
```

### Step 3: Update Code (1 minute)

**File: `frontend/src/app/page.tsx`**

Line 3, change:
```typescript
import { api } from '@/services/api';  // ❌ OLD
```
to:
```typescript
import { api } from '@/services/api-new';  // ✅ NEW
```

**File: `frontend/src/components/VoiceChatbot.tsx`**

Add at top (line 2):
```typescript
import { api } from '@/services/api-new';
```

Replace lines 82-87:
```typescript
// OLD CODE - DELETE THIS:
const res = await fetch('http://localhost:8000/api/v1/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: messageText }),
});
const data = await res.json();

// NEW CODE - USE THIS:
const data = await api.chat({
  message: messageText,
  conversation_history: messages,
  mode: 'helpful'
});
```

### Step 4: Test It! (30 seconds)

1. Open http://localhost:3000
2. Click the chat button (bottom right)
3. Ask: "What is Physical AI?"
4. You should get a REAL AI response with sources!

---

## 🧪 Verify It's Working

### Test 1: Chat Mode
```
You: "What is LIDAR?"
AI: [Should give detailed answer with citations from textbook]
```

### Test 2: Socratic Mode
Update VoiceChatbot line with mode:
```typescript
mode: 'socratic'  // Instead of 'helpful'
```

```
You: "What is LIDAR?"
AI: "Before I explain, what do you think the 'L' in LIDAR stands for?"
```

### Test 3: Embodiment Mode
```typescript
mode: 'embodiment'
```

```
You: "Tell me about sensors"
AI (as RAIA): "I'm trying to understand my LIDAR sensor... the laser pulses feel so fast! Do humans process visual information this quickly?"
```

### Test 4: Backend Health
```bash
curl http://localhost:8000/api/health
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

## ❌ Troubleshooting

### "OPENAI_API_KEY not found"
- Edit `backend/.env`
- Add: `OPENAI_API_KEY=sk-your-key`
- Restart backend

### "Module not found" errors (Python)
```bash
cd backend
pip install -r requirements.txt --upgrade
```

### "Cannot find module" (TypeScript)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Chat not working
1. Check backend is running: `curl http://localhost:8000/api/health`
2. Check frontend env: `cat frontend/.env.local`
3. Check browser console for errors

### No responses from AI
1. Verify content is indexed:
   ```bash
   cd backend
   python initialize_content.py
   ```
2. Check OpenAI API key is valid
3. Check backend logs for errors

---

## 🎯 What You Have Now

✅ **Real RAG System**
- Content indexed in Qdrant
- OpenAI embeddings
- Semantic search

✅ **3 AI Modes**
- Helpful (direct answers)
- Socratic (guided learning)
- Embodiment (robot persona)

✅ **Production Backend**
- FastAPI with async
- Error handling
- CORS configured

✅ **Working Frontend**
- Next.js 14
- Real API calls
- Voice mode

---

## 🚀 Next: Make It Beautiful

See `IMPLEMENTATION_GUIDE.md` for:
- Building sidebar navigation
- Adding AI companion panel
- Creating visual learning graph
- Implementing theme toggle
- Deployment to Vercel

**You're 80% done. The hard part (AI) is working!**
