from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.services.rag_service import rag_service

app = FastAPI(title="Physical AI Textbook API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/v1/modules")
async def list_modules():
    return [
        {"slug": "01-physical-ai-intro", "title": "Introduction to Physical AI", "icon": "🤖", "description": "Fundamentals of Physical AI, its applications in robotics, and key concepts.", "chapter_count": 2},
        {"slug": "02-ros2", "title": "ROS 2 Fundamentals", "icon": "🔧", "description": "Robot Operating System 2 architecture, nodes, topics, and services.", "chapter_count": 2},
        {"slug": "03-simulation", "title": "Simulation Environments", "icon": "🎮", "description": "Using Gazebo, Isaac Sim for testing robotics applications.", "chapter_count": 1},
        {"slug": "04-isaac", "title": "NVIDIA Isaac Platform", "icon": "🎯", "description": "Leveraging NVIDIA Isaac for robot development.", "chapter_count": 1},
        {"slug": "05-vla", "title": "Vision-Language-Action Systems", "icon": "🧠", "description": "Advanced multimodal AI systems for intelligent behavior.", "chapter_count": 1}
    ]

from src.services.agent_service import agent_service

@app.post("/api/v1/chat")
async def chat(request: dict):
    message = request.get("message", "")
    if not message:
        return {"response": "Please provide a question.", "sources": [], "steps": []}

    # Agent only takes message (no history parameter)
    result = agent_service.invoke(message)
    return result
