import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"✓ Available: {model.name}")

# Test simple generation
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello in 5 words")
print(f"\nTest response: {response.text}")
