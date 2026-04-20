"use client";

import { useEffect, useRef, useState } from "react";

import { backendUrl } from "@/lib/config";
import type {
  Agent,
  AgentsResponse,
  ExecutionMetrics,
  LatestTelemetryResponse,
  ProcessTurnStreamEvent,
  ServicesStatusResponse,
} from "@/lib/types";

import { ControlSidebar } from "./workbench/control-sidebar";
import { DiscussionPanel } from "./workbench/discussion-panel";
import { SpeakerSelectorModal } from "./workbench/speaker-selector-modal";
import { TelemetryPanel } from "./workbench/telemetry-panel";
import type { DebateMessage, LegendDetails } from "./workbench/types";
import {
  calculateSessionBurnUsd,
  clampNumber,
  countWords,
  estimateTokenCount,
  getDefaultCouncilAgentIds,
  getLegendDetails,
  getRoleBreakdown,
  makeSessionId,
} from "./workbench/utils";

const SESSION_STORAGE_KEY = "exhumed-front-session-id";
const COUNCIL_STORAGE_KEY = "exhumed-front-council-agent-ids";
const TOPIC_STORAGE_KEY = "exhumed-front-topic";
const SIDEBAR_STORAGE_KEY = "exhumed-front-sidebar-open";
const SIDEBAR_WIDTH_STORAGE_KEY = "exhumed-front-sidebar-width";
const ENTROPY_STORAGE_KEY = "exhumed-front-target-entropy";
const SERVICES_CACHE_KEY = "exhumed-front-services-cache";
const DEFAULT_TOPIC = "The future of AI in society.";
const MOBILE_BREAKPOINT_PX = 1024;
const CONTEXT_WINDOW_TOKENS = 8192;
const SERVICES_CACHE_TTL_MS = 60_000;
const TELEMETRY_REFRESH_THROTTLE_MS = 15_000;
const DEFAULT_SIDEBAR_WIDTH_PX = 320;
const MIN_SIDEBAR_WIDTH_PX = 280;
const MAX_SIDEBAR_WIDTH_PX = 520;
const STREAM_REVEAL_CHARS_PER_FRAME = 4;

export function ChatWorkbench() {
  const [sessionId, setSessionId] = useState("");
  const [topic, setTopic] = useState(DEFAULT_TOPIC);
  const [targetEntropy, setTargetEntropy] = useState(0.7);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [messages, setMessages] = useState<DebateMessage[]>([]);
  const [speakerProgress, setSpeakerProgress] = useState<Record<string, number>>({});
  const [discussionActive, setDiscussionActive] = useState(false);
  const [turnCount, setTurnCount] = useState(0);
  const [currentAgentIndex, setCurrentAgentIndex] = useState(0);
  const [debateEntropy, setDebateEntropy] = useState<number | null>(null);
  const [statusNote, setStatusNote] = useState("Standby.");
  const [agentsError, setAgentsError] = useState("");
  const [isLoadingAgents, setIsLoadingAgents] = useState(true);
  const [services, setServices] = useState<ServicesStatusResponse | null>(null);
  const [latestTelemetry, setLatestTelemetry] = useState<ExecutionMetrics | null>(null);
  const [servicesError, setServicesError] = useState("");
  const [telemetryError, setTelemetryError] = useState("");
  const [controlError, setControlError] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [sidebarWidth, setSidebarWidth] = useState(DEFAULT_SIDEBAR_WIDTH_PX);
  const [isMobileViewport, setIsMobileViewport] = useState(false);
  const [isWipingSession, setIsWipingSession] = useState(false);
  const [isDownloadingTranscript, setIsDownloadingTranscript] = useState(false);
  const [isSpeakerModalOpen, setIsSpeakerModalOpen] = useState(false);
  const transcriptRef = useRef<HTMLDivElement | null>(null);
  const turnInFlightRef = useRef(false);
  const isDraggingSidebarRef = useRef(false);
  const resetSequenceRef = useRef(0);
  const currentTurnAbortControllerRef = useRef<AbortController | null>(null);
  const lastTelemetryFetchAtRef = useRef(0);
  const streamRevealQueuesRef = useRef<Record<string, string>>({});
  const streamRevealFrameRef = useRef<number | null>(null);

  function clearStreamRevealQueue(messageId?: string) {
    if (messageId) {
      delete streamRevealQueuesRef.current[messageId];
    } else {
      streamRevealQueuesRef.current = {};
    }

    if (Object.keys(streamRevealQueuesRef.current).length === 0 && streamRevealFrameRef.current !== null) {
      cancelAnimationFrame(streamRevealFrameRef.current);
      streamRevealFrameRef.current = null;
    }
  }

  function scheduleStreamReveal() {
    if (streamRevealFrameRef.current !== null) {
      return;
    }

    const step = () => {
      const queueEntries = Object.entries(streamRevealQueuesRef.current).filter(([, queuedText]) => queuedText.length > 0);
      if (queueEntries.length === 0) {
        streamRevealFrameRef.current = null;
        return;
      }

      const revealBatch = new Map<string, string>();

      for (const [messageId, queuedText] of queueEntries) {
        const revealedText = queuedText.slice(0, STREAM_REVEAL_CHARS_PER_FRAME);
        const remainingText = queuedText.slice(STREAM_REVEAL_CHARS_PER_FRAME);
        revealBatch.set(messageId, revealedText);

        if (remainingText) {
          streamRevealQueuesRef.current[messageId] = remainingText;
        } else {
          delete streamRevealQueuesRef.current[messageId];
        }
      }

      setMessages((currentMessages) =>
        currentMessages.map((message) => {
          const revealedText = revealBatch.get(message.id);
          if (!revealedText) {
            return message;
          }

          return {
            ...message,
            message: `${message.message}${revealedText}`,
          };
        }),
      );

      streamRevealFrameRef.current = requestAnimationFrame(step);
    };

    streamRevealFrameRef.current = requestAnimationFrame(step);
  }

  useEffect(() => {
    const storedSessionId = window.localStorage.getItem(SESSION_STORAGE_KEY);
    const storedTopic = window.localStorage.getItem(TOPIC_STORAGE_KEY);
    const storedSidebarState = window.localStorage.getItem(SIDEBAR_STORAGE_KEY);
    const storedSidebarWidth = window.localStorage.getItem(SIDEBAR_WIDTH_STORAGE_KEY);
    const storedEntropy = window.localStorage.getItem(ENTROPY_STORAGE_KEY);
    const nextSessionId = storedSessionId || makeSessionId();
    const mobileViewport = window.innerWidth <= MOBILE_BREAKPOINT_PX;

    setSessionId(nextSessionId);
    window.localStorage.setItem(SESSION_STORAGE_KEY, nextSessionId);
    setIsMobileViewport(mobileViewport);
    setIsSidebarOpen(mobileViewport ? true : storedSidebarState !== "false");

    if (storedSidebarWidth) {
      const parsedWidth = Number(storedSidebarWidth);
      if (!Number.isNaN(parsedWidth)) {
        setSidebarWidth(clampNumber(parsedWidth, MIN_SIDEBAR_WIDTH_PX, MAX_SIDEBAR_WIDTH_PX));
      }
    }

    if (storedTopic) {
      setTopic(storedTopic);
    }

    if (storedEntropy) {
      const parsedEntropy = Number(storedEntropy);
      if (!Number.isNaN(parsedEntropy)) {
        setTargetEntropy(clampNumber(parsedEntropy, 0, 1.5));
      }
    }
  }, []);

  useEffect(() => {
    window.localStorage.setItem(TOPIC_STORAGE_KEY, topic);
  }, [topic]);

  useEffect(() => {
    window.localStorage.setItem(ENTROPY_STORAGE_KEY, String(targetEntropy));
  }, [targetEntropy]);

  useEffect(() => {
    window.localStorage.setItem(COUNCIL_STORAGE_KEY, JSON.stringify(selectedAgents));
  }, [selectedAgents]);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }

    function syncViewportState() {
      const mobileViewport = window.innerWidth <= MOBILE_BREAKPOINT_PX;
      setIsMobileViewport(mobileViewport);

      if (mobileViewport) {
        setIsSidebarOpen(true);
        return;
      }

      const storedSidebarState = window.localStorage.getItem(SIDEBAR_STORAGE_KEY);
      setIsSidebarOpen(storedSidebarState !== "false");
    }

    window.addEventListener("resize", syncViewportState);

    return () => {
      window.removeEventListener("resize", syncViewportState);
    };
  }, []);

  useEffect(() => {
    return () => {
      if (streamRevealFrameRef.current !== null) {
        cancelAnimationFrame(streamRevealFrameRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (typeof window === "undefined" || isMobileViewport) {
      return;
    }

    window.localStorage.setItem(SIDEBAR_STORAGE_KEY, String(isSidebarOpen));
  }, [isMobileViewport, isSidebarOpen]);

  useEffect(() => {
    if (typeof window === "undefined" || isMobileViewport) {
      return;
    }

    window.localStorage.setItem(SIDEBAR_WIDTH_STORAGE_KEY, String(Math.round(sidebarWidth)));
  }, [isMobileViewport, sidebarWidth]);

  useEffect(() => {
    if (typeof window === "undefined" || isMobileViewport) {
      return;
    }

    function handlePointerMove(event: PointerEvent) {
      if (!isDraggingSidebarRef.current) {
        return;
      }

      const nextWidth = clampNumber(event.clientX, MIN_SIDEBAR_WIDTH_PX, MAX_SIDEBAR_WIDTH_PX);
      setSidebarWidth(nextWidth);
    }

    function stopDragging() {
      if (!isDraggingSidebarRef.current) {
        return;
      }

      isDraggingSidebarRef.current = false;
      document.body.classList.remove("sidebarResizing");
    }

    window.addEventListener("pointermove", handlePointerMove);
    window.addEventListener("pointerup", stopDragging);
    window.addEventListener("pointercancel", stopDragging);

    return () => {
      window.removeEventListener("pointermove", handlePointerMove);
      window.removeEventListener("pointerup", stopDragging);
      window.removeEventListener("pointercancel", stopDragging);
      document.body.classList.remove("sidebarResizing");
    };
  }, [isMobileViewport]);

  useEffect(() => {
    let cancelled = false;

    async function loadAgents() {
      setIsLoadingAgents(true);
      setAgentsError("");

      try {
        const response = await fetch(`${backendUrl}/agents`, {
          headers: { Accept: "application/json" },
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error(`Backend returned ${response.status}`);
        }

        const data = (await response.json()) as AgentsResponse;
        if (cancelled) {
          return;
        }

        const nextAgents = Array.isArray(data.agents) ? data.agents : [];
        setAgents(nextAgents);

        const storedCouncilIds = window.localStorage.getItem(COUNCIL_STORAGE_KEY);
        const parsedCouncilIds = storedCouncilIds ? (JSON.parse(storedCouncilIds) as string[]) : [];
        const availableIds = new Set(nextAgents.map((agent) => agent.agent_id));
        const hydratedCouncilIds = parsedCouncilIds.filter((agentId) => availableIds.has(agentId));

        setSelectedAgents(
          hydratedCouncilIds.length > 0 ? hydratedCouncilIds : getDefaultCouncilAgentIds(nextAgents),
        );
      } catch (loadError) {
        if (cancelled) {
          return;
        }

        const message = loadError instanceof Error ? loadError.message : "Unknown backend error";
        setAgents([]);
        setAgentsError(message);
      } finally {
        if (!cancelled) {
          setIsLoadingAgents(false);
        }
      }
    }

    void loadAgents();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    async function loadServices() {
      const cachedValue = window.localStorage.getItem(SERVICES_CACHE_KEY);

      if (cachedValue) {
        try {
          const parsedCache = JSON.parse(cachedValue) as {
            cachedAt?: number;
            data?: ServicesStatusResponse;
          };

          if (
            typeof parsedCache.cachedAt === "number" &&
            parsedCache.data &&
            Date.now() - parsedCache.cachedAt < SERVICES_CACHE_TTL_MS
          ) {
            setServices(parsedCache.data);
            setServicesError("");
            return;
          }
        } catch {
          window.localStorage.removeItem(SERVICES_CACHE_KEY);
        }
      }

      try {
        const response = await fetch(`${backendUrl}/services-status`, {
          headers: { Accept: "application/json" },
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error(`Status probe failed with ${response.status}`);
        }

        const data = (await response.json()) as ServicesStatusResponse;
        setServices(data);
        setServicesError("");
        window.localStorage.setItem(
          SERVICES_CACHE_KEY,
          JSON.stringify({
            cachedAt: Date.now(),
            data,
          }),
        );
      } catch (loadError) {
        const message = loadError instanceof Error ? loadError.message : "Could not load service status";
        setServicesError(message);
      }
    }

    void loadServices();
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function loadLatestTelemetry() {
      const now = Date.now();
      if (now - lastTelemetryFetchAtRef.current < TELEMETRY_REFRESH_THROTTLE_MS) {
        return;
      }

      lastTelemetryFetchAtRef.current = now;

      try {
        const response = await fetch(`${backendUrl}/telemetry/latest`, {
          headers: { Accept: "application/json" },
          cache: "no-store",
        });

        if (!response.ok) {
          throw new Error(`Telemetry probe failed with ${response.status}`);
        }

        const data = (await response.json()) as LatestTelemetryResponse;
        if (cancelled) {
          return;
        }

        setLatestTelemetry(data.metrics);
        setTelemetryError("");
      } catch (loadError) {
        if (cancelled) {
          return;
        }

        const message = loadError instanceof Error ? loadError.message : "Could not load latest telemetry";
        setTelemetryError(message);
      }
    }

    function refreshTelemetryOnForeground() {
      if (document.visibilityState !== "visible") {
        return;
      }

      void loadLatestTelemetry();
    }

    void loadLatestTelemetry();
    window.addEventListener("focus", refreshTelemetryOnForeground);
    document.addEventListener("visibilitychange", refreshTelemetryOnForeground);

    return () => {
      cancelled = true;
      window.removeEventListener("focus", refreshTelemetryOnForeground);
      document.removeEventListener("visibilitychange", refreshTelemetryOnForeground);
    };
  }, []);

  useEffect(() => {
    const transcriptNode = transcriptRef.current;
    if (!transcriptNode) {
      return;
    }

    transcriptNode.scrollTop = transcriptNode.scrollHeight;
  }, [messages]);

  useEffect(() => {
    if (!isSpeakerModalOpen) {
      return;
    }

    function handleEscape(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setIsSpeakerModalOpen(false);
      }
    }

    window.addEventListener("keydown", handleEscape);
    return () => {
      window.removeEventListener("keydown", handleEscape);
    };
  }, [isSpeakerModalOpen]);

  useEffect(() => {
    if (!discussionActive || !sessionId || !topic.trim() || selectedAgents.length === 0) {
      return;
    }

    if (currentAgentIndex >= selectedAgents.length) {
      setDiscussionActive(false);
      setCurrentAgentIndex(0);
      setStatusNote("Round complete.");
      return;
    }

    if (turnInFlightRef.current) {
      return;
    }

    const currentAgentId = selectedAgents[currentAgentIndex];
    const currentAgent = agents.find((agent) => agent.agent_id === currentAgentId);
    const currentTurnNumber = turnCount + 1;
    const thinkingId = `thinking-${currentAgentId}-${currentTurnNumber}`;
    const displayName = currentAgent?.display_name ?? currentAgentId;
    const requestResetSequence = resetSequenceRef.current;
    const abortController = new AbortController();

    turnInFlightRef.current = true;
    currentTurnAbortControllerRef.current = abortController;
    setControlError("");
    setStatusNote(`Running ${displayName}...`);
    setSpeakerProgress((currentProgress) => ({
      ...currentProgress,
      [currentAgentId]: 0.25,
    }));
    setMessages((currentMessages) => [
      ...currentMessages,
      {
        id: thinkingId,
        agent_id: currentAgentId,
        display_name: displayName,
        message: "",
        turn_number: currentTurnNumber,
        created_at: new Date().toISOString(),
        isThinking: true,
      },
    ]);

    void (async () => {
      try {
        const response = await fetch(`${backendUrl}/process-turn/stream`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          signal: abortController.signal,
          body: JSON.stringify({
            session_id: sessionId,
            topic: topic.trim(),
            agent_id: currentAgentId,
            temperature: targetEntropy,
            turn_number: currentTurnNumber,
          }),
        });

        if (requestResetSequence !== resetSequenceRef.current) {
          return;
        }

        if (!response.ok) {
          throw new Error(`Turn failed with ${response.status}`);
        }

        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error("Turn stream was unavailable");
        }

        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            break;
          }

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() ?? "";

          for (const line of lines) {
            const trimmedLine = line.trim();
            if (!trimmedLine) {
              continue;
            }

            const event = JSON.parse(trimmedLine) as ProcessTurnStreamEvent;
            if (requestResetSequence !== resetSequenceRef.current) {
              return;
            }

            if (event.type === "chunk") {
              streamRevealQueuesRef.current[thinkingId] = `${streamRevealQueuesRef.current[thinkingId] ?? ""}${event.content}`;
              scheduleStreamReveal();
              continue;
            }

            clearStreamRevealQueue(thinkingId);
            setLatestTelemetry(event.execution_metrics);
            setDebateEntropy(clampNumber(event.telemetry.entropy, 0, 1));
            setMessages((currentMessages) =>
              currentMessages.map((message) =>
                message.id === thinkingId
                  ? {
                      id: event.message_id,
                      agent_id: event.agent_id,
                      display_name: event.display_name,
                      message: event.message,
                      turn_number: event.turn_number,
                      created_at: event.created_at,
                      execution_metrics: event.execution_metrics,
                      isThinking: false,
                    }
                  : message,
              ),
            );
            setSpeakerProgress((currentProgress) => ({
              ...currentProgress,
              [currentAgentId]: 1,
            }));
            setTurnCount((currentTurnCount) => currentTurnCount + 1);

            const isLastSpeakerInRound = currentAgentIndex + 1 >= selectedAgents.length;
            if (isLastSpeakerInRound) {
              setDiscussionActive(false);
              setCurrentAgentIndex(0);
              setStatusNote("Round complete.");
            } else {
              const nextAgentId = selectedAgents[currentAgentIndex + 1];
              const nextAgentName = agents.find((agent) => agent.agent_id === nextAgentId)?.display_name ?? nextAgentId;
              setCurrentAgentIndex(currentAgentIndex + 1);
              setStatusNote(`Queued ${nextAgentName}.`);
            }
            return;
          }
        }

        throw new Error("Turn stream ended before final payload was received");
      } catch (turnError) {
        if (abortController.signal.aborted || requestResetSequence !== resetSequenceRef.current) {
          return;
        }

        const message = turnError instanceof Error ? turnError.message : "Turn execution failed";
        clearStreamRevealQueue(thinkingId);
        setControlError(message);
        setStatusNote(message);
        setDiscussionActive(false);
        setCurrentAgentIndex(0);
        setSpeakerProgress((currentProgress) => ({
          ...currentProgress,
          [currentAgentId]: 0,
        }));
        setMessages((currentMessages) =>
          currentMessages.map((message) =>
            message.id === thinkingId
              ? {
                  ...message,
                  message: "Agent failed to produce a response.",
                  isThinking: false,
                  failed: true,
                  created_at: new Date().toISOString(),
                }
              : message,
          ),
        );
      } finally {
        if (currentTurnAbortControllerRef.current === abortController) {
          currentTurnAbortControllerRef.current = null;
          turnInFlightRef.current = false;
        }
      }
    })();
  }, [agents, currentAgentIndex, discussionActive, selectedAgents, sessionId, targetEntropy, topic, turnCount]);

  const legendEntries = agents.map(getLegendDetails);
  const selectedCouncil = selectedAgents
    .map((agentId) => legendEntries.find((legend) => legend.agent_id === agentId))
    .filter((legend): legend is LegendDetails => Boolean(legend));
  const hasMessages = messages.some((message) => !message.isThinking);
  const transcriptTokenEstimate = estimateTokenCount(
    messages.filter((message) => !message.isThinking).map((message) => message.message).join(" "),
  );
  const serviceRows = services?.services ?? [];
  const onlineServices = serviceRows.filter((service) => service.status?.toUpperCase() === "ONLINE").length;
  const roleBreakdown = getRoleBreakdown(messages);
  const sessionBurnUsd = calculateSessionBurnUsd(messages);
  const sessionStateLabel = discussionActive ? "Live" : hasMessages ? "Dormant" : "Standby";
  const startButtonLabel = hasMessages ? "🏁 Advance Debate" : "🏁 Start Debate";

  function closeSidebar() {
    setIsSidebarOpen(false);
  }

  function toggleSidebar() {
    setIsSidebarOpen((currentValue) => !currentValue);
  }

  function toggleCouncilMember(agentId: string) {
    if (discussionActive) {
      return;
    }

    setSelectedAgents((currentSelection) => {
      if (currentSelection.includes(agentId)) {
        return currentSelection.filter((selectedId) => selectedId !== agentId);
      }

      return [...currentSelection, agentId];
    });
  }

  function openSpeakerModal() {
    setIsSpeakerModalOpen(true);
    if (isMobileViewport) {
      closeSidebar();
    }
  }

  function closeSpeakerModal() {
    setIsSpeakerModalOpen(false);
  }

  async function wipeDebate() {
    if (!sessionId) {
      return;
    }

    setIsWipingSession(true);
    setDiscussionActive(false);
    clearStreamRevealQueue();
    resetSequenceRef.current += 1;
    turnInFlightRef.current = false;
    currentTurnAbortControllerRef.current?.abort();
    currentTurnAbortControllerRef.current = null;
    setMessages([]);
    setSpeakerProgress({});
    setTurnCount(0);
    setCurrentAgentIndex(0);
    setDebateEntropy(null);
    setLatestTelemetry(null);

    try {
      const response = await fetch(`${backendUrl}/sessions/${sessionId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Backend cleanup failed with ${response.status}`);
      }

      setStatusNote("Debate cleared.");
      setControlError("");
    } catch (clearError) {
      const message = clearError instanceof Error ? clearError.message : "Debate cleared locally, but backend cleanup failed.";
      setStatusNote(message);
      setControlError(message);
    } finally {
      setIsWipingSession(false);
    }
  }

  function renewSession() {
    clearStreamRevealQueue();
    resetSequenceRef.current += 1;
    currentTurnAbortControllerRef.current?.abort();
    currentTurnAbortControllerRef.current = null;
    turnInFlightRef.current = false;
    const nextSessionId = makeSessionId();
    setSessionId(nextSessionId);
    window.localStorage.setItem(SESSION_STORAGE_KEY, nextSessionId);
    setMessages([]);
    setSpeakerProgress({});
    setTurnCount(0);
    setCurrentAgentIndex(0);
    setDebateEntropy(null);
    setDiscussionActive(false);
    setLatestTelemetry(null);
    setStatusNote("New session armed.");
    setControlError("");
    if (isMobileViewport) {
      closeSidebar();
    }
  }

  async function downloadTranscript() {
    if (!sessionId) {
      return;
    }

    if (!messages.some((message) => !message.isThinking)) {
      setControlError("No messages to export.");
      setStatusNote("No messages to export.");
      return;
    }

    setIsDownloadingTranscript(true);
    setControlError("");
    setStatusNote("Generating transcript...");

    try {
      const response = await fetch(`${backendUrl}/export-pdf/${sessionId}`);

      if (!response.ok) {
        throw new Error(`Transcript export failed with ${response.status}`);
      }

      const pdfBlob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(pdfBlob);
      const anchor = document.createElement("a");
      anchor.href = downloadUrl;
      anchor.download = `exhumed_${sessionId.slice(0, 8)}.pdf`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      window.URL.revokeObjectURL(downloadUrl);
      setStatusNote("Transcript ready.");
    } catch (downloadError) {
      const message = downloadError instanceof Error ? downloadError.message : "Transcript export failed";
      setControlError(message);
      setStatusNote(message);
    } finally {
      setIsDownloadingTranscript(false);
    }
  }

  function startDebate() {
    if (!topic.trim()) {
      setControlError("Set a discussion topic first.");
      setStatusNote("Set a discussion topic first.");
      return;
    }

    if (selectedAgents.length === 0) {
      setControlError("Draft at least one legend.");
      setStatusNote("Draft at least one legend.");
      return;
    }

    const canResumeQueuedSpeaker = currentAgentIndex > 0 && currentAgentIndex < selectedAgents.length;

    setControlError("");

    if (!canResumeQueuedSpeaker) {
      setSpeakerProgress(Object.fromEntries(selectedAgents.map((agentId) => [agentId, 0])));
      setCurrentAgentIndex(0);
    }

    setDiscussionActive(true);
    setStatusNote(canResumeQueuedSpeaker ? "Round resumed." : "Round armed.");
    if (isMobileViewport) {
      closeSidebar();
    }
  }

  function haltDebate() {
    clearStreamRevealQueue();
    currentTurnAbortControllerRef.current?.abort();
    currentTurnAbortControllerRef.current = null;
    turnInFlightRef.current = false;
    setDiscussionActive(false);
    setStatusNote("Round paused.");
  }

  function beginSidebarResize() {
    if (isMobileViewport || !isSidebarOpen) {
      return;
    }

    isDraggingSidebarRef.current = true;
    document.body.classList.add("sidebarResizing");
  }

  const workspaceStyle = !isMobileViewport
    ? {
        gridTemplateColumns: `${isSidebarOpen ? `${Math.round(sidebarWidth)}px` : "56px"} minmax(0, 1fr) 320px`,
      }
    : undefined;

  return (
    <main className="shell">
      {isMobileViewport && !isSidebarOpen ? (
        <button
          type="button"
          className="sidebarToggle sidebarToggleFloating"
          onClick={toggleSidebar}
          aria-expanded={isSidebarOpen}
          aria-controls="exhumed-control-sidebar"
          aria-label={isSidebarOpen ? "Close controls sidebar" : "Open controls sidebar"}
        >
          <span className="sidebarToggleGlyph" aria-hidden="true">
            {isSidebarOpen ? "×" : "≡"}
          </span>
          <span className="sidebarToggleLabel">Controls</span>
        </button>
      ) : null}

      {isMobileViewport && isSidebarOpen ? (
        <button
          type="button"
          className="sidebarScrim"
          aria-label="Close controls sidebar"
          onClick={closeSidebar}
        />
      ) : null}

      <section
        className={`workspace ${!isSidebarOpen && !isMobileViewport ? "workspaceSidebarCollapsed" : ""} ${
          isMobileViewport ? "workspaceMobile" : ""
        }`.trim()}
        style={workspaceStyle}
      >
        <aside
          id="exhumed-control-sidebar"
          className={`sidebar ${isSidebarOpen ? "sidebarOpen" : "sidebarClosed"} ${
            isMobileViewport ? "sidebarMobile" : "sidebarDesktop"
          }`.trim()}
          aria-hidden={isMobileViewport ? !isSidebarOpen : undefined}
        >
          <ControlSidebar
            isSidebarOpen={isSidebarOpen}
            isMobileViewport={isMobileViewport}
            discussionActive={discussionActive}
            sessionId={sessionId}
            selectedCouncil={selectedCouncil}
            targetEntropy={targetEntropy}
            controlError={controlError}
            isWipingSession={isWipingSession}
            isDownloadingTranscript={isDownloadingTranscript}
            startButtonLabel={startButtonLabel}
            onToggleSidebar={toggleSidebar}
            onOpenSpeakerModal={openSpeakerModal}
            onToggleCouncilMember={toggleCouncilMember}
            onTargetEntropyChange={setTargetEntropy}
            onStartDebate={startDebate}
            onHaltDebate={haltDebate}
            onWipeDebate={wipeDebate}
            onDownloadTranscript={downloadTranscript}
            onRenewSession={renewSession}
          />
          {!isMobileViewport && isSidebarOpen ? (
            <button
              type="button"
              className="sidebarResizeHandle"
              onPointerDown={beginSidebarResize}
              aria-label="Resize controls sidebar"
            />
          ) : null}
        </aside>

        <DiscussionPanel
          topic={topic}
          discussionActive={discussionActive}
          statusNote={controlError || statusNote}
          messages={messages}
          transcriptRef={transcriptRef}
          onTopicChange={setTopic}
        />

        <TelemetryPanel
          debateEntropy={debateEntropy}
          sessionBurnUsd={sessionBurnUsd}
          telemetryError={telemetryError}
          transcriptTokenEstimate={transcriptTokenEstimate}
          messages={messages}
          roleBreakdown={roleBreakdown}
          servicesError={servicesError}
          onlineServices={onlineServices}
          serviceRows={serviceRows}
        />
      </section>

      <SpeakerSelectorModal
        isOpen={isSpeakerModalOpen}
        discussionActive={discussionActive}
        agents={agents}
        legendEntries={legendEntries}
        selectedAgents={selectedAgents}
        agentsError={agentsError}
        isLoadingAgents={isLoadingAgents}
        onClose={closeSpeakerModal}
        onToggleCouncilMember={toggleCouncilMember}
      />

      <footer className="siteFooter">
        Built with ❤️ by <a className="siteFooterLink" href="https://ntemposd.me" target="_blank" rel="noreferrer">ntemposd</a>
      </footer>
    </main>
  );
}