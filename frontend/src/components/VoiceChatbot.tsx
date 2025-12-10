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
