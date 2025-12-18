export interface Module {
  slug: string;
  title: string;
  icon: string;
  description: string;
  chapter_count: number;
}

const mockModules: Module[] = [
  { slug: "01-physical-ai-intro", title: "Introduction to Physical AI", icon: "🤖", description: "Fundamentals of Physical AI, its applications in robotics, and key concepts.", chapter_count: 2 },
  { slug: "02-ros2", title: "ROS 2 Fundamentals", icon: "🔧", description: "Robot Operating System 2 architecture, nodes, topics, and services.", chapter_count: 2 },
  { slug: "03-simulation", title: "Simulation Environments", icon: "🎮", description: "Using Gazebo, Isaac Sim for testing robotics applications.", chapter_count: 1 },
  { slug: "04-isaac", title: "NVIDIA Isaac Platform", icon: "🎯", description: "Leveraging NVIDIA Isaac for robot development.", chapter_count: 1 },
  { slug: "05-vla", title: "Vision-Language-Action Systems", icon: "🧠", description: "Advanced multimodal AI systems for intelligent behavior.", chapter_count: 1 }
];

class APIClient {
  private baseUrl = 'http://localhost:8000/api/v1';

  async getModules(): Promise<Module[]> {
    try {
      const res = await fetch(`${this.baseUrl}/modules`);
      if (!res.ok) throw new Error('Failed');
      return res.json();
    } catch (error) {
      return mockModules;
    }
  }

  async chat(message: string, history: any[] = []) {
    try {
      const res = await fetch(`${this.baseUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, history }),
      });
      if (!res.ok) throw new Error('Failed');
      return res.json();
    } catch (error) {
      console.error("Chat error:", error);
      return { response: "Backend not responding. Is it running on port 8000?", sources: [] };
    }
  }

  content = {
    listModules: async () => this.getModules()
  };
}

export const api = new APIClient();
