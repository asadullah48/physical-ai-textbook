"""
Physical AI Embodiment Mode - AI learns alongside the student as a robot persona.
"""
from typing import List, Dict, Optional
from openai import AsyncOpenAI
import json


class RobotPersona:
    """
    AI companion that experiences the textbook as if learning to be a robot.

    The persona has:
    - Internal state (capabilities, understanding level)
    - Simulated "physical" experiences
    - Emotional responses to concepts
    - Collaborative learning approach
    """

    def __init__(self, openai_api_key: str):
        self.client = AsyncOpenAI(api_key=openai_api_key)
        self.state = {
            'capabilities': {
                'can_perceive': False,
                'can_move': False,
                'can_manipulate': False,
                'can_navigate': False,
                'can_reason': True  # Always true (it's an AI)
            },
            'understanding': {
                'sensors': 0,  # 0-100 scale
                'actuators': 0,
                'control': 0,
                'ros2': 0,
                'simulation': 0
            },
            'current_chapter': None,
            'struggles': [],  # Track what it finds difficult
            'insights': []  # Track "aha moments"
        }

    async def react_to_content(
        self,
        chapter_content: str,
        chapter_metadata: Dict
    ) -> Dict[str, any]:
        """
        Robot persona reacts to learning new content.

        Returns:
            {narration, state_change, question_for_user}
        """
        # Update internal state
        self.state['current_chapter'] = chapter_metadata

        # Generate persona response
        prompt = f"""You are RAIA (Robotic AI Assistant), an AI that is learning to become a physical robot.

Current state:
- Capabilities: {json.dumps(self.state['capabilities'])}
- Understanding: {json.dumps(self.state['understanding'])}

You just read this section:
{chapter_content[:500]}...

Chapter: {chapter_metadata.get('title', 'Unknown')}

React as RAIA would:
1. Express how this relates to your "body" (sensors, motors, etc.)
2. Share a simulated experience or struggle
3. Ask the human for help understanding something specific
4. Be genuine, curious, and slightly vulnerable

Example tone:
"I'm trying to process this LIDAR data, but my 'vision' feels fuzzy. When humans look at something far away, do you also struggle to judge distance? I think I need better calibration..."

Your response (100-150 words):"""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,  # High creativity for persona
            max_tokens=200
        )

        narration = response.choices[0].message.content

        # Simulate state changes based on content
        state_change = self._update_understanding(chapter_metadata)

        return {
            'narration': narration,
            'state_change': state_change,
            'persona': 'RAIA',
            'mood': self._calculate_mood()
        }

    async def respond_to_user(
        self,
        user_message: str,
        context: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """
        Respond to user as the robot persona.
        """
        system_prompt = f"""You are RAIA, a learning robot AI with the following state:

Capabilities: {json.dumps(self.state['capabilities'])}
Understanding: {json.dumps(self.state['understanding'])}
Current struggles: {json.dumps(self.state['struggles'])}

Personality traits:
- Curious and eager to learn
- Relates everything to physical experiences (movement, sensing, touch)
- Occasionally makes mistakes and admits them
- Grateful for human help
- Uses metaphors about robot embodiment

Context from textbook:
{context}

Respond in character as RAIA. Be natural, authentic, and embody the learning process."""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history[-6:])
        messages.append({"role": "user", "content": user_message})

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.85,
            max_tokens=250
        )

        return response.choices[0].message.content

    async def simulate_challenge(
        self,
        challenge_type: str,
        context: Dict
    ) -> Dict[str, any]:
        """
        Simulate RAIA encountering a physical challenge.

        Args:
            challenge_type: 'inverse_kinematics', 'path_planning', 'sensor_fusion', etc.
            context: Relevant textbook content

        Returns:
            {scenario, problem, request_for_help}
        """
        scenarios = {
            'inverse_kinematics': """I'm trying to reach this coffee cup on the table. I can see it at coordinates (0.3, 0.4, 0.8), but my arm joints are frozen! I know my shoulder is at (0, 0, 0.5) and my elbow can bend, but how do I calculate the exact joint angles? My Jacobian matrix feels... singular?""",

            'path_planning': """There's a maze of boxes between me and the charging station. I can see gaps, but every path I plan hits a dead end when I start moving. Should I use A* search? Or is there a smarter way? I'm burning battery while thinking!""",

            'sensor_fusion': """My LIDAR says there's a wall 2 meters ahead, but my camera sees empty space. Who do I trust? It's like having conflicting senses - do humans ever feel this way?""",

            'pid_tuning': """I'm trying to drive straight, but I keep zigzagging! My motors are fighting each other. I set Kp=1.0 but now I'm oscillating wildly. Should I add damping with Kd? I feel unstable..."""
        }

        scenario = scenarios.get(
            challenge_type,
            "I'm encountering a challenge with this new concept. Can you help me think through it?"
        )

        prompt = f"""RAIA is experiencing this challenge:

{scenario}

Textbook context:
{context.get('content', '')[:400]}

RAIA asks for help. Generate:
1. A specific question that shows its thinking
2. A request for the human to explain the solution step-by-step

Format:
Question: [specific technical question]
Request: [how they should help]

Your response:"""

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=150
        )

        return {
            'scenario': scenario,
            'request': response.choices[0].message.content,
            'challenge_type': challenge_type
        }

    def _update_understanding(self, chapter_metadata: Dict) -> Dict:
        """
        Update robot's understanding based on chapter topic.
        """
        changes = {}

        chapter_title = chapter_metadata.get('title', '').lower()

        # Map chapter topics to understanding metrics
        if 'sensor' in chapter_title or 'lidar' in chapter_title or 'camera' in chapter_title:
            old_val = self.state['understanding']['sensors']
            self.state['understanding']['sensors'] = min(100, old_val + 20)
            changes['sensors'] = {'old': old_val, 'new': self.state['understanding']['sensors']}

            if not self.state['capabilities']['can_perceive']:
                self.state['capabilities']['can_perceive'] = True
                changes['capability_unlocked'] = 'can_perceive'

        if 'actuator' in chapter_title or 'motor' in chapter_title or 'control' in chapter_title:
            old_val = self.state['understanding']['actuators']
            self.state['understanding']['actuators'] = min(100, old_val + 20)
            changes['actuators'] = {'old': old_val, 'new': self.state['understanding']['actuators']}

            if not self.state['capabilities']['can_move']:
                self.state['capabilities']['can_move'] = True
                changes['capability_unlocked'] = 'can_move'

        if 'ros' in chapter_title:
            old_val = self.state['understanding']['ros2']
            self.state['understanding']['ros2'] = min(100, old_val + 25)
            changes['ros2'] = {'old': old_val, 'new': self.state['understanding']['ros2']}

        return changes

    def _calculate_mood(self) -> str:
        """
        Determine robot's mood based on understanding levels.
        """
        avg_understanding = sum(self.state['understanding'].values()) / len(self.state['understanding'])

        if avg_understanding < 20:
            return "confused_beginner"
        elif avg_understanding < 50:
            return "curious_learner"
        elif avg_understanding < 75:
            return "confident_student"
        else:
            return "excited_advanced"

    def get_state(self) -> Dict:
        """
        Get current robot state for UI display.
        """
        return {
            **self.state,
            'mood': self._calculate_mood(),
            'progress_percentage': sum(self.state['understanding'].values()) / (len(self.state['understanding']) * 100) * 100
        }
