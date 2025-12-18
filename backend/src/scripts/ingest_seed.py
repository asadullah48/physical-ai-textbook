import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def ingest_data():
    # Define content directory (relative to this script: ../../content)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    content_dir = os.path.join(base_dir, "content")
    
    if not os.path.exists(content_dir):
        print(f"❌ Content directory not found at {content_dir}")
        return

    documents = []
    
    # Iterate over all .md files in the content directory
    print(f"📂 Scanning for content in {content_dir}...")
    for filename in os.listdir(content_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(content_dir, filename)
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                # Add source metadata just in case (TextLoader usually does this)
                for doc in docs:
                    doc.metadata["source"] = filename
                documents.extend(docs)
                print(f"  - Loaded {filename}")
            except Exception as e:
                print(f"  ❌ Failed to load {filename}: {e}")

    if not documents:
        print("⚠️ No documents found to ingest.")
        return

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings()
    
    persist_dir = os.path.join(base_dir, "db")
    print(f"Using DB directory: {persist_dir}")
    
    print("Creating Vector DB...")
    db = Chroma.from_documents(texts, embeddings, persist_directory=persist_dir)
    db.persist()
    print(f"✅ Ingestion Complete. {len(texts)} chunks stored in {persist_dir}")

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment.")
    else:
        ingest_data()
