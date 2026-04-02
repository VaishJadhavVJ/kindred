"use client";

import { MessageSquare, Briefcase, Heart, Sparkles } from "lucide-react";

interface FollowUpTabsProps {
  onSelect?: (variant: string) => void;
}

export const FollowUpTabs = ({ onSelect }: FollowUpTabsProps) => {
  return (
    <div className="flex bg-white/5 p-1 rounded-xl gap-1">
      {["Professional", "Casual", "Creative"].map((tab) => (
        <button
          key={tab}
          onClick={() => onSelect?.(tab)}
          className="flex-1 py-2 text-[10px] font-bold uppercase tracking-tight text-white/40 hover:text-white/80 active:bg-kindred-purple active:text-white rounded-lg transition-all"
        >
          {tab}
        </button>
      ))}
    </div>
  );
};

interface WarmPathBreadcrumbProps {
  path: string[];
}

export const WarmPathBreadcrumb = ({ path }: WarmPathBreadcrumbProps) => {
  return (
    <div className="flex items-center gap-2 overflow-x-auto py-2">
      {path.map((name, index) => (
        <div key={index} className="flex items-center gap-2 shrink-0">
          <div className="flex flex-col items-center gap-1">
            <div className="w-8 h-8 rounded-full bg-kindred-purple/20 border border-kindred-purple/40 flex items-center justify-center">
              <span className="text-[10px] font-bold text-kindred-purple">{name[0]}</span>
            </div>
            <span className="text-[8px] text-white/40 font-medium">{name}</span>
          </div>
          {index < path.length - 1 && (
            <div className="h-0.5 w-4 bg-white/10 rounded-full" />
          )}
        </div>
      ))}
    </div>
  );
};

interface MicroCircleCardProps {
  loopName: string;
  attendees: { name: string; avatar: string }[];
  flow: string;
}

export const MicroCircleCard = ({ loopName, attendees, flow }: MicroCircleCardProps) => {
  return (
    <div className="p-6 rounded-2xl bg-kindred-dark border border-kindred-purple/20 glow-purple relative overflow-hidden group">
      <div className="absolute top-0 right-0 p-3 opacity-20 group-hover:opacity-40 transition-opacity">
        <Sparkles className="text-kindred-cyan" size={24} />
      </div>
      <div className="flex flex-col items-center gap-4">
        <div className="relative w-32 h-32 flex items-center justify-center">
          {/* Visual Triangle */}
          <svg className="absolute w-full h-full p-2 overflow-visible">
            <polygon 
              points="50,0 100,86 0,86" 
              className="fill-none stroke-kindred-purple/20 stroke-1 transform translate-x-[15%] translate-y-[15%]" 
            />
          </svg>
          {attendees.slice(0, 3).map((a, i) => (
            <div 
              key={i}
              className={`absolute w-12 h-12 rounded-full border-2 border-kindred-cyan overflow-hidden bg-kindred-dark z-10 transition-transform hover:scale-110 ${
                i === 0 ? "-top-2" : i === 1 ? "bottom-0 -left-2" : "bottom-0 -right-2"
              }`}
            >
              <img src={a.avatar} alt={a.name} className="w-full h-full object-cover" />
            </div>
          ))}
        </div>
        <div className="text-center">
          <h3 className="text-lg font-black text-white">{loopName}</h3>
          <p className="mt-2 text-xs text-white/50 leading-relaxed px-4">{flow}</p>
        </div>
        <button className="mt-4 w-full py-3 bg-kindred-purple text-white rounded-xl font-bold text-sm tracking-wide shadow-lg shadow-kindred-purple/20 active:scale-95 transition-all">
          Connect All
        </button>
      </div>
    </div>
  );
};
