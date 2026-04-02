"use client";

import { useState } from "react";
import Link from "next/link";
import { QrCode, ArrowRight, Calendar, MapPin } from "lucide-react";

export default function JoinEventPage() {
  const [code, setCode] = useState("");

  const showPreview = code.toUpperCase() === "CHI-3";

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark p-6 pb-32">
      <div className="flex flex-col gap-8 animate-in fade-in slide-in-from-right-8 duration-700">
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-end">
            <h1 className="text-2xl font-black text-white tracking-tighter">Join an Event</h1>
            <span className="text-[10px] font-bold text-kindred-purple uppercase tracking-widest">Step 3 of 3</span>
          </div>
          <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
            <div className="h-full bg-kindred-purple w-full" />
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <label className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Enter event code</label>
            <div className="relative">
              <input 
                type="text" 
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="e.g. CHI-3"
                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 px-6 text-2xl font-black tracking-widest text-white placeholder:text-white/20 focus:border-kindred-purple/50 focus:bg-white/10 transition-all outline-none"
              />
            </div>
          </div>

          <div className="w-full flex items-center gap-4">
             <div className="h-px flex-1 bg-white/5" />
             <span className="text-[10px] font-bold text-white/20 uppercase tracking-widest">OR</span>
             <div className="h-px flex-1 bg-white/5" />
          </div>

          <button className="w-full py-4 border border-white/10 rounded-2xl bg-white/5 flex items-center justify-center gap-3 hover:bg-white/10 transition-all group">
            <QrCode size={20} className="text-kindred-cyan" />
            <span className="font-bold text-white/60">Scan QR Code</span>
          </button>
        </div>

        {showPreview ? (
          <div className="flex flex-col gap-4 animate-in fade-in zoom-in duration-500">
            <div className="p-6 rounded-2xl bg-gradient-to-br from-kindred-purple/20 to-kindred-cyan/20 border border-white/10 relative overflow-hidden backdrop-blur-sm">
                <div className="absolute top-0 right-0 p-4">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                </div>
                <h3 className="text-xl font-black text-white leading-tight">HackWithChicago 3.0</h3>
                <div className="mt-4 flex flex-col gap-2">
                  <div className="flex items-center gap-2 text-white/60 text-xs">
                    <Calendar size={14} className="text-kindred-purple" />
                    <span>April 2, 2026</span>
                  </div>
                  <div className="flex items-center gap-2 text-white/60 text-xs">
                    <MapPin size={14} className="text-kindred-cyan" />
                    <span>Chicago, IL</span>
                  </div>
                </div>
            </div>
            
            <Link href="/home" className="w-full">
              <button className="w-full py-4 bg-kindred-purple text-white font-black rounded-2xl shadow-xl shadow-kindred-purple/40 active:scale-95 transition-all">
                Enter Now →
              </button>
            </Link>
          </div>
        ) : (
          <div className="mt-4 flex flex-col gap-4">
            <h4 className="text-[10px] font-bold text-white/20 uppercase tracking-widest pl-1">Nearby Events</h4>
            {["Foundery Summit", "TechExpo"].map(event => (
               <div key={event} className="p-4 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between opacity-50">
                  <span className="text-xs font-bold text-white/60">{event}</span>
                  <ArrowRight size={14} className="text-white/20" />
               </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
