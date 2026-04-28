import type { CSSProperties } from "react";

import { SidebarSection } from "./sidebar-section";
import type { LegendDetails } from "./types";
import { logoUrl } from "./utils";

type ControlSidebarProps = {
  isSidebarOpen: boolean;
  isMobileViewport: boolean;
  showSidebarToggle: boolean;
  discussionActive: boolean;
  sessionId: string;
  selectedCouncil: LegendDetails[];
  targetEntropy: number;
  controlError: string;
  isWipingSession: boolean;
  isDownloadingTranscript: boolean;
  startButtonLabel: string;
  onToggleSidebar: () => void;
  onOpenSpeakerModal: () => void;
  onToggleCouncilMember: (agentId: string) => void;
  onTargetEntropyChange: (value: number) => void;
  onStartDebate: () => void;
  onHaltDebate: () => void;
  onWipeDebate: () => void | Promise<void>;
  onDownloadTranscript: () => void | Promise<void>;
  onRenewSession: () => void;
};

export function ControlSidebar({
  isSidebarOpen,
  isMobileViewport,
  showSidebarToggle,
  discussionActive,
  sessionId,
  selectedCouncil,
  targetEntropy,
  controlError,
  isWipingSession,
  isDownloadingTranscript,
  startButtonLabel,
  onToggleSidebar,
  onOpenSpeakerModal,
  onToggleCouncilMember,
  onTargetEntropyChange,
  onStartDebate,
  onHaltDebate,
  onWipeDebate,
  onDownloadTranscript,
  onRenewSession,
}: ControlSidebarProps) {
  const sliderFill = `${Math.max(0, Math.min(100, (targetEntropy / 1.5) * 100))}%`;
  const sliderStyle = {
    "--slider-fill": sliderFill,
  } as CSSProperties;

  return (
    <>
      <div className="sidebarRailHeader">
        <div className="sidebarBrand">
          <img className="sidebarLogo" src={logoUrl()} alt="Exhumed logo" />
          {isSidebarOpen || isMobileViewport ? (
            <div className="sidebarBrandCopy">
              <span className="sidebarBrandTitle">EXHUMED</span>
              <span className="sidebarBrandSubtitle">Historical Logic Engine</span>
            </div>
          ) : null}
        </div>
        {showSidebarToggle ? (
          <button
            type="button"
            className="sidebarToggle sidebarToggleIntegrated"
            onClick={onToggleSidebar}
            aria-expanded={isSidebarOpen}
            aria-controls="exhumed-control-sidebar"
            aria-label={isSidebarOpen ? "Collapse controls sidebar" : "Expand controls sidebar"}
          >
            <span className="sidebarToggleGlyph" aria-hidden="true">
              {isMobileViewport ? "x" : isSidebarOpen ? "<" : ">"}
            </span>
          </button>
        ) : null}
      </div>

      <div className="panel">
        <div className="stack">
          <button className="button buttonPrimaryCta" type="button" onClick={onOpenSpeakerModal}>
            Select Speaker
          </button>

          <SidebarSection title="DRAFTED COUNCIL" panelClassName="panel">
            {selectedCouncil.length === 0 ? (
              <p className="statusNote">No entities recovered. Draft at least one legend.</p>
            ) : null}
            <div className="draftedCouncil">
              {selectedCouncil.map((legend) => (
                <button
                  key={legend.agent_id}
                  type="button"
                  className="draftedChip"
                  onClick={() => onToggleCouncilMember(legend.agent_id)}
                  disabled={discussionActive}
                >
                  <span className="draftedChipLabel">{legend.display_name}</span>
                  <span className="draftedChipRemove" aria-hidden="true">x</span>
                </button>
              ))}
            </div>
          </SidebarSection>

          <SidebarSection title="LOGIC ENTROPY" panelClassName="entropyPanel">
            <div className="entropyHeader">
              <div>
                <p className="helper">Adjust between rigid logic and creative unpredictability.</p>
              </div>
            </div>
            <input
              className="entropySlider"
              type="range"
              min="0"
              max="1.5"
              step="0.05"
              value={targetEntropy}
              style={sliderStyle}
              onChange={(event) => onTargetEntropyChange(Number(event.target.value))}
              disabled={discussionActive}
            />
            <div className="sliderLabels">
              <span>Rigid</span>
              <span>Creative</span>
            </div>
          </SidebarSection>

          <SidebarSection title="COMMANDS" panelClassName="stack commandPanel">
            <div className="actions actionsCompact">
              <button className="button" type="button" onClick={onStartDebate} disabled={discussionActive}>
                {startButtonLabel}
              </button>
              <button className="buttonGhost" type="button" onClick={onHaltDebate} disabled={!discussionActive}>
                Halt Debate
              </button>
            </div>

            <div className="actions actionsCompact">
              <button className="buttonDanger" type="button" onClick={() => void onWipeDebate()} disabled={isWipingSession}>
                {isWipingSession ? "Wiping..." : "Wipe Debate"}
              </button>
              <button
                className="buttonGhost"
                type="button"
                onClick={() => void onDownloadTranscript()}
                disabled={isDownloadingTranscript}
              >
                {isDownloadingTranscript ? "Preparing..." : "Download Transcript"}
              </button>
            </div>
          </SidebarSection>

          <SidebarSection title="SESSION" panelClassName="sessionPanel">
            <div className="sessionInline">
              <span className="sessionInlineLabel">Current ID:</span>
              <span className="sessionInlineValue" title={sessionId || "Pending"}>
                {sessionId || "Pending"}
              </span>
            </div>
            <div className="actions actionsCompact sessionActions">
              <button className="buttonGhost" type="button" onClick={onRenewSession}>
                Refresh Session
              </button>
            </div>
          </SidebarSection>

          {controlError ? <p className="statusNote">{controlError}</p> : null}
        </div>
      </div>
    </>
  );
}
