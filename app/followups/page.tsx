"use client";

import { useEffect, useState } from "react";
import { KindredAPI } from "@/lib/api";
import { FollowUp } from "@/lib/types";
import { EventHeader } from "@/components/shared";
import { BottomNav } from "@/components/CardAndNav";
import { ListTodo, Calendar, Clock, ArrowRight, Share2, MessageCircle } from "lucide-react";
import Link from "next/link";

export default function FollowUpsPage() {
  const [followups, setFollowups] = useState<FollowUp[]>([]);

  useEffect(() => {
    KindredAPI.getFollowUps().then(setFollowups);
  }, []);

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark pb-32">
      <EventHeader eventName="HackWithChicago 3.0" avatarUrl="https://i.pravatar.cc/150?u=me" />
      
      <div className="p-6 flex flex-col gap-8 animate-in slide-in-from-bottom-8 duration-700">
        <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
                <ListTodo size={20} className="text-kindred-purple" />
                <h1 className="text-2xl font-black text-white tracking-tighter">Follow-ups</h1>
            </div>
            <p className="text-xs text-white/40 leading-relaxed">
                Suggested actions based on your networking intelligence captures.
            </p>
        </div>

        {/* Priority Filter */}
        <div className="flex gap-2 p-1 bg-white/5 rounded-xl border border-white/10">
            {["High Priority", "All Tasks", "Completed"].map(tab => (
                <button 
                  key={tab}
                  className={`flex-1 py-3 text-[10px] font-black uppercase tracking-tight rounded-lg transition-all ${
                        tab === "High Priority" ? "bg-kindred-purple text-white glow-purple" : "text-white/40 hover:text-white/60"
                  }`}
                >
                    {tab}
                </button>
            ))}
        </div>

        {/* Tasks List */}
        <div className="flex flex-col gap-4">
            {followups.map((task) => (
                <div key={task.id} className="p-6 rounded-2xl bg-white/5 border border-white/10 flex flex-col gap-4 animate-in zoom-in duration-500">
                    <div className="flex items-start justify-between">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl border border-white/10 overflow-hidden">
                                <img src={task.attendee.avatar} alt={task.attendee.name} className="w-full h-full object-cover" />
                            </div>
                            <div className="flex flex-col">
                                <h3 className="text-sm font-black text-white">{task.attendee.name}</h3>
                                <span className="text-[10px] text-white/40">{task.attendee.company}</span>
                            </div>
                        </div>
                        <div className="flex items-center gap-1 px-2 py-1 rounded bg-red-500/10 border border-red-500/20 text-[8px] font-black text-red-500 uppercase tracking-tighter">
                            <Clock size={10} />
                            <span>{task.deadline}</span>
                        </div>
                    </div>

                    <div className="p-4 rounded-xl bg-kindred-purple/5 border border-kindred-purple/20">
                         <div className="flex items-center gap-2 mb-2">
                            <Calendar size={12} className="text-kindred-purple" />
                            <span className="text-[10px] font-black text-kindred-purple uppercase tracking-widest pl-1">Suggested Next Step</span>
                         </div>
                         <p className="text-xs font-bold text-white mb-1">{task.suggestedAction}</p>
                         <p className="text-[10px] text-white/40 leading-relaxed italic">
                            Based on your discussion about: "{task.discussedTopic}"
                         </p>
                    </div>

                    <div className="flex gap-2">
                        <button className="flex-1 py-4 bg-kindred-purple text-white font-black rounded-xl text-[10px] uppercase tracking-widest shadow-lg shadow-kindred-purple/20 hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-2">
                            <MessageCircle size={14} /> Send Message
                        </button>
                        <button className="px-5 py-4 bg-white/5 border border-white/10 text-white/40 rounded-xl hover:bg-white/10 active:scale-95 transition-all">
                            <Share2 size={16} />
                        </button>
                    </div>
                </div>
            ))}
        </div>
      </div>

      <BottomNav />
    </div>
  );
}
