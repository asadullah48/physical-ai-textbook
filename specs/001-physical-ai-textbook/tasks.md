# Tasks: Physical AI & Humanoid Robotics Textbook Platform

**Input**: Design documents from `/specs/001-physical-ai-textbook/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: Tests are included as the constitution mandates 80% test coverage and FR-032 requires tested code.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `physical-ai-textbook/backend/src/`
- **Frontend**: `physical-ai-textbook/frontend/src/`
- **Content**: `physical-ai-textbook/content/`
- **Scripts**: `physical-ai-textbook/scripts/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both frontend and backend

- [X] T001 Create project root directory structure per plan.md in physical-ai-textbook/
- [X] T002 [P] Initialize Python backend with FastAPI in physical-ai-textbook/backend/pyproject.toml
- [X] T003 [P] Initialize Next.js 14 frontend with TypeScript in physical-ai-textbook/frontend/package.json
- [X] T004 [P] Configure backend linting (Black, Flake8, mypy) in physical-ai-textbook/backend/pyproject.toml
- [X] T005 [P] Configure frontend linting (ESLint, Prettier) in physical-ai-textbook/frontend/.eslintrc.js
- [X] T006 [P] Create backend requirements.txt with FastAPI, SQLAlchemy, Alembic, LangChain dependencies
- [X] T007 [P] Configure TailwindCSS with RTL support in physical-ai-textbook/frontend/tailwind.config.js
- [X] T008 [P] Create .env.example files for backend and frontend with required variables
- [X] T009 [P] Create Dockerfile for backend in physical-ai-textbook/backend/Dockerfile
- [X] T010 [P] Configure Next.js static export in physical-ai-textbook/frontend/next.config.js

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database & ORM Setup

- [X] T011 Create SQLAlchemy base model and session in physical-ai-textbook/backend/src/db/session.py
- [X] T012 Configure Alembic for migrations in physical-ai-textbook/backend/src/db/migrations/env.py
- [X] T013 Create initial migration with all tables in physical-ai-textbook/backend/src/db/migrations/versions/001_initial.py

### API Infrastructure

- [X] T014 Create FastAPI app entry point with CORS in physical-ai-textbook/backend/src/api/main.py
- [X] T015 [P] Create dependency injection utilities in physical-ai-textbook/backend/src/api/deps.py
- [X] T016 [P] Create Pydantic base schemas in physical-ai-textbook/backend/src/api/schemas/base.py
- [X] T017 [P] Create error handling middleware in physical-ai-textbook/backend/src/api/middleware/errors.py
- [X] T018 Create health check endpoint in physical-ai-textbook/backend/src/api/routes/health.py

### Frontend Infrastructure

- [X] T019 Create root layout with font loading in physical-ai-textbook/frontend/src/app/layout.tsx
- [X] T020 [P] Create API client service in physical-ai-textbook/frontend/src/services/api.ts
- [X] T021 [P] Create global CSS with TailwindCSS base in physical-ai-textbook/frontend/src/styles/globals.css
- [X] T022 [P] Create reusable UI components (Button, Input, Card) in physical-ai-textbook/frontend/src/components/ui/

### Testing Infrastructure

- [X] T023 [P] Configure pytest with async support in physical-ai-textbook/backend/tests/conftest.py
- [X] T024 [P] Configure Jest for frontend tests in physical-ai-textbook/frontend/jest.config.js

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Interactive Textbook Access (Priority: P1)

**Goal**: Students can browse structured textbook content with 10+ chapters across 5 modules, navigate between chapters, view syntax-highlighted code examples, and access responsive content on all devices.

**Independent Test**: Navigate to textbook URL, browse all modules and chapters, verify code highlighting and mobile responsiveness.

### Tests for User Story 1

- [X] T025 [P] [US1] Integration test for content listing in physical-ai-textbook/backend/tests/integration/test_content.py
- [X] T026 [P] [US1] Component tests for ChapterContent in physical-ai-textbook/frontend/tests/components/ChapterContent.test.tsx

### Backend Implementation for User Story 1

- [X] T027 [P] [US1] Create content service to load MDX files in physical-ai-textbook/backend/src/services/content.py
- [X] T028 [P] [US1] Create Pydantic schemas for Module, Chapter in physical-ai-textbook/backend/src/api/schemas/content.py
- [X] T029 [US1] Create content routes (GET /modules, /modules/{slug}, /chapters/{slug}) in physical-ai-textbook/backend/src/api/routes/content.py
- [X] T030 [US1] Register content routes in main.py router

### Frontend Implementation for User Story 1

- [X] T031 [P] [US1] Create TableOfContents component in physical-ai-textbook/frontend/src/components/TableOfContents.tsx
- [X] T032 [P] [US1] Create CodeBlock component with syntax highlighting in physical-ai-textbook/frontend/src/components/CodeBlock.tsx
- [X] T033 [P] [US1] Create ChapterContent component with MDX rendering in physical-ai-textbook/frontend/src/components/ChapterContent.tsx
- [X] T034 [US1] Create homepage with module listing in physical-ai-textbook/frontend/src/app/page.tsx
- [X] T035 [US1] Create dynamic chapter page in physical-ai-textbook/frontend/src/app/modules/[moduleId]/[chapterId]/page.tsx
- [X] T036 [US1] Create generateStaticParams for all chapters in physical-ai-textbook/frontend/src/app/modules/[moduleId]/[chapterId]/page.tsx
- [X] T037 [US1] Add chapter navigation (prev/next) to chapter page
- [X] T038 [US1] Add mobile responsive styles and test on small screens

### Content Setup for User Story 1

- [X] T039 [P] [US1] Create content manifest index.json in physical-ai-textbook/content/index.json
- [X] T040 [P] [US1] Create Module 1 sample chapter (Introduction) in physical-ai-textbook/content/modules/01-physical-ai-intro/01-introduction.mdx
- [X] T041 [P] [US1] Create Module 2 sample chapter (ROS 2 Basics) in physical-ai-textbook/content/modules/02-ros2/01-basics.mdx

**Checkpoint**: User Story 1 complete - Textbook navigation and content display working independently

---

## Phase 4: User Story 2 - AI-Powered Q&A Assistant (Priority: P1)

**Goal**: Learners can ask questions about textbook material through an integrated chatbot that retrieves relevant content using RAG and maintains conversation history.

**Independent Test**: Open any chapter, ask a question through chatbot, verify contextual response with textbook references within 5 seconds.

### Tests for User Story 2

- [ ] T042 [P] [US2] Unit test for RAG service in physical-ai-textbook/backend/tests/unit/test_rag.py
- [ ] T043 [P] [US2] Integration test for chat endpoints in physical-ai-textbook/backend/tests/integration/test_chat.py
- [ ] T044 [P] [US2] Component test for Chatbot in physical-ai-textbook/frontend/tests/components/Chatbot.test.tsx

### Backend Implementation for User Story 2

- [ ] T045 [P] [US2] Create Conversation model in physical-ai-textbook/backend/src/models/conversation.py
- [ ] T046 [P] [US2] Create Message model in physical-ai-textbook/backend/src/models/conversation.py
- [ ] T047 [US2] Create Alembic migration for conversation tables in physical-ai-textbook/backend/src/db/migrations/versions/002_conversations.py
- [ ] T048 [P] [US2] Create LLM service wrapper (Groq client) in physical-ai-textbook/backend/src/services/llm.py
- [ ] T049 [US2] Create RAG service with Qdrant integration in physical-ai-textbook/backend/src/services/rag.py
- [ ] T050 [US2] Create chat service combining RAG + LLM in physical-ai-textbook/backend/src/services/chat.py
- [ ] T051 [P] [US2] Create Pydantic schemas for chat in physical-ai-textbook/backend/src/api/schemas/chat.py
- [ ] T052 [US2] Create chat routes (conversations, messages, quick ask) in physical-ai-textbook/backend/src/api/routes/chat.py
- [ ] T053 [US2] Register chat routes in main.py router

### Frontend Implementation for User Story 2

- [ ] T054 [P] [US2] Create useChat hook for chatbot state in physical-ai-textbook/frontend/src/hooks/useChat.ts
- [ ] T055 [US2] Create Chatbot component with message history in physical-ai-textbook/frontend/src/components/Chatbot.tsx
- [ ] T056 [US2] Add text highlight and "Ask about this" feature in ChapterContent
- [ ] T057 [US2] Integrate Chatbot into chapter page layout
- [ ] T058 [US2] Add loading state and error handling to Chatbot

### Vector Database Setup for User Story 2

- [ ] T059 [P] [US2] Create content ingestion script in physical-ai-textbook/scripts/ingest-content.py
- [ ] T060 [P] [US2] Create embedding generation script in physical-ai-textbook/scripts/generate-embeddings.py
- [ ] T061 [US2] Run ingestion for sample chapters and verify Qdrant indexing

**Checkpoint**: User Story 2 complete - RAG chatbot working independently with textbook content

---

## Phase 5: User Story 3 - User Account and Learning Profile (Priority: P2)

**Goal**: New learners can create accounts, complete a 2-step profile questionnaire (basic info + background), and have their preferences persisted across sessions.

**Independent Test**: Sign up, complete profile questionnaire, log out, log back in, verify profile data persists.

### Tests for User Story 3

- [ ] T062 [P] [US3] Unit test for auth service in physical-ai-textbook/backend/tests/unit/test_auth.py
- [ ] T063 [P] [US3] Integration test for auth endpoints in physical-ai-textbook/backend/tests/integration/test_auth.py
- [ ] T064 [P] [US3] Component test for SignupForm in physical-ai-textbook/frontend/tests/components/SignupForm.test.tsx

### Backend Implementation for User Story 3

- [ ] T065 [P] [US3] Create User model in physical-ai-textbook/backend/src/models/user.py
- [ ] T066 [P] [US3] Create UserProfile model in physical-ai-textbook/backend/src/models/user.py
- [ ] T067 [US3] Create Alembic migration for user tables in physical-ai-textbook/backend/src/db/migrations/versions/003_users.py
- [ ] T068 [US3] Create auth service (signup, login, logout, session) in physical-ai-textbook/backend/src/services/auth.py
- [ ] T069 [P] [US3] Create Pydantic schemas for auth in physical-ai-textbook/backend/src/api/schemas/auth.py
- [ ] T070 [US3] Create auth routes (signup, login, logout, me) in physical-ai-textbook/backend/src/api/routes/auth.py
- [ ] T071 [US3] Create profile routes (get, update) in physical-ai-textbook/backend/src/api/routes/auth.py
- [ ] T072 [US3] Register auth routes in main.py router
- [ ] T073 [US3] Add session authentication middleware in physical-ai-textbook/backend/src/api/middleware/auth.py

### Frontend Implementation for User Story 3

- [ ] T074 [P] [US3] Create auth service for state management in physical-ai-textbook/frontend/src/services/auth.ts
- [ ] T075 [P] [US3] Create SignupForm component in physical-ai-textbook/frontend/src/components/SignupForm.tsx
- [ ] T076 [P] [US3] Create LoginForm component in physical-ai-textbook/frontend/src/components/LoginForm.tsx
- [ ] T077 [P] [US3] Create ProfileQuestionnaire component in physical-ai-textbook/frontend/src/components/ProfileQuestionnaire.tsx
- [ ] T078 [US3] Create signup page in physical-ai-textbook/frontend/src/app/auth/signup/page.tsx
- [ ] T079 [US3] Create login page in physical-ai-textbook/frontend/src/app/auth/login/page.tsx
- [ ] T080 [US3] Create profile page in physical-ai-textbook/frontend/src/app/profile/page.tsx
- [ ] T081 [US3] Add authentication state to root layout
- [ ] T082 [US3] Add login/signup navigation to header

**Checkpoint**: User Story 3 complete - Authentication and profiles working independently

---

## Phase 6: User Story 4 - Adaptive Content Personalization (Priority: P3)

**Goal**: Logged-in users with completed profiles can request personalized content adaptation that simplifies familiar topics and elaborates on unfamiliar ones while preserving code examples.

**Independent Test**: Create profiles with different backgrounds, click "Personalize" on same chapter, verify content adapts differently.

**Dependency**: Requires US3 (User Profiles) to be complete

### Tests for User Story 4

- [ ] T083 [P] [US4] Unit test for personalization service in physical-ai-textbook/backend/tests/unit/test_personalization.py
- [ ] T084 [P] [US4] Integration test for personalize endpoint in physical-ai-textbook/backend/tests/integration/test_personalize.py

### Backend Implementation for User Story 4

- [ ] T085 [P] [US4] Create PersonalizedContent model in physical-ai-textbook/backend/src/models/content.py
- [ ] T086 [US4] Create Alembic migration for personalized_content table in physical-ai-textbook/backend/src/db/migrations/versions/004_personalization.py
- [ ] T087 [US4] Create personalization service with LLM in physical-ai-textbook/backend/src/services/personalization.py
- [ ] T088 [P] [US4] Create Pydantic schemas for personalization in physical-ai-textbook/backend/src/api/schemas/personalize.py
- [ ] T089 [US4] Create personalize routes (POST, GET cached) in physical-ai-textbook/backend/src/api/routes/personalize.py
- [ ] T090 [US4] Register personalize routes in main.py router

### Frontend Implementation for User Story 4

- [ ] T091 [US4] Create PersonalizeButton component in physical-ai-textbook/frontend/src/components/PersonalizeButton.tsx
- [ ] T092 [US4] Add personalization toggle to ChapterContent component
- [ ] T093 [US4] Handle profile-incomplete redirect (FR-020)
- [ ] T094 [US4] Add loading state for personalization generation

**Checkpoint**: User Story 4 complete - Content personalization working independently

---

## Phase 7: User Story 5 - Multilingual Access (Urdu Translation) (Priority: P3)

**Goal**: Learners can translate chapters to Urdu with proper RTL layout while keeping code blocks in English and toggling between languages.

**Independent Test**: Click "Translate to Urdu" on any chapter, verify RTL layout, English code blocks, and toggle back to English.

### Tests for User Story 5

- [ ] T095 [P] [US5] Unit test for translation service in physical-ai-textbook/backend/tests/unit/test_translation.py
- [ ] T096 [P] [US5] Integration test for translate endpoint in physical-ai-textbook/backend/tests/integration/test_translate.py

### Backend Implementation for User Story 5

- [ ] T097 [P] [US5] Create TranslationCache model in physical-ai-textbook/backend/src/models/content.py
- [ ] T098 [US5] Create Alembic migration for translation_cache table in physical-ai-textbook/backend/src/db/migrations/versions/005_translation.py
- [ ] T099 [US5] Create translation service with OpenAI/Qwen in physical-ai-textbook/backend/src/services/translation.py
- [ ] T100 [P] [US5] Create Pydantic schemas for translation in physical-ai-textbook/backend/src/api/schemas/translate.py
- [ ] T101 [US5] Create translate routes (POST, GET cached) in physical-ai-textbook/backend/src/api/routes/translate.py
- [ ] T102 [US5] Register translate routes in main.py router

### Frontend Implementation for User Story 5

- [ ] T103 [P] [US5] Create LanguageToggle component in physical-ai-textbook/frontend/src/components/LanguageToggle.tsx
- [ ] T104 [US5] Add RTL styles and direction switching in physical-ai-textbook/frontend/src/styles/globals.css
- [ ] T105 [US5] Integrate LanguageToggle into chapter page
- [ ] T106 [US5] Handle code block preservation during translation display
- [ ] T107 [US5] Add Urdu font (Noto Nastaliq) loading in layout.tsx

**Checkpoint**: User Story 5 complete - Urdu translation with RTL working independently

---

## Phase 8: User Story 6 - AI-Assisted Content Creation (Priority: P4 - Bonus)

**Goal**: Authors can use AI assistants to generate draft chapters, review code examples, and create practice exercises.

**Independent Test**: Invoke each AI skill with sample input, verify structured output following textbook conventions.

### Implementation for User Story 6

- [ ] T108 [P] [US6] Create book-writer skill prompt in physical-ai-textbook/.claude/skills/book-writer.md
- [ ] T109 [P] [US6] Create code-reviewer skill prompt in physical-ai-textbook/.claude/skills/code-reviewer.md
- [ ] T110 [P] [US6] Create exercise-generator skill prompt in physical-ai-textbook/.claude/skills/exercise-generator.md
- [ ] T111 [US6] Test skills with sample chapter outline

**Checkpoint**: User Story 6 complete - Content creation tools available for authors

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T112 [P] Add comprehensive error handling across all API routes
- [ ] T113 [P] Add rate limiting middleware for AI endpoints in physical-ai-textbook/backend/src/api/middleware/rate_limit.py
- [ ] T114 [P] Add logging configuration in physical-ai-textbook/backend/src/core/logging.py
- [ ] T115 [P] Create GitHub Actions CI workflow in physical-ai-textbook/.github/workflows/ci.yml
- [ ] T116 [P] Create GitHub Actions deploy workflow in physical-ai-textbook/.github/workflows/deploy.yml
- [ ] T117 Run quickstart.md validation - verify local setup works
- [ ] T118 Run full test suite and verify >80% backend coverage
- [ ] T119 Performance testing for 100 concurrent users
- [ ] T120 Security review: CORS, auth, input validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational
- **US2 (Phase 4)**: Depends on Foundational, benefits from US1 content
- **US3 (Phase 5)**: Depends on Foundational
- **US4 (Phase 6)**: Depends on Foundational AND US3 (needs user profiles)
- **US5 (Phase 7)**: Depends on Foundational, independent of other stories
- **US6 (Phase 8)**: No dependencies on other stories
- **Polish (Phase 9)**: After all desired stories complete

### User Story Dependencies

```
Foundational (Phase 2)
        │
        ├──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
      US1 (P1)      US2 (P1)       US3 (P2)      US5 (P3)
   (Textbook)     (Chatbot)      (Auth)       (Translation)
        │                            │
        │                            ▼
        │                        US4 (P3)
        │                    (Personalization)
        │
        └──────────────────────────────────────────►  US6 (P4)
                                                   (Content Tools)
```

### Parallel Opportunities

**Phase 1 (Setup)**: T002-T010 can all run in parallel
**Phase 2 (Foundation)**: T015-T016, T019-T024 can run in parallel after T011-T014
**User Stories**: US1, US2, US3, US5 can all run in parallel after Phase 2
**Within Stories**: All [P] tasks can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# After T011-T014 complete, launch in parallel:
Task: "Create dependency injection utilities in physical-ai-textbook/backend/src/api/deps.py"
Task: "Create Pydantic base schemas in physical-ai-textbook/backend/src/api/schemas/base.py"
Task: "Create error handling middleware in physical-ai-textbook/backend/src/api/middleware/errors.py"
Task: "Create root layout with font loading in physical-ai-textbook/frontend/src/app/layout.tsx"
Task: "Create API client service in physical-ai-textbook/frontend/src/services/api.ts"
Task: "Configure pytest with async support in physical-ai-textbook/backend/tests/conftest.py"
Task: "Configure Jest for frontend tests in physical-ai-textbook/frontend/jest.config.js"
```

---

## Parallel Example: User Story 1

```bash
# Launch all US1 tests in parallel:
Task: "Integration test for content listing in physical-ai-textbook/backend/tests/integration/test_content.py"
Task: "Component tests for ChapterContent in physical-ai-textbook/frontend/tests/components/ChapterContent.test.tsx"

# Launch all US1 components in parallel:
Task: "Create TableOfContents component in physical-ai-textbook/frontend/src/components/TableOfContents.tsx"
Task: "Create CodeBlock component with syntax highlighting in physical-ai-textbook/frontend/src/components/CodeBlock.tsx"
Task: "Create ChapterContent component with MDX rendering in physical-ai-textbook/frontend/src/components/ChapterContent.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1 (Textbook Access)
4. Complete Phase 4: User Story 2 (Chatbot)
5. **STOP and VALIDATE**: Test both stories work independently
6. Deploy to GitHub Pages + Fly.io

### Suggested MVP Scope

Given the 6-hour development window (C-003), the MVP should include:
- **US1 (P1)**: Interactive Textbook Access (core value)
- **US2 (P1)**: AI-Powered Q&A Assistant (differentiation)

**Tasks for MVP**: T001-T061 (61 tasks)
**Deferred to future**: US3-US6 (authentication, personalization, translation, content tools)

### Incremental Delivery After MVP

1. Add US3 (Auth) → Enable user persistence
2. Add US4 (Personalization) → Adaptive content
3. Add US5 (Translation) → Urdu accessibility
4. Add US6 (Content Tools) → Author productivity

---

## Task Summary

| Phase | User Story | Task Count | Parallel Opportunities |
|-------|-----------|------------|----------------------|
| Phase 1 | Setup | 10 | 9 parallelizable |
| Phase 2 | Foundational | 14 | 10 parallelizable |
| Phase 3 | US1 - Textbook | 17 | 10 parallelizable |
| Phase 4 | US2 - Chatbot | 20 | 11 parallelizable |
| Phase 5 | US3 - Auth | 21 | 11 parallelizable |
| Phase 6 | US4 - Personalization | 12 | 4 parallelizable |
| Phase 7 | US5 - Translation | 13 | 4 parallelizable |
| Phase 8 | US6 - Content Tools | 4 | 3 parallelizable |
| Phase 9 | Polish | 9 | 6 parallelizable |
| **Total** | | **120** | **68 parallelizable** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach per constitution)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP focus: US1 + US2 only for initial 6-hour window
