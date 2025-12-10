# Data Model

**Feature**: Physical AI & Humanoid Robotics Textbook Platform
**Date**: 2025-12-09
**Database**: Neon Serverless Postgres (PostgreSQL 14+)

## Overview

This document defines the database schema for user data, authentication, profiles, conversations, and cached AI-generated content. The schema supports user authentication, learning profiles, chatbot conversations, personalized content, and translation caching.

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────────┐       ┌──────────────────┐
│    User     │1────N│  Conversation    │1────N│     Message      │
│             │       │                  │       │                  │
│ - id (PK)   │       │ - id (PK)        │       │ - id (PK)        │
│ - email     │       │ - user_id (FK)   │       │ - conversation_id│
│ - password  │       │ - created_at     │       │ - role           │
│ - name      │       │ - updated_at     │       │ - content        │
│ - created_at│       │ - title          │       │ - context_refs   │
└─────────────┘       └──────────────────┘       │ - created_at     │
       │1                                         └──────────────────┘
       │
       │
       │N
┌─────────────────────────┐
│     UserProfile         │
│                         │
│ - id (PK)               │
│ - user_id (FK unique)   │
│ - sw_experience         │
│ - hw_experience         │
│ - interests (JSONB)     │
│ - difficulty_preference │
│ - completed_at          │
│ - updated_at            │
└─────────────────────────┘


┌──────────────────────────┐
│   PersonalizedContent    │
│                          │
│ - id (PK)                │
│ - user_id (FK)           │
│ - chapter_slug           │
│ - adapted_content (TEXT) │
│ - adaptation_metadata    │
│ - created_at             │
│ - expires_at             │
└──────────────────────────┘


┌──────────────────────────┐
│   TranslationCache       │
│                          │
│ - id (PK)                │
│ - chapter_slug           │
│ - target_language        │
│ - translated_content     │
│ - source_hash            │
│ - created_at             │
│ - updated_at             │
└──────────────────────────┘
```

---

## Entity Definitions

### 1. User

Represents an authenticated user (learner or content author).

**Table**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique user identifier |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | User email address (used for login) |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt-hashed password |
| `name` | VARCHAR(255) | NOT NULL | User's display name |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last account update timestamp |

**Indexes**:
- `idx_users_email` on `email` (unique, for login lookups)

**Validation Rules**:
- Email must match RFC 5322 email format
- Password must be at least 8 characters (validated before hashing)
- Name must be 1-255 characters

**Relationships**:
- One-to-one with `UserProfile`
- One-to-many with `Conversation`
- One-to-many with `PersonalizedContent`

---

### 2. UserProfile

Stores user background information for personalized learning experiences.

**Table**: `user_profiles`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique profile identifier |
| `user_id` | UUID | NOT NULL, UNIQUE, FOREIGN KEY → users(id) ON DELETE CASCADE | Associated user |
| `sw_experience` | VARCHAR(20) | NOT NULL | Software experience: 'beginner', 'intermediate', 'advanced' |
| `hw_experience` | VARCHAR(20) | NOT NULL | Hardware experience: 'beginner', 'intermediate', 'advanced' |
| `interests` | JSONB | NOT NULL, DEFAULT '[]' | List of learning interests (e.g., ["ros2", "manipulation", "vslam"]) |
| `difficulty_preference` | VARCHAR(20) | NOT NULL, DEFAULT 'balanced' | Preferred difficulty: 'gentle', 'balanced', 'challenging' |
| `completed_at` | TIMESTAMP | NULL | When profile questionnaire was completed (NULL if incomplete) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Profile creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last profile update timestamp |

**Indexes**:
- `idx_user_profiles_user_id` on `user_id` (unique, for user → profile lookup)

**Validation Rules**:
- `sw_experience` ENUM: 'beginner', 'intermediate', 'advanced'
- `hw_experience` ENUM: 'beginner', 'intermediate', 'advanced'
- `difficulty_preference` ENUM: 'gentle', 'balanced', 'challenging'
- `interests` must be valid JSON array of strings

**JSONB Structure for `interests`**:
```json
["ros2", "manipulation", "perception", "navigation", "vslam", "isaac_sim"]
```

**Relationships**:
- Many-to-one with `User` (belongs to one user)

---

### 3. Conversation

Represents a chatbot conversation session.

**Table**: `conversations`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique conversation identifier |
| `user_id` | UUID | NULL, FOREIGN KEY → users(id) ON DELETE CASCADE | Associated user (NULL for anonymous users) |
| `title` | VARCHAR(255) | NULL | Auto-generated conversation title (from first message) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Conversation start timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message timestamp |

**Indexes**:
- `idx_conversations_user_id` on `user_id` (for user conversation history)
- `idx_conversations_updated_at` on `updated_at` (for recent conversations)

**Validation Rules**:
- Title generated from first 50 characters of first user message

**Relationships**:
- Many-to-one with `User` (belongs to one user, optional)
- One-to-many with `Message`

---

### 4. Message

Represents individual messages within a conversation (user queries and assistant responses).

**Table**: `messages`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique message identifier |
| `conversation_id` | UUID | NOT NULL, FOREIGN KEY → conversations(id) ON DELETE CASCADE | Parent conversation |
| `role` | VARCHAR(20) | NOT NULL | Message role: 'user' or 'assistant' |
| `content` | TEXT | NOT NULL | Message text content |
| `context_refs` | JSONB | NULL | References to textbook sections used (for assistant messages) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message creation timestamp |

**Indexes**:
- `idx_messages_conversation_id` on `conversation_id` (for conversation retrieval)
- `idx_messages_created_at` on `created_at` (for chronological ordering)

**Validation Rules**:
- `role` ENUM: 'user', 'assistant'
- `content` must be non-empty (1-10,000 characters)

**JSONB Structure for `context_refs`**:
```json
[
  {
    "chapter_slug": "module2-ros2-nodes",
    "section": "Creating a Publisher",
    "relevance_score": 0.87
  },
  {
    "chapter_slug": "module2-ros2-topics",
    "section": "Topic Communication",
    "relevance_score": 0.82
  }
]
```

**Relationships**:
- Many-to-one with `Conversation`

---

### 5. PersonalizedContent

Caches personalized chapter content for users to avoid redundant AI generation.

**Table**: `personalized_content`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique cache entry identifier |
| `user_id` | UUID | NOT NULL, FOREIGN KEY → users(id) ON DELETE CASCADE | User who requested personalization |
| `chapter_slug` | VARCHAR(255) | NOT NULL | Chapter identifier (e.g., "module2-ros2-nodes") |
| `adapted_content` | TEXT | NOT NULL | Personalized Markdown content |
| `adaptation_metadata` | JSONB | NOT NULL | Metadata about adaptation (profile used, sections modified) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Cache creation timestamp |
| `expires_at` | TIMESTAMP | NOT NULL | Expiration timestamp (7 days from creation) |

**Indexes**:
- `idx_personalized_user_chapter` on (`user_id`, `chapter_slug`) (unique composite, for cache lookup)
- `idx_personalized_expires_at` on `expires_at` (for cleanup job)

**Validation Rules**:
- `chapter_slug` must match existing chapter in Docusaurus content
- `expires_at` defaults to `created_at + 7 days`

**JSONB Structure for `adaptation_metadata`**:
```json
{
  "profile_snapshot": {
    "sw_experience": "advanced",
    "hw_experience": "beginner",
    "difficulty_preference": "balanced"
  },
  "sections_modified": ["Hardware Setup", "Serial Communication"],
  "modification_summary": "Simplified software concepts, expanded hardware explanations",
  "token_usage": 3420
}
```

**Relationships**:
- Many-to-one with `User`

**Cleanup Strategy**:
- Scheduled job runs daily to delete entries where `expires_at < NOW()`

---

### 6. TranslationCache

Caches translated chapter content to avoid redundant AI translation calls.

**Table**: `translation_cache`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique cache entry identifier |
| `chapter_slug` | VARCHAR(255) | NOT NULL | Chapter identifier |
| `target_language` | VARCHAR(10) | NOT NULL | Target language code (e.g., "ur" for Urdu) |
| `translated_content` | TEXT | NOT NULL | Translated Markdown content (code blocks preserved in English) |
| `source_hash` | VARCHAR(64) | NOT NULL | SHA-256 hash of source content (for invalidation detection) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Cache creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last cache update timestamp |

**Indexes**:
- `idx_translation_slug_lang` on (`chapter_slug`, `target_language`) (unique composite, for cache lookup)

**Validation Rules**:
- `target_language` must be ISO 639-1 language code
- `source_hash` is SHA-256 hex digest (64 characters)

**Cache Invalidation**:
- When chapter source content changes, recompute `source_hash`
- If cached `source_hash` doesn't match current, regenerate translation

**Relationships**:
- None (global cache, not user-specific)

---

## Database Migrations Strategy

Using **Alembic** for schema migrations:

1. Initial migration creates all tables
2. Subsequent migrations for schema changes (add columns, indexes, etc.)
3. Rollback support for safe deployment
4. Version-controlled migration scripts in `backend/src/db/migrations/versions/`

**Migration Workflow**:
```bash
# Generate new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Data Access Patterns

### High-Frequency Queries (Optimize with Indexes)

1. **User Login**: `SELECT * FROM users WHERE email = ?`
   - Index: `idx_users_email`

2. **Load User Profile**: `SELECT * FROM user_profiles WHERE user_id = ?`
   - Index: `idx_user_profiles_user_id`

3. **Fetch Conversation History**: `SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC LIMIT 20`
   - Index: `idx_conversations_user_id`, `idx_conversations_updated_at`

4. **Load Conversation Messages**: `SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC`
   - Index: `idx_messages_conversation_id`, `idx_messages_created_at`

5. **Check Personalized Content Cache**: `SELECT * FROM personalized_content WHERE user_id = ? AND chapter_slug = ? AND expires_at > NOW()`
   - Index: `idx_personalized_user_chapter`

6. **Check Translation Cache**: `SELECT * FROM translation_cache WHERE chapter_slug = ? AND target_language = ?`
   - Index: `idx_translation_slug_lang`

### Write Patterns

1. **Create User + Profile**: Transaction with two inserts (user, profile)
2. **Save Message**: Insert into `messages`, update `conversations.updated_at`
3. **Cache Personalization**: Insert or update (upsert) `personalized_content`
4. **Cache Translation**: Insert or update (upsert) `translation_cache`

---

## Storage Estimates

**Assumptions**:
- 1,000 users
- 50 conversations per user (lifetime)
- 10 messages per conversation
- 10% of users request personalization (5 chapters each)
- 15 chapters with Urdu translations

| Entity | Row Count | Avg Row Size | Total Size |
|--------|-----------|--------------|------------|
| `users` | 1,000 | 0.5 KB | 0.5 MB |
| `user_profiles` | 1,000 | 1 KB | 1 MB |
| `conversations` | 50,000 | 0.3 KB | 15 MB |
| `messages` | 500,000 | 0.5 KB | 250 MB |
| `personalized_content` | 500 | 10 KB | 5 MB |
| `translation_cache` | 15 | 20 KB | 0.3 MB |
| **Total** | | | **~272 MB** |

**Neon Free Tier**: 512 MB → Sufficient headroom for growth

---

## Security & Privacy Considerations

1. **Password Storage**: Bcrypt hashing with salt (never store plaintext)
2. **Sensitive Data**: Email is PII; comply with GDPR-style data deletion requests
3. **Cascade Deletes**: User deletion cascades to profiles, conversations, messages, personalized content
4. **Access Control**: API validates `user_id` in JWT matches resource ownership
5. **Anonymous Users**: Conversations can exist without `user_id` (guest mode), but not persisted long-term

---

## Backup & Recovery

**Neon Features**:
- **Point-in-Time Recovery (PITR)**: Restore to any point within retention window
- **Automated Backups**: Daily snapshots
- **Branch Isolation**: Separate dev/staging/production databases

**Manual Export**:
- Periodic `pg_dump` exports for critical tables
- Store exports in secure cloud storage (encrypted)

---

## Performance Optimizations

1. **Connection Pooling**: SQLAlchemy with `pool_size=20`, `max_overflow=10`
2. **Prepared Statements**: SQLAlchemy ORM uses prepared statements by default
3. **JSONB Indexing**: Consider GIN indexes on `interests` if filtering by interest becomes common
4. **Partitioning**: If `messages` table grows beyond 10M rows, partition by `created_at` (monthly)
5. **Archival**: Move conversations older than 1 year to cold storage

---

## Sample SQL Queries

### Create User with Profile (Transaction)
```sql
BEGIN;

INSERT INTO users (email, password_hash, name)
VALUES ('student@example.com', '$2b$12$...', 'Alice')
RETURNING id INTO user_id;

INSERT INTO user_profiles (user_id, sw_experience, hw_experience, interests, difficulty_preference, completed_at)
VALUES (user_id, 'intermediate', 'beginner', '["ros2", "manipulation"]', 'balanced', NOW());

COMMIT;
```

### Fetch Recent Conversations with Message Count
```sql
SELECT
  c.id,
  c.title,
  c.updated_at,
  COUNT(m.id) AS message_count
FROM conversations c
LEFT JOIN messages m ON m.conversation_id = c.id
WHERE c.user_id = '123e4567-e89b-12d3-a456-426614174000'
GROUP BY c.id
ORDER BY c.updated_at DESC
LIMIT 10;
```

### Check and Retrieve Personalized Content
```sql
SELECT adapted_content, adaptation_metadata
FROM personalized_content
WHERE user_id = '123e4567-e89b-12d3-a456-426614174000'
  AND chapter_slug = 'module2-ros2-nodes'
  AND expires_at > NOW();
```

### Invalidate Expired Personalized Content (Cleanup Job)
```sql
DELETE FROM personalized_content
WHERE expires_at < NOW();
```

---

## SQLAlchemy Model Mapping

**Example** (User model):
```python
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    personalized_content = relationship("PersonalizedContent", back_populates="user", cascade="all, delete-orphan")
```

---

## Next Steps

1. Implement SQLAlchemy models in `backend/src/models/`
2. Create Alembic initial migration
3. Define Pydantic schemas for API request/response validation
4. Generate OpenAPI contract with model definitions
