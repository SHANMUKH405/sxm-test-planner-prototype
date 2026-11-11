import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "SXM Test Planner",
  description: "Simulator-first visual Robot Framework test planner",
};

const nav = [
  ["Dashboard", "/"],
  ["Test Catalogue", "/catalog"],
  ["Create Cycle", "/runs/new"],
  ["Run History", "/runs"],
  ["Targets", "/targets"],
  ["Architecture", "/architecture"],
];

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <div className="appShell">
          <aside className="sidebar">
            <div className="brandMark">S</div>
            <div>
              <div className="brand">SXM Test Planner</div>
              <div className="brandSub">Prototype workspace</div>
            </div>
            <nav>{nav.map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}</nav>
            <div className="boundary"><strong>Simulator first</strong><span>No real DUT control</span></div>
          </aside>
          <main className="main">{children}</main>
        </div>
      </body>
    </html>
  );
}
