import Link from "next/link";
import { api } from "@/lib/api";
import { Status } from "@/components/status";

export default async function Dashboard() {
  const [tests, targets, runs] = await Promise.all([api.catalogue(), api.targets(), api.runs()]);
  const running = runs.filter(run => ["queued", "preparing", "running", "collecting_results"].includes(run.status)).length;
  const passed = runs.filter(run => run.status === "passed").length;
  return <>
    <header className="pageHead"><div><div className="eyebrow">Simulator-first prototype</div><h1>Execution overview</h1><p className="subtitle">Select existing Robot tests visually, start an approved run, and inspect individual results without entering commands.</p></div><Link className="button" href="/runs/new">Create test cycle</Link></header>
    <div className="stats"><div className="stat"><b>{tests.length}</b><span>Discovered tests</span></div><div className="stat"><b>{targets.filter(t=>t.status==="available").length}</b><span>Available targets</span></div><div className="stat"><b>{running}</b><span>Active runs</span></div><div className="stat"><b>{passed}</b><span>Passed cycles</span></div></div>
    <div className="twoCol"><section className="panel" style={{padding:20}}><div className="sectionTitle"><h2>How the prototype works</h2></div><div className="flow"><div className="flowBox">Robot scripts</div><span className="arrow">→</span><div className="flowBox">Catalogue</div><span className="arrow">→</span><div className="flowBox">Select</div><span className="arrow">→</span><div className="flowBox">Run</div><span className="arrow">→</span><div className="flowBox">Results</div></div><div className="warning"><strong>Boundary:</strong> the default runner is simulated. No real DUT or driver is controlled.</div></section><section className="panel" style={{padding:20}}><div className="sectionTitle"><h2>Recent cycles</h2><Link href="/runs">View all</Link></div>{runs.length === 0 ? <div className="empty">No cycle has run yet.</div> : runs.slice(0,4).map(run=><div className="resultRow" key={run.id}><div><strong>{run.name}</strong><div className="meta">{run.id} · {run.source_revision}</div></div><Status value={run.status}/><span className="meta">{run.results.length} results</span></div>)}</section></div>
  </>;
}
