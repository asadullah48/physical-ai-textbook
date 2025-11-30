import google.generativeai as genai
import json
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-flash-latest")

# Hardcoded chapters (no JSON needed)
chapters = [
    ("module0-hardware", "Hardware Requirements & Setup", "docs"),
    ("module1-ros2-basics", "ROS 2: The Robotic Nervous System", "docs/module-ros2"),
    ("module1-ros2-nodes", "ROS 2 Nodes, Topics & Services", "docs/module-ros2"),
    ("module1-ros2-python", "Bridging Python Agents to ROS", "docs/module-ros2"),
    ("module1-ros2-urdf", "URDF: Robot Description Format", "docs/module-ros2"),
    ("module2-gazebo", "Gazebo Simulation Physics", "docs/module-simulation"),
    ("module2-unity", "Unity for Human-Robot Interaction", "docs/module-simulation"),
    ("module2-sensors", "Simulating LIDAR, Cameras & IMUs", "docs/module-simulation"),
    ("module3-isaac-sim", "NVIDIA Isaac Sim & Synthetic Data", "docs/module-isaac"),
    ("module3-isaac-ros", "Isaac ROS: VSLAM & Navigation", "docs/module-isaac"),
    ("module3-nav2", "Nav2 for Bipedal Locomotion", "docs/module-isaac"),
    ("module4-vla-concepts", "Vision-Language-Action Models", "docs/module-vla"),
    ("module4-whisper", "Voice-to-Action with Whisper", "docs/module-vla"),
    ("capstone-project", "Capstone: The Autonomous Humanoid", "docs")
]

for file_id, title, folder in chapters:
    print(f"Generating: {title}")
    prompt = f"Create textbook chapter: {title}. Include overview, ROS 2 code, pitfalls, exercises."
    response = model.generate_content(prompt)
    
    with open(f"{folder}/{file_id}.md", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print(f"  ✓ Saved to {folder}/{file_id}.md")

print("Done!")
