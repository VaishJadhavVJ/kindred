"use client";

import { useState, useEffect } from "react";
import { Mic, MicOff, X, Sparkles, CheckCircle2 } from "lucide-react";
import { useRouter } from "next/navigation";

export default function VoiceCapturePage() {
  const router = useRouter();
  const [isRecording, setIsRecording] = useState(true);
  const [status, setStatus] = useState<'recording' | 'processing' | 'done'>('recording');
  const [transcript, setTranscript] = useState("");

  useEffect(() => {
     if (status === 'processing') {
        const timer = setTimeout(() => {
           setStatus('done');
           setTranscript("Discussed clinical trial data sharing models and potential collaboration on the next Stanford dataset...");
        }, 3000);
        return () => clearTimeout(timer);
     }
  }, [status]);

  const handleStop = () => {
    setIsRecording(false);
    setStatus('processing');
  };

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark p-8 relative overflow-hidden">
      {/* Background Pulse Glow */}
      <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] blur-[100px] rounded-full transition-all duration-1000 ${
        status === 'recording' ? 'bg-kindred-cyan/10 animate-pulse' : 
        status === 'processing' ? 'bg-kindred-purple/10 animate-pulse-slow' : 
        'bg-green-500/5'
      }`} />

      <header className="flex justify-end p-2 relative z-10">
        <button onClick={() => router.back()} className="p-2 rounded-full bg-white/5 border border-white/10 text-white/40">
          <X size={24} />
        </button>
      </header>

      <div className="flex-1 flex flex-col items-center justify-center gap-12 relative z-10">
        <div className="text-center flex flex-col gap-2">
            <h1 className="text-3xl font-black text-white tracking-tighter">
                {status === 'recording' ? "Listening..." : 
                 status === 'processing' ? "Analyzing Intelligence" : 
                 "Capture Complete"}
            </h1>
            <p className="text-xs font-bold text-kindred-cyan uppercase tracking-widest animate-pulse">
                {status === 'recording' ? "Neural Capture Active" : 
                 status === 'processing' ? "Running Graph Pipeline" : 
                 "Insights Generated"}
            </p>
        </div>

        {/* Visualizer / Record Button */}
        <div className="relative flex items-center justify-center">
             {status === 'recording' && (
                <div className="absolute w-48 h-48 border border-kindred-cyan/30 rounded-full animate-ping" />
             )}
             <button 
                onClick={status === 'recording' ? handleStop : undefined}
                className={`w-32 h-32 rounded-full flex items-center justify-center transition-all duration-500 ${
                    status === 'recording' ? 'bg-kindred-cyan text-kindred-dark glow-cyan scale-110' : 
                    status === 'processing' ? 'bg-kindred-purple/20 border-2 border-kindred-purple text-kindred-purple glow-purple animate-pulse' : 
                    'bg-green-500 text-white shadow-xl shadow-green-500/20'
                }`}
             >
                {status === 'recording' ? <MicOff size={48} /> : 
                 status === 'processing' ? <Sparkles size={48} /> : 
                 <CheckCircle2 size={48} />}
             </button>
        </div>

        {/* Live Transcript / Result */}
        <div className="w-full max-w-[300px] min-h-[100px] p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md">
            {status === 'recording' ? (
                <div className="flex flex-col gap-4">
                  <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full bg-kindred-cyan/40 w-1/2 animate-[progress_1.5s_infinite]" />
                  </div>
                  <p className="text-[10px] text-white/20 text-center uppercase font-bold tracking-widest italic">Capturing conversation audio...</p>
                </div>
            ) : status === 'processing' ? (
                <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 bg-kindred-purple rounded-full animate-bounce" />
                    <span className="text-[10px] font-bold text-white/40 uppercase tracking-widest">Querying Neo4j...</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 bg-kindred-cyan rounded-full animate-bounce [animation-delay:0.2s]" />
                    <span className="text-[10px] font-bold text-white/40 uppercase tracking-widest">RocketRide LLM active...</span>
                  </div>
                </div>
            ) : (
                <div className="flex flex-col gap-4 animate-in fade-in slide-in-from-bottom-4">
                    <p className="text-xs text-white/80 leading-relaxed italic line-clamp-3">"{transcript}"</p>
                    <button 
                      onClick={() => router.push('/followups')}
                      className="w-full py-3 bg-kindred-purple text-white font-black rounded-xl text-[10px] uppercase tracking-widest shadow-lg shadow-kindred-purple/20 active:scale-95 transition-all"
                    >
                        View Insights
                    </button>
                </div>
            )}
        </div>
      </div>

      <style jsx>{`
        @keyframes progress {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(200%); }
        }
      `}</style>
    </div>
  );
}
