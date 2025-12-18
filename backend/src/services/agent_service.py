from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

class AgentService:
    def invoke(self, message: str):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=f"You are a Physical AI Professor. Answer this question: {message}"
            )
            return {
                "response": response.text,
                "steps": ["Gemini 2.0 Flash"],
                "sources": []
            }
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "steps": [],
                "sources": []
            }

agent_service = AgentService()
