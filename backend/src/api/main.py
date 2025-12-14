"""
Physical AI Textbook API - Production-grade backend.
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our engines
from ..rag.content_processor import ContentChunker
from ..rag.rag_engine import RAGEngine
from ..learning_engine.socratic_tutor import SocraticTutor
from ..learning_engine.embodiment_mode import RobotPersona

# Initialize FastAPI
app = FastAPI(
    title="Physical AI Textbook API",
    version="2.0.0",
    description="Production RAG-powered learning platform"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://asadullahshafique-devunity.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances (initialized on startup)
rag_engine: Optional[RAGEngine] = None
socratic_tutor: Optional[SocraticTutor] = None
robot_persona: Optional[RobotPersona] = None
modules_data: Dict = {}


# ============================================================================
# Request/Response Models
# ============================================================================

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []
    mode: str = "helpful"  # "helpful", "socratic", "embodiment"
    module_filter: Optional[str] = None
    reading_context: Optional[Dict] = None


class ChatResponse(BaseModel):
    response: str
    sources: List[Dict]
    mode: str
    teaching_move: Optional[str] = None
    robot_state: Optional[Dict] = None


class Module(BaseModel):
    slug: str
    title: str
    icon: str
    description: str
    chapter_count: int
    difficulty: Optional[str] = None


class Chapter(BaseModel):
    id: str
    title: str
    content: str
    metadata: Dict


class InitRequest(BaseModel):
    force_reindex: bool = False


# ============================================================================
# Startup & Initialization
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Initialize all AI services on startup.
    """
    global rag_engine, socratic_tutor, robot_persona, modules_data

    # Get API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("WARNING: OPENAI_API_KEY not set. AI features will not work.")
        return

    # Initialize engines
    rag_engine = RAGEngine(
        openai_api_key=openai_key,
        qdrant_url=":memory:",  # Use in-memory for demo; switch to URL for production
        collection_name="physical_ai_textbook"
    )

    socratic_tutor = SocraticTutor(openai_api_key=openai_key)
    robot_persona = RobotPersona(openai_api_key=openai_key)

    # Load modules index
    content_dir = Path(__file__).parent.parent.parent.parent / "content"
    index_path = content_dir / "modules" / "modules-index.json"

    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            modules_data = json.load(f)

    print("✅ All AI services initialized successfully")


# ============================================================================
# Content Endpoints
# ============================================================================

@app.get("/api/health")
async def health():
    """Health check."""
    return {
        "status": "healthy",
        "rag_ready": rag_engine is not None,
        "socratic_ready": socratic_tutor is not None,
        "embodiment_ready": robot_persona is not None
    }


@app.get("/api/v1/modules", response_model=List[Module])
async def list_modules():
    """
    List all available modules.
    """
    if not modules_data:
        raise HTTPException(status_code=503, detail="Modules not loaded")

    return [
        Module(
            slug=m['id'],
            title=m['title'],
            icon=m['icon'],
            description=m['description'],
            chapter_count=len(m['chapters']),
            difficulty=m.get('difficulty', 'beginner')
        )
        for m in modules_data.get('modules', [])
    ]


@app.get("/api/v1/modules/{module_id}/chapters")
async def list_chapters(module_id: str):
    """
    List chapters in a module.
    """
    for module in modules_data.get('modules', []):
        if module['id'] == module_id:
            return module['chapters']

    raise HTTPException(status_code=404, detail="Module not found")


@app.get("/api/v1/modules/{module_id}/chapters/{chapter_id}")
async def get_chapter(module_id: str, chapter_id: str):
    """
    Get chapter content.
    """
    content_dir = Path(__file__).parent.parent.parent.parent / "content"

    # Find chapter metadata
    chapter_meta = None
    for module in modules_data.get('modules', []):
        if module['id'] == module_id:
            for chapter in module['chapters']:
                if chapter['id'] == chapter_id:
                    chapter_meta = chapter
                    break

    if not chapter_meta:
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Load content
    chapter_path = content_dir / "modules" / module_id / chapter_meta['file']

    if not chapter_path.exists():
        raise HTTPException(status_code=404, detail="Chapter file not found")

    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return Chapter(
        id=chapter_id,
        title=chapter_meta['title'],
        content=content,
        metadata=chapter_meta
    )


@app.get("/api/v1/skill-graph")
async def get_skill_graph():
    """
    Get the learning skill dependency graph.
    """
    return modules_data.get('skill_graph', {})


# ============================================================================
# AI/Chat Endpoints
# ============================================================================

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - supports multiple modes.
    """
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")

    # Retrieve relevant context
    context_chunks = await rag_engine.hybrid_retrieve(
        query=request.message,
        top_k=5
    )

    if not context_chunks:
        return ChatResponse(
            response="I couldn't find relevant information in the textbook for that question. Could you try rephrasing or ask about a topic covered in the modules?",
            sources=[],
            mode=request.mode
        )

    # Route to appropriate mode
    if request.mode == "socratic":
        result = await socratic_tutor.engage(
            user_message=request.message,
            context_chunks=context_chunks,
            conversation_history=request.conversation_history,
            reading_context=request.reading_context
        )

        return ChatResponse(
            response=result['response'],
            sources=[
                {
                    'title': c['metadata']['chapter_title'],
                    'module': c['metadata']['module_title'],
                    'score': c['score']
                }
                for c in context_chunks[:3]
            ],
            mode="socratic",
            teaching_move=result.get('teaching_move')
        )

    elif request.mode == "embodiment":
        # Robot persona mode
        context_text = "\n".join([c['content'][:300] for c in context_chunks[:2]])

        robot_response = await robot_persona.respond_to_user(
            user_message=request.message,
            context=context_text,
            conversation_history=request.conversation_history
        )

        return ChatResponse(
            response=robot_response,
            sources=[],  # Robot doesn't cite sources directly
            mode="embodiment",
            robot_state=robot_persona.get_state()
        )

    else:
        # Helpful mode (default)
        result = await rag_engine.generate_answer(
            query=request.message,
            context_chunks=context_chunks,
            conversation_history=request.conversation_history,
            mode="helpful"
        )

        return ChatResponse(
            response=result['answer'],
            sources=result['sources'],
            mode="helpful"
        )


@app.post("/api/v1/embodiment/react")
async def embodiment_react(chapter_metadata: Dict):
    """
    Robot persona reacts to new chapter content.
    """
    if not robot_persona:
        raise HTTPException(status_code=503, detail="Robot persona not initialized")

    # Get chapter content
    content_dir = Path(__file__).parent.parent.parent.parent / "content"
    chapter_path = content_dir / "modules" / chapter_metadata['module_id'] / chapter_metadata['file']

    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()

    reaction = await robot_persona.react_to_content(content, chapter_metadata)

    return reaction


@app.post("/api/v1/embodiment/challenge")
async def embodiment_challenge(challenge_type: str, context: Dict):
    """
    Trigger a challenge scenario for robot persona.
    """
    if not robot_persona:
        raise HTTPException(status_code=503, detail="Robot persona not initialized")

    challenge = await robot_persona.simulate_challenge(challenge_type, context)

    return challenge


@app.get("/api/v1/embodiment/state")
async def get_robot_state():
    """
    Get current robot persona state.
    """
    if not robot_persona:
        raise HTTPException(status_code=503, detail="Robot persona not initialized")

    return robot_persona.get_state()


# ============================================================================
# Admin/Initialization Endpoints
# ============================================================================

@app.post("/api/v1/admin/initialize")
async def initialize_content(request: InitRequest, background_tasks: BackgroundTasks):
    """
    Index all textbook content into RAG system.
    """
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG engine not initialized")

    # Run indexing in background
    background_tasks.add_task(index_content_task, request.force_reindex)

    return {"status": "indexing_started", "message": "Content indexing initiated in background"}


async def index_content_task(force_reindex: bool = False):
    """
    Background task to index content.
    """
    try:
        # Initialize collection
        await rag_engine.initialize_collection()

        # Load and chunk content
        content_dir = Path(__file__).parent.parent.parent.parent / "content"
        chunker = ContentChunker(max_tokens=512)

        chunks = chunker.load_modules(str(content_dir))

        print(f"📚 Loaded {len(chunks)} chunks from textbook")

        # Index into Qdrant
        await rag_engine.index_chunks(chunks)

        print("✅ Content indexing complete")

    except Exception as e:
        print(f"❌ Indexing failed: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
