# 🧪 STEP-BY-STEP IMPLEMENTATION & TESTING

## 📋 Prerequisites Checklist

Before starting, verify you have:

- [ ] Python 3.10 or higher (`python --version`)
- [ ] Node.js 18 or higher (`node --version`)
- [ ] Git installed
- [ ] Text editor (VS Code recommended)
- [ ] OpenAI API account

---

## 🔑 STEP 1: GET OPENAI API KEY

### Option A: If You Have an OpenAI Account

1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it: "physical-ai-textbook"
4. Copy the key (starts with `sk-`)
5. **IMPORTANT**: Save it somewhere safe (you can't see it again!)

### Option B: If You Don't Have an Account

1. Go to: https://platform.openai.com/signup
2. Sign up with email
3. Verify your email
4. Go to: https://platform.openai.com/api-keys
5. Create key as above

### Option C: Free Trial Credits

OpenAI gives $5 free credits to new accounts. This is enough for:
- ~500 chat messages
- ~1000 content indexing operations

**Cost estimate for this project**: ~$0.50 for full demo

### ⚠️ If OpenAI Key Doesn't Work (Alternatives)

#### Alternative 1: Use Gemini (Google AI) - FREE

If your OpenAI key has issues, we can switch to Google's Gemini (free tier):

1. Go to: https://makersuite.google.com/app/apikey
2. Create API key
3. We'll modify the code to use Gemini instead

#### Alternative 2: Use Ollama (Fully Local) - FREE

Run AI completely locally:
1. Install Ollama: https://ollama.ai/download
2. Run: `ollama pull llama2`
3. We'll modify code to use local models

**For now, try OpenAI first. I'll provide alternative implementations if needed.**

---

## 🛠️ STEP 2: BACKEND SETUP

### 2.1: Install Python Dependencies

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 openai-1.6.1 qdrant-client-1.7.0 ...
```

**❌ If you get errors:**

```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then retry
pip install -r requirements.txt
```

### 2.2: Configure API Key

**Edit the file**: `backend/.env`

Replace `your-api-key-here` with your actual OpenAI key:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

**Test the key:**

```bash
# Create a test file
cat > test_key.py << 'EOF'
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'Key works!'"}],
        max_tokens=10
    )
    print("✅ API Key is VALID!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API Key ERROR: {e}")
EOF

# Run the test
python test_key.py
```

**Expected output:**
```
✅ API Key is VALID!
Response: Key works!
```

**❌ If you see errors:**

| Error | Solution |
|-------|----------|
| `AuthenticationError` | Key is invalid - generate a new one |
| `RateLimitError` | You've hit free tier limit - wait or add payment |
| `APIConnectionError` | Check internet connection |
| `Module not found` | Run `pip install openai python-dotenv` |

### 2.3: Initialize Content (Index Textbook)

This step generates embeddings for all textbook content:

```bash
cd backend
python initialize_content.py
```

**Expected output (takes 2-3 minutes):**
```
🚀 Initializing Physical AI Textbook RAG System...
✅ OpenAI API key found
✅ RAG engine initialized
✅ Qdrant collection created
📂 Loading content from: C:\...\content
✅ Loaded 45 chunks from textbook

📝 Sample chunk:
   Module: Introduction to Physical AI
   Chapter: Fundamentals of Physical AI
   Section: What is Physical AI?
   Tokens: 487
   Content preview: # Chapter 1: Fundamentals of Physical AI

## Learning Objectives
- Understand what Physical AI means...

🔄 Indexing 45 chunks into Qdrant...
   This will take a few minutes (generating embeddings)...
✅ All chunks indexed successfully!

🧪 Testing retrieval...

Query: 'What is Physical AI?'
Found 3 relevant chunks:

1. [Fundamentals of Physical AI]
   Score: 0.892
   Preview: **Physical AI** refers to artificial intelligence systems that interact with the physical world...

✅ INITIALIZATION COMPLETE!
```

**❌ Troubleshooting:**

| Issue | Solution |
|-------|----------|
| `OPENAI_API_KEY not found` | Check `.env` file exists and has correct key |
| `Content directory not found` | Make sure you're in the backend folder |
| `RateLimitError during indexing` | Free tier: wait 60 seconds between retries |
| `No chunks loaded` | Verify `content/modules/` folder exists |

### 2.4: Start Backend Server

```bash
python -m uvicorn src.api.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['C:\\...\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
✅ All AI services initialized successfully
INFO:     Application startup complete.
```

**✅ TEST: Open browser to http://localhost:8000/docs**

You should see FastAPI's interactive API documentation (Swagger UI).

**✅ TEST: Health Check**

In a NEW terminal:
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "rag_ready": true,
  "socratic_ready": true,
  "embodiment_ready": true
}
```

**✅ TEST: Get Modules**

```bash
curl http://localhost:8000/api/v1/modules
```

Expected: JSON array with 5 modules.

**✅ TEST: Chat Endpoint (THE BIG ONE)**

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is Physical AI?\", \"mode\": \"helpful\"}"
```

**Expected response:**
```json
{
  "response": "Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents like robots, drones, or autonomous vehicles. Unlike pure software AI, Physical AI must perceive the environment through sensors, reason about physical constraints, and act through actuators...",
  "sources": [
    {
      "title": "Fundamentals of Physical AI",
      "module": "Introduction to Physical AI",
      "score": 0.89
    }
  ],
  "mode": "helpful"
}
```

**🎉 IF YOU SEE THIS RESPONSE = BACKEND IS FULLY WORKING!**

---

## 🎨 STEP 3: FRONTEND SETUP

### 3.1: Install Node Dependencies

Open a NEW terminal (keep backend running):

```bash
cd frontend
npm install
```

**Expected output:**
```
added 324 packages in 45s
```

**❌ If you get errors:**

```bash
# Clear cache and retry
rm -rf node_modules package-lock.json
npm install
```

### 3.2: Configure Environment

```bash
# Windows PowerShell:
"NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath .env.local -Encoding utf8

# Windows CMD:
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local

# Mac/Linux:
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

**Verify:**
```bash
cat .env.local
```

Should show:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3.3: Update Imports (Already Done!)

The files have already been renamed:
- ✅ `api.ts` is now the REAL implementation (was `api-new.ts`)
- ✅ `main.py` is now the REAL backend (was `main_new.py`)

No changes needed!

### 3.4: Start Frontend

```bash
npm run dev
```

**Expected output:**
```
  ▲ Next.js 14.2.0
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in 2.1s
```

**✅ TEST: Open http://localhost:3000**

You should see the homepage with 5 modules displayed.

---

## 🧪 STEP 4: INTEGRATION TESTING

### Test 1: Basic Chat (Helpful Mode)

1. Open http://localhost:3000
2. Click the chat button (💬 bottom right)
3. Type: "What is LIDAR?"
4. Click Send

**Expected behavior:**
- Loading animation appears
- Response appears within 3 seconds
- Response mentions laser, distance measurement, etc.
- AI speaks the response (voice output)

**✅ Success indicators:**
- Response is detailed and accurate (not a generic placeholder)
- Multiple sentences explaining LIDAR
- May mention use cases or technical specs

**❌ If it doesn't work:**

Open browser console (F12):
- Look for network errors
- Check if POST to `/api/v1/chat` succeeded
- Verify response status is 200

Backend terminal should show:
```
INFO:     127.0.0.1:XXXXX - "POST /api/v1/chat HTTP/1.1" 200 OK
```

### Test 2: Voice Input

1. In the chat widget, click the microphone button 🎙️
2. Say: "What are sensors?"
3. Wait for transcription

**Expected:**
- Mic button turns red and pulses
- "Listening..." appears
- Your speech converts to text
- AI responds

**❌ If voice doesn't work:**
- Check browser permissions (allow microphone)
- Try a different browser (Chrome works best)
- Voice is a bonus feature - text input is sufficient for demo

### Test 3: Socratic Mode (THE DIFFERENTIATOR)

We need to update VoiceChatbot to support mode switching.

**Create a quick test file:**

```bash
# In a new terminal
cd frontend
cat > src/app/test-socratic/page.tsx << 'EOF'
'use client';
import { useState } from 'react';
import { api } from '@/services/api';

export default function TestSocratic() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const testMode = async (mode: 'helpful' | 'socratic' | 'embodiment') => {
    setLoading(true);
    try {
      const result = await api.chat({
        message,
        mode,
        conversation_history: []
      });
      setResponse(`[${mode.toUpperCase()}]\n\n${result.response}\n\n${result.teaching_move ? `Teaching move: ${result.teaching_move}` : ''}`);
    } catch (e) {
      setResponse(`Error: ${e}`);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen p-8 bg-gray-50">
      <h1 className="text-3xl font-bold mb-6">Test AI Modes</h1>

      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask a question..."
        className="w-full p-4 border rounded mb-4"
      />

      <div className="flex gap-4 mb-6">
        <button onClick={() => testMode('helpful')} className="px-6 py-3 bg-blue-600 text-white rounded">
          Test Helpful
        </button>
        <button onClick={() => testMode('socratic')} className="px-6 py-3 bg-purple-600 text-white rounded">
          Test Socratic
        </button>
        <button onClick={() => testMode('embodiment')} className="px-6 py-3 bg-green-600 text-white rounded">
          Test RAIA (Embodiment)
        </button>
      </div>

      {loading && <p>Loading...</p>}

      {response && (
        <div className="bg-white p-6 rounded shadow">
          <pre className="whitespace-pre-wrap">{response}</pre>
        </div>
      )}
    </div>
  );
}
EOF
```

**Test it:**

1. Go to: http://localhost:3000/test-socratic
2. Enter: "What is inverse kinematics?"
3. Click "Test Helpful"

**Expected (Helpful Mode):**
```
[HELPFUL]

Inverse kinematics is the process of calculating the joint angles needed
to position a robot's end effector at a desired location. Unlike forward
kinematics which computes position from joint angles, IK works backwards...
```

4. Now click "Test Socratic" with same question

**Expected (Socratic Mode):**
```
[SOCRATIC]

Before I explain inverse kinematics, tell me - what do you think "inverse"
means in this context? And if forward kinematics tells us where the robot's
hand ends up given joint angles, what do you think inverse kinematics
would calculate?

Teaching move: redirect_to_text
```

5. Now click "Test RAIA (Embodiment)"

**Expected (Embodiment Mode):**
```
[EMBODIMENT]

Oh! Inverse kinematics is actually something I struggle with every day!
When I see an object I want to grab - like a coffee cup - I know WHERE
it is in space, but figuring out how to bend my elbow, rotate my shoulder,
and twist my wrist to reach it exactly... that's the inverse problem!

Sometimes my joints get stuck in weird positions and I can't reach at all.
Do you ever experience this - knowing where you want your hand to be but
not sure how to move your arm to get there?
```

**🎉 IF YOU GET DIFFERENT RESPONSES FOR EACH MODE = CORE FEATURES WORKING!**

### Test 4: Robot State Tracking

```bash
curl http://localhost:8000/api/v1/embodiment/state
```

**Expected response:**
```json
{
  "capabilities": {
    "can_perceive": false,
    "can_move": false,
    "can_manipulate": false,
    "can_navigate": false,
    "can_reason": true
  },
  "understanding": {
    "sensors": 0,
    "actuators": 0,
    "control": 0,
    "ros2": 0,
    "simulation": 0
  },
  "mood": "confused_beginner",
  "progress_percentage": 0
}
```

Now, simulate reading a sensor chapter:

```bash
curl -X POST http://localhost:8000/api/v1/embodiment/react \
  -H "Content-Type: application/json" \
  -d "{\"module_id\": \"01-physical-ai-intro\", \"file\": \"02-sensors-actuators.md\", \"title\": \"Sensors and Actuators\"}"
```

**Expected:**
```json
{
  "narration": "I just learned about LIDAR sensors! The laser pulses feel so precise - 2-3 cm accuracy! But I'm worried about fog and rain... my 'vision' might get cloudy. Do humans also struggle to see in bad weather?",
  "state_change": {
    "sensors": {"old": 0, "new": 20},
    "capability_unlocked": "can_perceive"
  },
  "persona": "RAIA",
  "mood": "curious_learner"
}
```

Check state again:
```bash
curl http://localhost:8000/api/v1/embodiment/state
```

Now `can_perceive` should be `true` and `sensors` should be `20`!

**🎉 IF STATE UPDATES = EMBODIMENT MODE FULLY WORKING!**

---

## 🎯 STEP 5: VERIFY EVERYTHING WORKS

### Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Health check returns all `true`
- [ ] Can list modules (shows 5)
- [ ] Chat in helpful mode works
- [ ] Chat in socratic mode asks questions
- [ ] Chat in embodiment mode uses RAIA persona
- [ ] Robot state updates when reading chapters
- [ ] Voice input works (optional)
- [ ] Voice output works (text-to-speech)

**If ALL checked = YOU'RE READY TO DEMO!**

---

## 🚨 COMMON ISSUES & SOLUTIONS

### Issue 1: "Module not found" (Python)

```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

### Issue 2: OpenAI Key Invalid

1. Generate new key: https://platform.openai.com/api-keys
2. Update `backend/.env`
3. Restart backend

### Issue 3: No Response from Chat

Check:
1. Backend terminal for errors
2. Browser console (F12) for network errors
3. Run health check: `curl http://localhost:8000/api/health`

### Issue 4: CORS Errors

Update `backend/src/api/main.py` line 30:
```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001",  # Add if using different port
    "*"  # Allow all (for development only!)
],
```

### Issue 5: Frontend Can't Connect to Backend

Check `.env.local`:
```bash
cat frontend/.env.local
```

Should be:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If missing:
```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev  # Restart
```

---

## 🎬 READY FOR DEMO?

If all tests pass, you now have:

✅ Real RAG system with 45 indexed chunks
✅ 3 AI modes (Helpful, Socratic, Embodiment)
✅ Robot persona with state tracking
✅ Real textbook content
✅ Working voice interface
✅ Production-quality backend

**Next:** Create a demo video or practice live demo!

---

## 📞 NEED ALTERNATIVE API KEYS?

If OpenAI doesn't work, I can modify the code to use:

1. **Google Gemini** (Free tier, good performance)
2. **Anthropic Claude** (If you have access)
3. **Ollama + Llama2** (Fully local, no API key needed)
4. **Hugging Face** (Free inference API)

Just let me know which alternative you need, and I'll provide the updated code!

**For now, try OpenAI first - it's the most reliable for this demo.**
