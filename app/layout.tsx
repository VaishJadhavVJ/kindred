import type { Metadata } from "next";
import { Inter, Manrope } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const manrope = Manrope({
  variable: "--font-manrope",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Kindred — Networking Intelligence",
  description: "Your professional networking intelligence engine.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark scroll-smooth">
      <body
        className={`${inter.variable} ${manrope.variable} antialiased bg-kindred-dark text-foreground`}
      >
        {/* Mobile Viewport Simulation */}
        <div className="flex min-h-screen flex-col items-center justify-start overflow-x-hidden bg-black/20">
          <main className="w-full max-w-[375px] min-h-screen relative shadow-2xl bg-kindred-dark border-x border-white/5 overflow-y-auto overflow-x-hidden">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
