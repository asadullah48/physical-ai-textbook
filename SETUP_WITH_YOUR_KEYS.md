# 🚀 SETUP GUIDE - Using YOUR Production API Keys

## ✅ Your API Keys (Already Configured!)

You have **EXCELLENT** API keys with generous free tiers:

| Service | Status | Free Tier Limit | Cost After Free |
|---------|--------|-----------------|-----------------|
| **Gemini** | ✅ Active | 1M tokens/min, 60 req/min | $0 (enough for hackathon!) |
| **Claude** | ✅ Active | Limited messages | Backup option |
| **Cohere** | ✅ Active | Good for embeddings | Alternative embeddings |
| **Qdrant Cloud** | ✅ Active | 1GB RAM forever free | Production-ready! |
| **Context7 (MCP)** | ✅ Active | Advanced features | For curriculum analysis |
| **GitHub (MCP)** | ✅ Active | Full access | For repo integration |

**Recommendation**: Use **Gemini** as primary (best free tier!)

---

## 🎯 QUICK START (3 Steps)

### Step 1: Install Backend Dependencies (2 min)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows):
venv\Scripts\activate

# Activate (Mac/Linux):
# source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed google-generativeai-0.3.2 anthropic-0.18.1 ...
```

**✅ Verify Gemini SDK:**
```bash
python -c "import google.generativeai as genai; print('✅ Gemini SDK ready!')"
```

### Step 2: Test Your Gemini API Key (30 sec)

```bash
python << 'EOF'
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {api_key[:20]}...")

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Gemini is working!'")
    print(f"\n✅ SUCCESS!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")
EOF
```

**Expected:**
```
API Key found: AIzaSyDgQcQri6JQN_A...
✅ SUCCESS!
Response: Gemini is working!
```

### Step 3: Initialize Content & Start (3 min)

```bash
# Index all textbook content
python initialize_content.py

# Start backend server
python -m uvicorn src.api.main:app --reload --port 8000
```

**Expected (after indexing):**
```
🚀 Initializing Physical AI Textbook RAG System...
✅ Gemini AI provider initialized
✅ Qdrant collection created
✅ Loaded 45 chunks from textbook
🔄 Indexing...
✅ All chunks indexed successfully!

INFO: Uvicorn running on http://127.0.0.1:8000
```

---

## 🧪 TEST YOUR SETUP

### Test 1: Health Check

```bash
curl http://localhost:8000/api/health
```

**Expected:**
```json
{
  "status": "healthy",
  "rag_ready": true,
  "socratic_ready": true,
  "embodiment_ready": true
}
```

### Test 2: Chat with Gemini

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Physical AI?", "mode": "helpful"}'
```

**Expected:**
- Detailed response about Physical AI
- Sources from textbook
- Response in < 2 seconds (Gemini is FAST!)

### Test 3: Socratic Mode

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is inverse kinematics?", "mode": "socratic"}'
```

**Expected:**
```json
{
  "response": "Before I explain, tell me - what do you think 'inverse' means in this robotics context?...",
  "teaching_move": "socratic_question",
  ...
}
```

### Test 4: Robot Embodiment

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about sensors", "mode": "embodiment"}'
```

**Expected (RAIA persona):**
```json
{
  "response": "As a learning robot, sensors are like my senses! My LIDAR is like vision, but using laser pulses instead of light...",
  "robot_state": {
    "capabilities": {"can_perceive": false, ...},
    "mood": "curious_learner"
  }
}
```

---

## 🎨 Frontend Setup

```bash
# New terminal (keep backend running)
cd frontend

# Install dependencies
npm install

# Set API URL
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start dev server
npm run dev
```

**Open:** http://localhost:3000

---

## 🔥 USING YOUR QDRANT CLOUD (Production DB)

Your `.env` is already configured with Qdrant Cloud!

**Benefits:**
- ✅ Persistent storage (vectors survive restart)
- ✅ 1GB RAM free forever
- ✅ Production-ready
- ✅ Web UI dashboard

**Access Dashboard:**
1. Go to: https://cloud.qdrant.io
2. Login with your account
3. See your cluster: `110c8859-6a7d-4a49-bb57-b23873fc2d41`
4. View indexed vectors!

**Note:** Content initialization automatically uses your Qdrant Cloud instance.

---

## 💰 Cost Analysis (With YOUR Keys)

### Gemini Free Tier
- **Limit**: 1,000,000 tokens/minute (!)
- **Requests**: 60/minute
- **Cost**: $0

**For this hackathon:**
- 1000 user questions = ~500K tokens
- **Total cost: $0** (well within free tier!)

### Qdrant Cloud Free Tier
- **Storage**: 1GB RAM
- **Vectors**: ~1.3M vectors (768-dim)
- **Cost**: $0 forever

**For this project:**
- 45 chunks × 768 dimensions = ~35KB
- **Total cost: $0**

### Fallback to Claude (if needed)
- You have Anthropic API key as backup
- Claude Haiku: Very affordable
- Only used if Gemini has issues

---

## 🚨 Troubleshooting

### "ImportError: No module named 'google.generativeai'"

```bash
pip install google-generativeai==0.3.2
```

### "Gemini API key invalid"

Your key looks correct, but if issues:
1. Go to: https://makersuite.google.com/app/apikey
2. Verify key is enabled
3. Check usage quota
4. Generate new key if needed

### "Qdrant connection failed"

Your Qdrant URL looks correct. If issues:
1. Go to: https://cloud.qdrant.io
2. Check cluster status (should be "Running")
3. Verify API key in `.env` matches dashboard

### Switch to Local Qdrant (if cloud issues)

Edit `.env`:
```env
# Comment out cloud:
# QDRANT_URL=https://...
# QDRANT_API_KEY=...

# Use local:
QDRANT_URL=:memory:
```

Restart backend. Data won't persist but will work for demo.

### Switch to Claude (if Gemini issues)

Edit `.env`:
```env
AI_PROVIDER=anthropic  # Instead of "gemini"
```

Restart backend. Uses your Claude API key instead.

---

## 📊 VERIFICATION CHECKLIST

Before demoing, verify:

- [ ] Backend running on :8000
- [ ] Frontend running on :3000
- [ ] Health check returns all `true`
- [ ] Chat in helpful mode works
- [ ] Chat in socratic mode asks questions back
- [ ] Chat in embodiment mode uses RAIA persona
- [ ] Qdrant dashboard shows vectors (if using cloud)
- [ ] Response time < 3 seconds
- [ ] No errors in backend console

**If all checked = READY TO WIN! 🏆**

---

## 🎬 DEMO SCRIPT (2 Minutes)

**:00-:30** - Show the problem
"AI textbooks are static. Students can't interact meaningfully."

**:30-:60** - Demonstrate Socratic Mode
- Ask: "What is inverse kinematics?"
- Show AI responds with questions, not answers
- **Judge reaction**: "This is pedagogy, not just RAG!"

**:60-:90** - Embodiment Mode (Showstopper)
- Switch to RAIA
- RAIA: "I'm stuck! My Jacobian is singular..."
- **Judge reaction**: "The AI IS the robot?!"

**:90-:120** - Prove it's real
- Open Qdrant dashboard → Show vectors
- Show backend code (rag_engine.py)
- "This is production AI, not demo magic"

**Closing**: "First AI textbook that teaches Physical AI by BEING Physical AI."

---

## 🎯 NEXT: Make It Beautiful

Core AI is DONE. Optional enhancements:

1. **Sidebar Navigation** (1 hour)
2. **Visual Learning Graph** (1 hour)
3. **AI Companion Panel** (1 hour)
4. **Dark Mode** (30 min)

**You can win with what you have now!** The differentiators are implemented.

---

## 🆘 NEED HELP?

1. Check backend logs for errors
2. Check browser console (F12)
3. Test API with curl first
4. Verify .env has all keys
5. Try restarting both servers

**Your setup is production-ready. The hard part is done! 🚀**
