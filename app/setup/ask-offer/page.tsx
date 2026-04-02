"use client";

import Link from "next/link";
import { HelpCircle, Gift } from "lucide-react";

const ASKS = ["Find internship", "Get funding advice", "Hire engineers", "Co-founder search", "Technical mentor", "GTM Strategy"];
const OFFERS = ["Can mentor", "Can refer at startup", "Investor intro", "Code review", "Growth strategy", "Design feedback"];

export default function AskOfferPage() {
  return (
    <div className="flex min-h-screen flex-col bg-kindred-dark p-6 pb-32">
      <div className="flex flex-col gap-8 animate-in fade-in slide-in-from-right-8 duration-700">
        <div className="flex flex-col gap-2">
          <div className="flex justify-between items-end">
            <h1 className="text-2xl font-black text-white tracking-tighter">Your Goals</h1>
            <span className="text-[10px] font-bold text-kindred-purple uppercase tracking-widest">Step 2 of 3</span>
          </div>
          <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
            <div className="h-full bg-kindred-purple w-2/3" />
          </div>
        </div>

        <p className="text-xs text-white/40 leading-relaxed">
          Select at least one ask and one offer to help our intelligence engine find your best matches.
        </p>

        <div className="flex flex-col gap-10">
          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-2 pl-1">
              <HelpCircle size={16} className="text-kindred-cyan" />
              <h2 className="text-[10px] font-bold text-white uppercase tracking-widest">What do you need? (Asks)</h2>
            </div>
            <div className="flex flex-wrap gap-2">
              {ASKS.map(ask => (
                <button 
                  key={ask}
                  className="px-4 py-2 rounded-xl border border-white/10 bg-white/5 text-[10px] font-bold text-white/60 hover:border-kindred-cyan hover:text-kindred-cyan hover:bg-white/10 transition-all hover:scale-[1.02] active:scale-95"
                >
                  {ask}
                </button>
              ))}
            </div>
          </div>

          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-2 pl-1">
              <Gift size={16} className="text-kindred-purple" />
              <h2 className="text-[10px] font-bold text-white uppercase tracking-widest">What can you offer? (Offers)</h2>
            </div>
            <div className="flex flex-wrap gap-2">
              {OFFERS.map(offer => (
                <button 
                  key={offer}
                  className="px-4 py-2 rounded-xl border border-white/10 bg-white/5 text-[10px] font-bold text-white/60 hover:border-kindred-purple hover:text-kindred-purple hover:bg-white/10 transition-all hover:scale-[1.02] active:scale-95"
                >
                  {offer}
                </button>
              ))}
            </div>
          </div>
        </div>

        <Link href="/setup/join-event" className="mt-8">
          <button className="w-full py-4 bg-kindred-purple text-white font-black rounded-2xl shadow-xl shadow-kindred-purple/20 hover:scale-[1.02] active:scale-95 transition-all">
            Next →
          </button>
        </Link>
      </div>
    </div>
  );
}
