"""
Socratic Tutor - Guides learning through questions rather than direct answers.
"""
from typing import List, Dict, Optional
from openai import AsyncOpenAI


class SocraticTutor:
    """
    Implements Socratic method for teaching:
    - Asks probing questions before giving answers
    - Checks understanding through dialogue
    - Guides discovery rather than telling
    """

    def __init__(self, openai_api_key: str):
        self.client = AsyncOpenAI(api_key=openai_api_key)

    async def engage(
        self,
        user_message: str,
        context_chunks: List[Dict],
        conversation_history: List[Dict[str, str]],
        reading_context: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Engage in Socratic dialogue with the learner.

        Args:
            user_message: What the learner said/asked
            context_chunks: Relevant textbook sections
            conversation_history: Previous messages
            reading_context: What section they just read

        Returns:
            {response, teaching_move, confidence_check}
        """
        # Analyze the user's message type
        message_analysis = await self._analyze_message(user_message, conversation_history)

        # Decide teaching strategy
        if message_analysis['type'] == 'direct_question':
            # Check if they should know this from recent reading
            if reading_context and self._is_in_recent_content(user_message, reading_context):
                response = await self._ask_clarifying_question(
                    user_message, context_chunks, conversation_history
                )
                teaching_move = "redirect_to_text"
            else:
                # They're exploring new territory - guide them
                response = await self._guide_discovery(
                    user_message, context_chunks, conversation_history
                )
                teaching_move = "guided_discovery"

        elif message_analysis['type'] == 'statement':
            # They're explaining something - validate understanding
            response = await self._check_understanding(
                user_message, context_chunks, conversation_history
            )
            teaching_move = "understanding_check"

        elif message_analysis['type'] == 'confusion':
            # They're genuinely stuck - provide scaffolding
            response = await self._provide_scaffold(
                user_message, context_chunks, conversation_history
            )
            teaching_move = "scaffolding"

        else:
            # Default: Socratic questioning
            response = await self._socratic_question(
                user_message, context_chunks, conversation_history
            )
            teaching_move = "socratic_question"

        return {
            'response': response,
            'teaching_move': teaching_move,
            'analysis': message_analysis
        }

    async def _analyze_message(
        self,
        message: str,
        history: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Analyze what type of message this is.
        """
        prompt = f"""Analyze this student message and classify it:

Message: "{message}"

Classify as one of:
- direct_question: Asking for an explanation (e.g., "What is LIDAR?")
- statement: Making a claim or explaining (e.g., "I think LIDAR uses lasers")
- confusion: Expressing difficulty (e.g., "I don't understand how...")
- clarification: Responding to a previous question

Return ONLY the classification type."""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=20
        )

        return {
            'type': response.choices[0].message.content.strip().lower(),
            'original': message
        }

    def _is_in_recent_content(self, question: str, reading_context: Dict) -> bool:
        """
        Check if the question is about content they just read.
        """
        # Simple heuristic: check if key terms from question appear in recent section
        question_lower = question.lower()
        content_lower = reading_context.get('content', '').lower()

        # Extract potential key terms (words > 4 letters, not common)
        common_words = {'what', 'when', 'where', 'which', 'would', 'could', 'should', 'does'}
        question_terms = [
            w.strip('.,?!') for w in question_lower.split()
            if len(w) > 4 and w.lower() not in common_words
        ]

        # Check overlap
        overlap = sum(1 for term in question_terms if term in content_lower)

        return overlap >= 2

    async def _ask_clarifying_question(
        self,
        question: str,
        context: List[Dict],
        history: List[Dict[str, str]]
    ) -> str:
        """
        Ask a question to guide them back to the text.
        """
        context_text = "\n".join([c['content'][:300] for c in context[:2]])

        prompt = f"""Student question: "{question}"

Relevant textbook content:
{context_text}

The answer is in the textbook content above. Instead of answering directly, ask a Socratic question that:
1. Points them to the relevant concept
2. Helps them discover the answer themselves
3. Checks what they already understand

Your question:"""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=150
        )

        return response.choices[0].message.content

    async def _guide_discovery(
        self,
        question: str,
        context: List[Dict],
        history: List[Dict[str, str]]
    ) -> str:
        """
        Guide them to discover the answer through questions.
        """
        context_text = "\n".join([c['content'][:400] for c in context[:3]])

        prompt = f"""Student wants to learn: "{question}"

Textbook content:
{context_text}

As a Socratic tutor:
1. Break down the concept into smaller pieces
2. Ask a question about the FIRST piece they should understand
3. Don't give away the answer
4. Be encouraging and specific

Your guiding question:"""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=200
        )

        return response.choices[0].message.content

    async def _check_understanding(
        self,
        statement: str,
        context: List[Dict],
        history: List[Dict[str, str]]
    ) -> str:
        """
        Validate or probe their understanding.
        """
        context_text = "\n".join([c['content'][:300] for c in context[:2]])

        prompt = f"""Student statement: "{statement}"

Ground truth from textbook:
{context_text}

Evaluate their understanding:
- If correct: Confirm and ask a deeper question
- If partially correct: Acknowledge what's right, then probe the gap
- If incorrect: Ask a question that reveals the error

Your response:"""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )

        return response.choices[0].message.content

    async def _provide_scaffold(
        self,
        confusion: str,
        context: List[Dict],
        history: List[Dict[str, str]]
    ) -> str:
        """
        Provide just enough help to unstick them.
        """
        context_text = "\n".join([c['content'][:400] for c in context[:2]])

        prompt = f"""Student is confused: "{confusion}"

Textbook content:
{context_text}

Provide minimal scaffolding:
1. Break the concept into the SMALLEST next step
2. Give a hint or analogy, not the full answer
3. Ask if that helps clarify

Your scaffolding:"""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )

        return response.choices[0].message.content

    async def _socratic_question(
        self,
        message: str,
        context: List[Dict],
        history: List[Dict[str, str]]
    ) -> str:
        """
        Default Socratic response.
        """
        context_text = "\n".join([c['content'][:300] for c in context[:2]])

        prompt = f"""Student: "{message}"

Relevant content:
{context_text}

Respond in Socratic style:
- Ask probing questions
- Guide thinking
- Don't lecture
- Be curious about their reasoning

Your question:"""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=150
        )

        return response.choices[0].message.content
