import type { ExecutionMetrics, ServiceStatus } from "@/lib/types";

import type { DebateMessage } from "./types";
import { SidebarSection } from "./sidebar-section";

const SESSION_COST_HELPER_TEXT = "Spend estimate based on token volume.";

type TelemetryTableRow = Record<string, string>;

type RoleBreakdownEntry = {
  label: string;
  words: number;
  share: number;
};

type TelemetryPanelProps = {
  debateEntropy: number | null;
  sessionBurnUsd: number;
  telemetryError: string;
  transcriptTokenEstimate: number;
  messages: DebateMessage[];
  roleBreakdown: RoleBreakdownEntry[];
  servicesError: string;
  onlineServices: number;
  serviceRows: ServiceStatus[];
};

export function TelemetryPanel({
  debateEntropy,
  sessionBurnUsd,
  telemetryError,
  transcriptTokenEstimate,
  messages,
  roleBreakdown,
  servicesError,
  onlineServices,
  serviceRows,
}: TelemetryPanelProps) {
  const metricsHistory = messages
    .map((message) => message.execution_metrics)
    .filter((metrics): metrics is ExecutionMetrics => Boolean(metrics));

  const requestRows = metricsHistory.map((metrics, index) => {
    const prompt = Number(metrics.prompt_tokens ?? 0);
    const completion = Number(metrics.completion_tokens ?? 0);
    const total = Number(metrics.total_tokens ?? prompt + completion);

    return {
      Turn: `T${String(index + 1).padStart(2, "0")}`,
      Prompt: String(prompt),
      Comp: String(completion),
      Total: String(total),
    };
  });

  const promptTokens = metricsHistory.reduce((sum, metrics) => sum + Number(metrics.prompt_tokens ?? 0), 0);
  const completionTokens = metricsHistory.reduce((sum, metrics) => sum + Number(metrics.completion_tokens ?? 0), 0);
  const aggregateTokens = metricsHistory.reduce(
    (sum, metrics) => sum + Number(metrics.total_tokens ?? Number(metrics.prompt_tokens ?? 0) + Number(metrics.completion_tokens ?? 0)),
    0,
  );
  const requestCount = requestRows.length;
  const displayedTotalTokens = aggregateTokens || transcriptTokenEstimate;

  if (requestRows.length > 0) {
    requestRows.push({
      Turn: "Total",
      Prompt: String(promptTokens),
      Comp: String(completionTokens),
      Total: String(displayedTotalTokens),
    });
  }

  const generationSamples = metricsHistory
    .map((metrics) => metrics.generation_duration_ms)
    .filter((value): value is number => typeof value === "number");
  const queueSamples = metricsHistory
    .map((metrics) => metrics.queue_time_ms)
    .filter((value): value is number => typeof value === "number");
  const promptSamples = metricsHistory
    .map((metrics) => metrics.prompt_time_ms)
    .filter((value): value is number => typeof value === "number");
  const ttftSamples = metricsHistory
    .map((metrics) => metrics.ttft_ms)
    .filter((value): value is number => typeof value === "number");

  const averageGenerationMs = generationSamples.length > 0
    ? generationSamples.reduce((sum, value) => sum + value, 0) / generationSamples.length
    : null;
  const averageQueueMs = queueSamples.length > 0
    ? queueSamples.reduce((sum, value) => sum + value, 0) / queueSamples.length
    : null;
  const averagePromptMs = promptSamples.length > 0
    ? promptSamples.reduce((sum, value) => sum + value, 0) / promptSamples.length
    : null;
  const averageTtftMs = ttftSamples.length > 0
    ? ttftSamples.reduce((sum, value) => sum + value, 0) / ttftSamples.length
    : null;
  const totalGenerationMs = generationSamples.reduce((sum, value) => sum + value, 0);
  const sessionTps = completionTokens > 0 && totalGenerationMs > 0
    ? completionTokens / (totalGenerationMs / 1000)
    : null;

  const performanceRows: TelemetryTableRow[] = [
    {
      Metric: "GEN TIME (AVG)",
      Value: averageGenerationMs !== null ? `${Math.round(averageGenerationMs)}ms` : "IDLE",
    },
    {
      Metric: "QUEUE (AVG)",
      Value: averageQueueMs !== null ? `${Math.round(averageQueueMs)}ms` : "N/A",
    },
    {
      Metric: "PROMPT (AVG)",
      Value: averagePromptMs !== null ? `${Math.round(averagePromptMs)}ms` : "N/A",
    },
    {
      Metric: "TTF (AVG)",
      Value: averageTtftMs !== null ? `${Math.round(averageTtftMs)}ms` : "N/A",
    },
    {
      Metric: "SESSION TPS",
      Value: sessionTps !== null ? `${sessionTps.toFixed(2)} TPS` : "N/A",
    },
  ];

  const serviceTableRows: TelemetryTableRow[] = serviceRows.map((service) => ({
    Service: service.name,
    "Net RTT": typeof service.latency_ms === "number" ? `${Math.round(service.latency_ms)} ms` : "--",
  }));
  const serviceNotes = serviceRows
    .filter((service) => service.detail && service.status?.toUpperCase() !== "ONLINE")
    .map((service) => `${service.name}: ${service.detail}`);

  const tokenTableRows = requestRows;
  const vocalShareRows: TelemetryTableRow[] = roleBreakdown.map((entry) => ({
    Speaker: entry.label,
    Words: String(entry.words),
    Share: `${Math.max(0, entry.share).toFixed(0)}%`,
  }));

  const overallStatusSlug = servicesError
    ? "offline"
    : onlineServices === 0
      ? "standby"
      : onlineServices === serviceRows.length
        ? "online"
        : "degraded";

  const observedRatio = debateEntropy !== null ? Math.max(0, Math.min(1, debateEntropy)) : 0;
  let diversityLabel = "No Data";
  let diversityValue = "0%";

  if (debateEntropy !== null) {
    diversityValue = `${Math.round(observedRatio * 100)}%`;
    diversityLabel = "High Spread";
    if (debateEntropy < 0.7) {
      diversityLabel = "Moderate";
    }
    if (debateEntropy < 0.35) {
      diversityLabel = "Low Spread";
    }
  }

  return (
    <aside className="telemetryColumn">
      <div className="panel telemetryPanel">
        <div className="telemetryHero">
          <h2 className="telemetryHeroTitle">TELEMETRY</h2>
          {/* <p className="telemetryHeroSubtitle">Live app metrics.</p> */}
        </div>

        <section className="sidebarSectionGroup">
          <h3 className="sidebarSectionHeading telemetryStatusHeading">
            <span className={`telemetryStatusDot telemetryStatusDot${overallStatusSlug.charAt(0).toUpperCase()}${overallStatusSlug.slice(1)}`} />
            <span>SYSTEM STATUS</span>
          </h3>
          <details className="telemetryDetails">
            <summary>{serviceRows.length === 0 ? "Open services to run live checks." : `Services (${onlineServices}/${serviceRows.length})`}</summary>
            {serviceTableRows.length > 0 ? <TelemetryTable rows={serviceTableRows} /> : null}
            {serviceTableRows.length === 0 ? <p className="statusNote">Open services to run live checks.</p> : null}
            {serviceNotes.map((note) => (
              <p key={note} className="telemetryNote">{note}</p>
            ))}
            {servicesError ? <p className="statusNote">{servicesError}</p> : null}
          </details>
        </section>

        <SidebarSection title="MODEL PERFORMANCE" panelClassName="telemetryStreamlitSection">
          <TelemetryTable rows={performanceRows} />
          {telemetryError ? <p className="statusNote">{telemetryError}</p> : null}
        </SidebarSection>

        <SidebarSection title="TOKEN USAGE" panelClassName="telemetryStreamlitSection">
          <div className="telemetryTokenShell">
            <div className="telemetryTokenHeader">
              <div className="telemetryTokenTopline">
                <div className="telemetryTokenValue">{displayedTotalTokens} Tokens</div>
                <span className="telemetryTokenBadge">{requestCount} {requestCount === 1 ? "Request" : "Requests"}</span>
              </div>
            </div>
            {tokenTableRows.length > 0 ? <TelemetryTable rows={tokenTableRows} /> : <p className="statusNote">No request metrics yet. Each turn will be one model request.</p>}
            {/* <p className="telemetryNote">Each turn is one model request.</p> */}
          </div>
        </SidebarSection>

        <SidebarSection title="SESSION COST" panelClassName="telemetryStreamlitSection">
          <div className="telemetryCostCard">
            <div className="telemetryCostValue">${sessionBurnUsd.toFixed(6)}</div>
            <div className="telemetryCostCaption">{SESSION_COST_HELPER_TEXT}</div>
          </div>
        </SidebarSection>

        <SidebarSection title="DEBATE DIVERSITY" panelClassName="telemetryStreamlitSection">
          <div className="telemetryEntropyCard">
            <div className="telemetryEntropyTopline">
              <span className="telemetryEntropyValue">{diversityValue}</span>
              <span className="telemetryEntropyStatus">{diversityLabel}</span>
            </div>
            <div className="telemetryEntropyTrack">
              <div className="telemetryEntropyFill" style={{ width: `${observedRatio * 100}%` }} />
            </div>
            <div className="telemetryEntropyCaption">
              Diversity calculated as average pairwise Jaccard entropy between a response and the immediately preceding one.
            </div>
          </div>
        </SidebarSection>

        <SidebarSection title="VOCAL SHARE" panelClassName="telemetryStreamlitSection">
          {vocalShareRows.length > 0 ? <TelemetryTable rows={vocalShareRows} /> : <p className="statusNote">No air-time data yet.</p>}
        </SidebarSection>
      </div>
    </aside>
  );
}

function TelemetryTable({ rows }: { rows: TelemetryTableRow[] }) {
  if (rows.length === 0) {
    return null;
  }

  const columns = Object.keys(rows[0]);

  return (
    <div className="telemetryTableShell">
      <table className="telemetryTable">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${index}-${row[columns[0]]}`}>
              {columns.map((column) => (
                <td key={column}>{row[column]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}