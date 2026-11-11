import { RunStatus } from "@/lib/types";

export function Status({ value }: { value: RunStatus | string }) {
  const cls = value === "passed" || value === "ready" || value === "available" ? "pass" : value === "failed" || value === "blocked" ? "fail" : "run";
  return <span className={`chip ${cls}`}>{value.replaceAll("_", " ").toUpperCase()}</span>;
}
