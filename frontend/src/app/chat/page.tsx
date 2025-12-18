'use client';

import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User, RefreshCw, BookOpen } from 'lucide-react';
import { api } from '@/services/api';
import Link from 'next/link';
import { useStore } from '@/store/useStore';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    sources?: string[];
    steps?: string[];
}

export default function ChatPage() {
    const messages = useStore((state) => state.messages);
    const addMessage = useStore((state) => state.addMessage);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input;
        setInput('');

        // Add User Message to Store
        addMessage({ role: 'user', content: userMessage });
        setIsLoading(true);

        // Prepare context for backend (last 10 messages for context)
        const history = messages.slice(-10).map(m => ({ role: m.role, content: m.content }));

        try {
            const response = await api.chat(userMessage, history);
            addMessage({
                role: 'assistant',
                content: response.response,
                sources: response.sources,
                steps: response.steps
            });
        } catch (error) {
            addMessage({
                role: 'assistant',
                content: "I'm having trouble connecting to my knowledge base right now. Please try again later."
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-slate-950/50">
            {/* Header Removed - Managed by AppLayout */}

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
                <div className="max-w-3xl mx-auto space-y-8">
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                            <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-600/30' : 'bg-slate-800 text-slate-400 border border-slate-700'
                                }`}>
                                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                            </div>

                            <div className={`flex-1 max-w-[80%]`}>
                                <div className={`p-5 rounded-2xl shadow-sm ${msg.role === 'user'
                                    ? 'bg-indigo-600 text-white rounded-br-none'
                                    : 'bg-slate-900 border border-slate-800 rounded-bl-none'
                                    }`}>
                                    <div className={`prose ${msg.role === 'user' ? 'prose-invert' : 'prose-invert'} max-w-none text-sm md:text-base`}>
                                        <ReactMarkdown
                                            components={{
                                                code({ node, inline, className, children, ...props }: any) {
                                                    return (
                                                        <code className={`${className} ${inline ? 'bg-black/30 px-1 py-0.5 rounded' : 'block bg-gray-950 border border-gray-800 p-3 rounded-lg overflow-x-auto'}`} {...props}>
                                                            {children}
                                                        </code>
                                                    )
                                                }
                                            }}
                                        >
                                            {msg.content}
                                        </ReactMarkdown>
                                    </div>
                                </div>

                                {/* Sources & Steps (Agent metadata) */}
                                {msg.role === 'assistant' && (
                                    <div className="mt-2 text-xs space-y-2">
                                        {msg.steps && msg.steps.length > 0 && (
                                            <div className="bg-slate-900/50 rounded p-2 text-slate-400 border border-slate-800">
                                                <div className="font-semibold mb-1 flex items-center gap-1 text-slate-300">
                                                    <RefreshCw size={12} /> Thinking Process:
                                                </div>
                                                <ul className="list-disc pl-4 space-y-1 font-mono">
                                                    {msg.steps.map((step, i) => (
                                                        <li key={i}>{step}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}

                                        {msg.sources && msg.sources.length > 0 && (
                                            <div className="flex gap-2 flex-wrap">
                                                {msg.sources.map((source, i) => (
                                                    <span key={i} className="inline-flex items-center gap-1 bg-indigo-900/30 text-indigo-300 px-2 py-1 rounded border border-indigo-500/20">
                                                        <BookOpen size={10} />
                                                        {source}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="flex gap-4">
                            <div className="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center text-slate-400 border border-slate-700">
                                <Bot size={20} />
                            </div>
                            <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl rounded-bl-none shadow-sm flex items-center gap-2">
                                <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></div>
                                <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce delay-75"></div>
                                <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce delay-150"></div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-slate-800 bg-slate-900/50 backdrop-blur-sm">
                <div className="max-w-3xl mx-auto">
                    <form onSubmit={handleSubmit} className="relative flex items-center gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask Professor PhysAI about concepts (e.g., 'What is Forward Kinematics?')..."
                            disabled={isLoading}
                            className="w-full pl-4 pr-12 py-4 bg-slate-950 border border-slate-800 text-slate-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all disabled:opacity-50 placeholder:text-slate-600"
                        />
                        <button
                            type="submit"
                            disabled={!input.trim() || isLoading}
                            className="absolute right-2 p-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-600 disabled:cursor-not-allowed transition-colors"
                        >
                            <Send size={20} />
                        </button>
                    </form>
                    <p className="text-center text-xs text-slate-600 mt-2">
                        AI can make mistakes. Verify important information from the textbook modules.
                    </p>
                </div>
            </div>
        </div>
    );
}
