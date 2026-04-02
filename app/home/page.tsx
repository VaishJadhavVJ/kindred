"use client";

import { useEffect, useState } from "react";
import { KindredAPI } from "@/lib/api";
import { Attendee, Event as KindredEvent } from "@/lib/types";
import { EventHeader } from "@/components/shared";
import { PersonCard, BottomNav } from "@/components/CardAndNav";
import { Network, Sparkles, Filter } from "lucide-react";

export default function HomePage() {
  const [event, setEvent] = useState<KindredEvent | null>(null);
  const [recommendations, setRecommendations] = useState<Attendee[]>([]);

  useEffect(() => {
    KindredAPI.getCurrentEvent().then(setEvent);
    KindredAPI.getRecommendations().then(setRecommendations);
  }, []);

  if (!event) return null;

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark pb-32">
      <EventHeader eventName={event.name} avatarUrl="https://i.pravatar.cc/150?u=me" />
      
      {/* Network Graph Visualization Area (40% height approx) */}
      <div className="w-full aspect-[4/3] bg-kindred-dark relative overflow-hidden flex items-center justify-center border-b border-white/5">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(168,85,247,0.1),transparent_70%)]" />
        
        {/* Placeholder for Interactive Graph */}
        <div className="relative flex flex-col items-center gap-4">
          <div className="w-64 h-64 border border-kindred-purple/20 rounded-full animate-pulse-slow flex items-center justify-center">
             <div className="w-48 h-48 border border-kindred-cyan/20 rounded-full animate-pulse flex items-center justify-center">
                <div className="w-4 h-4 bg-kindred-cyan rounded-full glow-cyan z-20" />
             </div>
          </div>
          
          {/* Animated Floaties */}
          {[...Array(6)].map((_, i) => (
             <div 
               key={i} 
               className="absolute w-2 h-2 bg-kindred-purple rounded-full opacity-40 animate-bounce" 
               style={{ 
                 top: `${Math.random() * 100}%`, 
                 left: `${Math.random() * 100}%`,
                 animationDelay: `${i * 0.5}s` 
               }}
             />
          ))}
          
          <div className="absolute -bottom-4 flex items-center gap-2 px-4 py-2 rounded-full bg-kindred-purple/10 border border-kindred-purple/20 backdrop-blur-md">
            <Network size={14} className="text-kindred-purple" />
            <span className="text-[10px] font-black text-white uppercase tracking-tighter">Live Intelligence Graph</span>
          </div>
        </div>
      </div>

      {/* Recommendations Section */}
      <div className="flex-1 p-6 flex flex-col gap-6 animate-in slide-in-from-bottom-12 duration-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles size={16} className="text-kindred-cyan" />
            <h2 className="text-sm font-black text-white tracking-tight uppercase">Recommended for You</h2>
          </div>
          <button className="p-2 rounded-lg bg-white/5 border border-white/10 text-white/40">
            <Filter size={14} />
          </button>
        </div>

        <div className="flex flex-col gap-4">
          {recommendations.map((attendee) => (
            <PersonCard 
              key={attendee.id}
              id={attendee.id}
              name={attendee.name}
              role={attendee.role}
              company={attendee.company}
              avatar={attendee.avatar}
              matchScore={attendee.matchScore}
              reason={attendee.matchReason}
            />
          ))}
        </div>
      </div>

      <BottomNav />
    </div>
  );
}
