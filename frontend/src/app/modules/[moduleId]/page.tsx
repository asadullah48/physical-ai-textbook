import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

export default function ModulePage({ params }: { params: { moduleId: string } }) {
  const moduleId = params.moduleId;
  
  const modules: Record<string, any> = {
    "01-physical-ai-intro": { title: "Introduction to Physical AI", icon: "🤖", description: "Fundamentals of Physical AI." },
    "02-ros2": { title: "ROS 2 Fundamentals", icon: "🔧", description: "Robot Operating System 2." },
    "03-simulation": { title: "Simulation Environments", icon: "🎮", description: "Gazebo and Isaac Sim." },
    "04-isaac": { title: "NVIDIA Isaac Platform", icon: "🎯", description: "NVIDIA Isaac." },
    "05-vla": { title: "Vision-Language-Action", icon: "🧠", description: "Multimodal AI." }
  };

  const module = modules[moduleId] || { title: "Module", icon: "❓", description: "Coming soon" };

  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <Link href="/"><Button variant="ghost"><ArrowLeft className="mr-2 h-4 w-4" />Back</Button></Link>
        <div className="bg-white rounded-xl shadow-lg p-8 mt-6">
          <div className="text-6xl mb-4">{module.icon}</div>
          <h1 className="text-4xl font-bold mb-4">{module.title}</h1>
          <p className="text-xl text-gray-600 mb-8">{module.description}</p>
          <div className="bg-indigo-50 rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-semibold mb-4">📚 Content Coming Soon</h2>
            <ul className="space-y-2">
              <li>✅ Try <Link href="/lab" className="text-indigo-600 font-semibold">Interactive Lab</Link></li>
              <li>✅ Ask AI Tutor (💬 button)</li>
            </ul>
          </div>
          <Link href="/lab"><Button>🧪 Visit Lab</Button></Link>
        </div>
      </div>
    </main>
  );
}
