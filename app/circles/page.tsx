"use client";

import { useEffect, useState } from "react";
import { KindredAPI } from "@/lib/api";
import { MicroCircle } from "@/lib/types";
import { EventHeader } from "@/components/shared";
import { BottomNav } from "@/components/CardAndNav";
import { MicroCircleCard } from "@/components/DetailsAndCircles";
import { Users, Info, Sparkles } from "lucide-react";

export default function CirclesPage() {
  const [circles, setCircles] = useState<MicroCircle[]>([]);

  useEffect(() => {
    KindredAPI.getMicroCircles().then(setCircles);
  }, []);

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark pb-32">
      <EventHeader eventName="HackWithChicago 3.0" avatarUrl="https://i.pravatar.cc/150?u=me" />
      
      <div className="p-6 flex flex-col gap-8 animate-in slide-in-from-bottom-8 duration-700">
        <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
                <Users size={20} className="text-kindred-purple" />
                <h1 className="text-2xl font-black text-white tracking-tighter">Micro-Circles</h1>
            </div>
            <p className="text-xs text-white/40 leading-relaxed max-w-[280px]">
                High-value triangular matches where everyone has something to offer and something to ask.
            </p>
        </div>

        <div className="p-4 rounded-2xl bg-kindred-purple/10 border border-kindred-purple/20 flex items-start gap-3 relative overflow-hidden group">
            <div className="absolute top-0 left-0 h-full w-1 bg-kindred-purple" />
            <Info size={16} className="text-kindred-purple shrink-0 mt-0.5" />
            <p className="text-[10px] text-white/60 leading-relaxed">
                Connect all three members to initiate a <span className="text-white font-bold">Funding Loop</span> or <span className="text-white font-bold">Engineering Sprint</span> group chat.
            </p>
        </div>

        <div className="flex flex-col gap-8">
            {circles.map((circle) => (
                <div key={circle.id} className="animate-in zoom-in duration-500">
                    <MicroCircleCard 
                        loopName={circle.loopName}
                        attendees={circle.attendees.map(a => ({ name: a.name, avatar: a.avatar }))}
                        flow={circle.flowDescription}
                    />
                </div>
            ))}
        </div>

        {/* Empty State / Search More */}
        <div className="mt-12 flex flex-col items-center gap-4 text-center">
            <div className="w-12 h-12 rounded-full border border-white/5 flex items-center justify-center opacity-20">
                <Sparkles size={20} className="text-white" />
            </div>
            <div className="flex flex-col gap-1">
                <p className="text-[10px] font-black text-white/20 uppercase tracking-widest">Searching more nodes...</p>
                <p className="text-[8px] text-white/10 italic">Intelligence engine is computing triangular matches in real-time.</p>
            </div>
        </div>
      </div>

      <BottomNav />
    </div>
  );
}
