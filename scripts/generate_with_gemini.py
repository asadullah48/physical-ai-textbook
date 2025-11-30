import google.generativeai as genai
import json
import os
import time
from pathlib import Path

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-flash-latest")

# Create directories
Path("docs").mkdir(exist_ok=True)
Path("docs/module-ros2").mkdir(exist_ok=True)
Path("docs/module-simulation").mkdir(exist_ok=True)
Path("docs/module-isaac").mkdir(exist_ok=True)
Path("docs/module-vla").mkdir(exist_ok=True)

with open("spec-kit/chapter-specs.json", "r") as f:
    specs = json.load(f)

print(f"Generating {len(specs['chapters'])} chapters...\\n")

for i, chapter in enumerate(specs["chapters"], 1):
    print(f"[{i}/{len(specs['chapters'])}] {chapter['title']}")
    
    prompt = f"Create textbook chapter: {chapter['title']}. Include overview, ROS 2/Python code, pitfalls, exercises."
    
    try:
        response = model.generate_content(prompt)
        
        # Check for empty response
        if not hasattr(response, 'text') or not response.text:
            print(f"  ✗ Empty response, creating placeholder...")
            content = f"# {chapter['title']}\\n\\n*Content generation failed. Add manually.*"
        else:
            content = response.text
        
        # Determine save path
        if "ros2" in chapter["id"]:
            path = f"docs/module-ros2/{chapter['id']}.md"
        elif "gazebo" in chapter["id"] or "unity" in chapter["id"]:
            path = f"docs/module-simulation/{chapter['id']}.md"
        elif "isaac" in chapter["id"]:
            path = f"docs/module-isaac/{chapter['id']}.md"
        elif "vla" in chapter["id"] or "whisper" in chapter["id"]:
            path = f"docs/module-vla/{chapter['id']}.md"
        else:
            path = f"docs/{chapter['id']}.md"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"  ✓ Saved: {path}")
        
        # Small delay to respect rate limits
        time.sleep(0.5)
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print(f"  → Skipping {chapter['title']}")

print("\\n🎉 Generation complete!")
