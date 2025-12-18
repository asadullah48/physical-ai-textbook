"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useStore } from '@/store/useStore';
import {
    BookOpen,
    MessageSquare,
    Activity,
    Menu,
    X,
    Home,
    Cpu,
    Layers
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

export function AppLayout({ children }: { children: React.ReactNode }) {
    const isSidebarOpen = useStore((state) => state.isSidebarOpen);
    const toggleSidebar = useStore((state) => state.toggleSidebar);
    const pathname = usePathname();

    const navItems = [
        { label: 'Home', icon: Home, href: '/' },
        { label: 'Modules', icon: BookOpen, href: '/modules/01-physical-ai-intro' },
        { label: 'AI Chat', icon: MessageSquare, href: '/chat' },
        { label: 'Sim Lab', icon: Activity, href: '/lab' },
    ];

    return (
        <div className="flex h-screen bg-background text-foreground overflow-hidden">
            {/* Sidebar */}
            <aside
                className={cn(
                    "fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 border-r border-slate-800 transition-transform duration-300 ease-in-out md:relative md:translate-x-0",
                    !isSidebarOpen && "-translate-x-full md:hidden"
                )}
            >
                <div className="p-6 flex items-center gap-2 border-b border-slate-800">
                    <Cpu className="h-6 w-6 text-indigo-500" />
                    <span className="font-bold text-lg tracking-tight">PhysAI<span className="text-indigo-500">.Textbook</span></span>
                </div>

                <nav className="p-4 space-y-2">
                    {navItems.map((item) => {
                        const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors",
                                    isActive
                                        ? "bg-indigo-600/10 text-indigo-400 border border-indigo-600/20"
                                        : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/50"
                                )}
                            >
                                <item.icon className="h-4 w-4" />
                                {item.label}
                            </Link>
                        );
                    })}
                </nav>

                <div className="absolute bottom-0 w-full p-4 border-t border-slate-800">
                    <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">
                        <div className="text-xs text-slate-400 uppercase font-bold mb-2">System Status</div>
                        <div className="flex items-center gap-2 text-xs text-green-400">
                            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                            RAG Knowledge Base Active
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col h-full overflow-hidden relative">
                <header className="h-16 border-b border-slate-800 bg-background/50 backdrop-blur-md flex items-center px-6 justify-between shrink-0">
                    <Button variant="ghost" size="sm" onClick={toggleSidebar} className="md:hidden">
                        <Menu className="h-5 w-5" />
                    </Button>

                    <div className="flex items-center gap-4 text-sm text-slate-500">
                        <Layers className="h-4 w-4" />
                        <span>Workspace / {pathname.split('/')[1] || 'Home'}</span>
                    </div>
                </header>

                <main className="flex-1 overflow-auto p-0 md:p-6 bg-slate-950/50">
                    {children}
                </main>
            </div>
        </div>
    );
}
