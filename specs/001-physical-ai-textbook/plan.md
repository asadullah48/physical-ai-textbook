# Implementation Plan: Physical AI & Humanoid Robotics Textbook Platform

**Branch**: `001-physical-ai-textbook` | **Date**: 2025-12-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-textbook/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an interactive educational textbook platform for Physical AI & Humanoid Robotics with:
- Structured content (10+ chapters across 5 modules) with syntax-highlighted code examples
- RAG-powered chatbot for contextual Q&A with textbook content retrieval
- User authentication with learning profile questionnaire
- Adaptive content personalization based on user background
- Urdu translation with RTL layout support

Technical approach: Static frontend (React/Next.js static export) on GitHub Pages + Python FastAPI backend on Fly.io/Render free tier, with free-tier vector database for RAG.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.x (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLAlchemy, LangChain, sentence-transformers
- Frontend: Next.js 14 (static export), React 18, TailwindCSS
- AI: Groq (Llama 3.1 70B) primary, OpenAI GPT-4o-mini for Urdu translation (hybrid approach)
- Vector DB: Qdrant Cloud (1GB free tier, hybrid semantic + keyword search)

**Storage**:
- PostgreSQL via Neon Serverless (512MB free tier, auto-suspend, fast cold start)
- Qdrant Cloud for textbook content embeddings (managed, 1GB free)

**Testing**:
- Backend: pytest with pytest-asyncio
- Frontend: Jest + React Testing Library

**Target Platform**: Web (modern browsers: Chrome, Firefox, Safari, Edge - last 2 versions)
**Project Type**: Web application (frontend + backend)
**Performance Goals**:
- Page navigation: <2 seconds (FR-031)
- Chatbot response: <5 seconds (FR-010)
- 100 concurrent users without degradation (FR-033)

**Constraints**:
- Free tier services only (C-001)
- 58,000 token budget for AI operations (C-002)
- 6-hour development window (C-003)
- Static hosting for frontend (C-004)
- Free tier backend hosting (C-005)

**Scale/Scope**: <1000 users in first month (A-008), 10+ chapters, 5 modules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Gates (Phase 0 Entry)

| Principle | Gate | Status | Notes |
|-----------|------|--------|-------|
| I. Accuracy & Scientific Rigor (NON-NEGOTIABLE) | All technical claims must be verifiable | PASS | Content will reference authoritative robotics sources |
| II. Practical Implementation Focus | Every concept has working code | PASS | FR-002 requires executable code examples per chapter |
| III. Clear Documentation & Progressive Learning | Logical progression Module 1→5 | PASS | Spec defines 5 modules with explicit progression |
| IV. Test-Driven Examples (NON-NEGOTIABLE) | All code includes tests | PASS | FR-032 requires tested code, constitution mandates 80% coverage |
| V. Safety & Ethics | Safety considerations documented | PASS | Constitution requires safety in hardware interfaces |
| VI. Reproducibility & Version Control | Documented environments | PASS | FR-032 requires documented execution environments |

### Design Verification (Post Phase 1)

| Aspect | Requirement | Verification Method |
|--------|-------------|-------------------|
| Code Quality | PEP 8 (Python), ESLint (TS) | CI linting checks |
| Test Coverage | >80% core library | pytest-cov, jest --coverage |
| Documentation | Docstrings on all public functions | pydoc verification |
| Accessibility | Alt-text on visuals | A11y audit |
| Performance | Real-time ops documented | Benchmark tests |

### Risk Assessment

| Risk | Mitigation |
|------|------------|
| Free tier limits exceeded | Token budgeting, caching translations |
| 6-hour constraint vs scope | MVP focuses on P1 stories only (textbook access + chatbot) |
| RAG quality issues | Hybrid semantic + keyword retrieval (FR-007) |

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── openapi.yaml     # REST API contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
physical-ai-textbook/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── main.py              # FastAPI app entry
│   │   │   ├── routes/
│   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   ├── chat.py          # Chatbot endpoints
│   │   │   │   ├── content.py       # Textbook content endpoints
│   │   │   │   ├── personalize.py   # Content personalization
│   │   │   │   └── translate.py     # Translation endpoints
│   │   │   └── deps.py              # Dependency injection
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User & UserProfile
│   │   │   ├── content.py           # Module, Chapter, Translation
│   │   │   └── conversation.py      # Conversation, Message
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Authentication logic
│   │   │   ├── rag.py               # RAG retrieval service
│   │   │   ├── llm.py               # LLM interaction wrapper
│   │   │   ├── personalization.py   # Content adaptation
│   │   │   └── translation.py       # Urdu translation
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── session.py           # Database session
│   │       └── migrations/          # Alembic migrations
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── app/                     # Next.js App Router pages
│   │   │   ├── page.tsx             # Homepage/ToC
│   │   │   ├── layout.tsx           # Root layout
│   │   │   ├── modules/
│   │   │   │   └── [moduleId]/
│   │   │   │       └── [chapterId]/
│   │   │   │           └── page.tsx # Chapter view
│   │   │   ├── auth/
│   │   │   │   ├── login/
│   │   │   │   └── signup/
│   │   │   └── profile/
│   │   ├── components/
│   │   │   ├── ui/                  # Reusable UI components
│   │   │   ├── Chatbot.tsx          # RAG chatbot widget
│   │   │   ├── ChapterContent.tsx   # Content renderer
│   │   │   ├── CodeBlock.tsx        # Syntax-highlighted code
│   │   │   ├── TableOfContents.tsx  # Navigation
│   │   │   └── LanguageToggle.tsx   # EN/UR switcher
│   │   ├── services/
│   │   │   ├── api.ts               # API client
│   │   │   └── auth.ts              # Auth state management
│   │   ├── hooks/
│   │   │   └── useChat.ts           # Chatbot state hook
│   │   └── styles/
│   │       └── globals.css          # TailwindCSS + RTL styles
│   ├── public/
│   │   └── content/                 # Static textbook content (MDX)
│   ├── tests/
│   ├── next.config.js               # Static export config
│   ├── tailwind.config.js
│   └── package.json
│
├── content/                         # Textbook source content
│   ├── modules/
│   │   ├── 01-physical-ai-intro/
│   │   │   ├── 01-introduction.mdx
│   │   │   └── 02-sensors.mdx
│   │   ├── 02-ros2/
│   │   ├── 03-simulation/
│   │   ├── 04-nvidia-isaac/
│   │   └── 05-vla-systems/
│   └── index.json                   # Content manifest
│
└── scripts/
    ├── ingest-content.py            # Vector DB ingestion
    └── generate-embeddings.py       # Embedding generation
```

**Structure Decision**: Web application structure selected (Option 2) with clear frontend/backend separation. Frontend uses Next.js App Router with static export for GitHub Pages. Backend uses FastAPI with clean separation of routes/models/services. Content stored as MDX files for easy authoring with separate ingestion scripts for RAG.

## Post-Design Constitution Check (Phase 1 Complete)

*Re-evaluation after completing research and design artifacts.*

| Principle | Gate | Status | Design Evidence |
|-----------|------|--------|-----------------|
| I. Accuracy & Scientific Rigor | Technical claims verifiable | PASS | research.md cites specific technologies with version requirements |
| II. Practical Implementation Focus | Working code examples | PASS | OpenAPI contract defines all endpoints; quickstart.md provides setup |
| III. Clear Documentation & Progressive Learning | Logical structure | PASS | data-model.md defines entity relationships; 5-module progression preserved |
| IV. Test-Driven Examples | Tests specified | PASS | Testing strategy in research.md: pytest (80% coverage), Jest, Playwright |
| V. Safety & Ethics | Security addressed | PASS | research.md includes security considerations section |
| VI. Reproducibility & Version Control | Environment documented | PASS | quickstart.md includes all dependencies and setup instructions |

**Design Artifacts Generated:**
- [x] research.md - Technology decisions with rationale
- [x] data-model.md - Database schema with relationships
- [x] contracts/openapi.yaml - Complete API specification
- [x] quickstart.md - Developer setup guide

**All NEEDS CLARIFICATION items resolved:**
- LLM Provider: Groq (Llama 3.1 70B) + OpenAI GPT-4o-mini hybrid
- Vector DB: Qdrant Cloud (1GB free tier)
- PostgreSQL: Neon Serverless (512MB free tier)
- Frontend Deployment: Next.js 14 static export to GitHub Pages

## Complexity Tracking

> **No violations to report.** Design adheres to all constitution principles.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none) | - | - |

## Architectural Decisions Summary

Key decisions made during planning (candidates for ADR if significant):

1. **Hybrid LLM Strategy**: Groq for general Q&A (free tier), OpenAI for translation (better Urdu support)
2. **Static Frontend**: Next.js static export enables GitHub Pages hosting (free)
3. **Serverless Database**: Neon auto-suspend reduces costs for intermittent usage
4. **Separate Vector DB**: Qdrant Cloud instead of pgvector for optimized semantic search
