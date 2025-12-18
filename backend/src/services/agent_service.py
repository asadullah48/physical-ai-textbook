class AgentService:
    def invoke(self, message: str):
        msg_lower = message.lower()
        
        if "forward kinematics" in msg_lower or "forward kinematic" in msg_lower or "fk" in msg_lower:
            response = """**Forward Kinematics (FK)** calculates the end-effector position from joint angles.

**For a 2-link planar arm:**
- **Given:** θ₁, θ₂ (joint angles), L₁, L₂ (link lengths)
- **Formulas:** 
  - x = L₁cos(θ₁) + L₂cos(θ₁+θ₂)
  - y = L₁sin(θ₁) + L₂sin(θ₁+θ₂)

**Try it!** Visit the Interactive Lab (/lab) to visualize FK in real-time by adjusting joint angles."""
        
        elif "inverse kinematics" in msg_lower or "ik" in msg_lower:
            response = """**Inverse Kinematics (IK)** solves for joint angles needed to reach a target position.

- **Input:** Desired end-effector position (x, y)
- **Output:** Joint angles (θ₁, θ₂)
- **Challenge:** May have multiple solutions or no solution
- **Methods:** Geometric, Jacobian, optimization-based"""
        
        elif "physical ai" in msg_lower or "pai" in msg_lower:
            response = """**Physical AI** refers to AI systems that interact with the physical world:

**Examples:**
- Humanoid robots (Tesla Optimus, Figure 01)
- Autonomous vehicles
- Robot manipulators
- Embodied agents

**Key difference:** Unlike text/image AI, Physical AI outputs motor commands and forces."""
        
        elif "ros" in msg_lower:
            response = """**ROS 2** (Robot Operating System 2) is the standard middleware for robotics:

**Core Concepts:**
- **Nodes:** Independent processes
- **Topics:** Publish-subscribe messaging
- **Services:** Request-response communication
- **DDS:** Data Distribution Service for real-time comms

**Languages:** C++, Python"""
        
        elif "simulation" in msg_lower or "gazebo" in msg_lower or "isaac" in msg_lower:
            response = """**Robot Simulation** enables testing without real hardware:

**Popular Tools:**
- **Gazebo:** Open-source physics simulator
- **Isaac Sim:** NVIDIA's photorealistic simulator with AI integration
- **MuJoCo:** Fast physics engine for research
- **PyBullet:** Python physics simulation

**Benefits:** Safe testing, rapid iteration, cost-effective"""
        
        elif "vla" in msg_lower or "vision language action" in msg_lower:
            response = """**Vision-Language-Action (VLA)** models are multimodal systems that:

**Combine:**
1. Computer Vision (perceive environment)
2. Natural Language (understand commands)
3. Robot Control (execute actions)

**Examples:**
- RT-1, RT-2 (Google DeepMind)
- PaLM-E (Embodied language model)
- OpenVLA (Open-source VLA)

**Use case:** "Pick up the red cup" → Vision identifies cup → Language understands command → Action executes grasp"""
        
        elif "kinematics" in msg_lower:
            response = """**Kinematics** studies motion without considering forces:

**Two Types:**
1. **Forward Kinematics (FK):** Joint angles → Position
2. **Inverse Kinematics (IK):** Position → Joint angles

**Applications:** Robot arm control, animation, path planning

Try the /lab to see FK visualization!"""
        
        else:
            response = f"""I'm your Physical AI tutor! I can explain:

- **Kinematics** (Forward/Inverse)
- **Physical AI** concepts
- **ROS 2** fundamentals
- **Simulation** tools (Gazebo, Isaac)
- **VLA models**

Try asking: "What is forward kinematics?" or visit **/lab** for interactive demos!

Your question: "{message}" """
        
        return {
            "response": response,
            "steps": ["AI Tutor"],
            "sources": []
        }

agent_service = AgentService()
