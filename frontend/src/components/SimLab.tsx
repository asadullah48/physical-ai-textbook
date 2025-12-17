"use client";

import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';

export function SimLab() {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    // State for Joint Angles (in degrees)
    const [theta1, setTheta1] = useState(45);
    const [theta2, setTheta2] = useState(-45);

    // Link Lengths (pixels)
    const L1 = 100;
    const L2 = 80;

    // Forward Kinematics Calculation
    const calculateFK = () => {
        const t1 = theta1 * (Math.PI / 180);
        const t2 = theta2 * (Math.PI / 180);

        const x1 = L1 * Math.cos(t1);
        const y1 = L1 * Math.sin(t1);

        // Relative to the first link's end
        const x2 = x1 + L2 * Math.cos(t1 + t2);
        const y2 = y1 + L2 * Math.sin(t1 + t2);

        return { x1, y1, x2, y2 };
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Clear Canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Set Origin (Center-ish)
        const ox = 150;
        const oy = 250;

        const { x1, y1, x2, y2 } = calculateFK();

        // Draw Base
        ctx.fillStyle = '#333';
        ctx.fillRect(ox - 20, oy, 40, 10);

        // Draw Link 1
        ctx.beginPath();
        ctx.moveTo(ox, oy);
        ctx.lineTo(ox + x1, oy - y1); // Canvas Y is inverted
        ctx.lineWidth = 8;
        ctx.strokeStyle = '#4f46e5'; // Indigo-600
        ctx.stroke();

        // Joint 1
        ctx.beginPath();
        ctx.arc(ox, oy, 6, 0, 2 * Math.PI);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.stroke();

        // Draw Link 2
        ctx.beginPath();
        ctx.moveTo(ox + x1, oy - y1);
        ctx.lineTo(ox + x2, oy - y2);
        ctx.strokeStyle = '#9333ea'; // Purple-600
        ctx.stroke();

        // Joint 2
        ctx.beginPath();
        ctx.arc(ox + x1, oy - y1, 6, 0, 2 * Math.PI);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.stroke();

        // End Effector
        ctx.beginPath();
        ctx.arc(ox + x2, oy - y2, 8, 0, 2 * Math.PI);
        ctx.fillStyle = '#ef4444'; // Red-500
        ctx.fill();

    }, [theta1, theta2]);

    return (
        <Card className="w-full max-w-md mx-auto">
            <CardHeader>
                <CardTitle>Physical AI Lab: Kinematics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="border rounded-lg bg-gray-100 flex justify-center p-4">
                    <canvas ref={canvasRef} width={300} height={300} className="bg-white rounded shadow-sm" />
                </div>

                <div className="space-y-4">
                    <div>
                        <label className="text-sm font-medium">Joint 1 Angle (θ1): {theta1}°</label>
                        <input
                            type="range"
                            min="-90" max="180"
                            value={theta1}
                            onChange={(e) => setTheta1(Number(e.target.value))}
                            className="w-full mt-2"
                        />
                    </div>
                    <div>
                        <label className="text-sm font-medium">Joint 2 Angle (θ2): {theta2}°</label>
                        <input
                            type="range"
                            min="-135" max="135"
                            value={theta2}
                            onChange={(e) => setTheta2(Number(e.target.value))}
                            className="w-full mt-2"
                        />
                    </div>

                    <div className="p-3 bg-blue-50 text-blue-800 text-xs rounded-md">
                        <strong>Robot Insight:</strong> As you move the sliders, you are performing <em>Forward Kinematics</em>—calculating the end-effector position (Red Dot) from joint angles. Physical AI agents do the opposite (Inverse Kinematics) to reach a target!
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
