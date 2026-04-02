"use client";

import { useEffect, useState } from "react";
import { KindredAPI } from "@/lib/api";
import { Attendee } from "@/lib/types";
import { PersonCard, BottomNav } from "@/components/CardAndNav";
import { Search, Filter, X, Sparkles, FilterIcon } from "lucide-react";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Attendee[]>([]);
  const [isFiltering, setIsFiltering] = useState(false);

  useEffect(() => {
    KindredAPI.getRecommendations().then(setResults);
  }, []);

  const filteredResults = results.filter(r => 
    r.name.toLowerCase().includes(query.toLowerCase()) || 
    r.role.toLowerCase().includes(query.toLowerCase()) ||
    r.company.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark pb-32">
      <header className="p-6 pb-2 sticky top-0 bg-kindred-dark/80 backdrop-blur-md z-50">
          <div className="flex flex-col gap-4">
              <h1 className="text-2xl font-black text-white tracking-tighter">Search Nodes</h1>
              <div className="relative">
                  <Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30" />
                  <input 
                    type="text" 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search by name, role, or skill..."
                    className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-12 text-sm text-white placeholder:text-white/20 focus:border-kindred-cyan/50 focus:bg-white/10 transition-all outline-none"
                  />
                  {query && (
                    <button onClick={() => setQuery("")} className="absolute right-4 top-1/2 -translate-y-1/2 text-white/40">
                        <X size={16} />
                    </button>
                  )}
              </div>
          </div>
      </header>

      <div className="px-6 py-4 flex flex-wrap gap-2">
          {["All", "Investors", "Engineers", "Designers", "Founders"].map(tag => (
              <button 
                key={tag}
                className={`px-4 py-2 rounded-xl border text-[10px] font-bold uppercase tracking-tight transition-all ${
                    tag === "All" ? "border-kindred-cyan bg-kindred-cyan/10 text-kindred-cyan" : "border-white/10 bg-white/5 text-white/40"
                }`}
              >
                  {tag}
              </button>
          ))}
          <button onClick={() => setIsFiltering(!isFiltering)} className="ml-auto p-2 rounded-xl bg-white/5 border border-white/10 text-white/40">
              <FilterIcon size={14} />
          </button>
      </div>

      <div className="p-6 flex flex-col gap-6">
          <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-white/40 uppercase tracking-widest pl-1">{filteredResults.length} Intelligence Hits</span>
              <div className="flex items-center gap-1 group cursor-pointer">
                  <span className="text-[8px] font-black text-kindred-purple uppercase tracking-tighter">Sorted by Score</span>
                  <Sparkles size={10} className="text-kindred-purple group-hover:animate-pulse" />
              </div>
          </div>

          <div className="flex flex-col gap-4 animate-in fade-in slide-in-from-bottom-8 duration-700">
              {filteredResults.map((attendee) => (
                <PersonCard 
                    key={attendee.id}
                    id={attendee.id}
                    name={attendee.name}
                    role={attendee.role}
                    company={attendee.company}
                    avatar={attendee.avatar}
                    matchScore={attendee.matchScore}
                    reason={attendee.matchReason}
                />
              ))}
          </div>
      </div>

      <BottomNav />
    </div>
  );
}
