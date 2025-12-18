import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface Message {
    role: 'user' | 'assistant';
    content: string;
    sources?: string[];
    steps?: string[];
    timestamp?: number;
}

interface AppState {
    // Chat State
    messages: Message[];
    addMessage: (msg: Message) => void;
    clearMessages: () => void;

    // UI State
    isSidebarOpen: boolean;
    toggleSidebar: () => void;

    // Lab State
    activeModuleId: string | null;
    setActiveModule: (id: string | null) => void;
}

export const useStore = create<AppState>()(
    persist(
        (set) => ({
            messages: [
                {
                    role: 'assistant',
                    content: "Hello! I'm Professor PhysAI. I'm ready to help you with your research in Physical AI. What's on your mind?",
                    timestamp: Date.now()
                }
            ],
            addMessage: (msg) => set((state) => ({
                messages: [...state.messages, { ...msg, timestamp: Date.now() }]
            })),
            clearMessages: () => set({ messages: [] }),

            isSidebarOpen: true,
            toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),

            activeModuleId: null,
            setActiveModule: (id) => set({ activeModuleId: id }),
        }),
        {
            name: 'physai-storage', // unique name
            partialize: (state) => ({ messages: state.messages }), // Persist only messages by default
        }
    )
);
