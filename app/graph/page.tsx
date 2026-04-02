"use client";

import { useState } from "react";
import { ArrowLeft, Maximize2, Minimize2, ZoomIn, ZoomOut, Database, Layers } from "lucide-react";
import { useRouter } from "next/navigation";

export default function GraphPage() {
  const router = useRouter();
  const [zoom, setZoom] = useState(1);

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark relative overflow-hidden">
      {/* Immersive Graph Background */}
      <div className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_50%_50%,rgba(58,223,250,0.05),transparent_80%)]" />
      
      {/* Graph Content (Simulation) */}
      <div 
        className="absolute inset-0 flex items-center justify-center transition-transform duration-500 ease-out z-10"
        style={{ transform: `scale(${zoom})` }}
      >
        <div className="relative w-[800px] h-[800px]">
           {/* Center Node (You) */}
           <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-kindred-cyan border-4 border-kindred-cyan/20 glow-cyan z-30" />
           
           {/* Edge Connections (SVG) */}
           <svg className="absolute inset-0 w-full h-full">
              {[...Array(12)].map((_, i) => (
                <line 
                   key={i}
                   x1="50%" y1="50%" 
                   x2={`${50 + 30 * Math.cos(2 * Math.PI * i / 12)}%`}
                   y2={`${50 + 30 * Math.sin(2 * Math.PI * i / 12)}%`}
                   className="stroke-kindred-purple/20 stroke-1"
                />
              ))}
           </svg>

           {/* Neighbor Nodes */}
           {[...Array(12)].map((_, i) => (
              <div 
                key={i}
                className="absolute w-4 h-4 rounded-full bg-kindred-purple border border-kindred-purple/40 glow-purple z-20 group cursor-pointer hover:scale-125 transition-all"
                style={{ 
                  top: `${50 + 30 * Math.sin(2 * Math.PI * i / 12)}%`, 
                  left: `${50 + 30 * Math.cos(2 * Math.PI * i / 12)}%`
                }}
              >
                  <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 bg-kindred-dark/80 px-2 py-1 rounded text-[8px] text-white whitespace-nowrap">
                      Intelligence Node #{i + 1}
                  </div>
              </div>
           ))}
        </div>
      </div>

      {/* Interface Overlay */}
      <header className="fixed top-0 w-full p-4 flex items-center justify-between z-50">
        <button onClick={() => router.back()} className="p-2 rounded-lg bg-kindred-dark/80 backdrop-blur-md border border-white/10 text-white/60">
            <ArrowLeft size={20} />
        </button>
        <div className="px-4 py-2 rounded-full bg-kindred-dark/80 backdrop-blur-md border border-white/10 flex items-center gap-2">
            <Layers size={14} className="text-kindred-cyan" />
            <span className="text-[10px] font-black text-white uppercase tracking-widest">Full Network Graph</span>
        </div>
        <div className="w-10" /> {/* Spacer */}
      </header>

      {/* Bottom Controls */}
      <div className="fixed bottom-12 left-0 w-full px-6 z-50 flex items-end justify-between pointer-events-none">
          <div className="pointer-events-auto flex flex-col gap-2">
              <button 
                onClick={() => setZoom(z => Math.min(z + 0.2, 2.5))}
                className="p-3 rounded-lg bg-kindred-dark/80 backdrop-blur-md border border-white/10 text-white/60 hover:text-white transition-all shadow-xl"
              >
                <ZoomIn size={20} />
              </button>
              <button 
                onClick={() => setZoom(z => Math.max(z - 0.2, 0.5))}
                className="p-3 rounded-lg bg-kindred-dark/80 backdrop-blur-md border border-white/10 text-white/60 hover:text-white transition-all shadow-xl"
              >
                <ZoomOut size={20} />
              </button>
          </div>

          <div className="pointer-events-auto flex flex-col gap-4">
              <div className="p-4 rounded-2xl bg-kindred-dark/80 backdrop-blur-md border border-white/10 flex flex-col gap-2 max-w-[200px]">
                  <div className="flex items-center justify-between">
                     <span className="text-[8px] font-bold text-white/40 uppercase tracking-widest">Active Nodes</span>
                     <span className="text-[10px] font-black text-kindred-cyan">1,204</span>
                  </div>
                  <div className="flex items-center justify-between">
                     <span className="text-[8px] font-bold text-white/40 uppercase tracking-widest">Match Density</span>
                     <span className="text-[10px] font-black text-kindred-purple">High</span>
                  </div>
              </div>
              <button className="w-full py-4 bg-kindred-purple text-white font-black rounded-2xl text-[10px] uppercase tracking-widest shadow-xl shadow-kindred-purple/20">
                  Global Cluster View
              </button>
          </div>
      </div>

      {/* Database Status */}
      <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 opacity-40">
          <Database size={12} className="text-kindred-cyan" />
          <span className="text-[8px] font-bold text-white uppercase tracking-tighter">Connected to Neo4j AuraDB</span>
      </div>
    </div>
  );
}
