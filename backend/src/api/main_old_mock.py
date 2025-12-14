from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/api/v1/chat")
async def chat(request: dict):
    message = request.get("message", "").lower()
    
    responses = {
        "ros": "ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It provides tools, libraries, and conventions to simplify creating complex robot behavior.",
        "physical ai": "Physical AI refers to AI systems that interact with the physical world through embodied agents like robots. It combines perception, reasoning, and action in real environments.",
        "sensor": "Sensors in robotics include LIDAR for distance measurement, cameras for vision, IMUs for orientation, and force sensors for tactile feedback.",
        "simulation": "Simulation environments like Gazebo and Isaac Sim allow testing robot behaviors in virtual environments before deploying to real hardware.",
    }
    
    response_text = "I'm an AI tutor for Physical AI. I can help you understand robotics, ROS 2, and simulation. What would you like to learn?"
    for key, value in responses.items():
        if key in message:
            response_text = value
            break
    
    return {"response": response_text, "sources": []}
