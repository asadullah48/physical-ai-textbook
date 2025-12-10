export interface Module {
  slug: string;
  title: string;
  icon: string;
  description: string;
  chapter_count: number;
}

const mockModules: Module[] = [
  {
    slug: "01-physical-ai-intro",
    title: "Introduction to Physical AI",
    icon: "🤖",
    description: "Fundamentals of Physical AI, its applications in robotics, and key concepts.",
    chapter_count: 2
  },
  {
    slug: "02-ros2",
    title: "ROS 2 Fundamentals",
    icon: "🔧",
    description: "Robot Operating System 2 architecture, nodes, topics, and services.",
    chapter_count: 2
  },
  {
    slug: "03-simulation",
    title: "Simulation Environments",
    icon: "🎮",
    description: "Using Gazebo, Isaac Sim for testing robotics applications.",
    chapter_count: 1
  },
  {
    slug: "04-isaac",
    title: "NVIDIA Isaac Platform",
    icon: "🎯",
    description: "Leveraging NVIDIA Isaac for robot development.",
    chapter_count: 1
  },
  {
    slug: "05-vla",
    title: "Vision-Language-Action Systems",
    icon: "🧠",
    description: "Advanced multimodal AI systems for intelligent behavior.",
    chapter_count: 1
  }
];

class APIClient {
  async getModules(): Promise<Module[]> {
    return mockModules;
  }

  async chat(message: string) {
    const msg = message.toLowerCase();
    let response = "I'm an AI tutor for Physical AI. Ask me about robotics, ROS 2, or simulation!";
    
    if (msg.includes("ros")) {
      response = "ROS 2 is a flexible framework for robot software with tools and libraries for complex robot behavior.";
    } else if (msg.includes("physical ai")) {
      response = "Physical AI refers to AI systems that interact with the physical world through robots, combining perception and action.";
    } else if (msg.includes("sensor")) {
      response = "Sensors include LIDAR, cameras, IMUs, and force sensors for robot perception.";
    }
    
    return { response, sources: [] };
  }

  content = {
    listModules: async () => this.getModules()
  };
}

export const api = new APIClient();
