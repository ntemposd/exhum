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

    section[data-testid="stSidebar"] * {
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

    [data-testid="stSidebar"] .exhum-sidebar-heading,
    [data-testid="stMain"] h2,
    .exhum-section-title {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 6px 0 10px 0;
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

    .exhum-topic-edit-link:hover {
        color: #111111;
        background: #fff7ed;
        border-color: #000000;
    }

    div[class*="st-key-topic_edit_toggle"] button {
        width: 100%;
        min-height: 36px !important;
        padding: 0 !important;
        border: 2px solid #000000 !important;
        border-radius: 0 !important;
        background: #fff7ed !important;
        color: #111111 !important;
        box-shadow: 2px 2px 0 0 #000000 !important;
    }

    div[class*="st-key-topic_edit_toggle"] button:hover {
        background: #facc15 !important;
        color: #111111 !important;
        box-shadow: 3px 3px 0 0 #000000 !important;
        transform: translate(-1px, -1px);
    }

    .exhum-topic-title {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 700;
        line-height: 1.35;
    }

    .exhum-badge {
        display: inline-block;
        border: 2px solid #000000;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        background: #ffffff;
        box-shadow: 2px 2px 0 0 #000000;
    }

    .exhum-badge-draft {
        background: #fff4d6;
    }

    .exhum-badge-live {
        background: #dcfce7;
    }

    .exhum-selected-chip-group {
        width: 100%;
        margin-top: 6px;
    }

    .exhum-drafted-chip-wrap {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
        margin-top: 8px;
        margin-bottom: 14px;
    }

    .exhum-drafted-chip {
        display: flex;
        align-items: stretch;
        width: 100%;
        min-height: 50px;
        text-decoration: none !important;
        border: 3px solid #000000;
        border-radius: 0;
        background: #ff6b00;
        box-shadow: 4px 4px 0 0 #000000;
        color: #111111 !important;
        transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
    }

    .exhum-drafted-chip:hover {
        background: #ff8a36;
        transform: translate(-1px, -1px);
        box-shadow: 5px 5px 0 0 #000000;
    }

    .exhum-drafted-chip .drafted-chip-label {
        display: flex;
        align-items: center;
        flex: 1;
        min-width: 0;
        padding: 8px 10px 7px 12px;
        line-height: 1.15;
        font-size: 0.78rem;
        font-weight: 800;
        color: #111111;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        overflow: hidden;
        white-space: normal;
        text-overflow: ellipsis;
    }

    .exhum-drafted-chip .drafted-chip-x {
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 40px;
        padding: 0 10px;
        border-left: 3px solid #000000;
        background: #ffffff;
        line-height: 1;
        font-size: 0.95rem;
        font-weight: 900;
        color: #111111;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips {
        margin-top: 8px;
        margin-bottom: 14px;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stHorizontalBlock"] {
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
        border: 2px solid #000000 !important;
        border-radius: 0 !important;
        background: #ffffff !important;
        box-shadow: 2px 2px 0 0 #000000 !important;
        color: #111111 !important;
        font-size: 0.76rem;
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
        background: #fff7ed !important;
        border-color: #000000 !important;
        color: #111111 !important;
        transform: translate(-1px, -1px);
        box-shadow: 3px 3px 0 0 #000000 !important;
    }

    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] > button:focus,
    section[data-testid="stSidebar"] .st-key-drafted_council_chips [data-testid="stButton"] > button:focus-visible,
    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button:focus,
    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button:focus-visible {
        outline: none;
        border-color: #000000 !important;
        box-shadow: 3px 3px 0 0 #000000 !important;
    }

    section[data-testid="stSidebar"] div[class*="st-key-remove_drafted_"] button p {
        color: #111111 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.76rem !important;
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
        width: 78%;
        max-width: 180px;
        height: auto;
        margin: 0 auto 10px auto;
    }

    .exhum-brand-copy {
        text-align: center;
        margin: 0 auto 14px auto;
        max-width: 230px;
    }

    .exhum-brand-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: 0.18em;
        line-height: 1;
        color: #111111;
        margin-bottom: 6px;
    }

    .exhum-brand-subtitle {
        font-size: 0.72rem;
        line-height: 1.35;
        color: #444444;
        letter-spacing: 0.02em;
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

    .exhum-telemetry-desktop {
        display: block;
    }

    .exhum-telemetry-mobile {
        display: none;
        margin-top: 0;
    }

    .st-key-exhum_telemetry_desktop_system_status_card {
        display: block;
        margin: 0 0 16px 0;
        border: 3px solid #000000;
        border-radius: 0;
        background: #ffffff;
        box-shadow: 6px 6px 0 #000000;
        padding: 12px 12px 11px 12px;
    }

    .st-key-exhum_telemetry_mobile_system_status_card {
        display: none;
        margin: 0 0 16px 0;
        border: 3px solid #000000;
        border-radius: 0;
        background: #ffffff;
        box-shadow: 6px 6px 0 #000000;
        padding: 12px 12px 11px 12px;
    }

    .st-key-exhum_telemetry_desktop_services_toggle_row,
    .st-key-exhum_telemetry_mobile_services_toggle_row {
        margin-top: 12px;
        margin-bottom: 8px;
        padding-top: 10px;
        border-top: 2px solid #111111;
    }

    .st-key-exhum_telemetry_desktop_services_toggle_row [data-testid="stHorizontalBlock"],
    .st-key-exhum_telemetry_mobile_services_toggle_row [data-testid="stHorizontalBlock"] {
        align-items: center;
        gap: 0.55rem;
    }

    .st-key-exhum_telemetry_desktop_services_toggle_row [data-testid="column"],
    .st-key-exhum_telemetry_mobile_services_toggle_row [data-testid="column"] {
        display: flex;
        align-items: center;
    }

    .st-key-exhum_telemetry_desktop_services_toggle_row [data-testid="column"]:last-child,
    .st-key-exhum_telemetry_mobile_services_toggle_row [data-testid="column"]:last-child {
        justify-content: flex-end;
    }

    .exhum-services-toggle-label {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #111111;
        line-height: 1;
        padding-top: 0;
        white-space: nowrap;
    }

    .st-key-exhum_telemetry_desktop_services_toggle_row [data-testid="stToggle"],
    .st-key-exhum_telemetry_mobile_services_toggle_row [data-testid="stToggle"] {
        margin: 0;
        width: auto;
        min-width: 0;
    }

    .st-key-exhum_telemetry_desktop_services_toggle_row [data-testid="stToggle"] label,
    .st-key-exhum_telemetry_mobile_services_toggle_row [data-testid="stToggle"] label {
        justify-content: flex-end;
        gap: 0;
        width: auto;
        margin: 0;
        min-height: 20px;
    }

    .st-key-exhum_telemetry_desktop_services_toggle_row [data-testid="stToggle"] p,
    .st-key-exhum_telemetry_mobile_services_toggle_row [data-testid="stToggle"] p {
        display: none !important;
    }

    .st-key-exhum_telemetry_desktop_services_toggle_row [data-baseweb="switch"],
    .st-key-exhum_telemetry_mobile_services_toggle_row [data-baseweb="switch"] {
        transform: scale(0.95);
        transform-origin: right center;
    }

    .st-key-exhum_telemetry_desktop_services_toggle_row [data-baseweb="switch"] > div,
    .st-key-exhum_telemetry_mobile_services_toggle_row [data-baseweb="switch"] > div {
        min-width: 34px !important;
        background: #1f2937 !important;
        border: 2px solid #000000 !important;
    }

    .st-key-exhum_telemetry_desktop_system_status_card details,
    .st-key-exhum_telemetry_mobile_system_status_card details {
        border: none;
        border-radius: 0;
        background: transparent;
        box-shadow: none;
        padding: 0;
    }

    .st-key-exhum_telemetry_desktop_system_status_card summary,
    .st-key-exhum_telemetry_mobile_system_status_card summary {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding-top: 8px;
        color: #111111 !important;
        background: #ffffff !important;
    }

    .st-key-exhum_telemetry_desktop_system_status_card summary *,
    .st-key-exhum_telemetry_mobile_system_status_card summary * {
        color: #111111 !important;
        fill: #111111 !important;
    }

    .st-key-exhum_telemetry_desktop_system_status_card details[open] summary,
    .st-key-exhum_telemetry_mobile_system_status_card details[open] summary,
    .st-key-exhum_telemetry_desktop_system_status_card details[open] summary *,
    .st-key-exhum_telemetry_mobile_system_status_card details[open] summary * {
        background: #ffffff !important;
        color: #111111 !important;
        fill: #111111 !important;
    }

    .st-key-exhum_telemetry_desktop_system_status_card [data-testid="stExpander"] {
        margin-top: 14px;
    }

    .st-key-exhum_telemetry_mobile_system_status_card [data-testid="stExpander"] {
        margin-top: 14px;
    }

    .exhum-telemetry-shell {
        font-family: 'Courier New', 'Roboto Mono', monospace;
        color: #000000;
        margin-top: 0;
        padding-top: 0;
    }

    .exhum-telemetry-header {
        position: sticky;
        top: 8px;
        z-index: 2;
        border: 3px solid #000000;
        border-radius: 0;
        box-shadow: 6px 6px 0 #000000;
        background: #ffffff;
        padding: 8px 10px;
        margin-top: 0;
        margin-bottom: 16px;
        font-weight: 800;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .exhum-system-status-summary {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
    }

    .exhum-system-status-left {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        min-width: 0;
    }

    .exhum-system-status-label {
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        line-height: 1.1;
    }

    .exhum-system-status-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 4px 8px 3px 8px;
        border: 2px solid #000000;
        background: #f3f4f6;
        font-size: 0.66rem;
        font-weight: 800;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        white-space: nowrap;
        line-height: 1;
        box-shadow: 2px 2px 0 #000000;
    }

    .exhum-system-status-pill-optimal,
    .exhum-system-status-pill-online {
        background: #dcfce7;
        color: #166534;
    }

    .exhum-system-status-pill-standby {
        background: #fef3c7;
        color: #92400e;
    }

    .exhum-system-status-pill-offline,
    .exhum-system-status-pill-degraded {
        background: #fee2e2;
        color: #991b1b;
    }

    .exhum-system-status-block {
        padding-top: 10px;
        margin-bottom: 0;
        box-shadow: 6px 0 0 #000000;
    }

    .exhum-system-status-header {
        position: static;
        top: auto;
        z-index: auto;
        border: none;
        box-shadow: none;
        background: transparent;
        padding: 0;
        margin: 0;
    }

    .exhum-system-status-shell {
        margin: 0;
        padding: 0;
    }

    .exhum-telemetry-dot {
        width: 10px;
        height: 10px;
        border: 2px solid #000000;
        border-radius: 50%;
        background: #23c552;
        animation: exhum-dot-blink 1.1s infinite;
    }

    @keyframes exhum-dot-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.25; }
    }

    .exhum-telemetry-block {
        border: 3px solid #000000;
        border-radius: 0;
        box-shadow: 6px 6px 0 #000000;
        background: #ffffff;
        margin-bottom: 14px;
        padding: 12px 12px 11px 12px;
    }

    .exhum-telemetry-kicker {
        display: block;
        font-size: 0.66rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .exhum-telemetry-value {
        font-size: 1.02rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .exhum-context-label {
        font-size: 0.72rem;
        line-height: 1.45;
        letter-spacing: 0.02em;
    }

    .exhum-neural-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        border: 2px solid #000000;
        background: #fcfcfc;
        box-shadow: 3px 3px 0 #000000;
        padding: 8px 10px;
        margin-top: 8px;
    }

    .exhum-neural-label {
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .exhum-neural-value {
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        text-align: right;
        white-space: nowrap;
    }

    .exhum-service-row {
        border: 2px solid #000000;
        background: #fbfdff;
        box-shadow: 3px 3px 0 #000000;
        padding: 10px 10px 8px 10px;
        margin-top: 8px;
    }

    .exhum-service-main {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 4px;
    }

    .exhum-service-name {
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        line-height: 1.25;
    }

    .exhum-service-pill {
        border: 2px solid #000000;
        padding: 1px 6px 0 6px;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        white-space: nowrap;
    }

    .exhum-service-online {
        background: #dcfce7;
        color: #166534;
    }

    .exhum-service-offline {
        background: #fee2e2;
        color: #991b1b;
    }

    .exhum-service-latency {
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #111111;
    }

    .exhum-service-detail {
        margin-top: 4px;
        font-size: 0.66rem;
        line-height: 1.35;
        color: #4b5563;
    }

    .exhum-telemetry-emphasis {
        background: #FFD700;
        border: 2px solid #000000;
        padding: 0 4px;
        box-decoration-break: clone;
    }

    .exhum-ctx-track {
        height: 14px;
        border: 2px solid #000000;
        background: #ffffff;
        box-shadow: 3px 3px 0 #000000;
        margin-top: 8px;
        overflow: hidden;
    }

    .exhum-ctx-fill {
        height: 100%;
        background: #FFD700;
        border-right: 2px solid #000000;
    }

    .exhum-ctx-fill-green {
        background: #22c55e;
    }

    .exhum-ctx-fill-yellow {
        background: #facc15;
    }

    .exhum-ctx-fill-red {
        background: #ef4444;
    }

    .exhum-air-row {
        display: grid;
        grid-template-columns: 78px 1fr 46px;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }

    .exhum-air-label,
    .exhum-air-value {
        font-size: 0.66rem;
        font-weight: 700;
        line-height: 1.2;
        text-transform: uppercase;
    }

    .exhum-air-track {
        height: 12px;
        border: 2px solid #000000;
        background: #ffffff;
        overflow: hidden;
    }

    .exhum-air-fill {
        height: 100%;
        background: #000000;
    }

    @media (max-width: 768px) {
        .exhum-telemetry-desktop {
            display: none;
        }

        .exhum-telemetry-mobile {
            display: block;
        }

        .st-key-exhum_telemetry_desktop_system_status_card {
            display: none;
        }

        .st-key-exhum_telemetry_mobile_system_status_card {
            display: block;
        }

        [data-testid="stMain"] h2 {
            margin: 4px 0 8px 0;
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
        margin: 0;
        color: inherit;
    }

    section[data-testid="stSidebar"] .exhum-card {
        border-width: 1.5px;
        box-shadow: 2px 2px 0 0 #000000;
        padding: 10px 12px;
        margin-bottom: 8px;
    }

    section[data-testid="stSidebar"] div[class*="st-key-new_session_button"] button {
        min-height: 40px !important;
        padding: 6px 8px !important;
        border: 3px solid #000000 !important;
        border-radius: 0 !important;
        background: #1f2937 !important;
        color: #f8fafc !important;
        box-shadow: 3px 3px 0 0 #000000 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }

    section[data-testid="stSidebar"] div[class*="st-key-new_session_button"] button:hover {
        background: #374151 !important;
        border-color: #000000 !important;
        color: #f8fafc !important;
        box-shadow: 4px 4px 0 0 #000000 !important;
        transform: translate(-1px, -1px);
    }

    section[data-testid="stSidebar"] div[class*="st-key-new_session_button"] button p {
        color: #f8fafc !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        white-space: nowrap !important;
    }

    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stFormSubmitButton > button {
        border-width: 3px;
        box-shadow: 3px 3px 0 0 #000000;
        min-height: 42px;
        font-size: 0.9rem;
    }

    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stFormSubmitButton > button:hover {
        box-shadow: 4px 4px 0 0 #000000;
        background: #374151;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
    section[data-testid="stSidebar"] .stFormSubmitButton > button[kind="primary"]:hover {
        background: #e0a800 !important;
        color: #111111 !important;
        box-shadow: 5px 5px 0 0 #000000 !important;
    }

    .exhum-critical-warning {
        display: inline-block;
        background: #ff0000;
        color: #ffffff;
        border: 2px solid #000000;
        padding: 2px 6px;
        font-size: 0.7rem;
        font-weight: 800;
        animation: exhum-critical-blink 0.6s infinite;
        margin-left: 8px;
    }

    @keyframes exhum-critical-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
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
