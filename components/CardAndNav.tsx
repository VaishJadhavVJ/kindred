"use client";

import { Home, Users, Network, User, Search, MessageSquare, Bell } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export const BottomNav = () => {
  const pathname = usePathname();

  const navItems = [
    { icon: Home, label: "Home", href: "/home" },
    { icon: Network, label: "Graph", href: "/graph" },
    { icon: Users, label: "Circles", href: "/circles" },
    { icon: Bell, label: "Alerts", href: "/notifications" },
    { icon: User, label: "Profile", href: "/profile" },
  ];

  return (
    <nav className="fixed bottom-0 w-full max-w-[375px] bg-kindred-dark/95 backdrop-blur-xl border-t border-white/10 px-6 py-3 flex justify-between items-center z-50">
      {navItems.map((item) => {
        const isActive = pathname === item.href;
        const Icon = item.icon;
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`flex flex-col items-center gap-1 transition-all ${
              isActive ? "text-kindred-cyan" : "text-white/40 hover:text-white/60"
            }`}
          >
            <Icon size={20} strokeWidth={isActive ? 2.5 : 2} className={isActive ? "glow-cyan" : ""} />
            <span className="text-[10px] font-medium tracking-tighter">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
};

interface PersonCardProps {
  id: string;
  name: string;
  role: string;
  company: string;
  avatar: string;
  matchScore: number;
  reason?: string;
}

export const PersonCard = ({ id, name, role, company, avatar, matchScore, reason }: PersonCardProps) => {
  return (
    <Link href={`/person/${id}`} className="block">
      <div className="w-full p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all group">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-lg overflow-hidden border border-kindred-purple/30">
            <img src={avatar} alt={name} className="w-full h-full object-cover" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-sm font-bold text-white truncate">{name}</h3>
            <p className="text-[10px] text-white/50 truncate">
              {role} @ {company}
            </p>
          </div>
          <div className="text-right">
            <div className="text-xs font-black text-kindred-cyan">{matchScore}%</div>
            <div className="text-[8px] uppercase tracking-tighter text-white/30 font-bold">Match</div>
          </div>
        </div>
        {reason && (
          <div className="mt-3 pt-3 border-t border-white/5 flex items-start gap-2">
            <p className="text-[10px] text-kindred-purple/80 italic line-clamp-1">"{reason}"</p>
          </div>
        )}
      </div>
    </Link>
  );
};
