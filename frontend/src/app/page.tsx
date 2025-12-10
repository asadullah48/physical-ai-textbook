import React from 'react';
import Link from 'next/link';
import { api } from '@/services/api';

export default async function Home() {
  const modules = await api.content.listModules();

  return (
    <main className="min-h-screen bg-gray-50 text-gray-900">
      <section className="relative bg-gradient-to-br from-indigo-700 via-purple-700 to-blue-700 text-white py-20">
        <div className="container mx-auto px-6 max-w-6xl text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">Physical AI & Humanoid Robotics</h1>
          <p className="text-lg md:text-xl text-indigo-100 max-w-2xl mx-auto">
            Learn robotics with clean modules, hands-on code labs, and AI-powered support.
          </p>
          <div className="mt-8 flex justify-center gap-4">
            <Link href="/modules/01-physical-ai-intro" className="px-8 py-3 bg-white text-indigo-700 rounded-lg font-semibold shadow-sm hover:shadow-md transition-all">
              Start Learning →
            </Link>
          </div>
        </div>
      </section>

      <section className="bg-white border-b py-10">
        <div className="container mx-auto px-6 max-w-6xl grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          {[
            { icon: '📘', label: '5 Modules' },
            { icon: '💻', label: 'Code Labs' },
            { icon: '🤖', label: 'AI Tutor' },
            { icon: '🎙️', label: 'Voice Mode' }
          ].map((item, i) => (
            <div key={i} className="p-4">
              <div className="text-3xl mb-2">{item.icon}</div>
              <div className="font-medium text-gray-700">{item.label}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="py-16">
        <div className="container mx-auto px-6 max-w-6xl">
          <h2 className="text-3xl font-bold text-center mb-10">Course Modules</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {modules.map((module, index) => (
              <Link 
                key={module.slug} 
                href={`/modules/${module.slug}`}
                className="bg-white border rounded-xl p-6 hover:border-indigo-600 hover:shadow-md transition-all"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="text-4xl">{module.icon}</div>
                  <span className="text-sm font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full">
                    Module {index + 1}
                  </span>
                </div>
                <h3 className="text-lg font-semibold mb-2">{module.title}</h3>
                <p className="text-gray-600 text-sm mb-4 line-clamp-3">{module.description}</p>
                <div className="text-sm text-indigo-600 font-semibold">View →</div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-gradient-to-r from-indigo-700 to-purple-700 text-white py-16 text-center">
        <h2 className="text-3xl font-bold mb-4">Ready to Begin?</h2>
        <p className="text-indigo-100 mb-6">Start with the fundamentals and progress at your own pace.</p>
        <Link href="/modules/01-physical-ai-intro" className="px-8 py-3 bg-white text-indigo-700 rounded-lg font-semibold shadow-sm hover:shadow-md transition-all">
          Begin Your Journey
        </Link>
      </section>

      <footer className="bg-gray-900 text-gray-400 py-8 text-center">
        <p>© 2025 Physical AI Textbook • Built for Panaversity Hackathon</p>
      </footer>
    </main>
  );
}
