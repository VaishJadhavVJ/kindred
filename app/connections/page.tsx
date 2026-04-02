"use client";

import { useEffect, useState } from "react";
import { KindredAPI } from "@/lib/api";
import { Connection } from "@/lib/types";
import { EventHeader } from "@/components/shared";
import { BottomNav } from "@/components/CardAndNav";
import { Users, Clock, ArrowRight, MessageSquare, CheckCircle } from "lucide-react";
import Link from "next/link";

export default function ConnectionsPage() {
  const [connections, setConnections] = useState<Connection[]>([]);

  useEffect(() => {
    KindredAPI.getConnections().then(setConnections);
  }, []);

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark pb-32">
      <EventHeader eventName="HackWithChicago 3.0" avatarUrl="https://i.pravatar.cc/150?u=me" />
      
      <div className="p-6 flex flex-col gap-8 animate-in slide-in-from-bottom-8 duration-700">
        <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
                <Users size={20} className="text-kindred-purple" />
                <h1 className="text-2xl font-black text-white tracking-tighter">My Connections</h1>
            </div>
            <p className="text-xs text-white/40 leading-relaxed">
                People you've met and captured intelligence on during this event.
            </p>
        </div>

        {/* Connections List */}
        <div className="flex flex-col gap-6">
            {connections.length > 0 ? (
                connections.map((conn) => (
                    <div key={conn.id} className="flex flex-col gap-3 group animate-in fade-in zoom-in duration-500">
                        <div className="flex items-center justify-between px-1">
                            <div className="flex items-center gap-2 text-[8px] font-bold text-white/40 uppercase tracking-widest">
                                <Clock size={10} />
                                <span>Met {conn.timestamp}</span>
                            </div>
                            {conn.followupStatus === 'done' && (
                                <div className="flex items-center gap-1 text-[8px] font-black text-green-500 uppercase tracking-tighter">
                                    <CheckCircle size={10} />
                                    <span>Followed Up</span>
                                </div>
                            )}
                        </div>
                        
                        <Link href={`/person/${conn.attendee.id}`} className="block">
                            <div className="p-5 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all flex items-center gap-4 group-hover:border-kindred-purple/30">
                                <div className="w-12 h-12 rounded-xl border border-white/10 overflow-hidden">
                                    <img src={conn.attendee.avatar} alt={conn.attendee.name} className="w-full h-full object-cover" />
                                </div>
                                <div className="flex-1 min-w-0">
                                    <h3 className="text-sm font-black text-white">{conn.attendee.name}</h3>
                                    <p className="text-[10px] text-white/40 truncate">{conn.attendee.role} @ {conn.attendee.company}</p>
                                </div>
                                <ArrowRight size={16} className="text-white/20 group-hover:text-kindred-purple group-hover:translate-x-1 transition-all" />
                            </div>
                        </Link>

                        <div className="p-4 rounded-xl bg-kindred-purple/5 border-l border-kindred-purple/40">
                             <div className="flex items-center gap-2 mb-1">
                                <MessageSquare size={10} className="text-kindred-purple" />
                                <span className="text-[8px] font-bold text-kindred-purple uppercase tracking-widest">Capture Summary</span>
                             </div>
                             <p className="text-[10px] text-white/60 leading-relaxed line-clamp-2">
                                "{conn.summary}"
                             </p>
                        </div>
                    </div>
                ))
            ) : (
                <div className="mt-20 flex flex-col items-center gap-4 text-center opacity-30">
                    <Users size={48} className="text-white" />
                    <div className="flex flex-col gap-1">
                        <p className="text-sm font-black text-white tracking-tighter">No connections yet</p>
                        <p className="text-[10px] uppercase tracking-widest">Met people and capture voice to see them here.</p>
                    </div>
                </div>
            )}
        </div>
      </div>

      <BottomNav />
    </div>
  );
}
