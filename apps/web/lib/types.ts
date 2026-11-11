export type Driver = "headunit" | "sxm_emu" | "proxy" | "demo";
export type RunStatus = "queued" | "preparing" | "running" | "collecting_results" | "passed" | "failed" | "blocked" | "cancelled";

export interface TestDefinition {
  id: string;
  name: string;
  suite_name: string;
  suite_path: string;
  product_area: string;
  driver: Driver;
  tags: string[];
  case_id?: string | null;
  documentation: string;
  capabilities: string[];
  readiness: "ready" | "blocked" | "disabled";
  estimated_seconds: number;
}

export interface Target {
  id: string;
  name: string;
  status: string;
  target_type: string;
  driver: Driver;
  capabilities: string[];
  description: string;
}

export interface TestResult {
  test_id: string;
  name: string;
  status: RunStatus;
  elapsed_seconds: number;
  message: string;
}

export interface RunRecord {
  id: string;
  name: string;
  test_ids: string[];
  target_id: string;
  status: RunStatus;
  source_revision: string;
  created_at: string;
  started_at?: string | null;
  finished_at?: string | null;
  results: TestResult[];
  artifacts: string[];
  error?: string | null;
}
