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
