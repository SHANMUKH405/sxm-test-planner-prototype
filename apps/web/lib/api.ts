import { RunRecord, Target, TestDefinition } from "./types";

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function read<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

export const api = {
  catalogue: () => read<TestDefinition[]>("/api/catalog"),
  targets: () => read<Target[]>("/api/targets"),
  runs: () => read<RunRecord[]>("/api/runs"),
  run: (id: string) => read<RunRecord>(`/api/runs/${id}`),
  createRun: async (payload: { name: string; test_ids: string[]; target_id: string }) => {
    const response = await fetch(`${API_BASE}/api/runs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error(await response.text());
    return response.json() as Promise<RunRecord>;
  },
};
