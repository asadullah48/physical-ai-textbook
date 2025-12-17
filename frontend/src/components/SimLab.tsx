"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { Slider } from './ui/slider'; // Assuming we have or will use a native range input if this doesn't exist
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Play, RotateCcw, Target, CheckCircle2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useStore } from '@/store/useStore';

export function SimLab() {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Robot State
    const [theta1, setTheta1] = useState(45);
    const [theta2, setTheta2] = useState(-45);
    const [target, setTarget] = useState({ x: 180, y: 50 }); // Random initial target
    const [score, setScore] = useState(0);
    const [isSuccess, setIsSuccess] = useState(false);

    // Data Logging for Graph (Last 20 points)
    const [data, setData] = useState<any[]>([]);

    // Link Lengths (pixels)
    const L1 = 100;
    const L2 = 80;

    // Inverse Kinematics Challenge logic
    useEffect(() => {
        const { x2, y2 } = calculateFK(theta1, theta2);
        const dist = Math.sqrt(Math.pow(x2 - target.x, 2) + Math.pow(y2 - target.y, 2));

        if (dist < 15 && !isSuccess) {
            setIsSuccess(true);
            setScore(prev => prev + 100);
        } else if (dist >= 15 && isSuccess) {
            setIsSuccess(false);
        }

        // Log data for graph
        setData(prev => {
            const newData = [...prev, { name: prev.length, t1: theta1, t2: theta2 }];
            if (newData.length > 50) return newData.slice(-50);
            return newData;
        });
    }, [theta1, theta2, target]);

    const calculateFK = (t1_deg: number, t2_deg: number) => {
        const t1 = t1_deg * (Math.PI / 180);
        const t2 = t2_deg * (Math.PI / 180);

        const x1 = L1 * Math.cos(t1);
        const y1 = L1 * Math.sin(t1);
        const x2 = x1 + L2 * Math.cos(t1 + t2);
        const y2 = y1 + L2 * Math.sin(t1 + t2);

        return { x1, y1, x2, y2 };
    };

    const resetGame = () => {
        setTarget({
            x: Math.random() * 150 + 50,
            y: Math.random() * 200 - 100
        });
        setIsSuccess(false);
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Clear Canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Set Origin
        const ox = 150;
        const oy = 250;

        const { x1, y1, x2, y2 } = calculateFK(theta1, theta2);

        // Draw Target
        ctx.beginPath();
        ctx.arc(ox + target.x, oy - target.y, 15, 0, 2 * Math.PI); // Target radius 15
        ctx.fillStyle = isSuccess ? '#22c55e' : 'rgba(34, 197, 94, 0.2)'; // Green-500
        ctx.fill();
        ctx.strokeStyle = '#22c55e';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw Base
        ctx.fillStyle = '#1e293b'; // Slate-800
        ctx.fillRect(ox - 20, oy, 40, 10);

        // Draw Link 1
        ctx.beginPath();
        ctx.moveTo(ox, oy);
        ctx.lineTo(ox + x1, oy - y1);
        ctx.lineWidth = 12;
        ctx.lineCap = 'round';
        ctx.strokeStyle = '#6366f1'; // Indigo-500
        ctx.stroke();

        // Joint 1
        ctx.beginPath();
        ctx.arc(ox, oy, 8, 0, 2 * Math.PI);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.stroke();

        // Draw Link 2
        ctx.beginPath();
        ctx.moveTo(ox + x1, oy - y1);
        ctx.lineTo(ox + x2, oy - y2);
        ctx.strokeStyle = '#a855f7'; // Purple-500
        ctx.stroke();

        // Joint 2
        ctx.beginPath();
        ctx.arc(ox + x1, oy - y1, 8, 0, 2 * Math.PI);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.stroke();

        // End Effector
        ctx.beginPath();
        ctx.arc(ox + x2, oy - y2, 10, 0, 2 * Math.PI);
        ctx.fillStyle = isSuccess ? '#22c55e' : '#ef4444'; // Green if success, Red otherwise
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();

    }, [theta1, theta2, target, isSuccess]);

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full max-w-6xl mx-auto">
            {/* Left: Simulation Canvas */}
            <Card className="bg-slate-900 border-slate-800 text-slate-100">
                <CardHeader>
                    <div className="flex justify-between items-center">
                        <div>
                            <CardTitle className="flex items-center gap-2">
                                <Target className="w-5 h-5 text-green-500" />
                                Kinematics Challenge
                            </CardTitle>
                            <CardDescription className="text-slate-400">
                                Move the end-effector to the green target zone.
                            </CardDescription>
                        </div>
                        <div className="bg-slate-800 px-3 py-1 rounded text-sm font-mono border border-slate-700">
                            Score: <span className="text-green-400 font-bold">{score}</span>
                        </div>
                    </div>
                </CardHeader>
                <CardContent className="flex flex-col items-center gap-6">
                    <div className="relative">
                        <canvas
                            ref={canvasRef}
                            width={350}
                            height={350}
                            className="bg-slate-950 rounded-xl border border-slate-800 shadow-inner"
                        />
                        {isSuccess && (
                            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                                <div className="bg-green-500/20 backdrop-blur-sm rounded-xl px-6 py-4 border border-green-500/50 animate-in zoom-in duration-300">
                                    <div className="text-green-400 font-bold text-xl flex items-center gap-2">
                                        <CheckCircle2 /> Target Reached!
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="w-full space-y-6 bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <label>Joint 1 (Base): <span className="font-mono text-indigo-400">{theta1}°</span></label>
                            </div>
                            <input
                                type="range"
                                min="-90" max="180"
                                value={theta1}
                                onChange={(e) => setTheta1(Number(e.target.value))}
                                className="w-full accent-indigo-500 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
                            />
                        </div>
                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <label>Joint 2 (Elbow): <span className="font-mono text-purple-400">{theta2}°</span></label>
                            </div>
                            <input
                                type="range"
                                min="-135" max="135"
                                value={theta2}
                                onChange={(e) => setTheta2(Number(e.target.value))}
                                className="w-full accent-purple-500 h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
                            />
                        </div>
                        <Button
                            onClick={resetGame}
                            variant="outline"
                            className="w-full border-slate-700 hover:bg-slate-700 hover:text-white"
                        >
                            <RotateCcw className="mr-2 h-4 w-4" /> New Target
                        </Button>
                    </div>
                </CardContent>
            </Card>

            {/* Right: Code & Analytics */}
            <div className="space-y-6">
                {/* Math Visualization */}
                <Card className="bg-slate-900 border-slate-800 text-slate-100">
                    <CardHeader>
                        <CardTitle className="text-sm font-mono uppercase text-slate-400 tracking-wider">
                            Real-time Matrix Math
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="font-mono text-xs md:text-sm bg-slate-950 p-4 rounded-lg border border-slate-800 overflow-x-auto text-cyan-400 space-y-1">
                            <div>// Forward Kinematics Calculation</div>
                            <div className="text-slate-500">const L1 = {L1}, L2 = {L2};</div>
                            <br />
                            <div>x1 = L1 * cos({theta1}°) = <span className="text-white">{(L1 * Math.cos(theta1 * Math.PI / 180)).toFixed(1)}</span></div>
                            <div>y1 = L1 * sin({theta1}°) = <span className="text-white">{(L1 * Math.sin(theta1 * Math.PI / 180)).toFixed(1)}</span></div>
                            <br />
                            <div>// End Effector Position</div>
                            <div>x2 = x1 + L2 * cos({theta1 + theta2}°) = <span className="text-yellow-400 font-bold">{(L1 * Math.cos(theta1 * Math.PI / 180) + L2 * Math.cos((theta1 + theta2) * Math.PI / 180)).toFixed(1)}</span></div>
                            <div>y2 = y1 + L2 * sin({theta1 + theta2}°) = <span className="text-yellow-400 font-bold">{(L1 * Math.sin(theta1 * Math.PI / 180) + L2 * Math.sin((theta1 + theta2) * Math.PI / 180)).toFixed(1)}</span></div>
                        </div>
                    </CardContent>
                </Card>

                {/* Live Graph */}
                <Card className="bg-slate-900 border-slate-800 text-slate-100 flex-1">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Activity className="w-5 h-5 text-indigo-500" />
                            Joint State Telemetry
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="h-[200px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={data}>
                                <XAxis dataKey="name" hide />
                                <YAxis domain={[-180, 180]} hide />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                                    itemStyle={{ color: '#e2e8f0' }}
                                />
                                <Line type="monotone" dataKey="t1" stroke="#6366f1" strokeWidth={2} dot={false} isAnimationActive={false} />
                                <Line type="monotone" dataKey="t2" stroke="#a855f7" strokeWidth={2} dot={false} isAnimationActive={false} />
                            </LineChart>
                        </ResponsiveContainer>
                        <div className="flex gap-4 justify-center mt-2 text-xs text-slate-400">
                            <div className="flex items-center gap-1"><div className="w-3 h-3 bg-indigo-500 rounded-full"></div> Joint 1</div>
                            <div className="flex items-center gap-1"><div className="w-3 h-3 bg-purple-500 rounded-full"></div> Joint 2</div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
