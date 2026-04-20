import type { Agent } from "@/lib/types";

import type { LegendDetails } from "./types";
import { avatarUrlForAgent } from "./utils";

type LegendCardProps = {
  legend: LegendDetails;
  agent?: Agent;
  badge: string;
  active?: boolean;
  onClick?: () => void;
  disabled?: boolean;
};

export function LegendCard({ legend, agent, badge, active = false, onClick, disabled = false }: LegendCardProps) {
  const className = `agentCard ${active ? "agentCardActive" : ""} ${onClick ? "legendCardButton" : "legendCardStatic"}`.trim();

  const content = (
    <>
      <div className="agentCardHeader">
        <img
          className="agentPortrait"
          src={avatarUrlForAgent(legend.agent_id)}
          alt={`${legend.display_name} portrait`}
          loading="lazy"
        />
        <div className="agentIdentity">
          <div className="agentNameRow">
            <p className="agentName">{legend.display_name}</p>
            <span className="agentDraftState">{badge}</span>
          </div>
          <p className="agentMeta">{legend.archetype}</p>
          <p className="agentMeta">ID: {legend.agent_id}</p>
        </div>
      </div>
      <p className="agentMeta">
        Temp {agent?.temperature ?? "--"} · Max {agent?.max_tokens ?? "--"} tokens
      </p>
    </>
  );

  if (onClick) {
    return (
      <button type="button" className={className} onClick={onClick} disabled={disabled}>
        {content}
      </button>
    );
  }

  return <article className={className}>{content}</article>;
}