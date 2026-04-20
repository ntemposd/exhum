import type { ExecutionMetrics } from "@/lib/types";

export type LegendDetails = {
  agent_id: string;
  display_name: string;
  archetype: string;
};

export type DebateMessage = {
  id: string;
  agent_id: string;
  display_name: string;
  message: string;
  turn_number: number;
  created_at: string;
  isThinking?: boolean;
  failed?: boolean;
  execution_metrics?: ExecutionMetrics | null;
};