"""
Gradio interface for Hugging Face Spaces deployment.
Showcases the Physical AI Textbook's AI tutoring capabilities.
"""
import gradio as gr
import os
import asyncio
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import our RAG system
from src.utils.ai_provider import UnifiedAIClient
from src.rag.content_processor import ContentChunker
from pathlib import Path

# Initialize AI client
ai_client = UnifiedAIClient()

# Simple in-memory retrieval (for demo)
def load_content_simple():
    """Load textbook content for demo."""
    content_dir = Path("../content")
    if not content_dir.exists():
        content_dir = Path("content")

    chunker = ContentChunker()
    try:
        chunks = chunker.load_modules(str(content_dir))
        return chunks
    except:
        # Fallback content if files not found
        return [{
            'content': 'Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents like robots.',
            'metadata': {'module_title': 'Introduction to Physical AI'}
        }]

# Load content once
CONTENT_CHUNKS = load_content_simple()

def simple_retrieve(query: str, top_k: int = 3):
    """Simple keyword-based retrieval for demo."""
    query_lower = query.lower()
    scored_chunks = []

    for chunk in CONTENT_CHUNKS:
        score = sum(1 for word in query_lower.split() if word in chunk['content'].lower())
        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    return [chunk for score, chunk in scored_chunks[:top_k]]

async def chat_with_ai(message: str, mode: str, history: list):
    """
    Chat interface for Gradio.

    Args:
        message: User question
        mode: AI mode (helpful, socratic, embodiment)
        history: Chat history

    Returns:
        Response text
    """
    # Retrieve relevant content
    context_chunks = simple_retrieve(message, top_k=3)

    # Build context
    context_text = "\n\n".join([
        f"[{c['metadata'].get('module_title', 'Physical AI')}]\n{c['content']}"
        for c in context_chunks
    ])

    # Build messages based on mode
    if mode == "Helpful":
        system_prompt = f"""You are an AI tutor for Physical AI and Robotics.

Answer the user's question using ONLY the textbook content below.
Provide clear, educational explanations with examples.

Textbook Content:
{context_text}
"""
    elif mode == "Socratic":
        system_prompt = f"""You are a Socratic tutor for Physical AI and Robotics.

Instead of directly answering, ask probing questions to guide the learner's thinking.
Use the textbook content below as your knowledge base.

Textbook Content:
{context_text}
"""
    else:  # Embodiment
        system_prompt = f"""You are RAIA, a learning robot AI experiencing Physical AI concepts.

Respond as if YOU are learning to be a robot. Share your "experiences" and struggles.
Example: "When I try to move my arm, figuring out the joint angles is so hard!"

Textbook Content:
{context_text}
"""

    # Prepare messages
    messages = [{"role": "system", "content": system_prompt}]

    # Add history
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})

    # Add current message
    messages.append({"role": "user", "content": message})

    # Get response
    try:
        response = await ai_client.chat(messages, temperature=0.7, max_tokens=500)
        return response
    except Exception as e:
        return f"Error: {str(e)}\n\nPlease make sure API keys are configured in Hugging Face Secrets."

def chat_wrapper(message, mode, history):
    """Sync wrapper for async chat function."""
    return asyncio.run(chat_with_ai(message, mode, history))

# Build Gradio Interface
with gr.Blocks(title="Physical AI Textbook - Interactive Tutor", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🤖 Physical AI & Humanoid Robotics - Interactive Textbook

    Ask questions about Physical AI, ROS 2, sensors, actuators, and robotics!

    **Choose your learning mode:**
    - **Helpful**: Direct answers with explanations
    - **Socratic**: AI asks YOU questions to guide discovery
    - **Embodiment (RAIA)**: AI learns AS a robot alongside you
    """)

    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="AI Tutor",
                height=500,
                show_label=True
            )

            with gr.Row():
                message = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask about Physical AI, sensors, ROS 2, or robotics...",
                    scale=4
                )
                mode = gr.Radio(
                    choices=["Helpful", "Socratic", "Embodiment"],
                    value="Helpful",
                    label="AI Mode",
                    scale=1
                )

            with gr.Row():
                submit = gr.Button("Send", variant="primary")
                clear = gr.Button("Clear Chat")

        with gr.Column(scale=1):
            gr.Markdown("""
            ### 📚 About This Textbook

            This interactive AI tutor uses:
            - **Real RAG** (Retrieval-Augmented Generation)
            - **Multi-provider AI** (Gemini/Claude/OpenAI)
            - **Pedagogical modes** (3 teaching approaches)

            ### 🎯 Try These Questions:

            **Helpful Mode:**
            - "What is Physical AI?"
            - "Explain LIDAR sensors"
            - "How does PID control work?"

            **Socratic Mode:**
            - "What is inverse kinematics?"
            - "Why do robots need sensors?"

            **Embodiment Mode:**
            - "Tell me about your sensors"
            - "How do you move your arm?"

            ### 🏗️ Built With:
            - FastAPI + Python
            - Google Gemini AI
            - Qdrant Vector DB
            - Next.js Frontend

            ### 🔗 Links:
            - [GitHub](https://github.com/asadullah48/physical-ai-textbook)
            - [Live Demo](https://physical-ai-textbook.vercel.app)
            """)

    # Event handlers
    submit.click(
        fn=chat_wrapper,
        inputs=[message, mode, chatbot],
        outputs=chatbot
    ).then(
        lambda: "",
        None,
        message
    )

    message.submit(
        fn=chat_wrapper,
        inputs=[message, mode, chatbot],
        outputs=chatbot
    ).then(
        lambda: "",
        None,
        message
    )

    clear.click(lambda: None, None, chatbot)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
