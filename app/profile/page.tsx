"use client";

import { EventHeader } from "@/components/shared";
import { BottomNav } from "@/components/CardAndNav";
import { User, Shield, Bell, Settings, LogOut, ChevronRight, Moon, Network, Sparkles } from "lucide-react";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const router = useRouter();

  const handleLogout = () => {
    router.push("/login");
  };

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark pb-32">
      <EventHeader eventName="HackWithChicago 3.0" avatarUrl="https://i.pravatar.cc/150?u=me" />
      
      <div className="p-6 flex flex-col gap-8 animate-in slide-in-from-bottom-8 duration-700">
        {/* User Card */}
        <div className="p-6 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-between">
            <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl border-2 border-kindred-purple overflow-hidden">
                    <img src="https://i.pravatar.cc/150?u=me" alt="Me" className="w-full h-full object-cover" />
                </div>
                <div className="flex flex-col">
                    <h1 className="text-xl font-black text-white leading-tight">Alex Sterling</h1>
                    <p className="text-xs text-kindred-purple/80 font-bold uppercase tracking-wide">Lead Architect @ Nexus Tech</p>
                </div>
            </div>
            <button className="p-3 bg-white/5 border border-white/10 rounded-xl text-white/40">
                <Settings size={20} />
            </button>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-kindred-purple/5 border border-kindred-purple/20 flex flex-col gap-1">
                <span className="text-[8px] font-bold text-kindred-purple uppercase tracking-widest pl-1">Network Score</span>
                <div className="flex items-baseline gap-2">
                    <span className="text-2xl font-black text-white">884</span>
                    <Sparkles size={14} className="text-kindred-purple" />
                </div>
            </div>
            <div className="p-4 rounded-xl bg-kindred-cyan/5 border border-kindred-cyan/20 flex flex-col gap-1">
                <span className="text-[8px] font-bold text-kindred-cyan uppercase tracking-widest pl-1">Knowledge Nodes</span>
                <div className="flex items-baseline gap-2">
                    <span className="text-2xl font-black text-white">12</span>
                    <Network size={14} className="text-kindred-cyan" />
                </div>
            </div>
        </div>

        {/* Settings Sections */}
        <div className="flex flex-col gap-6">
            <div className="flex flex-col gap-3">
                <h3 className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Networking Preferences</h3>
                <div className="flex flex-col gap-2">
                    {[
                        { icon: User, label: "Edit Profile Info" },
                        { icon: Sparkles, label: "Intelligence Match Algorithm" },
                        { icon: Bell, label: "Alert Settings" },
                    ].map(item => (
                        <div key={item.label} className="p-4 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between group cursor-pointer hover:bg-white/10 transition-all">
                            <div className="flex items-center gap-3">
                                <item.icon size={16} className="text-white/40 group-hover:text-kindred-cyan" />
                                <span className="text-xs font-bold text-white/80">{item.label}</span>
                            </div>
                            <ChevronRight size={14} className="text-white/20" />
                        </div>
                    ))}
                </div>
            </div>

            <div className="flex flex-col gap-3">
                <h3 className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">Account & Privacy</h3>
                <div className="flex flex-col gap-2">
                    {[
                        { icon: Shield, label: "Data & Privacy Controls" },
                        { icon: Moon, label: "Dark Theme (Neural Mode)" },
                    ].map(item => (
                        <div key={item.label} className="p-4 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between group cursor-pointer hover:bg-white/10 transition-all">
                            <div className="flex items-center gap-3">
                                <item.icon size={16} className="text-white/40 group-hover:text-kindred-purple" />
                                <span className="text-xs font-bold text-white/80">{item.label}</span>
                            </div>
                            <div className="w-8 h-4 bg-kindred-purple rounded-full relative">
                                <div className="absolute right-0.5 top-0.5 w-3 h-3 bg-white rounded-full shadow-sm" />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>

        {/* Action Button */}
        <button 
           onClick={handleLogout}
           className="mt-8 w-full py-4 bg-white/5 border border-red-500/20 text-red-500/80 font-black rounded-2xl flex items-center justify-center gap-2 hover:bg-red-500/10 active:scale-95 transition-all"
        >
            <LogOut size={18} />
            Sign Out
        </button>

        <div className="mt-8 text-center flex flex-col gap-1">
            <p className="text-[8px] font-bold text-white/10 uppercase tracking-widest leading-loose">Kindred Intelligence Engine v1.0.4-beta</p>
            <p className="text-[8px] text-white/10 leading-loose">Building the future of human connectivity.</p>
        </div>
      </div>

      <BottomNav />
    </div>
  );
}
