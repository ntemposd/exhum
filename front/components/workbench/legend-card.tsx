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
  const hoverBadge = active ? "REMOVE" : "DRAFT NOW";

  const content = (
    <>
      <div className="agentCardTopRow">
        <span className="agentDraftState" data-hover-label={hoverBadge}>
          <span className="agentDraftStateText">{badge}</span>
        </span>
      </div>
      <div className="agentCardHeader">
        <img
          className="agentPortrait"
          src={avatarUrlForAgent(legend.agent_id)}
          alt={`${legend.display_name} portrait`}
          loading="lazy"
        />
        <div className="agentIdentity">
          <p className="agentName">{legend.display_name}</p>
          <p className="agentDescription">{legend.archetype}</p>
        </div>
      </div>
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