#!/bin/bash

# Layout
cat > src/app/layout.tsx << 'EOF1'
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../styles/globals.css";
import VoiceChatbot from "@/components/VoiceChatbot";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Physical AI & Humanoid Robotics | Interactive Textbook",
  description: "Master Physical AI, ROS 2, and humanoid robotics.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <VoiceChatbot />
      </body>
    </html>
  );
}
EOF1

# Homepage
cat > src/app/page.tsx << 'EOF2'
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
EOF2

# VoiceChatbot Component
cat > src/components/VoiceChatbot.tsx << 'EOF3'
'use client';
import React, { useState, useRef, useEffect } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function VoiceChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const recognitionRef = useRef<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = false;
        recognitionRef.current.lang = 'en-US';
        
        recognitionRef.current.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInput(transcript);
          setIsListening(false);
          handleSend(transcript);
        };
        
        recognitionRef.current.onerror = () => setIsListening(false);
        recognitionRef.current.onend = () => setIsListening(false);
      }
    }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  const speak = (text: string) => {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  };

  const handleSend = async (text?: string) => {
    const messageText = text || input;
    if (!messageText.trim() || isLoading) return;

    setMessages(prev => [...prev, { role: 'user', content: messageText }]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      speak(data.response);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error occurred. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full shadow-lg flex items-center justify-center text-white hover:scale-110 transition-all z-50"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {isOpen && (
        <div className="fixed bottom-24 right-6 w-96 h-[500px] bg-white rounded-2xl shadow-2xl flex flex-col z-50 border border-gray-200">
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 rounded-t-2xl">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-lg">AI Tutor 🤖</h3>
                <p className="text-xs opacity-90">Ask about Physical AI</p>
              </div>
              {isListening && (
                <div className="flex items-center gap-2 text-xs bg-red-500 px-3 py-1 rounded-full animate-pulse">
                  🎙️ Listening...
                </div>
              )}
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 mt-8">
                <p className="mb-4">👋 Hi! I'm your AI tutor.</p>
                <div className="space-y-2 text-sm">
                  <div className="bg-white p-3 rounded-lg shadow-sm">💬 Type your question</div>
                  <div className="bg-white p-3 rounded-lg shadow-sm">🎙️ Or click mic to speak!</div>
                </div>
              </div>
            )}
            
            {messages.map((msg, i) => (
              <div key={i} className={'flex ' + (msg.role === 'user' ? 'justify-end' : 'justify-start')}>
                <div className={'max-w-[80%] p-3 rounded-lg ' + (
                  msg.role === 'user' 
                    ? 'bg-indigo-600 text-white' 
                    : 'bg-white text-gray-900 shadow-sm'
                )}>
                  {msg.content}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white p-3 rounded-lg shadow-sm">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="p-4 bg-white border-t rounded-b-2xl">
            {isSpeaking && (
              <div className="mb-2 flex items-center justify-between text-sm text-indigo-600 bg-indigo-50 px-3 py-2 rounded-lg">
                <span className="flex items-center gap-2">🔊 Speaking...</span>
                <button onClick={stopSpeaking} className="underline font-medium">Stop</button>
              </div>
            )}
            <div className="flex gap-2">
              <button
                onClick={isListening ? stopListening : startListening}
                className={'p-3 rounded-full transition-all ' + (
                  isListening 
                    ? 'bg-red-500 text-white animate-pulse' 
                    : 'bg-gray-100 hover:bg-gray-200'
                )}
                title={isListening ? 'Stop listening' : 'Start voice input'}
              >
                🎙️
              </button>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder={isListening ? 'Listening...' : 'Ask a question...'}
                className="flex-1 px-4 py-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500"
                disabled={isListening}
              />
              <button
                onClick={() => handleSend()}
                disabled={!input.trim() || isLoading}
                className="px-6 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
EOF3

echo "✅ All files created!"
