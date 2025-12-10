# Quickstart Guide: Physical AI Textbook Platform

**Branch**: `001-physical-ai-textbook` | **Date**: 2025-12-09

## Prerequisites

- **Node.js**: 18.x or 20.x LTS
- **Python**: 3.11+
- **Git**: 2.x+
- **Docker**: (optional, for containerized development)

## Quick Setup (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/physical-ai-textbook.git
cd physical-ai-textbook
```

### 2. Environment Setup

```bash
# Copy environment templates
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Edit backend/.env with your API keys:
# - OPENAI_API_KEY (required)
# - QDRANT_API_KEY (optional for local dev)
# - DATABASE_URL (Neon connection string)
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn src.api.main:app --reload --port 8000
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 5. Verify Setup

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Environment Variables

### Backend (`backend/.env`)

```env
# Database
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require

# AI Services
OPENAI_API_KEY=sk-...
QWEN_API_KEY=sk-...  # For Urdu translation

# Vector Database
QDRANT_URL=https://xxx.qdrant.tech
QDRANT_API_KEY=...

# Security
SECRET_KEY=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:3000

# Optional
DEBUG=true
LOG_LEVEL=INFO
```

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Development Workflow

### Running Tests

```bash
# Backend tests
cd backend
pytest --cov=src --cov-report=html

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

### Code Quality

```bash
# Backend linting
cd backend
black src tests  # Format
flake8 src tests  # Lint
mypy src  # Type check

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

### Database Migrations

```bash
cd backend

# Generate new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

---

## Local Development with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**docker-compose.yml** includes:
- Backend (FastAPI)
- Frontend (Next.js dev server)
- PostgreSQL (local development)
- Qdrant (local vector DB)

---

## Project Structure Overview

```
physical-ai-textbook/
├── backend/
│   ├── src/
│   │   ├── api/          # FastAPI routes
│   │   ├── models/       # SQLAlchemy models
│   │   ├── services/     # Business logic
│   │   └── db/           # Database config
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js App Router
│   │   ├── components/   # React components
│   │   └── services/     # API client
│   └── package.json
│
├── content/              # Textbook MDX files
│   └── modules/
│
└── scripts/              # Utility scripts
```

---

## Common Tasks

### Adding a New Chapter

1. Create MDX file in `content/modules/<module>/`
2. Update `content/index.json` manifest
3. Run embedding script: `python scripts/ingest-content.py`

### Testing Chatbot Locally

1. Ensure backend is running
2. Seed vector database: `python scripts/generate-embeddings.py`
3. Test via API: `curl -X POST http://localhost:8000/api/chat/ask -d '{"question":"What is ROS 2?"}'`

### Deploying to Production

```bash
# Frontend (GitHub Pages)
npm run build  # Generates /out directory
# Push to main branch - GitHub Actions deploys automatically

# Backend (Fly.io)
fly deploy  # Requires fly.toml configuration
```

---

## Troubleshooting

### Database Connection Issues

```bash
# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Check Neon status
# Visit https://console.neon.tech
```

### API Key Issues

```bash
# Verify OpenAI key
python -c "import openai; openai.api_key='YOUR_KEY'; print(openai.models.list())"
```

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

---

## Next Steps

1. Review [research.md](./research.md) for technology decisions
2. Review [data-model.md](./data-model.md) for database schema
3. Review [contracts/openapi.yaml](./contracts/openapi.yaml) for API specification
4. Run `/sp.tasks` to generate implementation tasks
