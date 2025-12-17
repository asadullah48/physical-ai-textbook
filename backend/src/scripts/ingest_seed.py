import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def ingest_data():
    # TEMPORARY: Ingesting a dummy file for testing. 
    # In production/next-step, we will scan the 'content' directory of the textbook.
    
    sample_text = """
    # Physical AI Introduction
    Physical AI (PAI) refers to AI systems that perceive, reason, and act in the physical world.
    Unlike Generative AI which outputs text/images, Physical AI outputs motor commands and forces.
    
    ## Embodiment
    Embodiment is the hypothesis that intelligence emerges from the interaction of an agent with an environment.
    
    ## ROS 2
    ROS 2 is the standard middleware for robotics. It uses a DDS (Data Distribution Service) for real-time communication.
    """
    
    # Save temp file
    with open("temp_knowledge.md", "w") as f:
        f.write(sample_text)
        
    loader = TextLoader("temp_knowledge.md")
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings()
    
    print("Creating Vector DB...")
    db = Chroma.from_documents(texts, embeddings, persist_directory="./db")
    db.persist()
    print("✅ Ingestion Complete. DB created at ./db")
    
    # Cleanup
    os.remove("temp_knowledge.md")

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment.")
    else:
        ingest_data()
