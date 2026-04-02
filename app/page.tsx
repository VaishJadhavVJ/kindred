"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Sparkles } from "lucide-react";

export default function SplashPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
      router.push("/login");
    }, 3000);
    return () => clearTimeout(timer);
  }, [router]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-kindred-dark p-8 overflow-hidden relative">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] bg-kindred-purple/20 blur-[120px] rounded-full animate-pulse-slow" />
      
      <div className="relative flex flex-col items-center gap-6 animate-in fade-in zoom-in duration-1000">
        <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-kindred-purple to-kindred-cyan p-[2px] shadow-2xl shadow-kindred-purple/40">
          <div className="w-full h-full rounded-[22px] bg-kindred-dark flex items-center justify-center overflow-hidden relative">
            <NetworkIcon className="w-12 h-12 text-white glow-purple" />
          </div>
        </div>
        
        <div className="text-center">
          <h1 className="text-4xl font-black text-white tracking-tighter">Kindred</h1>
          <p className="mt-2 text-sm font-bold text-kindred-cyan uppercase tracking-widest animate-pulse">
            Your networking intelligence engine
          </p>
        </div>
      </div>

      <div className="absolute bottom-12 flex flex-col items-center gap-2">
        <div className="h-1 w-32 bg-white/5 rounded-full overflow-hidden">
          <div className="h-full bg-kindred-purple w-full animate-progress" />
        </div>
        <span className="text-[10px] font-bold text-white/20 uppercase tracking-widest">Initializing...</span>
      </div>

      <style jsx>{`
        @keyframes progress {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        .animate-progress {
          animation: progress 2s infinite ease-in-out;
        }
      `}</style>
    </div>
  );
}

function NetworkIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <circle cx="12" cy="12" r="3" />
      <circle cx="19" cy="5" r="2" />
      <circle cx="5" cy="19" r="2" />
      <circle cx="19" cy="19" r="2" />
      <circle cx="5" cy="5" r="2" />
      <path d="M12 12L19 5" />
      <path d="M12 12L5 19" />
      <path d="M12 12L19 19" />
      <path d="M12 12L5 5" />
    </svg>
  );
}
