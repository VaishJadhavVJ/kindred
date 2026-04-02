"use client";

import { useEffect, useState, use } from "react";
import { KindredAPI } from "@/lib/api";
import { Attendee } from "@/lib/types";
import { SerendipityBadge } from "@/components/shared";
import { WarmPathBreadcrumb, FollowUpTabs } from "@/components/DetailsAndCircles";
import { ArrowLeft, MessageSquare, Mic, Copy, Send, Mail } from "lucide-react";
import { useRouter } from "next/navigation";

export default function PersonDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const [attendee, setAttendee] = useState<Attendee | null>(null);

  useEffect(() => {
    KindredAPI.getAttendee(id).then((a) => setAttendee(a || null));
  }, [id]);

  if (!attendee) return null;

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark pb-32">
      <header className="w-full px-4 py-4 flex items-center justify-between sticky top-0 bg-kindred-dark/80 backdrop-blur-md z-50">
        <button onClick={() => router.back()} className="p-2 rounded-lg bg-white/5 border border-white/10 text-white/60">
          <ArrowLeft size={20} />
        </button>
        <div className="flex flex-col items-center">
          <span className="text-[10px] font-black text-white">{attendee.name}</span>
          <span className="text-[8px] text-white/40 uppercase tracking-tighter">Match Insight</span>
        </div>
        <button className="p-2 rounded-lg bg-white/5 border border-white/10 text-kindred-purple">
          <Mail size={20} />
        </button>
      </header>

      <div className="p-6 flex flex-col gap-8 animate-in slide-in-from-right-12 duration-700">
        {/* Profile Info */}
        <div className="flex flex-col items-center gap-4 text-center">
          <div className="relative">
             <div className="w-32 h-32 rounded-3xl overflow-hidden border-2 border-white/10">
                <img src={attendee.avatar} alt={attendee.name} className="w-full h-full object-cover" />
             </div>
             <div className="absolute -bottom-4 right-1/2 translate-x-1/2">
                <SerendipityBadge score={attendee.serendipityScore} size="lg" />
             </div>
          </div>
          
          <div className="mt-4">
            <h2 className="text-2xl font-black text-white tracking-tighter">{attendee.name}</h2>
            <p className="text-sm font-bold text-kindred-purple/80 uppercase tracking-wide">
               {attendee.role} @ {attendee.company}
            </p>
          </div>
        </div>

        {/* Warm Path */}
        <div className="flex flex-col gap-4">
          <h3 className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Warm Connection Path</h3>
          <div className="p-5 rounded-2xl bg-white/5 border border-white/10">
            <WarmPathBreadcrumb path={attendee.warmPath || ["You", attendee.name]} />
          </div>
        </div>

        {/* Graph Insight */}
        <div className="flex flex-col gap-4">
          <h3 className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Intelligence Insight</h3>
          <div className="p-5 rounded-2xl bg-white/5 border border-white/10 flex flex-col gap-3">
             <p className="text-xs text-white/80 leading-relaxed italic border-l-2 border-kindred-cyan pl-4">
                "{attendee.matchReason}"
             </p>
             <p className="text-[10px] text-white/40 leading-relaxed">
                Found shared research at Stanford and overlapping interests in climate-neutral AI.
             </p>
          </div>
        </div>

        {/* Icebreaker */}
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between px-1">
            <h3 className="text-[10px] font-bold text-white/40 uppercase tracking-widest">Icebreaker</h3>
            <button className="text-[10px] font-bold text-kindred-cyan flex items-center gap-1 hover:brightness-110 active:scale-95 transition-all">
              <Copy size={12} /> COPY
            </button>
          </div>
          <div className="p-5 rounded-2xl bg-gradient-to-br from-kindred-purple/20 to-kindred-cyan/20 border border-white/10 relative overflow-hidden backdrop-blur-md">
             <p className="text-sm font-black text-white leading-relaxed">
                "Hey {attendee.name.split(' ')[0]}, I saw we both have context on clinical LLM bias. What's your take on the latest Stanford healthcare benchmark?"
             </p>
          </div>
        </div>

        {/* Follow-up Variants */}
        <div className="flex flex-col gap-4">
            <h3 className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Follow-up Variants</h3>
            <FollowUpTabs />
            <div className="p-5 rounded-2xl bg-white/5 border border-white/10 flex flex-col gap-4">
               <p className="text-xs text-white/60 leading-relaxed">
                  "Great meeting you at HackChicago! Would love to compare notes on those clinical trial datasets you mentioned. Drinks next week?"
               </p>
               <div className="flex gap-2">
                  <button className="flex-1 py-3 bg-kindred-purple/20 border border-kindred-purple/40 text-kindred-purple font-black rounded-xl text-[10px] uppercase tracking-widest hover:bg-kindred-purple/30 active:scale-95 transition-all">
                    Copy Message
                  </button>
                  <button className="flex-1 py-3 bg-kindred-purple text-white font-black rounded-xl text-[10px] uppercase tracking-widest hover:bg-kindred-purple-dim shadow-lg shadow-kindred-purple/20 active:scale-95 transition-all">
                    Send Link
                  </button>
               </div>
            </div>
        </div>
      </div>

      {/* Floating Record Button */}
      <div className="fixed bottom-12 right-12 z-50">
          <button 
            onClick={() => router.push('/voice')}
            className="w-16 h-16 rounded-full bg-kindred-cyan text-kindred-dark flex items-center justify-center glow-cyan shadow-xl hover:scale-110 active:scale-90 transition-all group"
          >
            <Mic size={24} className="group-hover:animate-pulse" />
          </button>
      </div>
    </div>
  );
}
