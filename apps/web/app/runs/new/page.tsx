import { Suspense } from "react";
import CycleBuilder from "./cycle-builder";
import { api } from "@/lib/api";

export default async function NewRunPage() {
  const [tests, targets] = await Promise.all([api.catalogue(), api.targets()]);
  return <><header className="pageHead"><div><div className="eyebrow">Step-by-step</div><h1>Create a test cycle</h1><p className="subtitle">Select approved catalogue objects. The backend validates compatibility and never accepts a free-text command.</p></div></header><Suspense fallback={<div className="empty">Loading cycle builder...</div>}><CycleBuilder tests={tests} targets={targets}/></Suspense></>;
}
