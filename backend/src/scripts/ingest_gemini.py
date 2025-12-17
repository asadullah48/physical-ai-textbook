import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def ingest_data():
    sample_text = '''
# Physical AI Introduction
Physical AI (PAI) refers to AI systems that perceive, reason, and act in the physical world.

## Forward Kinematics
FK calculates end-effector position from joint angles.
For 2-link arm: x = L1*cos(θ1) + L2*cos(θ1+θ2)

## ROS 2
ROS 2 uses DDS for real-time communication. Key concepts: Nodes, Topics, Services.

## VLA Models
Vision-Language-Action models combine CV, NLP, and robot control (RT-1, RT-2, PaLM-E).
'''
    
    with open("temp_knowledge.md", "w") as f:
        f.write(sample_text)
    
    loader = TextLoader("temp_knowledge.md")
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    print("Creating Vector DB with Gemini...")
    db = Chroma.from_documents(texts, embeddings, persist_directory="./db")
    print("✅ Done!")
    os.remove("temp_knowledge.md")

if __name__ == "__main__":
    ingest_data()
