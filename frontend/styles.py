"""
Roundtable Legends – global CSS injected on every page render.
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
        background: #ffffff;
        border-right: 2px solid #000000;
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

    .rtl-card {
        border: 2px solid #000000;
        border-radius: 4px;
        padding: 14px;
        background: #ffffff;
        margin-bottom: 10px;
        box-shadow: 4px 4px 0 0 #000000;
    }

    .rtl-topic-hero {
        border: 3px solid #000000;
        border-radius: 4px;
        padding: 16px 58px 16px 18px;
        background: #fff7ed;
        box-shadow: 5px 5px 0 0 #000000;
        margin-bottom: 12px;
        position: relative;
    }

    .rtl-topic-edit-link {
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
        border-radius: 4px;
        box-shadow: 2px 2px 0 0 #000000;
    }

    .rtl-topic-edit-link:hover {
        color: #111111;
        background: #fff7ed;
        border-color: #000000;
    }

    .rtl-topic-title {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 700;
        line-height: 1.35;
    }

    .rtl-badge {
        display: inline-block;
        border: 2px solid #000000;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        background: #ffffff;
        box-shadow: 2px 2px 0 0 #000000;
    }

    .rtl-badge-draft {
        background: #fff4d6;
    }

    .rtl-badge-live {
        background: #dcfce7;
    }

    .rtl-selected-chip-group {
        width: 100%;
        margin-top: 6px;
    }

    .rtl-drafted-chip-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
        margin-bottom: 14px;
    }

    .rtl-drafted-chip {
        display: inline-flex;
        align-items: stretch;
        text-decoration: none !important;
        border: 2px solid #000000;
        border-radius: 4px;
        background: #ffffff;
        box-shadow: 2px 2px 0 0 #000000;
        color: #111111 !important;
        max-width: 100%;
    }

    .rtl-drafted-chip:hover {
        background: #fff7ed;
    }

    .rtl-drafted-chip .drafted-chip-label {
        padding: 5px 9px;
        line-height: 1.1;
        font-size: 0.76rem;
        font-weight: 600;
        color: #111111;
        max-width: 170px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

    .rtl-drafted-chip .drafted-chip-x {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 25px;
        padding: 0 7px;
        border-left: 2px solid #000000;
        background: #ffe2e2;
        line-height: 1;
        font-size: 0.8rem;
        font-weight: 700;
        color: #111111;
    }

    .rtl-drafted-empty {
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

    .rtl-legend-card {
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

    .rtl-legend-card p, .rtl-legend-card div, .rtl-legend-card span {
        color: #111111 !important;
    }

    .rtl-legend-meta {
        font-size: 0.75rem;
        line-height: 1.25;
        color: #555555 !important;
        margin: 0;
    }

    .rtl-legend-state-badge {
        position: absolute;
        top: 8px;
        right: 8px;
        border: 2px solid #000000;
        border-radius: 999px;
        padding: 2px 8px;
        font-size: 0.7rem;
        font-weight: 700;
        background: #dcfce7;
        color: #166534;
        box-shadow: 2px 2px 0 0 #000000;
    }
    .rtl-legend-selected {
        border: 2px solid #000000;
        border-bottom: none;
        background: #ffffff;
        box-shadow: 5px 5px 0 0 #39ff14;
    }

    [data-testid="stDialog"] [data-testid="stVerticalBlock"]:has(.rtl-legend-card):has(button):not(:has([data-testid="stVerticalBlock"] .rtl-legend-card)) {
        gap: 0 !important;
    }

    [data-testid="stDialog"] [role="dialog"],
    [data-testid="stDialog"] > div {
        background: #ffffff !important;
    }

    [data-testid="stDialog"] [role="dialog"] {
        border: 3px solid #000000 !important;
        border-radius: 6px !important;
        box-shadow: 8px 8px 0 0 #000000 !important;
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
        color: #374151 !important;
        font-weight: 500;
    }

    [data-testid="stDialog"] button[aria-label="Close"] {
        border: 2px solid #000000 !important;
        border-radius: 4px !important;
        background: #ffffff !important;
        color: #111111 !important;
        box-shadow: 2px 2px 0 0 #000000 !important;
    }

    [data-testid="stDialog"] button[aria-label="Close"]:hover {
        background: #f3f4f6 !important;
        border-color: #000000 !important;
    }

    [data-testid="stDialog"] .rtl-legend-card:not(.rtl-legend-selected):hover {
        background: #ecfdf3;
        border-color: #16a34a;
        border-bottom: none;
    }

    [data-testid="stDialog"] .rtl-legend-selected:hover {
        background: #fff1f2;
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
        border-radius: 0 0 4px 4px !important;
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
        border-left: 2px solid #16a34a !important;
        border-right: 2px solid #16a34a !important;
        border-bottom: 2px solid #16a34a !important;
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

    .rtl-legend-avatar {
        width: 54px;
        height: 54px;
        border: 2px solid #000000;
        border-radius: 6px;
        object-fit: cover;
        box-shadow: 2px 2px 0 0 #000000;
        margin-bottom: 8px;
        background: #ffffff;
    }

    .rtl-bubble {
        border: 2px solid #000000;
        border-radius: 4px;
        padding: 14px 18px;
        margin: 10px 0;
        line-height: 1.6;
        font-size: 0.95rem;
        box-shadow: 4px 4px 0 0 #000000;
        background: #ffffff;
    }

    .rtl-bubble-0 { background: #fff1e8; border-left: 8px solid #ff6b00; }
    .rtl-bubble-1 { background: #eceff3; border-left: 8px solid #1f2937; }
    .rtl-bubble-2 { background: #e9fbfa; border-left: 8px solid #0ea5a4; }
    .rtl-bubble-3 { background: #e9f1ff; border-left: 8px solid #2563eb; }
    .rtl-bubble-4 { background: #ecfdf3; border-left: 8px solid #16a34a; }

    [data-testid="element-container"]:has(.rtl-read-more-anchor) + [data-testid="element-container"]:has(.stButton),
    [data-testid="element-container"]:has(.rtl-read-more-anchor) + [data-testid="element-container"]:has([data-testid="stButton"]) {
        display: flex !important;
        justify-content: flex-end !important;
        margin-top: -2px !important;
        margin-bottom: 10px !important;
    }

    [data-testid="element-container"]:has(.rtl-read-more-anchor) + [data-testid="element-container"]:has(.stButton) .stButton,
    [data-testid="element-container"]:has(.rtl-read-more-anchor) + [data-testid="element-container"]:has([data-testid="stButton"]) [data-testid="stButton"] {
        width: fit-content;
    }

    [data-testid="element-container"]:has(.rtl-read-more-anchor) + [data-testid="element-container"]:has(.stButton) .stButton > button,
    [data-testid="element-container"]:has(.rtl-read-more-anchor) + [data-testid="element-container"]:has([data-testid="stButton"]) [data-testid="stButton"] > button {
        min-height: 32px !important;
        padding: 4px 10px !important;
        font-size: 0.75rem !important;
        box-shadow: 2px 2px 0 0 #000000 !important;
    }

    [data-testid="element-container"]:has(.rtl-read-more-color-0) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #fff1e8 !important; }
    [data-testid="element-container"]:has(.rtl-read-more-color-1) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #eceff3 !important; }
    [data-testid="element-container"]:has(.rtl-read-more-color-2) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #e9fbfa !important; }
    [data-testid="element-container"]:has(.rtl-read-more-color-3) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #e9f1ff !important; }
    [data-testid="element-container"]:has(.rtl-read-more-color-4) + [data-testid="element-container"]:has(.stButton) .stButton > button { background: #ecfdf3 !important; }

    .rtl-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    }

    .rtl-brand-logo {
        display: block;
        width: 78%;
        max-width: 180px;
        height: auto;
        margin: 0 auto 10px auto;
    }

    .rtl-brand-copy {
        text-align: center;
        margin: 0 auto 14px auto;
        max-width: 230px;
    }

    .rtl-brand-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: 0.18em;
        line-height: 1;
        color: #111111;
        margin-bottom: 6px;
    }

    .rtl-brand-subtitle {
        font-size: 0.72rem;
        line-height: 1.35;
        color: #444444;
        letter-spacing: 0.02em;
    }

    .rtl-sticky-footer {
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

    .rtl-avatar {
        width: 32px;
        height: 32px;
        border-radius: 4px;
        border: 2px solid #000000;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 13px;
        flex-shrink: 0;
        box-shadow: 2px 2px 0 0 #000000;
    }

    .rtl-avatar-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 2px;
    }

    .rtl-name {
        font-weight: 700;
        font-size: 0.88rem;
        letter-spacing: 0.3px;
    }

    .rtl-meta {
        font-size: 0.75rem;
        opacity: 0.8;
        margin-left: auto;
    }

    .rtl-speaker {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
        padding: 8px 10px;
        border-radius: 4px;
        border: 2px solid #000000;
        margin-bottom: 6px;
        background: #ffffff;
        box-shadow: 3px 3px 0 0 #000000;
    }

    .rtl-speaker-count {
        margin-left: auto;
        font-size: 0.8rem;
        opacity: 0.8;
    }

    .rtl-speaker-archetype {
        font-size: 0.72rem;
        font-weight: 400;
        opacity: 0.6;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        margin-top: 1px;
    }

    .rtl-speaker-progress-wrap {
        flex-basis: 100%;
        width: 100%;
        margin-top: 8px;
    }

    .rtl-speaker-progress-track {
        width: 100%;
        height: 10px;
        border: 2px solid #000000;
        background: #ffffff;
        box-shadow: 2px 2px 0 0 #000000;
        overflow: hidden;
    }

    .rtl-speaker-progress-fill {
        height: 100%;
        background: #2563eb;
    }

    .rtl-speaker-progress-footer {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-top: 4px;
    }

    .rtl-speaker-progress-text {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .rtl-empty {
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
        border: 2px solid #000000;
        border-radius: 4px;
        background: #ffffff;
        color: #111111;
        box-shadow: 3px 3px 0 0 #000000;
        font-weight: 700;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .stButton > button p {
        white-space: nowrap;
    }

    .stButton > button:hover {
        transform: none;
        box-shadow: 3px 3px 0 0 #000000;
        border-color: #000000;
        background: #f7f7f7;
    }

    .stButton > button[kind="primary"] {
        background: #facc15;
        border: 3px solid #000000;
        box-shadow: 4px 4px 0 0 #000000;
        min-height: 48px;
        font-size: 0.95rem;
    }

    .rtl-telemetry-desktop {
        display: block;
    }

    .rtl-telemetry-mobile {
        display: none;
        margin-top: 14px;
    }

    .rtl-telemetry-shell {
        font-family: 'Courier New', 'Roboto Mono', monospace;
        color: #000000;
    }

    .rtl-telemetry-header {
        position: sticky;
        top: 8px;
        z-index: 2;
        border: 3px solid #000000;
        border-radius: 0;
        box-shadow: 6px 6px 0 #000000;
        background: #ffffff;
        padding: 8px 10px;
        margin-bottom: 16px;
        font-weight: 800;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .rtl-telemetry-dot {
        width: 10px;
        height: 10px;
        border: 2px solid #000000;
        border-radius: 50%;
        background: #23c552;
        animation: rtl-dot-blink 1.1s infinite;
    }

    @keyframes rtl-dot-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.25; }
    }

    .rtl-telemetry-block {
        border: 3px solid #000000;
        border-radius: 0;
        box-shadow: 6px 6px 0 #000000;
        background: #ffffff;
        margin-bottom: 20px;
        padding: 12px;
    }

    .rtl-telemetry-kicker {
        display: block;
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .rtl-telemetry-value {
        font-size: 1.18rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .rtl-telemetry-emphasis {
        background: #FFD700;
        border: 2px solid #000000;
        padding: 0 4px;
        box-decoration-break: clone;
    }

    .rtl-ctx-track {
        height: 18px;
        border: 2px solid #000000;
        background: #ffffff;
        box-shadow: 3px 3px 0 #000000;
        margin-top: 8px;
        overflow: hidden;
    }

    .rtl-ctx-fill {
        height: 100%;
        background: #FFD700;
        border-right: 2px solid #000000;
    }

    .rtl-air-row {
        display: grid;
        grid-template-columns: 88px 1fr 50px;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }

    .rtl-air-label,
    .rtl-air-value {
        font-size: 0.72rem;
        font-weight: 700;
        line-height: 1.2;
        text-transform: uppercase;
    }

    .rtl-air-track {
        height: 14px;
        border: 2px solid #000000;
        background: #ffffff;
        overflow: hidden;
    }

    .rtl-air-fill {
        height: 100%;
        background: #000000;
    }

    @media (max-width: 768px) {
        .rtl-telemetry-desktop {
            display: none;
        }

        .rtl-telemetry-mobile {
            display: block;
        }
    }

    .rtl-temperature-controller {
        border: none;
        background: transparent;
        padding: 0;
        margin: 2px 0 0 0;
        box-shadow: none;
        border-radius: 0;
    }

    .rtl-temperature-caption {
        display: block;
        font-size: 0.68rem;
        font-weight: 500;
        margin-top: 0;
        margin-bottom: 2px;
        color: #555555;
    }

    .rtl-sidebar-heading {
        font-size: 0.99rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin: 4px 0 8px 0;
        color: #111111;
    }

    section[data-testid="stSidebar"] .rtl-card {
        border-width: 1.5px;
        box-shadow: 2px 2px 0 0 #000000;
        padding: 10px 12px;
        margin-bottom: 8px;
    }

    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stFormSubmitButton > button {
        border-width: 1.5px;
        box-shadow: 1px 1px 0 0 #000000;
        min-height: 40px;
        font-size: 0.9rem;
    }

    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stFormSubmitButton > button:hover {
        box-shadow: 1px 1px 0 0 #000000;
        background: #f9fafb;
    }

    .rtl-critical-warning {
        display: inline-block;
        background: #ff0000;
        color: #ffffff;
        border: 2px solid #000000;
        padding: 2px 6px;
        font-size: 0.7rem;
        font-weight: 800;
        animation: rtl-critical-blink 0.6s infinite;
        margin-left: 8px;
    }

    @keyframes rtl-critical-blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    @media (max-width: 900px) {
        .main .block-container {
            padding-top: 0.8rem;
            padding-left: 0.6rem;
            padding-right: 0.6rem;
        }

        .rtl-card {
            padding: 10px;
        }

        .rtl-topic-hero {
            padding: 12px;
            box-shadow: 3px 3px 0 0 #000000;
        }

        .rtl-topic-title {
            font-size: 1rem;
        }

        .rtl-bubble {
            padding: 10px 12px;
            font-size: 0.9rem;
            box-shadow: 3px 3px 0 0 #000000;
        }

        .rtl-meta {
            margin-left: 0;
            display: block;
            margin-top: 4px;
        }

        .rtl-avatar {
            width: 28px;
            height: 28px;
        }

        .rtl-legend-avatar {
            width: 44px;
            height: 44px;
        }

        .rtl-legend-card {
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
