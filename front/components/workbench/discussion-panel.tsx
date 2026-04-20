import { useLayoutEffect, useRef, useState, type RefObject } from "react";

import type { DebateMessage } from "./types";
import { avatarUrlForAgent, getStyleIndex, sanitizeDebateMessageText } from "./utils";

const MESSAGE_PREVIEW_LIMIT = 140;

type DiscussionPanelProps = {
  topic: string;
  discussionActive: boolean;
  statusNote: string;
  messages: DebateMessage[];
  transcriptRef: RefObject<HTMLDivElement | null>;
  onTopicChange: (value: string) => void;
};

export function DiscussionPanel({
  topic,
  discussionActive,
  statusNote,
  messages,
  transcriptRef,
  onTopicChange,
}: DiscussionPanelProps) {
  const [expandedMessageIds, setExpandedMessageIds] = useState<Record<string, boolean>>({});
  const topicEditorRef = useRef<HTMLTextAreaElement | null>(null);

  useLayoutEffect(() => {
    const textarea = topicEditorRef.current;
    if (!textarea) {
      return;
    }

    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight + 4}px`;
  }, [topic]);

  function toggleExpandedMessage(messageId: string) {
    setExpandedMessageIds((currentValue) => ({
      ...currentValue,
      [messageId]: !(currentValue[messageId] ?? true),
    }));
  }

  return (
    <section className="chatColumn">
      <div className="discussionPane">
        <header className="chatHeader">
          <div className="discussionTitleRow">
            <h2 className="sectionTitle columnTitle">DISCUSSION</h2>
            <p className="discussionStatus">[{statusNote.toUpperCase()}]</p>
          </div>
        </header>

        <div className="topicSection">
          <h3 className="sidebarSectionHeading topicSectionHeading">DEBATE TOPIC</h3>
          <textarea
            ref={topicEditorRef}
            className="topicEditor"
            value={topic}
            rows={1}
            onChange={(event) => onTopicChange(event.target.value)}
            placeholder="Set the frame for the debate"
            disabled={discussionActive}
          />
        </div>

        <div className="transcript" ref={transcriptRef}>
          {!messages.length ? (
            <p className="emptyState">
              Draft the council, set the topic, and start the debate. Each selected legend will answer in sequence.
            </p>
          ) : null}

          {messages.map((message) => {
            const isExpanded = expandedMessageIds[message.id] ?? true;
            const sanitizedMessage = sanitizeDebateMessageText(message.message, message.display_name);
            const shouldTruncate = sanitizedMessage.length > MESSAGE_PREVIEW_LIMIT;
            const bubbleToneIndex = getStyleIndex(message.agent_id);
            const visibleMessage = shouldTruncate && !isExpanded
              ? `${sanitizedMessage.slice(0, MESSAGE_PREVIEW_LIMIT).trimEnd()}...`
              : sanitizedMessage;

            return (
              <article
                key={message.id}
                className={`bubble bubbleAssistant bubbleTone${bubbleToneIndex} ${message.failed ? "bubbleFailed" : ""}`.trim()}
              >
                <div className="bubbleHeader">
                  <img
                    className="avatar avatarImage"
                    src={avatarUrlForAgent(message.agent_id)}
                    alt={`${message.display_name} portrait`}
                  />
                  <div>
                    <p className="bubbleName">{message.display_name}</p>
                    <p className="bubbleMeta">Turn {message.turn_number}</p>
                  </div>
                </div>
                <p className="bubbleText">{visibleMessage}</p>
                {shouldTruncate ? (
                  <button
                    type="button"
                    className="bubbleReadMore"
                    onClick={() => toggleExpandedMessage(message.id)}
                  >
                    {isExpanded ? "Read less" : "Read more"}
                  </button>
                ) : null}
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}