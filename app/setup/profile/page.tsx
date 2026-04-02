"use client";

import Link from "next/link";
import { User, Briefcase, Building, FileText } from "lucide-react";

const SKILLS = ["AI", "Full-stack", "Product", "Design", "Sales", "Investing", "Healthcare", "Web3"];
const INTERESTS = ["Sustainability", "Robotics", "Fintech", "BioTech", "EdTech", "SaaS"];

export default function ProfileSetupPage() {
  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark p-6 pb-32">
      <div className="flex flex-col gap-8 animate-in fade-in slide-in-from-right-8 duration-700">
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-end">
            <h1 className="text-2xl font-black text-white tracking-tighter">Build your profile</h1>
            <span className="text-[10px] font-bold text-kindred-purple uppercase tracking-widest">Step 1 of 3</span>
          </div>
          <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
            <div className="h-full bg-kindred-purple w-1/3" />
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <label className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Full Name</label>
            <div className="relative">
              <User size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30" />
              <input 
                type="text" 
                placeholder="Alex Sterling"
                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-sm text-white placeholder:text-white/20 focus:border-kindred-purple/50 focus:bg-white/10 transition-all outline-none"
              />
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Professional Role</label>
            <div className="relative">
              <Briefcase size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30" />
              <input 
                type="text" 
                placeholder="Lead Architect"
                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-sm text-white placeholder:text-white/20 focus:border-kindred-purple/50 focus:bg-white/10 transition-all outline-none"
              />
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Company / Org</label>
            <div className="relative">
              <Building size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30" />
              <input 
                type="text" 
                placeholder="Nexus Tech"
                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-sm text-white placeholder:text-white/20 focus:border-kindred-purple/50 focus:bg-white/10 transition-all outline-none"
              />
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Bio</label>
            <div className="relative">
              <FileText size={16} className="absolute left-4 top-4 text-white/30" />
              <textarea 
                rows={3}
                placeholder="Share a bit about what you're building..."
                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-sm text-white placeholder:text-white/20 focus:border-kindred-purple/50 focus:bg-white/10 transition-all outline-none resize-none"
              />
            </div>
          </div>

          <div className="flex flex-col gap-3">
            <label className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Select Skills</label>
            <div className="flex flex-wrap gap-2">
              {SKILLS.map(skill => (
                <button 
                  key={skill}
                  className="px-4 py-2 rounded-xl border border-white/10 bg-white/5 text-[10px] font-bold text-white/60 hover:border-kindred-cyan/50 hover:text-kindred-cyan hover:bg-white/10 transition-all"
                >
                  {skill}
                </button>
              ))}
            </div>
          </div>
        </div>

        <Link href="/setup/ask-offer" className="mt-8">
          <button className="w-full py-4 bg-kindred-purple text-white font-black rounded-2xl shadow-xl shadow-kindred-purple/20 hover:scale-[1.02] active:scale-95 transition-all">
            Next →
          </button>
        </Link>
      </div>
    </div>
  );
}
