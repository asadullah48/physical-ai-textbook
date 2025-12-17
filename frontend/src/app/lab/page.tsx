import React from 'react';
import { SimLab } from '@/components/SimLab';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function LabPage() {
    return (
        <main className="min-h-screen bg-gray-50 p-6 md:p-12">
            <div className="max-w-4xl mx-auto">
                <div className="mb-8">
                    <Link href="/">
                        <Button variant="ghost" className="mb-4 pl-0 hover:bg-transparent hover:text-indigo-600">
                            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Textbook
                        </Button>
                    </Link>

                    <h1 className="text-4xl font-bold text-gray-900 mb-2">Physical AI Lab</h1>
                    <p className="text-xl text-gray-600">Interactive simulations to ground theoretical concepts in reality.</p>
                </div>

                <div className="grid md:grid-cols-1 gap-8">
                    <section>
                        <h2 className="text-2xl font-semibold mb-4 text-indigo-700 border-b pb-2">Module 1: Kinematics</h2>
                        <div className="flex flex-col md:flex-row gap-8 items-start">
                            <div className="flex-1">
                                <SimLab />
                            </div>
                            <div className="flex-1 prose prose-indigo">
                                <h3>Forward Kinematics (FK)</h3>
                                <p>
                                    FK is the process of calculating the position of the end-effector (hand) given the joint angles ($$ \theta_1, \theta_2 $$).
                                </p>
                                <ul className="list-disc pl-5 space-y-2 mt-4">
                                    <li><strong>L1, L2:</strong> Lengths of the robot links.</li>
                                    <li><strong>Joints:</strong> Revolute joints allowing rotation.</li>
                                    <li><strong>Goal:</strong> Map Configuration Space ($$ C $$) to Task Space ($$ T $$).</li>
                                </ul>

                                <div className="mt-6 p-4 bg-indigo-50 border border-indigo-100 rounded-lg">
                                    <h4 className="font-bold text-indigo-900 text-sm uppercase tracking-wide mb-2">Try this:</h4>
                                    <p className="text-sm text-indigo-800">
                                        Set <strong>θ1 = 0°</strong> and <strong>θ2 = 90°</strong>.
                                        Notice how the robot reaches straight up and then bends forward?
                                        This is a singularity-free configuration.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </main>
    );
}
