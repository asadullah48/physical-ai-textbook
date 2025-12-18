import google.generativeai as genai
import os
from src.services.rag_service import rag_service

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class AgentService:
    def invoke(self, message: str):
        try:
            # First try RAG service for textbook-specific knowledge
            rag_result = rag_service.query(message)
            
            # If RAG found relevant content (not just the initialization message)
            if rag_result.get("sources") and len(rag_result["sources"]) > 0:
                return {
                    "response": rag_result["response"],
                    "steps": ["Knowledge Base Retrieval", "Gemini 1.5 Flash"],
                    "sources": rag_result["sources"]
                }

            # Fallback to general Gemini 1.5 if no specific context found
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(
                f"You are a Physical AI Professor. Answer this question: {message}"
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
