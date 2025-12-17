import { create } from 'zustand'

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    sources?: string[];
    steps?: string[];
}

interface AppState {
    // Navigation State
    currentModuleId: string | null;
    setCurrentModuleId: (id: string | null) => void;

    // Chat State
    chatHistory: ChatMessage[];
    addMessage: (msg: ChatMessage) => void;
    clearChat: () => void;
    isChatOpen: boolean;
    toggleChat: () => void;

    // Learning State (Persisted in real app)
    completedModules: string[];
    markModuleComplete: (moduleId: string) => void;
}

export const useStore = create<AppState>((set) => ({
    currentModuleId: null,
    setCurrentModuleId: (id) => set({ currentModuleId: id }),

    chatHistory: [
        {
            role: 'assistant',
            content: 'Hello! I am your Physical AI Professor. Ask me anything about the textbook or robotics concepts.'
        }
    ],
    addMessage: (msg) => set((state) => ({ chatHistory: [...state.chatHistory, msg] })),
    clearChat: () => set({ chatHistory: [] }),

    isChatOpen: false,
    toggleChat: () => set((state) => ({ isChatOpen: !state.isChatOpen })),

    completedModules: [],
    markModuleComplete: (id) => set((state) => ({
        completedModules: [...state.completedModules, id]
    })),
}))
