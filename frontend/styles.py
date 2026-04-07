"""
EXHUMED – global CSS injected on every page render.
Kept in its own module so app.py stays focused on layout/logic.
"""

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;700&display=swap');

    :root {
        --exhum-native-header-height: 3.75rem;
        --exhum-main-top-gap: 4.5rem;
    }

    .stApp {
        background: #f3f4f6;
        color: #111111;
    }

    .stApp [data-testid="stAppViewContainer"] .main .block-container,
    .stApp .stMainBlockContainer.block-container {
            padding-top: var(--exhum-main-top-gap) !important;
    }

    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
        padding: 0 !important;
        min-height: 0 !important;
        height: 0 !important;
    }

    footer, [data-testid="stDecoration"] {
        display: none !important;
    }

    .stApp, .stApp p, .stApp li, .stApp label {
        font-family: 'IBM Plex Mono', monospace;
    }

    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="collapsedControl"] *,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="collapsedControl"] span,
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
        font-style: normal;
        font-weight: normal;
        font-size: 20px;
        line-height: 1;
        text-transform: none;
        letter-spacing: normal;
        white-space: nowrap;
        word-wrap: normal;
    }

    /* Always show sidebar collapse button */
    [data-testid="stSidebarCollapseButton"] {
        opacity: 1 !important;
        visibility: visible !important;
    }

    section[data-testid="stSidebar"] {
        position: relative;
        background: #ffffff;
        border-right: 2px solid #000000;
    }

    @media (max-width: 1024px) {
        header,
        [data-testid="stHeader"] {
            z-index: 1000 !important;
        }

        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            bottom: 0 !important;
            width: min(22rem, 86vw) !important;
            min-width: min(22rem, 86vw) !important;
            max-width: min(22rem, 86vw) !important;
            height: 100vh !important;
            z-index: 10020 !important;
            box-shadow: 8px 0 24px rgba(0, 0, 0, 0.18) !important;
            transform: translateX(0) !important;
            transition: transform 160ms ease, box-shadow 160ms ease !important;
        }

        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(calc(-1 * min(22rem, 86vw))) !important;
            box-shadow: none !important;
            border-right: none !important;
        }

        section[data-testid="stSidebar"]::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: min(22rem, 86vw);
            height: var(--exhum-native-header-height);
            background: #ffffff;
            border-right: 2px solid #000000;
            z-index: 10019;
            pointer-events: none;
        }

        section[data-testid="stSidebar"][aria-expanded="false"]::before {
            display: none !important;
        }

        section[data-testid="stSidebar"] > div {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
        }

        [data-testid="stSidebarCollapseButton"] {
            position: fixed !important;
            z-index: 10021 !important;
            top: 0.45rem !important;
            left: calc(min(22rem, 86vw) - 3.2rem) !important;
            right: auto !important;
        }

        [data-testid="collapsedControl"] {
            position: fixed !important;
            z-index: 10021 !important;
            top: 0.45rem !important;
            left: 0.55rem !important;
            right: auto !important;
        }
    }

    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        transform: scale(1.18) !important;
        transform-origin: center !important;
    }

    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="collapsedControl"] * {
        font-weight: 900 !important;
        color: #111111 !important;
    }

    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="collapsedControl"] span,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="collapsedControl"] svg {
        font-weight: 900 !important;
        stroke-width: 3 !important;
        color: #111111 !important;
        fill: #111111 !important;
        stroke: #111111 !important;
    }

    .st-key-sidebar_root,
    .st-key-sidebar_root p,
    .st-key-sidebar_root label,
    .st-key-sidebar_root h1,
    .st-key-sidebar_root h2,
    .st-key-sidebar_root h3,
    .st-key-sidebar_root caption,
    .st-key-sidebar_root [data-testid="stMarkdownContainer"],
    .st-key-sidebar_root [data-testid="stCaptionContainer"] {
        color: #111111 !important;
    }

    /* Ensure main area text is always visible */
    [data-testid="stMain"] p,
    [data-testid="stMain"] span,
    [data-testid="stMain"] label,
    [data-testid="stMain"] div,
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] caption,
    [data-testid="stMain"] [data-testid="stMetricLabel"],
    [data-testid="stMain"] [data-testid="stMetricValue"],
    [data-testid="stMain"] [data-testid="stMetricDelta"],
    [data-testid="stMain"] [data-testid="stCaptionContainer"] {
        color: #111111 !important;
    }

    .exhum-sidebar-heading,
    [data-testid="stMain"] h2,
    .exhum-section-title {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 6px 0 10px 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1.18rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        line-height: 1;
        color: #111111 !important;
    }

    [data-testid="stMain"] h2 {
        padding: 0;
        border: none;
        background: transparent;
        box-shadow: none;
    }

    .exhum-card {
        border: 2px solid #000000;
        border-radius: 0;
        padding: 14px;
        background: #ffffff;
        margin-bottom: 10px;
        box-shadow: 4px 4px 0 0 #000000;
    }

    .exhum-topic-hero {
        border: 3px solid #000000;
        border-radius: 0;
        padding: 16px 18px;
        background: #fff7ed;
        box-shadow: 5px 5px 0 0 #000000;
        margin-bottom: 4px;
        position: relative;
        min-height: 68px;
        display: flex;
        align-items: center;
    }

    .exhum-discussion-status-row {
        display: flex;
        align-items: center;
        min-height: 22px;
        margin: 0 0 2px 0;
        padding: 0;
    }

    .exhum-discussion-status-note {
        display: inline-flex;
        align-items: center;
        margin: 0;
        padding: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.92rem;
        font-weight: 500;
        letter-spacing: 0.01em;
        line-height: 1;
        color: #111111 !important;
        text-transform: none;
    }

    .exhum-topic-hero-clickable {
        cursor: pointer;
        transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
    }

    .exhum-topic-hero-clickable:hover {
        background: #ffedd5;
        transform: translate(-1px, -1px);
        box-shadow: 6px 6px 0 0 #000000;
    }

    .exhum-topic-hero-locked {
        background: #f3f4f6;
        color: #6b7280 !important;
        cursor: not-allowed;
    }

    .exhum-topic-hero-locked:hover {
        background: #f3f4f6;
        transform: none;
        box-shadow: 5px 5px 0 0 #000000;
    }

    .exhum-topic-hero-locked .exhum-topic-title {
        color: #6b7280 !important;
    }

    .exhum-topic-title {
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1.08rem;
        font-weight: 700;
        line-height: 1.45;
        letter-spacing: 0.01em;
        color: #111111 !important;
    }

    .st-key-discussion_topic_shell {
        margin-bottom: 2px;
    }

    .exhum-discussion-helper {
        margin: 6px 0 2px 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.77rem;
        line-height: 1.25;
        color: #6b7280 !important;
    }

    .st-key-discussion_topic_shell [data-testid="stMarkdownContainer"] > div:has(.exhum-discussion-helper) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    .st-key-discussion_topic_shell [data-testid="element-container"]:has(.exhum-discussion-helper) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    .st-key-discussion_topic_shell div[class*="st-key-topic_edit_trigger"],
    .st-key-discussion_topic_shell div[class*="st-key-topic_edit_trigger"] > div,
    .st-key-discussion_topic_shell div[class*="st-key-topic_edit_trigger"] [data-testid="stButton"],
    .st-key-discussion_topic_shell iframe {
        display: block !important;
        width: 0 !important;
        max-width: 0 !important;
        height: 0 !important;
        max-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        border: 0 !important;
    }

    .st-key-discussion_topic_shell div[class*="st-key-topic_edit_trigger"] > button,
    .st-key-discussion_topic_shell div[class*="st-key-topic_edit_trigger"] [data-testid="stButton"] > button,
    .st-key-discussion_topic_shell div[class*="st-key-topic_edit_trigger"] .stButton > button {
        position: absolute !important;
        width: 1px !important;
        min-width: 1px !important;
        height: 1px !important;
        min-height: 1px !important;
        padding: 0 !important;
        margin: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    .st-key-discussion_panel > [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(.st-key-discussion_panel),
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(.st-key-discussion_panel) > div,
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(.st-key-discussion_panel) [data-testid="stVerticalBlock"]:has(> .st-key-discussion_panel),
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(.st-key-discussion_panel) [data-testid="stVerticalBlock"]:has(.exhum-telemetry-hero) {
        gap: 0 !important;
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    .st-key-discussion_panel [data-testid="stVerticalBlock"]:has(.exhum-telemetry-hero) {
        gap: 0 !important;
    }

    .st-key-discussion_panel [data-testid="element-container"]:has(.exhum-telemetry-hero),
    .st-key-discussion_panel [data-testid="element-container"]:has(.exhum-discussion-status-row),
    .st-key-discussion_panel [data-testid="element-container"]:has(.st-key-discussion_topic_shell) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"]:has(.st-key-telemetry_panel) {
        padding-left: 1rem;
    }

    .st-key-topic_edit_form [data-testid="stFormSubmitButton"] > button,
    div[class*="st-key-topic_save_submit"] > button,
    div[class*="st-key-topic_cancel_submit"] > button,
    div[class*="st-key-topic_save_submit"] [data-testid="stFormSubmitButton"] > button,
    div[class*="st-key-topic_cancel_submit"] [data-testid="stFormSubmitButton"] > button {
        min-height: 48px;
        background: #ffffff !important;
        color: #111111 !important;
        border: 3px solid #000000 !important;
        box-shadow: 4px 4px 0 0 #000000 !important;
        text-transform: none !important;
    }

    .st-key-topic_edit_form [data-testid="stFormSubmitButton"] > button p,
    .st-key-topic_edit_form [data-testid="stFormSubmitButton"] > button span,
    .st-key-topic_edit_form [data-testid="stFormSubmitButton"] > button div,
    div[class*="st-key-topic_save_submit"] > button p,
    div[class*="st-key-topic_save_submit"] > button span,
    div[class*="st-key-topic_save_submit"] > button div,
    div[class*="st-key-topic_cancel_submit"] > button p,
    div[class*="st-key-topic_cancel_submit"] > button span,
    div[class*="st-key-topic_cancel_submit"] > button div,
    div[class*="st-key-topic_save_submit"] [data-testid="stFormSubmitButton"] > button p,
    div[class*="st-key-topic_cancel_submit"] [data-testid="stFormSubmitButton"] > button p {
        color: #111111 !important;
        font-weight: 800 !important;
    }

    div[class*="st-key-topic_save_submit"] > button,
    div[class*="st-key-topic_save_submit"] [data-testid="stFormSubmitButton"] > button {
        background: #facc15 !important;
    }

    div[class*="st-key-topic_save_submit"] > button:hover,
    div[class*="st-key-topic_save_submit"] [data-testid="stFormSubmitButton"] > button:hover {
        background: #eab308 !important;
        color: #111111 !important;
        box-shadow: 5px 5px 0 0 #000000 !important;
    }

    div[class*="st-key-topic_cancel_submit"] > button,
    div[class*="st-key-topic_cancel_submit"] [data-testid="stFormSubmitButton"] > button {
        background: #e5e7eb !important;
    }

    div[class*="st-key-topic_cancel_submit"] > button:hover,
    div[class*="st-key-topic_cancel_submit"] [data-testid="stFormSubmitButton"] > button:hover {
        background: #d1d5db !important;
        color: #111111 !important;
        box-shadow: 5px 5px 0 0 #000000 !important;
    }

    .exhum-topic-edit-link {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 36px;
        height: 36px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        font-size: 1rem;
        line-height: 1;
        color: #111111;
        background: #fff7ed;
        border: 2px solid #000000;
        border-radius: 0;
        box-shadow: 2px 2px 0 0 #000000;
    }

    }

    .st-key-sidebar_root .st-key-drafted_council_chips {
        margin-top: 8px;
        margin-bottom: 14px;
    }

    .st-key-sidebar_root .st-key-drafted_council_chips [data-testid="stHorizontalBlock"] {
        gap: 0.65rem;
        align-items: stretch;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="column"] {
        width: 100% !important;
        display: flex;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] {
        width: 100%;
        height: 100%;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] > button,
    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button {
        min-height: 42px;
        width: 100%;
        max-width: 100%;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start;
        text-align: left;
        padding: 7px 10px;
        border: 3px solid #000000 !important;
        border-radius: 0 !important;
        background: #fffaf3 !important;
        box-shadow: 6px 6px 0 0 #000000 !important;
        color: #111111 !important;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: none !important;
        letter-spacing: 0.01em;
        line-height: 1.15;
        font-family: 'IBM Plex Mono', monospace !important;
        overflow: hidden !important;
        transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] > button::after,
    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button::after {
        content: "x";
        margin-left: auto;
        padding-left: 0.65rem;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.78rem;
        font-weight: 800;
        line-height: 1;
        color: #111111 !important;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] > button:hover,
    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button:hover {
        background: #fff1de !important;
        border-color: #000000 !important;
        color: #111111 !important;
        transform: translate(-1px, -1px);
        box-shadow: 7px 7px 0 0 #000000 !important;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] > button:focus,
    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] > button:focus-visible,
    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button:focus,
    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button:focus-visible {
        outline: none;
        border-color: #000000 !important;
        box-shadow: 7px 7px 0 0 #000000 !important;
    }

    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button p {
        margin: 0 !important;
        color: #111111 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.74rem !important;
        font-weight: 700 !important;
        text-transform: none !important;
        letter-spacing: 0.01em !important;
        white-space: nowrap !important;
        line-height: 1.15 !important;
        text-align: left !important;
        max-width: 100% !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    .exhum-drafted-empty {
        margin-top: 8px;
        margin-bottom: 14px;
        border: 2px dashed #000000;
        border-radius: 4px;
        padding: 14px 12px;
        background: #fff7ed;
        box-shadow: 3px 3px 0 0 #000000;
        text-align: center;
        font-size: 0.76rem;
        font-weight: 700;
        line-height: 1.45;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #111111 !important;
    }

    .exhum-legend-card {
        border: 2px solid #000000;
        border-radius: 4px 4px 0 0;
        border-bottom: none;
        background: #ffffff;
        box-shadow: 3px 3px 0 0 #000000;
        padding: 10px 10px 4px 10px;
        margin-bottom: 0;
        color: #111111 !important;
        min-height: 136px;
        position: relative;
        transition: background-color 120ms ease, border-color 120ms ease;
    }

    .exhum-legend-card p, .exhum-legend-card div, .exhum-legend-card span {
        color: #111111 !important;
    }

    .exhum-legend-name {
        margin: 0 0 3px 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.94rem;
        font-weight: 700;
        line-height: 1.25;
        letter-spacing: 0.02em;
        color: #111111 !important;
        text-transform: uppercase;
    }

    .exhum-legend-meta {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.75rem;
        font-weight: 500;
        line-height: 1.25;
        letter-spacing: 0.02em;
        color: #555555 !important;
        margin: 0;
    }

    .exhum-legend-state-badge {
        position: absolute;
        top: 8px;
        right: 8px;
        border: 2px solid #000000;
        border-radius: 0;
        padding: 2px 8px;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: none;
        background: #dcfce7;
        color: #166534;
        box-shadow: 2px 2px 0 0 #000000;
    }
    .exhum-legend-selected {
        border: 2px solid #000000;
        border-bottom: none;
        background: #ffffff;
        box-shadow: 5px 5px 0 0 #39ff14;
    }

    [data-testid="stDialog"] [data-testid="stVerticalBlock"]:has(.exhum-legend-card):has(button):not(:has([data-testid="stVerticalBlock"] .exhum-legend-card)) {
        gap: 0 !important;
    }

    [data-testid="stDialog"] [role="dialog"],
    [data-testid="stDialog"] > div {
        background: #ffffff !important;
    }

    [data-testid="stDialog"] [role="dialog"] {
        border: 3px solid #000000 !important;
        border-radius: 0 !important;
        box-shadow: 8px 8px 0 0 #000000 !important;
    }

    [data-testid="stDialog"] [role="dialog"] > div,
    [data-testid="stDialog"] [role="dialog"] [data-testid="stVerticalBlock"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stDialog"] [role="dialog"] h1,
    [data-testid="stDialog"] [role="dialog"] h2,
    [data-testid="stDialog"] [role="dialog"] h3 {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stDialog"] [role="dialog"] h1,
    [data-testid="stDialog"] [role="dialog"] h2,
    [data-testid="stDialog"] [role="dialog"] h3,
    [data-testid="stDialog"] [role="dialog"] p,
    [data-testid="stDialog"] [role="dialog"] span,
    [data-testid="stDialog"] [role="dialog"] label,
    [data-testid="stDialog"] [role="dialog"] div {
        color: #111111;
    }

    [data-testid="stDialog"] [data-testid="stCaptionContainer"] p {
        margin: 0 0 14px 0 !important;
        color: #4b5563 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.74rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        line-height: 1.45 !important;
        text-transform: none !important;
    }

    [data-testid="stDialog"] button[aria-label="Close"] {
        border: 2px solid #000000 !important;
        border-radius: 0 !important;
        background: #ffffff !important;
        color: #111111 !important;
        box-shadow: 2px 2px 0 0 #000000 !important;
    }

    [data-testid="stDialog"] button[aria-label="Close"]:hover {
        background: #f3f4f6 !important;
        border-color: #000000 !important;
    }

    [data-testid="stDialog"] .exhum-legend-card:not(.exhum-legend-selected):hover {
        background: #ffffff;
        border-color: #000000;
        border-bottom: none;
    }

    [data-testid="stDialog"] .exhum-legend-card,
    [data-testid="stDialog"] .exhum-legend-selected {
        border-radius: 0 !important;
    }

    [data-testid="stDialog"] .exhum-legend-selected:hover {
        background: #ffffff;
        border-color: #000000;
        border-bottom: none;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_add_"],
    [data-testid="stDialog"] div[class*="st-key-draft_remove_"] {
        margin: 0 0 14px 0;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_add_"] button,
    [data-testid="stDialog"] div[class*="st-key-draft_remove_"] button {
        width: 100%;
        min-height: 42px;
        margin-top: 0 !important;
        border-radius: 0 !important;
        border-top: none !important;
        position: relative;
        box-shadow: 3px 3px 0 0 #000000 !important;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_add_"] button::before,
    [data-testid="stDialog"] div[class*="st-key-draft_remove_"] button::before {
        content: "";
        position: absolute;
        top: 0;
        left: 5%;
        width: 90%;
        border-top: 2px dashed #aaaaaa;
        pointer-events: none;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_add_"] button:hover,
    [data-testid="stDialog"] div[class*="st-key-draft_remove_"] button:hover {
        transform: none !important;
        box-shadow: 3px 3px 0 0 #000000 !important;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_add_"] button {
        background: #ffffff !important;
        color: #15803d !important;
        border: 2px solid #000000 !important;
        border-top: none !important;
        box-shadow: 3px 3px 0 0 #000000 !important;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_add_"] button * {
        color: #15803d !important;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_add_"] button:hover {
        background: #ecfdf3 !important;
        color: #15803d !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        text-shadow: 0.25px 0 currentColor, -0.25px 0 currentColor;
        border: 2px solid #000000 !important;
        border-top: none !important;
        box-shadow: 3px 3px 0 0 #000000 !important;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_add_"] button:hover * {
        color: #15803d !important;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_remove_"] button {
        background: #ffffff !important;
        color: #b91c1c !important;
        border: 2px solid #000000 !important;
        border-top: none !important;
        box-shadow: 5px 5px 0 0 #39ff14 !important;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_remove_"] button * {
        color: #b91c1c !important;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_remove_"] button:hover {
        background: #fff1f2 !important;
        color: #b91c1c !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        text-shadow: 0.25px 0 currentColor, -0.25px 0 currentColor;
        border: 2px solid #000000 !important;
        border-top: none !important;
        box-shadow: 5px 5px 0 0 #39ff14 !important;
    }

    [data-testid="stDialog"] div[class*="st-key-draft_remove_"] button:hover * {
        color: #b91c1c !important;
    }

    .exhum-legend-avatar {
        width: 64px;
        height: 64px;
        border: 1px solid #000000;
        border-radius: 0;
        object-fit: cover;
        box-shadow: 2px 2px 0 0 #000000;
        margin-bottom: 8px;
        background: #ffffff;
    }

    .exhum-bubble {
        border: 2px solid #000000;
        border-radius: 0;
        width: 100%;
        max-width: 100%;
        padding: 14px 18px;
        margin: 10px 0;
        line-height: 1.72;
        font-size: 1.06rem;
        box-shadow: 4px 4px 0 0 #000000;
        background: #ffffff;
    }

    .exhum-bubble p {
        margin: 0;
        font-size: 1.06rem;
        line-height: 1.72;
    }

    .exhum-bubble-header-main {
        display: flex;
        flex: 1;
        min-width: 0;
        flex-direction: column;
        justify-content: flex-end;
        gap: 3px;
    }

    .exhum-bubble-progress-track {
        width: calc(100% + 36px);
        height: 2px;
        border: none;
        background: #ffffff;
        overflow: hidden;
        margin: -14px -18px 10px -18px;
    }

    .exhum-bubble-progress-track-inline {
        background: rgba(17, 17, 17, 0.14);
    }

    .exhum-bubble-progress-fill {
        height: 100%;
        background: #2563eb;
    }

    .exhum-thinking-pulse {
        display: inline-block;
        font-weight: 400;
        animation: exhum-thinking-pulse 1s ease-in-out infinite;
    }

    @keyframes exhum-thinking-pulse {
        0%, 100% { opacity: 0.45; }
        50% { opacity: 1; }
    }

    .exhum-bubble-0 { background: #fff1e8; border-left: 8px solid #ff6b00; }
    .exhum-bubble-1 { background: #eceff3; border-left: 8px solid #1f2937; }
    .exhum-bubble-2 { background: #e9fbfa; border-left: 8px solid #0ea5a4; }
    .exhum-bubble-3 { background: #e9f1ff; border-left: 8px solid #2563eb; }
    .exhum-bubble-4 { background: #ecfdf3; border-left: 8px solid #16a34a; }

    [data-testid="element-container"]:has(.exhum-read-more-anchor) + [data-testid="element-container"]:has(.stButton),
    [data-testid="element-container"]:has(.exhum-read-more-anchor) + [data-testid="element-container"]:has([data-testid="stButton"]) {
        display: flex !important;
        justify-content: flex-end !important;
        margin-top: -2px !important;
        margin-bottom: 10px !important;
    }

    [data-testid="element-container"]:has(.exhum-read-more-anchor) + [data-testid="element-container"]:has(.stButton) .stButton,
    [data-testid="element-container"]:has(.exhum-read-more-anchor) + [data-testid="element-container"]:has([data-testid="stButton"]) [data-testid="stButton"] {
        width: fit-content;
    }

    [data-testid="element-container"]:has(.exhum-read-more-anchor) + [data-testid="element-container"]:has(.stButton) .stButton > button,
    [data-testid="element-container"]:has(.exhum-read-more-anchor) + [data-testid="element-container"]:has([data-testid="stButton"]) [data-testid="stButton"] > button {
        min-height: 32px !important;
        padding: 4px 10px !important;
        font-size: 0.75rem !important;
        box-shadow: 2px 2px 0 0 #000000 !important;
    }

    [data-testid="element-container"]:has(.exhum-read-more-color-0) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #fff1e8 !important; }
    [data-testid="element-container"]:has(.exhum-read-more-color-1) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #eceff3 !important; }
    [data-testid="element-container"]:has(.exhum-read-more-color-2) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #e9fbfa !important; }
    [data-testid="element-container"]:has(.exhum-read-more-color-3) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #e9f1ff !important; }
    [data-testid="element-container"]:has(.exhum-read-more-color-4) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #ecfdf3 !important; }

    .exhum-header {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 12px;
    }

    .exhum-bubble-header-static {
        align-items: flex-end;
    }

    .exhum-brand-logo {
        display: block;
        width: 62%;
        max-width: 140px;
        height: auto;
        margin: 0 auto 8px auto;
    }

    .exhum-brand-copy {
        text-align: center;
        margin: 0 auto 14px auto;
        width: 100%;
        max-width: 280px;
    }

    .exhum-brand-title {
        display: block;
        width: 100%;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        line-height: 0.95;
        color: #111111;
        margin-bottom: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: clip;
    }

    .exhum-brand-subtitle {
        display: block;
        font-size: 1.05rem;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 500;
        line-height: 1.35;
        margin-top: 0;
        margin-bottom: 2px;
        color: #555555;
    }

    .exhum-sticky-footer {
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 999;
        text-align: center;
        padding: 4px 12px;
        border-top: 2px solid #000000;
        background: #ffffff;
        opacity: 0.9;
        font-size: 12px;
    }

    .exhum-avatar {
        width: 44px;
        height: 44px;
        border-radius: 0;
        border: 1px solid #000000;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 13px;
        flex-shrink: 0;
    }

    .exhum-avatar-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 0;
    }

    .exhum-name {
        display: block;
        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 800;
        font-size: 1.45rem;
        letter-spacing: 0.04em;
        line-height: 0.98;
    }

    .exhum-meta {
        font-size: 0.76rem;
        opacity: 0.75;
        margin-left: 0;
    }

    .exhum-turn-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-left: auto;
        min-height: 24px;
        padding: 0.12rem 0.5rem;
        border: 2px solid #000000;
        background: #ffffff;
        box-shadow: 2px 2px 0 #000000;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.64rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #111111 !important;
        white-space: nowrap;
    }

    .exhum-speaker {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
        padding: 8px 10px;
        border-radius: 0;
        border: 2px solid #000000;
        margin-bottom: 6px;
        background: #ffffff;
    }

    .exhum-speaker-link {
        display: block;
        text-decoration: none;
        color: inherit !important;
    }

    .exhum-speaker-archetype {
        font-size: 0.72rem;
        font-weight: 400;
        opacity: 0.6;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        margin-top: 1px;
    }

    .exhum-speaker-progress-wrap {
        flex-basis: 100%;
        width: 100%;
        margin-top: 8px;
    }

    .exhum-speaker-progress-track {
        width: 100%;
        height: 10px;
        border: 2px solid #000000;
        background: #ffffff;
        box-shadow: 2px 2px 0 0 #000000;
        overflow: hidden;
    }

    .exhum-speaker-progress-fill {
        height: 100%;
        background: #2563eb;
    }

    .exhum-speaker-progress-footer {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-top: 4px;
    }

    .exhum-speaker-progress-text {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .exhum-empty {
        text-align: center;
        padding: 60px 20px;
        opacity: 0.75;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] > div {
        border: 2px solid #000000 !important;
        border-radius: 4px !important;
        background: #ffffff !important;
        color: #111111 !important;
        box-shadow: 3px 3px 0 0 #000000;
    }

    .stButton > button {
        border: 3px solid #000000;
        border-radius: 0;
        background: #1f2937;
        color: #f8fafc;
        box-shadow: 4px 4px 0 0 #000000;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .stButton > button p {
        white-space: nowrap;
        color: #f8fafc !important;
        font-weight: 800 !important;
    }

    .stButton > button:hover {
        transform: translate(-1px, -1px);
        box-shadow: 5px 5px 0 0 #000000;
        border-color: #000000;
        background: #374151;
        color: #f8fafc;
    }

    .stButton > button[kind="primary"] {
        background: #facc15;
        border: 3px solid #000000;
        color: #111111;
        box-shadow: 4px 4px 0 0 #000000;
        min-height: 48px;
        font-size: 0.95rem;
    }

    .stButton > button[kind="primary"] p {
        color: #111111 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #e0a800;
        color: #111111;
        box-shadow: 5px 5px 0 0 #000000;
    }

    .st-key-telemetry_panel {
        padding-top: 0;
    }

    .exhum-telemetry-hero {
        margin: 0 0 12px 0;
        padding: 0 0 10px 0;
        border-bottom: 2px solid #111111;
    }

    .exhum-telemetry-title {
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        line-height: 0.95;
        color: #111111 !important;
    }

    .exhum-telemetry-subtitle {
        margin: 6px 0 0 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.77rem;
        font-weight: 500;
        line-height: 1.45;
        letter-spacing: 0.01em;
        color: #4b5563 !important;
    }

    .st-key-exhum_telemetry_panel {
        font-family: 'IBM Plex Mono', monospace;
        color: #111111;
        margin-top: 0;
        padding-top: 0;
        --exhum-telemetry-box-gap: 14px;
        --exhum-telemetry-heading-gap: 8px;
    }

    .st-key-telemetry_panel > [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_system_status_section),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_neural_section),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_context_section),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_cost_section),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_entropy_section),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_airtime_section) {
        margin: 0 0 var(--exhum-telemetry-box-gap) 0 !important;
    }

    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_airtime_section) {
        margin-bottom: 0 !important;
    }

    .st-key-exhum_telemetry_system_status_section > [data-testid="stVerticalBlock"],
    .st-key-exhum_telemetry_neural_section > [data-testid="stVerticalBlock"],
    .st-key-exhum_telemetry_context_section > [data-testid="stVerticalBlock"],
    .st-key-exhum_telemetry_cost_section > [data-testid="stVerticalBlock"],
    .st-key-exhum_telemetry_entropy_section > [data-testid="stVerticalBlock"],
    .st-key-exhum_telemetry_airtime_section > [data-testid="stVerticalBlock"] {
        gap: var(--exhum-telemetry-heading-gap) !important;
    }

    .st-key-exhum_telemetry_entropy_section,
    .st-key-exhum_telemetry_airtime_section {
        padding-top: var(--exhum-telemetry-box-gap);
    }

    .st-key-telemetry_panel [data-testid="element-container"]:has(.exhum-telemetry-section-heading),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_system_status_card),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_neural_block),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_context_block),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_cost_block),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_entropy_block),
    .st-key-telemetry_panel [data-testid="element-container"]:has(.st-key-exhum_telemetry_airtime_block) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    .exhum-telemetry-section-heading {
        display: flex;
        flex-direction: column;
        gap: 2px;
        margin: 0;
    }

    .exhum-telemetry-section-heading-compact {
        margin: 0;
    }

    .exhum-telemetry-section-title {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        line-height: 1.05;
        color: #111111 !important;
        padding-bottom: 0.35rem;
    }

    .exhum-telemetry-status-dot {
        display: inline-block;
        flex: 0 0 auto;
        width: 0.72rem;
        height: 0.72rem;
        margin-right: 0;
        border: 2px solid #111111;
        border-radius: 999px;
        box-shadow: 1px 1px 0 #000000;
        vertical-align: baseline;
    }

    .exhum-telemetry-status-dot-optimal,
    .exhum-telemetry-status-dot-online {
        background: radial-gradient(circle at 35% 35%, #dcfce7 0 34%, #22c55e 35% 100%);
    }

    .exhum-telemetry-status-dot-degraded,
    .exhum-telemetry-status-dot-offline {
        background: radial-gradient(circle at 35% 35%, #fee2e2 0 34%, #ef4444 35% 100%);
    }

    .exhum-telemetry-status-dot-standby,
    .exhum-telemetry-status-dot-idle {
        background: radial-gradient(circle at 35% 35%, #fef3c7 0 34%, #f59e0b 35% 100%);
    }

    .st-key-exhum_telemetry_system_status_card {
        margin: 0;
        border: 3px solid #000000;
        border-radius: 0;
        background: #ffffff;
        box-shadow: 6px 6px 0 #000000;
        padding: 12px 12px 10px 12px;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="element-container"],
    .st-key-exhum_telemetry_neural_block [data-testid="element-container"],
    .st-key-exhum_telemetry_context_block [data-testid="element-container"],
    .st-key-exhum_telemetry_cost_block [data-testid="element-container"],
    .st-key-exhum_telemetry_entropy_block [data-testid="element-container"],
    .st-key-exhum_telemetry_airtime_block [data-testid="element-container"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    .st-key-exhum_telemetry_system_status_card details {
        border: none;
        border-radius: 0;
        background: transparent;
        box-shadow: none;
        padding: 0;
        margin-top: 0;
        padding-top: 0;
    }

    .st-key-exhum_telemetry_system_status_card summary {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding-top: 0;
        color: #111111 !important;
        background: #ffffff !important;
    }

    .st-key-exhum_telemetry_system_status_card summary *,
    .st-key-exhum_telemetry_system_status_card details[open] summary,
    .st-key-exhum_telemetry_system_status_card details[open] summary * {
        color: #111111 !important;
        fill: #111111 !important;
        background: #ffffff !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stExpander"] {
        margin-top: 0;
        margin-bottom: 0;
    }

    .st-key-exhum_telemetry_neural_block [data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #000000 !important;
        border-radius: 0 !important;
        background: #ffffff !important;
        box-shadow: 6px 6px 0 #000000 !important;
        margin: 0 !important;
    }

    .st-key-exhum_telemetry_neural_block,
    .st-key-exhum_telemetry_context_block,
    .st-key-exhum_telemetry_cost_block,
    .st-key-exhum_telemetry_entropy_block,
    .st-key-exhum_telemetry_airtime_block {
        margin: 0;
    }

    .st-key-exhum_telemetry_context_block > [data-testid="stVerticalBlock"] {
        gap: 0.45rem;
    }

    .st-key-exhum_telemetry_context_shell,
    .st-key-exhum_telemetry_context_shell[data-testid="stVerticalBlockBorderWrapper"],
    .st-key-exhum_telemetry_context_shell [data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #000000 !important;
        border-radius: 0 !important;
        background: #ffffff !important;
        box-shadow: 6px 6px 0 #000000 !important;
        padding: 0.8rem 0.85rem 0.75rem 0.85rem;
        margin: 0 !important;
    }

    .st-key-exhum_telemetry_context_shell > [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stMarkdownContainer"] > p {
        margin: 0;
    }

    .exhum-telemetry-token-header {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        padding-bottom: 0.45rem;
        border-bottom: 2px solid #111111;
        margin-bottom: 1rem;
    }

    .exhum-telemetry-token-note {
        border-top: 2px solid #111111;
        margin-top: 0.05rem;
        padding-top: 0.45rem;
        padding-bottom: 0.75rem;
    }

    .exhum-telemetry-context-topline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
    }

    .exhum-telemetry-context-value {
        display: block;
        flex: 1 1 auto;
        min-width: 0;
        margin: 0;
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1.15rem;
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: 0.01em;
        color: #111111 !important;
    }

    .exhum-telemetry-context-pct {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 0;
        min-height: 22px;
        padding: 0.08rem 0.45rem;
        border: 2px solid #000000;
        background: #ffffff;
        box-shadow: 2px 2px 0 #000000;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.66rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: 0.06em;
        color: #111111 !important;
    }

    .st-key-exhum_telemetry_cost_block [data-testid="stMarkdownContainer"] {
        width: 100%;
    }

    .st-key-exhum_telemetry_cost_block [data-testid="stMarkdownContainer"] > p {
        margin: 0;
    }

    .exhum-telemetry-cost-card {
        display: flex;
        flex-direction: column;
            gap: 0.5rem;
        width: 100%;
        border: 3px solid #000000;
        background: #ffffff;
        box-shadow: 6px 6px 0 #000000;
        padding: 0.8rem 0.85rem 0.75rem 0.85rem;
    }

    .exhum-telemetry-cost-value {
        display: block;
        width: 100%;
        margin: 0;
            padding-bottom: 0.45rem;
            border-bottom: 2px solid #111111;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1.4rem;
        font-weight: 800;
        line-height: 1.02;
        letter-spacing: 0.01em;
        color: #111111 !important;
    }

    .exhum-telemetry-cost-caption {
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.69rem;
        font-weight: 500;
        line-height: 1.35;
        color: #57534e !important;
    }

    .st-key-exhum_telemetry_neural_block [data-testid="stCaptionContainer"],
    .st-key-exhum_telemetry_airtime_block [data-testid="stCaptionContainer"],
    .st-key-exhum_telemetry_context_block [data-testid="stCaptionContainer"],
    .st-key-exhum_telemetry_system_status_card [data-testid="stCaptionContainer"] {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.69rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #374151 !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stMarkdownContainer"] > p {
        margin: 0;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stHorizontalBlock"] {
        align-items: center;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stExpanderDetails"] {
        padding-top: 4px;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"],
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"],
    .st-key-exhum_telemetry_context_block [data-testid="stTable"],
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] {
        display: block;
        width: 100%;
        max-width: 100%;
        border: 3px solid #000000;
        box-shadow: 6px 6px 0 #000000;
        background: #ffffff;
        overflow-x: auto;
        overflow-y: hidden;
        scrollbar-gutter: stable both-edges;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] > div,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] > div,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] > div,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] > div {
        width: max-content !important;
        min-width: 100% !important;
        max-width: 100% !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] *,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] *,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] *,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] * {
        font-family: 'IBM Plex Mono', monospace !important;
        color: #111111 !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] table,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] table,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] table,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] table {
        width: max-content !important;
        min-width: 100% !important;
        border-collapse: collapse;
        table-layout: auto !important;
        background: #ffffff !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] colgroup col:first-child,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] colgroup col:first-child,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] colgroup col:first-child,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] colgroup col:first-child {
        width: 0 !important;
        display: none !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] thead tr > *:first-child,
    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] tbody tr > *:first-child,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] thead tr > *:first-child,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] tbody tr > *:first-child,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] thead tr > *:first-child,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] tbody tr > *:first-child,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] thead tr > *:first-child,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] tbody tr > *:first-child {
        display: none !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] thead tr,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] thead tr,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] thead tr,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] thead tr {
        background: #f3f4f6 !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] th,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] th,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] th,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] th {
        background: #f3f4f6 !important;
        font-size: 0.65rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        border-bottom: 2px solid #000000 !important;
        padding: 0.3rem 0.55rem !important;
        text-align: left !important;
        line-height: 1.05 !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] th *,
    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] td * {
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] thead tr > *:last-child,
    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] tbody tr > *:last-child {
        min-width: 5.75rem !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] td,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] td,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] td,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] td {
        background: #ffffff !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        border-bottom: 1px solid #d1d5db !important;
        padding: 0.42rem 0.55rem !important;
        white-space: nowrap !important;
    }

    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] table,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] thead,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] tbody,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] tr,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] th,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] td,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] * {
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] th:nth-child(2),
    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] td:nth-child(2) {
        width: 60%;
        text-align: left !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] th:nth-child(3),
    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] td:nth-child(3) {
        width: 40%;
        text-align: right !important;
    }

    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] th:nth-child(2),
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] td:nth-child(2) {
        width: 60%;
    }

    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] th:nth-child(3),
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] td:nth-child(3) {
        width: 40%;
        text-align: right !important;
    }

    .st-key-exhum_telemetry_context_block [data-testid="stTable"] th:nth-child(2),
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] td:nth-child(2) {
        width: 60%;
    }

    .st-key-exhum_telemetry_context_block [data-testid="stTable"] th:nth-child(3),
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] td:nth-child(3) {
        width: 40%;
        text-align: right !important;
    }

    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] th:nth-child(2),
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] td:nth-child(2) {
        width: 60%;
        text-align: left !important;
    }

    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] th:nth-child(3),
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] td:nth-child(3) {
        text-align: right !important;
        width: 18%;
        padding-right: 0.85rem !important;
    }

    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] th:nth-child(4),
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] td:nth-child(4) {
        text-align: right !important;
        width: 22%;
        padding-left: 1rem !important;
        border-left: 1px solid #d1d5db !important;
    }

    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] td:nth-child(2),
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] td:nth-child(2) * {
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] tbody tr:last-child td,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] tbody tr:last-child td,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] tbody tr:last-child td,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] tbody tr:last-child td {
        border-bottom: none !important;
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stMetric"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }

    .st-key-exhum_telemetry_context_block [data-testid="stProgressBar"] {
        margin-top: 2px;
    }

    .st-key-exhum_telemetry_context_block [data-testid="stProgressBar"] div[role="progressbar"] {
        background: #111111 !important;
    }

    .st-key-exhum_telemetry_context_block [data-testid="stProgressBar"] > div {
        background: #ffffff !important;
        border: 3px solid #000000;
        border-radius: 0 !important;
        box-shadow: 6px 6px 0 #000000;
        overflow: hidden;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        overflow-x: auto;
        overflow-y: visible;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] table {
        background: transparent !important;
        table-layout: auto !important;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] thead tr {
        background: transparent !important;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] th {
        background: transparent !important;
        padding: 0.25rem 0.45rem 0.55rem 0.45rem !important;
        border-bottom: 1px solid #111111 !important;
        font-size: 0.58rem !important;
        line-height: 1 !important;
        white-space: nowrap !important;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] tbody tr > *:first-child,
    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] colgroup col:first-child {
        display: none !important;
        width: 0 !important;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] td {
        background: transparent !important;
        padding: 0.58rem 0.45rem !important;
        border-bottom: 1px solid #9ca3af !important;
        font-size: 0.68rem !important;
        line-height: 1.15 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] tbody tr:last-child td {
        border-bottom: none !important;
        padding-bottom: 0.55rem !important;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] th:nth-child(2),
    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] td:nth-child(2) {
        width: 22%;
        text-align: left !important;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] th:nth-child(3),
    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] td:nth-child(3) {
        width: 26%;
        text-align: right !important;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] th:nth-child(4),
    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] td:nth-child(4) {
        width: 26%;
        text-align: right !important;
    }

    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] th:nth-child(5),
    .st-key-exhum_telemetry_context_shell [data-testid="stTable"] td:nth-child(5) {
        width: 26%;
        text-align: right !important;
    }

    @media (max-width: 768px) {
        [data-testid="stMain"] h2 {
            margin: 4px 0 8px 0;
        }

        .st-key-exhum_telemetry_system_status_card {
            box-shadow: 4px 4px 0 #000000;
            padding: 10px 10px 8px 10px;
        }

        .st-key-exhum_telemetry_context_shell [data-testid="stTable"] td {
            font-size: 0.64rem !important;
        }

        .st-key-exhum_telemetry_context_shell [data-testid="stTable"] th {
            font-size: 0.54rem !important;
        }

        .st-key-exhum_telemetry_neural_block [data-testid="stVerticalBlockBorderWrapper"] {
            box-shadow: 4px 4px 0 #000000 !important;
        }

        .st-key-exhum_telemetry_system_status_card [data-testid="stTable"],
        .st-key-exhum_telemetry_neural_block [data-testid="stTable"],
        .st-key-exhum_telemetry_context_block [data-testid="stTable"],
        .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] {
            box-shadow: 4px 4px 0 #000000;
        }

        .exhum-telemetry-cost-card {
            box-shadow: 4px 4px 0 #000000;
        }

        .st-key-exhum_telemetry_context_shell,
        .st-key-exhum_telemetry_context_shell[data-testid="stVerticalBlockBorderWrapper"],
        .st-key-exhum_telemetry_context_shell [data-testid="stVerticalBlockBorderWrapper"] {
            box-shadow: 4px 4px 0 #000000 !important;
        }

        .st-key-exhum_telemetry_context_block [data-testid="stProgressBar"] > div {
            box-shadow: 4px 4px 0 #000000;
        }
    }

    .exhum-telemetry-entropy-card {
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
        width: 100%;
        border: 3px solid #000000;
        background: #ffffff;
        box-shadow: 6px 6px 0 #000000;
        padding: 0.8rem 0.85rem 0.75rem 0.85rem;
    }

    .exhum-telemetry-entropy-topline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
    }

    .exhum-telemetry-entropy-value-inline {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1.28rem;
        font-weight: 800;
        line-height: 1.02;
        color: #111111 !important;
    }

    .exhum-telemetry-entropy-status {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 22px;
        padding: 0.08rem 0.45rem;
        border: 2px solid #000000;
        background: #ffffff;
        box-shadow: 2px 2px 0 #000000;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #111111 !important;
        white-space: nowrap;
    }

    .exhum-telemetry-entropy-progress {
        display: flex;
        flex-direction: column;
        gap: 0.38rem;
    }

    .exhum-telemetry-entropy-track {
        position: relative;
        height: 18px;
        border: 2px solid #000000;
        background: #ffffff;
        box-shadow: 3px 3px 0 #000000;
        overflow: hidden;
    }

    .exhum-telemetry-entropy-fill {
        position: absolute;
        inset: 0 auto 0 0;
        height: 100%;
        background: #0ea5a4;
        border-right: 2px solid #000000;
    }

    .exhum-telemetry-entropy-caption {
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.69rem;
        font-weight: 500;
        line-height: 1.35;
        color: #475569 !important;
    }

    @media (max-width: 768px) {
        .exhum-telemetry-entropy-card {
            box-shadow: 4px 4px 0 #000000;
        }
    }

    .exhum-temperature-controller {
        border: none;
        background: transparent;
        padding: 0;
        margin: 2px 0 0 0;
        box-shadow: none;
        border-radius: 0;
    }

    .exhum-temperature-caption {
        display: block;
        font-size: 0.68rem;
        font-weight: 500;
        margin-top: 0;
        margin-bottom: 2px;
        color: #111111;
    }

    .exhum-sidebar-button-note {
        margin: 0.2rem 0 0.55rem 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.66rem;
        font-weight: 500;
        line-height: 1.35;
        color: #111111 !important;
    }

    .st-key-sidebar_entropy [data-testid="stSliderTickBar"] {
        opacity: 1 !important;
    }

    .exhum-section-title {
        color: #111111;
    }

    .exhum-section-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        border: 2px solid #000000;
        border-radius: 0;
        background: #ffffff;
        box-shadow: 2px 2px 0 0 #000000;
        font-size: 0.78rem;
        flex: 0 0 auto;
    }

    .exhum-sidebar-heading {
        margin: 10px 0 12px 0;
        color: inherit;
    }

    .st-key-sidebar_root .exhum-card {
        border-width: 1.5px;
        box-shadow: 2px 2px 0 0 #000000;
        padding: 10px 12px;
        margin-bottom: 8px;
    }

    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] [data-testid="stButton"] > button,
    section[data-testid="stSidebar"] .stFormSubmitButton > button,
    section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button,
    section[data-testid="stSidebar"] div[class*="st-key-new_session_button"] button {
        --exhum-sidebar-button-bg: #1f2937;
        --exhum-sidebar-button-fg: #f8fafc;
        --exhum-sidebar-button-hover-bg: #374151;
        --exhum-sidebar-button-hover-fg: #f8fafc;
        border: 3px solid #000000;
        border-radius: 0;
        background: var(--exhum-sidebar-button-bg);
        color: var(--exhum-sidebar-button-fg);
        box-shadow: 3px 3px 0 0 #000000;
        min-height: 42px;
        font-size: 0.9rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] [data-testid="stButton"] > button:hover,
    section[data-testid="stSidebar"] .stFormSubmitButton > button:hover,
    section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button:hover,
    section[data-testid="stSidebar"] div[class*="st-key-new_session_button"] button:hover {
        box-shadow: 4px 4px 0 0 #000000;
        background: var(--exhum-sidebar-button-hover-bg);
        color: var(--exhum-sidebar-button-hover-fg);
        border-color: #000000;
        transform: translate(-1px, -1px);
    }

    section[data-testid="stSidebar"] .stButton > button p,
    section[data-testid="stSidebar"] [data-testid="stButton"] > button p,
    section[data-testid="stSidebar"] .stFormSubmitButton > button p,
    section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button p,
    section[data-testid="stSidebar"] .stButton > button *,
    section[data-testid="stSidebar"] [data-testid="stButton"] > button *,
    section[data-testid="stSidebar"] .stFormSubmitButton > button *,
    section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button *,
    section[data-testid="stSidebar"] div[class*="st-key-new_session_button"] button * {
        color: inherit !important;
        font-weight: 800 !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
        min-width: 0;
    }

    section[data-testid="stSidebar"] .stButton > button > div,
    section[data-testid="stSidebar"] [data-testid="stButton"] > button > div,
    section[data-testid="stSidebar"] .stFormSubmitButton > button > div,
    section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button > div,
    section[data-testid="stSidebar"] div[class*="st-key-new_session_button"] button > div,
    section[data-testid="stSidebar"] .stButton > button p,
    section[data-testid="stSidebar"] [data-testid="stButton"] > button p,
    section[data-testid="stSidebar"] .stFormSubmitButton > button p,
    section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button p,
    section[data-testid="stSidebar"] div[class*="st-key-new_session_button"] button p {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        width: 100%;
        min-width: 0;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"],
    section[data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"],
    section[data-testid="stSidebar"] .stFormSubmitButton > button[kind="primary"],
    section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button[kind="primary"] {
        --exhum-sidebar-button-bg: #facc15;
        --exhum-sidebar-button-fg: #111111;
        --exhum-sidebar-button-hover-bg: #e0a800;
        --exhum-sidebar-button-hover-fg: #111111;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"] p,
    section[data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"] p,
    section[data-testid="stSidebar"] .stFormSubmitButton > button[kind="primary"] p,
    section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button[kind="primary"] p {
        color: inherit !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
    section[data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"]:hover,
    section[data-testid="stSidebar"] .stFormSubmitButton > button[kind="primary"]:hover,
    section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
        background: var(--exhum-sidebar-button-hover-bg) !important;
        color: var(--exhum-sidebar-button-hover-fg) !important;
    }

    section[data-testid="stSidebar"] div[class*="st-key-new_session_button"] button {
        --exhum-sidebar-button-bg: #2F353A;
        --exhum-sidebar-button-fg: #f8fafc;
        --exhum-sidebar-button-hover-bg: #b91c1c;
        --exhum-sidebar-button-hover-fg: #f8fafc;
    }

    section[data-testid="stSidebar"] div[class*="st-key-clear_button"] button {
        --exhum-sidebar-button-hover-bg: #b91c1c;
        --exhum-sidebar-button-hover-fg: #f8fafc;
    }

    @media (max-width: 900px) {
        .main .block-container,
        .stMainBlockContainer.block-container {
            padding-top: calc(var(--exhum-main-top-gap) * 0.62) !important;
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }

        .st-key-telemetry_panel {
            margin-top: 1.35rem !important;
        }

        .exhum-card {
            padding: 10px;
        }

        .exhum-topic-hero {
            padding: 12px;
            box-shadow: 3px 3px 0 0 #000000;
        }

        .exhum-topic-title {
            font-size: 1rem;
        }

        .exhum-bubble {
            padding: 10px 12px;
            font-size: 0.9rem;
            box-shadow: 3px 3px 0 0 #000000;
        }

        .exhum-meta {
            margin-left: 0;
            display: block;
            margin-top: 4px;
        }

        .exhum-avatar {
            width: 44px;
            height: 44px;
        }

        .exhum-legend-avatar {
            width: 44px;
            height: 44px;
        }

        .exhum-legend-card {
            padding: 6px;
        }

        .stButton > button {
            min-height: 42px;
            font-size: 0.82rem;
        }
    }

    </style>
    """,
        unsafe_allow_html=True,
    )
