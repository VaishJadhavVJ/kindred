"use client";

import Link from "next/link";
import { Mail, Globe } from "lucide-react";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-kindred-dark p-8 pb-32">
      <div className="w-full flex flex-col items-center gap-12 animate-in fade-in slide-in-from-bottom-8 duration-700">
        <div className="text-center">
          <h1 className="text-3xl font-black text-white tracking-tighter">Welcome back</h1>
          <p className="mt-2 text-sm text-kindred-cyan font-bold tracking-wide uppercase">
            Sign in to find your best connections
          </p>
        </div>

        <div className="w-full flex flex-col gap-4">
          <Link href="/setup/profile" className="w-full">
            <button className="w-full py-4 px-6 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center gap-3 hover:bg-white/10 transition-all active:scale-95 group">
              <Mail size={20} className="text-[#0077b5]" />
              <span className="font-bold text-white/80">Sign in with LinkedIn</span>
            </button>
          </Link>

          <Link href="/setup/profile" className="w-full">
            <button className="w-full py-4 px-6 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center gap-3 hover:bg-white/10 transition-all active:scale-95">
              <Globe size={20} className="text-white" />
              <span className="font-bold text-white/80">Sign in with Google</span>
            </button>
          </Link>
        </div>

        <p className="text-[10px] text-white/30 text-center leading-relaxed">
          By signing in, you agree to our <span className="text-kindred-purple underline">Terms of Service</span> and <span className="text-kindred-purple underline">Privacy Policy</span>.
        </p>
      </div>

      <div className="absolute bottom-12 left-0 w-full text-center">
         <p className="text-xs text-white/40">New to Kindred? <span className="text-kindred-cyan font-bold">Create account</span></p>
      </div>
    </div>
  );
}
