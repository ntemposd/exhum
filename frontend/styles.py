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

    .stApp {
        background: #f3f4f6;
        color: #111111;
    }

    .stApp [data-testid="stAppViewContainer"] .main .block-container {
            padding-bottom: 8px;
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

    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        transform: scale(1.18) !important;
        transform-origin: center !important;
    }

    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="collapsedControl"] * {
        font-weight: 900 !important;
    }

    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="collapsedControl"] span,
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="collapsedControl"] svg {
        font-weight: 900 !important;
        stroke-width: 3 !important;
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
        padding: 16px 58px 16px 18px;
        background: #fff7ed;
        box-shadow: 5px 5px 0 0 #000000;
        margin-bottom: 12px;
        position: relative;
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
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="column"] {
        width: 100% !important;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] {
        width: 100%;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] > button,
    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button {
        min-height: 40px;
        width: 100%;
        max-width: 100%;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between;
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
        width: 54px;
        height: 54px;
        border: 2px solid #000000;
        border-radius: 0;
        object-fit: cover;
        box-shadow: 2px 2px 0 0 #000000;
        margin-bottom: 8px;
        background: #ffffff;
    }

    .exhum-bubble {
        border: 2px solid #000000;
        border-radius: 0;
        padding: 14px 18px;
        margin: 10px 0;
        line-height: 1.6;
        font-size: 0.95rem;
        box-shadow: 4px 4px 0 0 #000000;
        background: #ffffff;
    }

    .exhum-bubble-header-main {
        display: flex;
        flex: 1;
        min-width: 0;
        flex-direction: column;
        gap: 1px;
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
        font-weight: 700;
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
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
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
        width: 32px;
        height: 32px;
        border-radius: 0;
        border: 2px solid #000000;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 13px;
        flex-shrink: 0;
        box-shadow: 2px 2px 0 0 #000000;
    }

    .exhum-avatar-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 0;
    }

    .exhum-name {
        font-weight: 700;
        font-size: 0.88rem;
        letter-spacing: 0.3px;
    }

    .exhum-meta {
        font-size: 0.75rem;
        opacity: 0.8;
        margin-left: 0;
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
        box-shadow: 3px 3px 0 0 #000000;
    }

    .exhum-speaker-link {
        display: block;
        text-decoration: none;
        color: inherit !important;
    }

    .exhum-speaker-count {
        margin-left: auto;
        font-size: 0.8rem;
        opacity: 0.8;
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
        margin: 0 0 14px 0;
        padding: 0 0 12px 0;
        border-bottom: 2px solid #111111;
    }

    .exhum-telemetry-kicker {
        display: block;
        margin: 0 0 4px 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.66rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6b7280 !important;
        line-height: 1;
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
    }

    .exhum-telemetry-section-heading {
        display: flex;
        flex-direction: column;
        gap: 2px;
        margin: 14px 0 8px 0;
    }

    .exhum-telemetry-section-heading-compact {
        margin: 0;
    }

    .exhum-telemetry-section-kicker {
        display: block;
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.63rem;
        font-weight: 800;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        line-height: 1;
        color: #6b7280 !important;
    }

    .exhum-telemetry-section-title {
        display: block;
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        line-height: 1.05;
        color: #111111 !important;
    }

    .exhum-telemetry-status-dot {
        display: inline-block;
        width: 0.72rem;
        height: 0.72rem;
        margin-right: 0.45rem;
        border: 2px solid #111111;
        border-radius: 999px;
        box-shadow: 1px 1px 0 #000000;
        vertical-align: middle;
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
        margin: 0 0 10px 0;
        border: 3px solid #000000;
        border-radius: 0;
        background: #ffffff;
        box-shadow: 6px 6px 0 #000000;
        padding: 12px 12px 10px 12px;
    }

    .st-key-exhum_telemetry_system_status_card details {
        border: none;
        border-radius: 0;
        background: transparent;
        box-shadow: none;
        padding: 0;
        border-top: 2px solid #111111;
        margin-top: 6px;
        padding-top: 6px;
    }

    .st-key-exhum_telemetry_system_status_card summary {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding-top: 8px;
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
        margin-top: 10px;
    }

    .st-key-exhum_telemetry_neural_block [data-testid="stVerticalBlockBorderWrapper"] {
        border: 3px solid #000000 !important;
        border-radius: 0 !important;
        background: #ffffff !important;
        box-shadow: 6px 6px 0 #000000 !important;
    }

    .st-key-exhum_telemetry_context_block,
    .st-key-exhum_telemetry_cost_block,
    .st-key-exhum_telemetry_entropy_block,
    .st-key-exhum_telemetry_airtime_block {
        margin-bottom: 10px;
    }

    .st-key-exhum_telemetry_cost_block {
        margin-bottom: 10px;
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
        gap: 0.45rem;
        width: 100%;
        border: 3px solid #000000;
        background: #fff7ed;
        box-shadow: 6px 6px 0 #000000;
        padding: 0.8rem 0.85rem 0.75rem 0.85rem;
    }

    .exhum-telemetry-cost-topline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #111111;
    }

    .exhum-telemetry-cost-kicker {
        display: block;
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.64rem;
        font-weight: 800;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        line-height: 1;
        color: #7c2d12 !important;
    }

    .exhum-telemetry-cost-unit {
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

    .exhum-telemetry-cost-value {
        display: block;
        width: 100%;
        margin: 0;
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

    .st-key-exhum_telemetry_context_block > [data-testid="stVerticalBlock"] {
        gap: 0.45rem;
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

    .st-key-exhum_telemetry_system_status_header {
        margin-bottom: 2px;
    }

    .st-key-exhum_telemetry_system_status_header [data-testid="column"] {
        display: flex;
        align-items: center;
        min-height: 28px;
    }

    .st-key-exhum_telemetry_system_status_header [data-testid="column"]:first-child {
        justify-content: flex-start;
    }

    .st-key-exhum_telemetry_system_status_header [data-testid="column"]:last-child {
        justify-content: flex-end;
    }

    .st-key-exhum_telemetry_system_status_header [data-testid="stHorizontalBlock"] {
        align-items: center;
        gap: 0.4rem;
    }

    .st-key-exhum_telemetry_system_status_header [data-testid="stMarkdownContainer"] > h5 {
        display: flex;
        align-items: center;
        margin: 0;
        font-size: 1rem;
        line-height: 1;
        min-height: 24px;
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
    }

    .st-key-exhum_telemetry_system_status_card [data-testid="stTable"] > div,
    .st-key-exhum_telemetry_neural_block [data-testid="stTable"] > div,
    .st-key-exhum_telemetry_context_block [data-testid="stTable"] > div,
    .st-key-exhum_telemetry_airtime_block [data-testid="stTable"] > div {
        width: 100% !important;
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
        width: 100%;
        min-width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
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
        white-space: nowrap;
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
        overflow: hidden !important;
        text-overflow: ellipsis !important;
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

    @media (max-width: 768px) {
        [data-testid="stMain"] h2 {
            margin: 4px 0 8px 0;
        }

        .st-key-exhum_telemetry_system_status_card {
            box-shadow: 4px 4px 0 #000000;
            padding: 10px 10px 8px 10px;
        }

        .st-key-exhum_telemetry_neural_block [data-testid="stVerticalBlockBorderWrapper"] {
            box-shadow: 4px 4px 0 #000000 !important;
        }

        .st-key-exhum_telemetry_system_status_header [data-testid="column"] {
            min-height: 24px;
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
        background: #eef6ff;
        box-shadow: 6px 6px 0 #000000;
        padding: 0.8rem 0.85rem 0.75rem 0.85rem;
    }

    .exhum-telemetry-entropy-topline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
    }

    .exhum-telemetry-entropy-kicker {
        display: block;
        margin: 0;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.64rem;
        font-weight: 800;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        line-height: 1;
        color: #1d4ed8 !important;
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

    .exhum-telemetry-entropy-values {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.65rem;
        padding-bottom: 0.45rem;
        border-bottom: 2px solid #111111;
    }

    .exhum-telemetry-entropy-value-block {
        display: flex;
        flex-direction: column;
        gap: 0.18rem;
        min-width: 0;
    }

    .exhum-telemetry-entropy-value-label {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.63rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #4b5563 !important;
    }

    .exhum-telemetry-entropy-value {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1.28rem;
        font-weight: 800;
        line-height: 1.02;
        color: #111111 !important;
    }

    .exhum-telemetry-entropy-progress {
        display: flex;
        flex-direction: column;
        gap: 0.38rem;
    }

    .exhum-telemetry-entropy-progress-labels {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.67rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #111111 !important;
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

    .exhum-telemetry-entropy-target-marker,
    .exhum-telemetry-entropy-current-marker {
        position: absolute;
        top: -2px;
        bottom: -2px;
        width: 0;
        border-left: 2px solid #000000;
        transform: translateX(-1px);
        z-index: 2;
    }

    .exhum-telemetry-entropy-target-marker {
        border-left-color: #dc2626;
    }

    .exhum-telemetry-entropy-current-marker {
        border-left-color: #111111;
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
        color: #555555;
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
        .main .block-container {
            padding-top: 0.8rem;
            padding-left: 0.6rem;
            padding-right: 0.6rem;
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
            width: 28px;
            height: 28px;
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
