"""
One-time script to initialize and index all textbook content.
Run this after setting up the backend to populate the RAG system.
"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.rag.content_processor import ContentChunker
from src.rag.rag_engine import RAGEngine


async def main():
    """
    Initialize RAG system with textbook content.
    """
    print("🚀 Initializing Physical AI Textbook RAG System...")

    # Load environment
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ ERROR: OPENAI_API_KEY not found in environment")
        print("   Please copy .env.example to .env and add your API key")
        sys.exit(1)

    print("✅ OpenAI API key found")

    # Initialize RAG engine
    rag_engine = RAGEngine(
        openai_api_key=openai_key,
        qdrant_url=":memory:",  # In-memory for local development
        collection_name="physical_ai_textbook"
    )

    print("✅ RAG engine initialized")

    # Initialize collection
    await rag_engine.initialize_collection()
    print("✅ Qdrant collection created")

    # Load content
    content_dir = Path(__file__).parent / "content"

    if not content_dir.exists():
        content_dir = Path(__file__).parent.parent / "content"

    if not content_dir.exists():
        print(f"❌ ERROR: Content directory not found at {content_dir}")
        sys.exit(1)

    print(f"📂 Loading content from: {content_dir}")

    # Chunk content
    chunker = ContentChunker(max_tokens=512, overlap_tokens=50)

    try:
        chunks = chunker.load_modules(str(content_dir))
        print(f"✅ Loaded {len(chunks)} chunks from textbook")

        # Show sample
        if chunks:
            sample = chunks[0]
            print(f"\n📝 Sample chunk:")
            print(f"   Module: {sample['metadata']['module_title']}")
            print(f"   Chapter: {sample['metadata']['chapter_title']}")
            print(f"   Section: {sample['metadata']['section_title']}")
            print(f"   Tokens: {sample['metadata']['token_count']}")
            print(f"   Content preview: {sample['content'][:150]}...")

    except Exception as e:
        print(f"❌ ERROR loading content: {e}")
        sys.exit(1)

    # Index chunks
    print(f"\n🔄 Indexing {len(chunks)} chunks into Qdrant...")
    print("   This will take a few minutes (generating embeddings)...")

    try:
        await rag_engine.index_chunks(chunks)
        print("✅ All chunks indexed successfully!")

    except Exception as e:
        print(f"❌ ERROR during indexing: {e}")
        sys.exit(1)

    # Test retrieval
    print("\n🧪 Testing retrieval...")

    test_query = "What is Physical AI?"
    results = await rag_engine.retrieve(test_query, top_k=3)

    print(f"\nQuery: '{test_query}'")
    print(f"Found {len(results)} relevant chunks:\n")

    for i, result in enumerate(results, 1):
        print(f"{i}. [{result['metadata']['chapter_title']}]")
        print(f"   Score: {result['score']:.3f}")
        print(f"   Preview: {result['content'][:100]}...\n")

    # Test answer generation
    print("🤖 Testing answer generation...")

    answer_result = await rag_engine.generate_answer(
        query=test_query,
        context_chunks=results,
        mode="helpful"
    )

    print(f"\nGenerated Answer:")
    print(answer_result['answer'])
    print(f"\nSources: {len(answer_result['sources'])}")

    print("\n" + "="*60)
    print("✅ INITIALIZATION COMPLETE!")
    print("="*60)
    print("\nYour RAG system is ready to use.")
    print("Start the backend with: python -m uvicorn src.api.main_new:app --reload")


if __name__ == "__main__":
    asyncio.run(main())
