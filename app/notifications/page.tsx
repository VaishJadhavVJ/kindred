"use client";

import { useEffect, useState } from "react";
import { KindredAPI } from "@/lib/api";
import { Notification } from "@/lib/types";
import { EventHeader } from "@/components/shared";
import { BottomNav } from "@/components/CardAndNav";
import { Bell, Sparkles, UserPlus, Info, CheckCircle2, MoreHorizontal } from "lucide-react";
import Link from "next/link";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  useEffect(() => {
    KindredAPI.getNotifications().then(setNotifications);
  }, []);

  const getIcon = (type: string) => {
    switch (type) {
        case 'match': return <Sparkles size={16} className="text-kindred-cyan" />;
        case 'proximity': return <UserPlus size={16} className="text-kindred-purple" />;
        case 'followup': return <CheckCircle2 size={16} className="text-kindred-purple" />;
        default: return <Info size={16} className="text-white/40" />;
    }
  };

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark pb-32">
      <EventHeader eventName="HackWithChicago 3.0" avatarUrl="https://i.pravatar.cc/150?u=me" />
      
      <div className="p-6 flex flex-col gap-8 animate-in slide-in-from-bottom-8 duration-700">
        <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
                <Bell size={20} className="text-kindred-purple" />
                <h1 className="text-2xl font-black text-white tracking-tighter">Activity Feed</h1>
            </div>
            <p className="text-xs text-white/40 leading-relaxed">
                Real-time intelligence alerts and community match updates.
            </p>
        </div>

        {/* Notifications List */}
        <div className="flex flex-col gap-4">
            {notifications.map((notif) => (
                <div 
                    key={notif.id} 
                    className={`p-5 rounded-2xl border flex items-start gap-4 transition-all animate-in fade-in zoom-in duration-500 ${
                        notif.type === 'match' ? 'bg-kindred-cyan/5 border-kindred-cyan/20 glow-cyan' : 'bg-white/5 border-white/10'
                    }`}
                >
                    <div className="p-2 rounded-xl bg-white/5 border border-white/10 shrink-0">
                        {getIcon(notif.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2 mb-1">
                            <span className="text-[10px] font-black text-white/40 uppercase tracking-tighter">{notif.type} Alert</span>
                            <span className="text-[8px] font-bold text-white/20 uppercase tracking-widest">{notif.timestamp}</span>
                        </div>
                        <p className="text-xs font-bold text-white/80 leading-relaxed mb-3">{notif.text}</p>
                        
                        {notif.relatedId && (
                            <Link href={`/person/${notif.relatedId}`}>
                                <button className="px-4 py-2 bg-kindred-purple text-white font-black rounded-lg text-[8px] uppercase tracking-widest shadow-lg shadow-kindred-purple/20 active:scale-95 transition-all">
                                    View Insight
                                </button>
                            </Link>
                        )}
                    </div>
                </div>
            ))}
        </div>

        {/* Older Context */}
        <div className="mt-12 flex flex-col gap-4">
            <h4 className="text-[10px] font-bold text-white/20 uppercase tracking-widest pl-1">Earlier Feed</h4>
            <div className="p-4 rounded-xl border border-dashed border-white/5 flex items-center justify-center text-center opacity-30">
                <MoreHorizontal size={16} className="text-white" />
            </div>
        </div>
      </div>

      <BottomNav />
    </div>
  );
}
