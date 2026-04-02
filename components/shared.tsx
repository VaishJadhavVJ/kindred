"use client";

import { LucideIcon } from "lucide-react";

interface SerendipityBadgeProps {
  score: number;
  size?: "sm" | "md" | "lg";
}

export const SerendipityBadge = ({ score, size = "md" }: SerendipityBadgeProps) => {
  const sizeClasses = {
    sm: "w-8 h-8 text-xs",
    md: "w-12 h-12 text-sm",
    lg: "w-20 h-20 text-xl font-bold",
  };

  return (
    <div className={`${sizeClasses[size]} rounded-full bg-kindred-dark border-2 border-kindred-cyan text-kindred-cyan flex items-center justify-center glow-cyan transition-transform hover:scale-110`}>
      {score}
    </div>
  );
};

interface EventHeaderProps {
  eventName: string;
  avatarUrl: string;
}

export const EventHeader = ({ eventName, avatarUrl }: EventHeaderProps) => {
  return (
    <header className="w-full px-4 py-4 flex items-center justify-between bg-kindred-dark/80 backdrop-blur-md sticky top-0 z-50">
      <div className="flex flex-col">
        <span className="text-[10px] uppercase tracking-widest text-kindred-purple/60 font-medium">Current Event</span>
        <h1 className="text-lg font-bold text-white">{eventName}</h1>
      </div>
      <div className="w-10 h-10 rounded-full border-2 border-kindred-purple overflow-hidden">
        <img src={avatarUrl} alt="User Avatar" className="w-full h-full object-cover" />
      </div>
    </header>
  );
};
