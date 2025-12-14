"""
Multi-provider AI adapter - supports Gemini, Claude, OpenAI
"""
import os
from typing import List, Dict, Optional
from enum import Enum


class AIProvider(Enum):
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class UnifiedAIClient:
    """
    Unified interface for multiple AI providers.
    Automatically selects provider based on environment variables.
    """

    def __init__(self, provider: Optional[str] = None):
        self.provider_name = provider or os.getenv("AI_PROVIDER", "gemini")
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate client based on provider."""
        if self.provider_name == "gemini":
            try:
                import google.generativeai as genai
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY not found")
                genai.configure(api_key=api_key)
                self.client = genai
                self.model_name = "gemini-1.5-flash"  # Fast and free
                print(f"✅ Initialized Gemini AI provider")
            except ImportError:
                raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")

        elif self.provider_name == "anthropic":
            try:
                from anthropic import Anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY not found")
                self.client = Anthropic(api_key=api_key)
                self.model_name = "claude-3-haiku-20240307"  # Fast and affordable
                print(f"✅ Initialized Anthropic AI provider")
            except ImportError:
                raise ImportError("anthropic not installed. Run: pip install anthropic")

        elif self.provider_name == "openai":
            try:
                from openai import AsyncOpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY not found")
                self.client = AsyncOpenAI(api_key=api_key)
                self.model_name = "gpt-4o-mini"
                print(f"✅ Initialized OpenAI AI provider")
            except ImportError:
                raise ImportError("openai not installed. Run: pip install openai")

        else:
            raise ValueError(f"Unknown AI provider: {self.provider_name}")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        Unified chat interface across all providers.

        Args:
            messages: List of {"role": "user/assistant/system", "content": "..."}
            temperature: Creativity (0-1)
            max_tokens: Max response length

        Returns:
            Response text
        """
        if self.provider_name == "gemini":
            return await self._gemini_chat(messages, temperature, max_tokens)
        elif self.provider_name == "anthropic":
            return await self._anthropic_chat(messages, temperature, max_tokens)
        elif self.provider_name == "openai":
            return await self._openai_chat(messages, temperature, max_tokens)

    async def _gemini_chat(self, messages: List[Dict], temp: float, max_tokens: int) -> str:
        """Gemini-specific chat."""
        # Convert messages to Gemini format
        model = self.client.GenerativeModel(self.model_name)

        # Gemini handles system messages differently
        system_message = None
        chat_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                # Gemini uses 'user' and 'model' instead of 'assistant'
                role = "model" if msg["role"] == "assistant" else "user"
                chat_messages.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

        # Start chat
        if system_message:
            # Prepend system message to first user message
            if chat_messages and chat_messages[0]["role"] == "user":
                chat_messages[0]["parts"][0] = f"{system_message}\n\n{chat_messages[0]['parts'][0]}"

        # Use generate_content for simpler single-turn
        if len(chat_messages) == 1:
            response = model.generate_content(
                chat_messages[0]["parts"][0],
                generation_config={
                    "temperature": temp,
                    "max_output_tokens": max_tokens,
                }
            )
            return response.text

        # Multi-turn chat
        chat = model.start_chat(history=chat_messages[:-1])
        response = chat.send_message(
            chat_messages[-1]["parts"][0],
            generation_config={
                "temperature": temp,
                "max_output_tokens": max_tokens,
            }
        )
        return response.text

    async def _anthropic_chat(self, messages: List[Dict], temp: float, max_tokens: int) -> str:
        """Anthropic-specific chat."""
        # Extract system message
        system_msg = None
        chat_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                chat_messages.append(msg)

        # Call Claude
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temp,
            system=system_msg,
            messages=chat_messages
        )

        return response.content[0].text

    async def _openai_chat(self, messages: List[Dict], temp: float, max_tokens: int) -> str:
        """OpenAI-specific chat."""
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temp,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    async def embed(self, text: str) -> List[float]:
        """
        Generate embeddings for text.

        Returns:
            List of floats (embedding vector)
        """
        if self.provider_name == "gemini":
            return await self._gemini_embed(text)
        elif self.provider_name == "anthropic":
            # Anthropic doesn't have embeddings - use Cohere instead
            return await self._cohere_embed(text)
        elif self.provider_name == "openai":
            return await self._openai_embed(text)

    async def _gemini_embed(self, text: str) -> List[float]:
        """Gemini embeddings."""
        result = self.client.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']

    async def _cohere_embed(self, text: str) -> List[float]:
        """Cohere embeddings (backup for Anthropic)."""
        try:
            import cohere
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                raise ValueError("COHERE_API_KEY required for embeddings with Anthropic")

            co = cohere.Client(api_key)
            response = co.embed(
                texts=[text],
                model="embed-english-v3.0",
                input_type="search_document"
            )
            return response.embeddings[0]

        except ImportError:
            raise ImportError("cohere not installed. Run: pip install cohere")

    async def _openai_embed(self, text: str) -> List[float]:
        """OpenAI embeddings."""
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def get_embedding_dim(self) -> int:
        """Get embedding dimension for current provider."""
        if self.provider_name == "gemini":
            return 768  # Gemini embedding-001
        elif self.provider_name == "anthropic":
            return 1024  # Cohere embed-english-v3.0
        elif self.provider_name == "openai":
            return 1536  # text-embedding-3-small
