"""
Content processing and chunking for RAG pipeline.
"""
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any
import markdown
from bs4 import BeautifulSoup
import tiktoken


class ContentChunker:
    """
    Intelligently chunks textbook content for embedding.
    """

    def __init__(self, max_tokens: int = 512, overlap_tokens: int = 50):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def load_modules(self, content_dir: str) -> List[Dict[str, Any]]:
        """
        Load all textbook modules from content directory.

        Returns:
            List of module dictionaries with metadata and chunks
        """
        index_path = Path(content_dir) / "modules" / "modules-index.json"

        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)

        all_chunks = []

        for module in index_data['modules']:
            module_id = module['id']
            module_title = module['title']

            for chapter in module['chapters']:
                chapter_path = Path(content_dir) / "modules" / module_id / chapter['file']

                if chapter_path.exists():
                    with open(chapter_path, 'r', encoding='utf-8') as f:
                        markdown_content = f.read()

                    chunks = self.chunk_markdown(
                        markdown_content,
                        module_id=module_id,
                        module_title=module_title,
                        chapter_id=chapter['id'],
                        chapter_title=chapter['title']
                    )

                    all_chunks.extend(chunks)

        return all_chunks

    def chunk_markdown(
        self,
        content: str,
        module_id: str,
        module_title: str,
        chapter_id: str,
        chapter_title: str
    ) -> List[Dict[str, Any]]:
        """
        Chunk markdown content into semantic units.

        Strategy:
        1. Split by headers (preserve hierarchy)
        2. Split code blocks separately (keep intact)
        3. Split long paragraphs by token count
        """
        chunks = []

        # Parse markdown to HTML for structure
        html = markdown.markdown(content, extensions=['fenced_code', 'tables'])
        soup = BeautifulSoup(html, 'html.parser')

        # Extract sections by headers
        sections = self._extract_sections(soup)

        for section in sections:
            section_chunks = self._chunk_section(section)

            for chunk in section_chunks:
                chunks.append({
                    'content': chunk['text'],
                    'metadata': {
                        'module_id': module_id,
                        'module_title': module_title,
                        'chapter_id': chapter_id,
                        'chapter_title': chapter_title,
                        'section_title': section['title'],
                        'heading_level': section['level'],
                        'chunk_type': chunk['type'],  # 'text' or 'code'
                        'token_count': chunk['tokens']
                    }
                })

        return chunks

    def _extract_sections(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract hierarchical sections from HTML.
        """
        sections = []
        current_section = {'title': 'Introduction', 'level': 1, 'content': []}

        for element in soup.children:
            if element.name in ['h1', 'h2', 'h3', 'h4']:
                # Save previous section
                if current_section['content']:
                    sections.append(current_section)

                # Start new section
                level = int(element.name[1])
                current_section = {
                    'title': element.get_text(),
                    'level': level,
                    'content': []
                }
            else:
                current_section['content'].append(element)

        # Add last section
        if current_section['content']:
            sections.append(current_section)

        return sections

    def _chunk_section(self, section: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk a single section into token-limited pieces.
        """
        chunks = []
        current_chunk_text = f"## {section['title']}\n\n"
        current_tokens = len(self.encoding.encode(current_chunk_text))

        for element in section['content']:
            # Handle code blocks specially (keep intact)
            if element.name == 'pre':
                code_text = element.get_text()
                code_tokens = len(self.encoding.encode(code_text))

                # Save current text chunk if exists
                if current_tokens > len(self.encoding.encode(f"## {section['title']}\n\n")):
                    chunks.append({
                        'text': current_chunk_text.strip(),
                        'type': 'text',
                        'tokens': current_tokens
                    })
                    current_chunk_text = f"## {section['title']}\n\n"
                    current_tokens = len(self.encoding.encode(current_chunk_text))

                # Add code as separate chunk
                chunks.append({
                    'text': f"## {section['title']}\n\n```python\n{code_text}\n```",
                    'type': 'code',
                    'tokens': code_tokens
                })

            else:
                element_text = element.get_text() + "\n\n"
                element_tokens = len(self.encoding.encode(element_text))

                # Check if adding this would exceed limit
                if current_tokens + element_tokens > self.max_tokens:
                    # Save current chunk
                    chunks.append({
                        'text': current_chunk_text.strip(),
                        'type': 'text',
                        'tokens': current_tokens
                    })

                    # Start new chunk with overlap (keep section title)
                    current_chunk_text = f"## {section['title']}\n\n{element_text}"
                    current_tokens = len(self.encoding.encode(current_chunk_text))
                else:
                    current_chunk_text += element_text
                    current_tokens += element_tokens

        # Add final chunk
        if current_chunk_text.strip():
            chunks.append({
                'text': current_chunk_text.strip(),
                'type': 'text',
                'tokens': current_tokens
            })

        return chunks

    def extract_key_concepts(self, text: str) -> List[str]:
        """
        Extract key concepts/terms for keyword-based retrieval.
        """
        # Simple extraction: look for technical terms, acronyms
        # More sophisticated NER could be added
        concepts = []

        # Find all-caps acronyms (e.g., LIDAR, ROS, IMU)
        acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
        concepts.extend(acronyms)

        # Find camelCase or PascalCase terms (e.g., SensorArray, PhysicsSimulator)
        camel_case = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text)
        concepts.extend(camel_case)

        return list(set(concepts))
