"use client";

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Send, Bot, MessageSquare } from 'lucide-react';
import { useStore } from '@/store/useStore';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { cn } from '@/lib/utils';
import ReactMarkdown from 'react-markdown';

export function AIChatSidebar() {
    const { isChatOpen, toggleChat, chatHistory, addMessage } = useStore();
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim()) return;

        // Add User Message
        addMessage({ role: 'user', content: input });
        const userMsg = input;
        setInput('');
        setIsLoading(true);

        try {
            // Call Real Backend
            // Call Real Backend
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const res = await fetch(`${apiUrl}/api/v1/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg })
            });

            const data = await res.json();

            // Add AI Response
            addMessage({
                role: 'assistant',
                content: data.response,
                sources: data.sources,
                steps: data.steps
            });
        } catch (error) {
            addMessage({
                role: 'assistant',
                content: "Before I can answer, please ensure the Backend Server is running on port 8000."
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            {/* Floating Toggle Button */}
            {!isChatOpen && (
                <motion.button
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    onClick={toggleChat}
                    className="fixed bottom-6 right-6 z-50 p-4 bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 transition-colors"
                >
                    <Bot className="w-6 h-6" />
                </motion.button>
            )}

            {/* Sidebar Panel */}
            <AnimatePresence>
                {isChatOpen && (
                    <motion.div
                        initial={{ x: '100%' }}
                        animate={{ x: 0 }}
                        exit={{ x: '100%' }}
                        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                        className="fixed top-0 right-0 h-full w-[400px] bg-background border-l shadow-2xl z-50 flex flex-col"
                    >
                        {/* Header */}
                        <div className="p-4 border-b flex items-center justify-between bg-indigo-50/50">
                            <div className="flex items-center gap-2">
                                <Bot className="w-5 h-5 text-indigo-600" />
                                <h2 className="font-semibold text-lg">AI Professor</h2>
                            </div>
                            <Button variant="ghost" size="sm" onClick={toggleChat}>
                                <X className="w-5 h-5" />
                            </Button>
                        </div>

                        {/* Chat Area */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50">
                            {chatHistory.map((msg, idx) => (
                                <div
                                    key={idx}
                                    className={cn(
                                        "max-w-[85%] rounded-lg p-3 text-sm",
                                        msg.role === 'user'
                                            ? "bg-indigo-600 text-white ml-auto"
                                            : "bg-white border text-gray-800 shadow-sm mr-auto"
                                    )}
                                >
                                    {msg.steps && msg.steps.length > 0 && (
                                        <div className="mb-2 space-y-1">
                                            {msg.steps.map((step, i) => (
                                                <div key={i} className="flex items-center text-xs bg-indigo-50 text-indigo-700 p-1 rounded border border-indigo-100 font-mono">
                                                    <div className="w-2 h-2 rounded-full bg-indigo-400 mr-2 animate-pulse" />
                                                    {step}
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                                    {msg.sources && msg.sources.length > 0 && (
                                        <div className="mt-2 text-xs opacity-70 border-t pt-1 border-gray-200">
                                            Sources: {msg.sources.join(', ')}
                                        </div>
                                    )}
                                </div>
                            ))}
                            {isLoading && (
                                <div className="text-gray-400 text-sm animate-pulse">Thinking...</div>
                            )}
                        </div>

                        {/* Input Area */}
                        <div className="p-4 border-t bg-white">
                            <div className="flex gap-2">
                                <input
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                    placeholder="Ask about robotics..."
                                    className="flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
                                />
                                <Button onClick={handleSend} disabled={isLoading} size="sm">
                                    <Send className="w-4 h-4" />
                                </Button>
                            </div>
                            <div className="text-xs text-center mt-2 text-gray-400">
                                Powered by RAG & OpenAI
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
}
