"""
RAG (Retrieval-Augmented Generation) Engine for textbook Q&A.
"""
import os
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import hashlib


class RAGEngine:
    """
    Handles embedding generation, vector storage, and retrieval for textbook content.
    """

    def __init__(
        self,
        openai_api_key: str,
        qdrant_url: str = ":memory:",  # In-memory for simplicity, use URL for production
        collection_name: str = "textbook_content"
    ):
        self.openai_client = AsyncOpenAI(api_key=openai_api_key)
        self.qdrant_client = QdrantClient(qdrant_url)
        self.collection_name = collection_name
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dim = 1536

    async def initialize_collection(self):
        """
        Create Qdrant collection if it doesn't exist.
        """
        collections = self.qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=Distance.COSINE
                )
            )

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI.
        """
        response = await self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

    async def index_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Index content chunks into Qdrant.

        Args:
            chunks: List of {content, metadata} dicts from ContentChunker
        """
        points = []

        for idx, chunk in enumerate(chunks):
            # Generate embedding
            embedding = await self.embed_text(chunk['content'])

            # Create unique ID from content hash
            chunk_id = hashlib.md5(chunk['content'].encode()).hexdigest()

            # Create point
            point = PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    'content': chunk['content'],
                    **chunk['metadata']
                }
            )
            points.append(point)

        # Batch upsert to Qdrant
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i+batch_size]
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=batch
            )

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        module_filter: Optional[str] = None,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks for a query.

        Args:
            query: User question
            top_k: Number of chunks to retrieve
            module_filter: Optional module ID to filter results
            score_threshold: Minimum similarity score

        Returns:
            List of {content, metadata, score} dicts
        """
        # Generate query embedding
        query_embedding = await self.embed_text(query)

        # Build filter if needed
        query_filter = None
        if module_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="module_id",
                        match=MatchValue(value=module_filter)
                    )
                ]
            )

        # Search Qdrant
        search_results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=query_filter,
            score_threshold=score_threshold
        )

        # Format results
        results = []
        for hit in search_results:
            results.append({
                'content': hit.payload['content'],
                'metadata': {
                    k: v for k, v in hit.payload.items()
                    if k != 'content'
                },
                'score': hit.score
            })

        return results

    async def hybrid_retrieve(
        self,
        query: str,
        top_k: int = 5,
        semantic_weight: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval: combine semantic search with keyword matching.

        Args:
            query: User question
            top_k: Number of results
            semantic_weight: Weight for semantic vs keyword (0-1)

        Returns:
            Ranked list of chunks
        """
        # Semantic search
        semantic_results = await self.retrieve(query, top_k=top_k * 2)

        # Keyword matching (simple implementation)
        # Extract query keywords
        keywords = set(query.lower().split())

        # Score results by keyword overlap
        for result in semantic_results:
            content_lower = result['content'].lower()
            keyword_score = sum(
                1 for kw in keywords if kw in content_lower
            ) / len(keywords) if keywords else 0

            # Combine scores
            result['hybrid_score'] = (
                semantic_weight * result['score'] +
                (1 - semantic_weight) * keyword_score
            )

        # Re-rank by hybrid score
        semantic_results.sort(key=lambda x: x['hybrid_score'], reverse=True)

        return semantic_results[:top_k]

    async def generate_answer(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        mode: str = "helpful"  # "helpful" or "socratic"
    ) -> Dict[str, Any]:
        """
        Generate answer using retrieved context.

        Args:
            query: User question
            context_chunks: Retrieved chunks from retrieve()
            conversation_history: Previous messages
            mode: Response mode

        Returns:
            {answer, sources, thinking}
        """
        # Build context from chunks
        context_text = "\n\n---\n\n".join([
            f"[Source: {c['metadata']['chapter_title']}]\n{c['content']}"
            for c in context_chunks
        ])

        # Build messages
        if mode == "socratic":
            system_prompt = """You are a Socratic tutor for Physical AI and Robotics.

Instead of directly answering questions, you:
1. Ask clarifying questions to check understanding
2. Guide students to discover answers themselves
3. Only provide direct explanations when the student is genuinely stuck

Use the textbook content below as your knowledge base."""
        else:
            system_prompt = """You are an AI tutor for Physical AI and Robotics textbook.

Your role:
1. Answer questions using ONLY the textbook content provided
2. Cite specific sections when referencing material
3. If the answer isn't in the textbook, say so clearly
4. Provide code examples when relevant
5. Connect concepts to real-world applications

Always be accurate, concise, and educational."""

        messages = [
            {"role": "system", "content": f"{system_prompt}\n\n# Textbook Content:\n{context_text}"}
        ]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Last 3 exchanges

        # Add current query
        messages.append({"role": "user", "content": query})

        # Generate response
        response = await self.openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Fast and cost-effective
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        answer = response.choices[0].message.content

        # Extract sources
        sources = [
            {
                'title': c['metadata']['chapter_title'],
                'module': c['metadata']['module_title'],
                'section': c['metadata'].get('section_title', ''),
                'score': c['score']
            }
            for c in context_chunks
        ]

        return {
            'answer': answer,
            'sources': sources,
            'mode': mode
        }
