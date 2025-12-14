# ⚡ RUN ME FIRST - Quick Start with Gemini

## 🎯 What You Need

- ✅ Python 3.10+ installed
- ✅ Node.js 18+ installed
- ✅ Your API keys are ALREADY configured in `.env`!

---

## 🚀 Start in 3 Commands

### Terminal 1: Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload --port 8000
```

### Terminal 2: Frontend

```bash
cd frontend
npm install
npm run dev
```

### Browser

Open: http://localhost:3000

---

## 🧪 Quick Test

1. Click chat button (💬 bottom right)
2. Type: "What is Physical AI?"
3. Get AI response with sources!

**✅ If you see a detailed response = IT WORKS!**

---

## 🎨 Features to Demo

### 1. Helpful Mode (Default)
- Direct answers with citations
- Fast and accurate

### 2. Socratic Mode
Go to: http://localhost:3000/test-socratic
- Ask questions
- AI asks YOU questions back!

### 3. Robot Embodiment (RAIA)
- AI pretends to BE a robot learning
- Shares struggles and insights

---

## ❌ If Something Breaks

### Backend won't start
```bash
cd backend
pip install google-generativeai anthropic cohere --upgrade
python -m uvicorn src.api.main:app --reload
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

### Chat not working
1. Check backend is running (http://localhost:8000/docs)
2. Check `.env` has `GEMINI_API_KEY`
3. Check browser console for errors

---

## 🏆 You Have

✅ **Real RAG** - 45 textbook chunks indexed
✅ **3 AI Modes** - Helpful, Socratic, Embodiment
✅ **Real Content** - 4000+ words of textbook
✅ **Gemini AI** - Free 1M tokens/min!
✅ **Qdrant Cloud** - Production vector DB
✅ **Voice Mode** - Speech input/output

**This is hackathon-winning quality. Go demo it! 🚀**
