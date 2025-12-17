import sys
import os

# Add backend to path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from src.services.agent_service import agent_service
from dotenv import load_dotenv

# Load env from backend root
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

def test_agent():
    print("🤖 Initializing Agent Test...")
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found. Please set it in backend/.env")
        return

    # specific query that requires math, not just retrieval
    query = "Calculate the torque if a 5kg robot arm is held at 90 degrees with length 2m."
    print(f"\n❓ Query: {query}")
    print("⏳ Agent is thinking...")
    
    try:
        result = agent_service.invoke(query)
        
        print("\n📝 Thinking Steps:")
        for step in result['steps']:
            print(f" - {step}")
            
        print("\n✅ Final Response:")
        print(result['response'])
        
    except Exception as e:
        print(f"\n❌ Execution Failed: {e}")

if __name__ == "__main__":
    test_agent()
