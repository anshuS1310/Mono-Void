import json
import html
import math
from concurrent.futures import ThreadPoolExecutor
import requests
import streamlit as st

# Page config (must be the first Streamlit command)
st.set_page_config(page_title="Mono Void", page_icon="✨", layout="centered")
# Custom CSS — Premium redesign: aurora background, compact sidebar, glassmorphism, Outfit+Inter, indigo/mint/amber palette
st.markdown(
    """
    <style>
        /* ═══════════════════════════════════════════════════════════
           FONTS
        ═══════════════════════════════════════════════════════════ */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

        *, *::before, *::after { box-sizing: border-box; }
        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* ═══════════════════════════════════════════════════════════
           HIDE STREAMLIT CHROME
        ═══════════════════════════════════════════════════════════ */
        /* Top header bar + toolbar */
        header[data-testid="stHeader"],
        [data-testid="stHeader"],
        .stHeader,
        #stHeader { display: none !important; visibility: hidden !important; height: 0 !important; }

        /* Deploy button, hamburger menu, status widget */
        #stAppDeployButton,
        [data-testid="stAppDeployButton"],
        .stDeployButton,
        [data-testid="stToolbar"],
        .stToolbar,
        #MainMenu,
        [data-testid="stMainMenu"],
        [data-testid="stStatusWidget"],
        .viewerBadge_container__r5tak,
        .viewerBadge_link__qRIco { display: none !important; }

        /* ═══════════════════════════════════════════════════════════
           AURORA DYNAMIC BACKGROUND
        ═══════════════════════════════════════════════════════════ */
        .stApp,
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(ellipse 72rem 52rem at -5% -12%,  rgba(108, 92, 231, 0.62), transparent 54%),
                radial-gradient(ellipse 58rem 44rem at 108%  6%,  rgba(0,  206, 201, 0.48), transparent 52%),
                radial-gradient(ellipse 50rem 38rem at  60% 114%, rgba(253, 203, 110, 0.46), transparent 54%),
                radial-gradient(ellipse 44rem 32rem at  12%  98%, rgba(132,  94, 247, 0.42), transparent 50%),
                radial-gradient(ellipse 38rem 28rem at  88%  55%, rgba(0, 184, 212, 0.22), transparent 52%),
                linear-gradient(128deg, #e8eaff 0%, #e2d8ff 35%, #d6f5ef 70%, #fdefd6 100%) !important;
            background-size: 132% 132%, 128% 128%, 138% 138%, 120% 120%, 110% 110%, 100% 100% !important;
            animation: auroraShift 26s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite alternate !important;
            overflow-x: hidden;
        }
        @keyframes auroraShift {
            0%   { background-position: 0%  0%,  100%  0%,  50% 100%, 10% 90%, 80% 50%, 0 0; }
            33%  { background-position: 15% 12%,  88%  20%, 62%  84%, 20% 78%, 65% 40%, 0 0; }
            66%  { background-position: 8%  22%,  76%  6%,  44%  68%, 5%  85%, 72% 55%, 0 0; }
            100% { background-position: 22% 8%,   64%  14%, 38%  80%, 15% 95%, 60% 45%, 0 0; }
        }
        /* Floating ambient orbs — stronger and more visible */
        .stApp::before {
            content: "";
            position: fixed; z-index: 0; pointer-events: none;
            width: 60vw; height: 60vw; min-width: 360px; min-height: 360px;
            top: -24vw; left: -20vw;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 38%, rgba(108,92,231,0.52) 0%, rgba(160,130,255,0.32) 40%, transparent 68%);
            filter: blur(28px);
            animation: orbDrift1 28s ease-in-out infinite alternate;
        }
        .stApp::after {
            content: "";
            position: fixed; z-index: 0; pointer-events: none;
            width: 54vw; height: 54vw; min-width: 300px; min-height: 300px;
            bottom: -20vw; right: -16vw;
            border-radius: 50%;
            background: radial-gradient(circle at 60% 60%, rgba(0,206,201,0.46) 0%, rgba(110,230,220,0.28) 45%, transparent 68%);
            filter: blur(24px);
            animation: orbDrift2 32s ease-in-out infinite alternate;
        }
        @keyframes orbDrift1 {
            from { transform: translate(0, 0) scale(1); }
            to   { transform: translate(8vw, 6vh) scale(1.18); }
        }
        @keyframes orbDrift2 {
            from { transform: translate(0, 0) scale(1); }
            to   { transform: translate(-6vw, -5vh) scale(1.14); }
        }

        /* ═══════════════════════════════════════════════════════════
           MAIN CONTENT CONTAINER
        ═══════════════════════════════════════════════════════════ */
        .main .block-container {
            max-width: 980px !important;
            padding: 2.4rem 2rem 3rem !important;
            position: relative; z-index: 1;
            animation: contentRise 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
        }
        @keyframes contentRise {
            from { opacity: 0; transform: translateY(20px) scale(0.985); }
            to   { opacity: 1; transform: none; }
        }

        /* ═══════════════════════════════════════════════════════════
           TYPOGRAPHY
        ═══════════════════════════════════════════════════════════ */
        h1 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
            font-size: clamp(2.4rem, 5.5vw, 4rem) !important;
            line-height: 1.02 !important;
            letter-spacing: -0.055em !important;
            color: #1a1530 !important;
            text-shadow: 0 8px 32px rgba(108, 92, 231, 0.12);
            margin-bottom: 0.6rem !important;
        }
        h2 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            color: #2d2447 !important;
            letter-spacing: -0.03em !important;
        }
        h3 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            color: #3a3055 !important;
            letter-spacing: -0.02em !important;
            font-size: 1.05rem !important;
        }
        .stMarkdown p, p {
            font-family: 'Inter', sans-serif;
            color: #4a4260 !important;
            font-size: 1rem;
            line-height: 1.68;
        }
        label, .stSelectbox label, .stTextInput label, .stTextArea label, .stRadio label {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.82rem !important;
            color: #3a3055 !important;
            letter-spacing: 0.01em;
        }

        /* ═══════════════════════════════════════════════════════════
           EYEBROW / BADGE LABELS
        ═══════════════════════════════════════════════════════════ */
        .eyebrow {
            display: inline-flex; align-items: center; gap: 0.4rem;
            font-family: 'Outfit', sans-serif;
            font-weight: 700; font-size: 0.72rem;
            letter-spacing: 0.14em; text-transform: uppercase;
            color: #6C5CE7 !important;
            padding: 0.32rem 0.82rem;
            background: rgba(108, 92, 231, 0.08);
            border: 1px solid rgba(108, 92, 231, 0.18);
            border-radius: 999px;
            box-shadow: 0 4px 16px rgba(108, 92, 231, 0.07);
            margin-bottom: 0.6rem;
        }

        /* ═══════════════════════════════════════════════════════════
           HERO COPY
        ═══════════════════════════════════════════════════════════ */
        .hero-copy {
            font-size: 1.05rem !important;
            line-height: 1.72 !important;
            color: #5e5680 !important;
            max-width: 660px;
            margin-bottom: 0.2rem !important;
        }

        /* ═══════════════════════════════════════════════════════════
           HR DIVIDERS — gradient fade
        ═══════════════════════════════════════════════════════════ */
        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, rgba(108,92,231,0.2) 30%, rgba(108,92,231,0.2) 70%, transparent) !important;
            margin: 1.2rem 0 !important;
        }

        /* ═══════════════════════════════════════════════════════════
           SIDEBAR — Compact no-scroll glass panel
        ═══════════════════════════════════════════════════════════ */
        div[data-testid="stSidebar"] {
            width: 340px !important;
            min-width: 340px !important;
            background: transparent !important;
            border: none !important;
            padding: 16px 0 16px 16px !important;
        }
        /* The inner scrollable div — make it a fixed-height no-scroll glass card */
        div[data-testid="stSidebar"] > div:first-child {
            height: calc(100vh - 32px) !important;
            overflow-y: hidden !important;
            overflow-x: hidden !important;
            background: linear-gradient(160deg,
                rgba(255,255,255,0.95) 0%,
                rgba(250,248,255,0.88) 55%,
                rgba(243,250,252,0.82) 100%) !important;
            border: 1px solid rgba(255,255,255,0.92) !important;
            border-radius: 28px !important;
            box-shadow:
                0 28px 72px rgba(67, 48, 112, 0.13),
                0  2px  8px rgba(108, 92, 231, 0.05),
                inset 0 1px 0 rgba(255,255,255,0.96) !important;
            backdrop-filter: blur(28px) saturate(1.15);
            -webkit-backdrop-filter: blur(28px) saturate(1.15);
            position: relative;
        }
        /* Subtle orb accent inside sidebar card */
        div[data-testid="stSidebar"] > div:first-child::before {
            content: "";
            position: absolute; pointer-events: none; z-index: 0;
            width: 200px; height: 200px; border-radius: 50%;
            top: -80px; right: -60px;
            background: radial-gradient(circle, rgba(108,92,231,0.09), transparent 70%);
            filter: blur(18px);
        }
        div[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            padding: 1.15rem 1rem 1rem !important;
            position: relative; z-index: 1;
        }
        /* Sidebar section headers */
        div[data-testid="stSidebar"] .stMarkdown h3 {
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            color: #6C5CE7 !important;
            margin: 0.8rem 0 0.4rem !important;
            padding-bottom: 0.3rem;
            border-bottom: 1px solid rgba(108, 92, 231, 0.12);
        }
        div[data-testid="stSidebar"] h3 {
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            color: #6C5CE7 !important;
            margin: 0.8rem 0 0.4rem !important;
        }
        /* Sidebar spacing */
        div[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0.22rem !important;
        }
        div[data-testid="stSidebar"] hr { margin: 0.55rem 0 !important; }
        /* Sidebar caption text */
        div[data-testid="stSidebar"] small,
        div[data-testid="stSidebar"] .stCaption,
        div[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            font-size: 0.72rem !important;
            color: #8a7fb5 !important;
            line-height: 1.45 !important;
        }
        /* Sidebar Workspace title */
        div[data-testid="stSidebar"] .stMarkdown h3:first-of-type {
            font-size: 0.9rem !important;
        }

        /* ═══════════════════════════════════════════════════════════
           SIDEBAR BUTTONS
        ═══════════════════════════════════════════════════════════ */
        /* Reset button in sidebar */
        div[data-testid="stSidebar"] .stButton > button {
            background: rgba(108, 92, 231, 0.07) !important;
            color: #6C5CE7 !important;
            border: 1px solid rgba(108, 92, 231, 0.18) !important;
            border-radius: 12px !important;
            padding: 0.35rem 0.85rem !important;
            font-size: 0.79rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            min-height: 2.1rem !important;
            box-shadow: none !important;
            margin-top: 0.1rem;
            transition: background 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease !important;
        }
        div[data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(108, 92, 231, 0.14) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(108, 92, 231, 0.14) !important;
            color: #5b4dd4 !important;
        }

        /* ═══════════════════════════════════════════════════════════
           INPUTS — Frosted glass style
        ═══════════════════════════════════════════════════════════ */
        div[data-baseweb="input"],
        div[data-baseweb="textarea"],
        div[data-baseweb="select"] {
            background: rgba(255, 255, 255, 0.82) !important;
            border: 1.5px solid rgba(108, 92, 231, 0.14) !important;
            border-radius: 14px !important;
            transition: all 0.22s cubic-bezier(0.22, 1, 0.36, 1) !important;
            box-shadow: 0 1px 4px rgba(108, 92, 231, 0.06) !important;
        }
        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="textarea"]:focus-within {
            background: rgba(255, 255, 255, 0.96) !important;
            border-color: rgba(108, 92, 231, 0.55) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 0 0 4px rgba(108, 92, 231, 0.09), 0 10px 28px rgba(80, 60, 140, 0.12) !important;
        }
        input, textarea {
            font-family: 'Inter', sans-serif !important;
            border-radius: 14px !important;
            border: none !important;
            padding: 0.55rem 0.9rem !important;
            background: transparent !important;
            color: #1a1530 !important;
            font-size: 0.92rem !important;
            transition: all 0.22s ease !important;
        }
        input::placeholder, textarea::placeholder {
            color: #a09abc !important;
            opacity: 1 !important;
        }
        /* Password field eye icon area */
        div[data-baseweb="input"] button {
            color: #8a7fb5 !important;
        }
        /* Select boxes */
        div[data-baseweb="select"] > div {
            background: transparent !important;
            border: none !important;
            color: #1a1530 !important;
            font-size: 0.88rem !important;
        }
        /* Radio buttons */
        div[data-testid="stRadio"] > div {
            gap: 0.3rem !important;
        }
        div[data-testid="stRadio"] label {
            font-size: 0.84rem !important;
            color: #3a3055 !important;
            cursor: pointer;
        }

        /* Sidebar inputs are even more compact */
        div[data-testid="stSidebar"] div[data-baseweb="input"],
        div[data-testid="stSidebar"] div[data-baseweb="textarea"],
        div[data-testid="stSidebar"] div[data-baseweb="select"] {
            border-radius: 10px !important;
        }
        div[data-testid="stSidebar"] input,
        div[data-testid="stSidebar"] textarea {
            font-size: 0.82rem !important;
            padding: 0.38rem 0.7rem !important;
        }
        div[data-testid="stSidebar"] div[data-baseweb="select"] > div {
            font-size: 0.82rem !important;
        }

        /* ═══════════════════════════════════════════════════════════
           MAIN CTA BUTTONS
        ═══════════════════════════════════════════════════════════ */
        .stButton > button {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.93rem !important;
            letter-spacing: 0.04em;
            text-transform: none;
            border: none !important;
            border-radius: 14px !important;
            min-height: 2.75rem;
            padding: 0.62rem 2rem !important;
            background: linear-gradient(135deg, #7E6BE0 0%, #6C5CE7 60%, #5648CC 100%) !important;
            color: #fff !important;
            box-shadow:
                0 6px 20px rgba(108, 92, 231, 0.28),
                inset 0 1px 0 rgba(255,255,255,0.20) !important;
            transition:
                background 0.18s ease,
                box-shadow 0.18s ease,
                transform 0.14s ease !important;
            cursor: pointer;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #8B78EC 0%, #7566E8 60%, #6256D4 100%) !important;
            box-shadow:
                0 10px 28px rgba(108, 92, 231, 0.36),
                inset 0 1px 0 rgba(255,255,255,0.22) !important;
            transform: translateY(-1px) !important;
            color: #fff !important;
        }
        .stButton > button:active {
            transform: translateY(0px) !important;
            box-shadow: 0 3px 10px rgba(108, 92, 231, 0.24) !important;
        }
        /* Transmit (primary form submit) button — extra emphasis */
        [data-testid="stFormSubmitButton"] > button,
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #7E6BE0 0%, #6C5CE7 55%, #5648CC 100%) !important;
            border-radius: 14px !important;
            font-size: 0.96rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em !important;
            padding: 0.7rem 2.2rem !important;
            min-height: 2.9rem;
            box-shadow:
                0 8px 24px rgba(108, 92, 231, 0.34),
                0 2px 6px rgba(108, 92, 231, 0.16),
                inset 0 1px 0 rgba(255,255,255,0.20) !important;
        }
        [data-testid="stFormSubmitButton"] > button:hover,
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #8B78EC 0%, #7566E8 55%, #6256D4 100%) !important;
            box-shadow:
                0 12px 32px rgba(108, 92, 231, 0.40),
                inset 0 1px 0 rgba(255,255,255,0.22) !important;
            transform: translateY(-1px) !important;
        }
        /* Secondary / Stop button */
        .stButton > button[kind="secondary"],
        .stButton > button:not([kind="primary"]):not([data-testid="stFormSubmitButton"]) {
            background: rgba(255,255,255,0.82) !important;
            color: #6C5CE7 !important;
            border: 1.5px solid rgba(108, 92, 231, 0.24) !important;
            box-shadow: 0 2px 10px rgba(108, 92, 231, 0.07) !important;
            font-weight: 600 !important;
        }
        .stButton > button[kind="secondary"]:hover,
        .stButton > button:not([kind="primary"]):not([data-testid="stFormSubmitButton"]):hover {
            background: rgba(108, 92, 231, 0.07) !important;
            border-color: rgba(108, 92, 231, 0.35) !important;
            box-shadow: 0 5px 16px rgba(108, 92, 231, 0.13) !important;
            transform: translateY(-1px) !important;
        }

        /* Sidebar toggle buttons — using Streamlit's native controls */

        /* ═══════════════════════════════════════════════════════════
           COMPOSER CARD
        ═══════════════════════════════════════════════════════════ */
        .composer {
            position: relative;
            overflow: hidden;
            background: linear-gradient(140deg,
                rgba(255,255,255,0.94) 0%,
                rgba(252,250,255,0.86) 100%) !important;
            border: 1px solid rgba(108, 92, 231, 0.12) !important;
            border-radius: 28px !important;
            padding: 1.8rem 1.75rem 1.3rem !important;
            box-shadow:
                0 12px 40px rgba(72, 54, 120, 0.10),
                0  2px  8px rgba(108, 92, 231, 0.05),
                inset 0 1px 0 rgba(255,255,255,0.95) !important;
            /* No transition — steady, calm card, no hover lift */
            margin: 1.5rem 0 1rem;
        }
        /* Decorative gradient orb inside composer */
        .composer::before {
            content: "";
            position: absolute; pointer-events: none;
            width: 18rem; height: 18rem; border-radius: 50%;
            right: -8rem; top: -10rem;
            background: radial-gradient(circle, rgba(108,92,231,0.09) 0%, rgba(0,206,201,0.05) 55%, transparent 72%);
            filter: blur(10px);
        }
        .composer::after {
            content: "";
            position: absolute; pointer-events: none;
            width: 10rem; height: 10rem; border-radius: 50%;
            left: -4rem; bottom: -5rem;
            background: radial-gradient(circle, rgba(253,203,110,0.10) 0%, transparent 70%);
            filter: blur(8px);
        }
        /* No :hover lift on composer — it stays flat and calm */
        .composer > * { position: relative; z-index: 1; }
        .composer-title {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.55rem !important;
            letter-spacing: -0.04em;
            color: #1a1530 !important;
            margin: 0 0 0.2rem !important;
        }
        .composer-help {
            font-size: 0.9rem !important;
            color: #7268a0 !important;
            margin: 0 0 1.2rem !important;
            line-height: 1.55;
            max-width: 560px;
        }
        .message-label {
            display: flex; align-items: center; gap: 0.5rem;
            color: #3a3055 !important;
            font-weight: 700; font-size: 0.84rem;
            margin: 0.8rem 0 0.3rem;
        }
        .message-label span {
            color: #a09abc !important;
            font-weight: 500; font-size: 0.76rem;
        }
        div[data-testid="stTextArea"] textarea {
            min-height: 155px !important;
            line-height: 1.62 !important;
            font-size: 0.94rem !important;
            resize: vertical !important;
        }
        /* Form border reset */
        .stForm { border: 0 !important; padding: 0 !important; background: transparent !important; }

        /* ═══════════════════════════════════════════════════════════
           COMPARE CARDS
        ═══════════════════════════════════════════════════════════ */
        .compare-card {
            background: linear-gradient(140deg,
                rgba(255,255,255,0.94) 0%,
                rgba(250,248,255,0.80) 100%) !important;
            border: 1px solid rgba(255,255,255,0.9) !important;
            border-radius: 24px !important;
            padding: 1.2rem 1.35rem !important;
            box-shadow:
                0 16px 42px rgba(72, 54, 120, 0.09),
                inset 0 1px 0 rgba(255,255,255,0.92) !important;
            animation: cardAppear 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.28s ease;
            height: 100%;
        }
        .compare-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 26px 52px rgba(72, 54, 120, 0.15) !important;
        }
        @keyframes cardAppear {
            from { opacity: 0; transform: translateY(14px) scale(0.97); }
            to   { opacity: 1; transform: none; }
        }
        .compare-label {
            font-family: 'Outfit', sans-serif;
            font-weight: 700; font-size: 0.7rem;
            text-transform: uppercase; letter-spacing: 0.14em;
            color: #6C5CE7 !important;
            margin-bottom: 0.5rem;
        }
        .compare-text {
            color: #2d2447 !important;
            font-size: 0.93rem;
            line-height: 1.58;
        }

        /* ═══════════════════════════════════════════════════════════
           TOKEN / BACKEND PILLS
        ═══════════════════════════════════════════════════════════ */
        .token-pill {
            display: inline-flex; align-items: center; gap: 0.28rem;
            margin-top: 0.65rem;
            background: rgba(108, 92, 231, 0.09) !important;
            color: #6C5CE7 !important;
            font-family: 'Outfit', sans-serif;
            font-size: 0.74rem; font-weight: 700;
            padding: 0.22rem 0.72rem; border-radius: 999px;
            border: 1px solid rgba(108, 92, 231, 0.14);
        }
        .backend-pill {
            display: inline-flex; align-items: center; gap: 0.28rem;
            margin: 0.35rem 0 0.9rem;
            background: rgba(0, 206, 201, 0.09) !important;
            color: #00897B !important;
            font-family: 'Outfit', sans-serif;
            font-size: 0.74rem; font-weight: 700;
            padding: 0.22rem 0.78rem; border-radius: 999px;
            border: 1px solid rgba(0, 206, 201, 0.18);
        }

        /* ═══════════════════════════════════════════════════════════
           METRIC CARDS
        ═══════════════════════════════════════════════════════════ */
        div[data-testid="stMetric"] {
            background: linear-gradient(140deg,
                rgba(255,255,255,0.94) 0%,
                rgba(250,248,255,0.82) 100%) !important;
            border: 1px solid rgba(255,255,255,0.9) !important;
            border-left: 3px solid #6C5CE7 !important;
            border-radius: 20px !important;
            padding: 1rem 1.2rem !important;
            box-shadow:
                0 14px 36px rgba(72, 54, 120, 0.09),
                inset 0 1px 0 rgba(255,255,255,0.92) !important;
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.28s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 22px 48px rgba(72, 54, 120, 0.14) !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.72rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            color: #8a7fb5 !important;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.55rem !important;
            color: #1a1530 !important;
            line-height: 1.15 !important;
        }

        /* ═══════════════════════════════════════════════════════════
           CODE BLOCK — Premium dark-glass style
        ═══════════════════════════════════════════════════════════ */
        div[data-testid="stCodeBlock"],
        div[data-testid="stCode"] {
            width: 100% !important;
            background: linear-gradient(135deg,
                rgba(26, 21, 48, 0.94) 0%,
                rgba(36, 28, 64, 0.88) 100%) !important;
            border: 1px solid rgba(108, 92, 231, 0.25) !important;
            border-radius: 22px !important;
            padding: 0.75rem !important;
            box-shadow:
                0 20px 50px rgba(26, 21, 48, 0.18),
                0  4px 14px rgba(108, 92, 231, 0.12),
                inset 0 1px 0 rgba(255,255,255,0.07) !important;
            min-height: 260px;
            max-width: 100% !important;
            position: relative;
            overflow: hidden;
        }
        /* Code block inner glow */
        div[data-testid="stCodeBlock"]::before,
        div[data-testid="stCode"]::before {
            content: "";
            position: absolute; pointer-events: none;
            width: 100%; height: 2px; top: 0; left: 0;
            background: linear-gradient(90deg, transparent, rgba(108,92,231,0.5) 40%, rgba(0,206,201,0.4) 70%, transparent);
            border-radius: 22px 22px 0 0;
        }
        div[data-testid="stCodeBlock"] pre,
        div[data-testid="stCode"] pre,
        div[data-testid="stCodeBlock"] code,
        div[data-testid="stCode"] code {
            font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace !important;
            font-size: 0.9rem !important;
            line-height: 1.78 !important;
            color: #e2dff5 !important;
            white-space: pre-wrap !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
            min-height: 200px;
            background: transparent !important;
        }
        /* Copy button */
        div[data-testid="stCodeBlock"] button,
        div[data-testid="stCode"] button {
            background: rgba(108, 92, 231, 0.2) !important;
            color: #c4b8ff !important;
            border-radius: 8px !important;
            border: 1px solid rgba(108, 92, 231, 0.3) !important;
        }
        div[data-testid="stCodeBlock"] button:hover,
        div[data-testid="stCode"] button:hover {
            background: rgba(108, 92, 231, 0.35) !important;
            color: #fff !important;
        }

        /* ═══════════════════════════════════════════════════════════
           ALERTS / INFO / WARNING
        ═══════════════════════════════════════════════════════════ */
        div[data-testid="stAlert"] {
            border-radius: 18px !important;
            border: none !important;
            padding: 0.9rem 1.1rem !important;
            animation: alertPop 0.42s cubic-bezier(0.34, 1.56, 0.64, 1) both;
            backdrop-filter: blur(10px);
        }
        @keyframes alertPop {
            from { opacity: 0; transform: scale(0.92) translateY(10px); }
            to   { opacity: 1; transform: scale(1) translateY(0); }
        }
        /* Info */
        div[data-testid="stAlert"][data-baseweb="notification"] {
            background: rgba(108, 92, 231, 0.07) !important;
            border-left: 3px solid #6C5CE7 !important;
        }
        /* Warning */
        div[data-testid="stAlert"].st-warning,
        [data-testid="stAlert"][data-type="warning"] {
            background: rgba(253, 203, 110, 0.12) !important;
            border-left: 3px solid #FDCB6E !important;
        }
        /* Error */
        div[data-testid="stAlert"].st-error,
        [data-testid="stAlert"][data-type="error"] {
            background: rgba(231, 76, 60, 0.08) !important;
            border-left: 3px solid #e74c3c !important;
        }
        /* Success */
        div[data-testid="stAlert"].st-success,
        [data-testid="stAlert"][data-type="success"] {
            background: rgba(0, 206, 201, 0.09) !important;
            border-left: 3px solid #00CEC9 !important;
        }

        /* ═══════════════════════════════════════════════════════════
           INPUT PREVIEW CARD
        ═══════════════════════════════════════════════════════════ */
        .input-preview {
            background: rgba(248, 246, 255, 0.9) !important;
            border: 1px solid rgba(108, 92, 231, 0.12) !important;
            border-radius: 18px !important;
            padding: 1rem 1.1rem !important;
            margin: 1.1rem 0;
        }
        .input-preview strong {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.7rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            color: #6C5CE7 !important;
            display: block;
            margin-bottom: 0.3rem;
        }
        .input-preview p {
            margin: 0 !important;
            color: #2d2447 !important;
            line-height: 1.6 !important;
            font-size: 0.9rem !important;
            white-space: pre-wrap;
        }

        /* ═══════════════════════════════════════════════════════════
           SCROLLBAR — thin, minimal
        ═══════════════════════════════════════════════════════════ */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(108,92,231,0.22); border-radius: 999px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(108,92,231,0.40); }

        /* ═══════════════════════════════════════════════════════════
           SPINNER
        ═══════════════════════════════════════════════════════════ */
        div[data-testid="stSpinner"] > div {
            border-color: rgba(108, 92, 231, 0.18) !important;
            border-top-color: #6C5CE7 !important;
        }

        /* ═══════════════════════════════════════════════════════════
           RESPONSIVE
        ═══════════════════════════════════════════════════════════ */
        @media (max-width: 900px) {
            .main .block-container { padding: 1.8rem 1rem 2rem !important; }
            div[data-testid="stSidebar"] {
                width: 100% !important; min-width: 0 !important; padding: 0 !important;
            }
            div[data-testid="stSidebar"] > div:first-child {
                height: auto !important;
                max-height: 80vh !important;
                overflow-y: auto !important;
                border-radius: 0 0 24px 24px !important;
            }
            h1 { font-size: clamp(2rem, 8vw, 3rem) !important; }
        }

        /* ═══════════════════════════════════════════════════════════
           REDUCED MOTION
        ═══════════════════════════════════════════════════════════ */
        @media (prefers-reduced-motion: reduce) {
            .stApp, [data-testid="stAppViewContainer"],
            .stApp::before, .stApp::after { animation: none !important; }
            .composer, .compare-card, .stButton > button { transition: none !important; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

OLLAMA_BASE = "http://localhost:11434"
PAID_API_TIMEOUT_SECONDS = 120
HOSTED_MODEL_TIMEOUT_SECONDS = 180
LOCAL_OLLAMA_TIMEOUT_SECONDS = 360


class LocalModelTimeout(RuntimeError):
    """Raised when any Ollama model has not produced output in time."""

    def __init__(self, model: str):
        super().__init__(
            f"Local Ollama model `{model}` did not produce output within "
            f"{LOCAL_OLLAMA_TIMEOUT_SECONDS // 60} minutes."
        )


class LocalModelRequestError(RuntimeError):
    """Raised when Ollama cannot complete a request for a local model."""

def refinement_system_prompt(minimum_tokens: int) -> str:
    """Keep enough detail while refining, without imposing any output maximum."""
    return (
        "Rewrite the user's prompt to a better prompt version to get more meaningful and useful output from a large language model. "
        "Refined prompt should use fewer tokens while preserving its intent ,aim , goal and essential details of the original user's prompt."
        "Remove filler and redundancy. Do not add information. "
        f"Keep the refined prompt at least approximately {minimum_tokens} tokens long so essential detail is not lost. "
        "There is no maximum output-token limit. Return only the refined prompt—"
        "no explanation, answer, preamble, or quotation marks."
    )

# Helpers
def estimate_tokens(text: str) -> float:
    """Return the requested rough heuristic: one token per four characters."""
    return max(0, len(text) / 4)


def format_token_count(token_count: float) -> str:
    """Keep whole estimates clean while retaining precision for short prompts."""
    return str(int(token_count)) if token_count.is_integer() else f"{token_count:.1f}"


def safe_text(text: str) -> str:
    """Prevent user and model text from being interpreted as HTML in cards."""
    return html.escape(text).replace("\n", "<br>")


def clean_optimized_output(text: str) -> str:
    text = text.strip()
    if len(text) >= 2 and text[0] in "\"'" and text[-1] in "\"'":
        text = text[1:-1].strip()
    lowered = text.lower()
    for lead in ["here is the rewritten message:", "here's the rewritten message:",
                 "rewritten message:", "optimized message:"]:
        if lowered.startswith(lead):
            text = text[len(lead):].strip()
            break
    return text


# Paid API backends
def query_openai(model, prompt, api_key, system=None):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    payload = {"model": model, "messages": messages}
    resp = requests.post(url, headers=headers, json=payload, timeout=(10, PAID_API_TIMEOUT_SECONDS))
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def query_anthropic(model, prompt, api_key, system=None):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    if system:
        payload["system"] = system
    resp = requests.post(url, headers=headers, json=payload, timeout=(10, PAID_API_TIMEOUT_SECONDS))
    resp.raise_for_status()
    blocks = resp.json().get("content", [])
    return "".join(b.get("text", "") for b in blocks if b.get("type") == "text").strip()


def query_gemini(model, prompt, api_key, system=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
    resp = requests.post(url, json=payload, timeout=(10, PAID_API_TIMEOUT_SECONDS))
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


def query_paid(platform, model, prompt, api_key, system=None):
    if platform == "OpenAI":
        return query_openai(model, prompt, api_key, system=system)
    elif platform == "Anthropic":
        return query_anthropic(model, prompt, api_key, system=system)
    elif platform == "Gemini":
        return query_gemini(model, prompt, api_key, system=system)
    raise ValueError(f"Unknown platform: {platform}")


# Local backends: Ollama (with auto-download) and Hugging Face hosted API
def get_ollama_models(base_url):
    resp = requests.get(f"{base_url}/api/tags", timeout=10)
    resp.raise_for_status()
    return [m.get("name", "") for m in resp.json().get("models", [])]


def pull_ollama_model(model, base_url, status_placeholder=None):
    with requests.post(f"{base_url}/api/pull", json={"name": model, "stream": True},
                        stream=True, timeout=None) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            if "error" in data:
                raise RuntimeError(data["error"])
            status = data.get("status", "")
            completed, total = data.get("completed"), data.get("total")
            if completed and total and status_placeholder:
                status_placeholder.text(f"⬇️ {status} — {int(completed / total * 100)}%")
            elif status_placeholder:
                status_placeholder.text(f"⬇️ {status}")
            if status == "success":
                break


def ensure_ollama_model(model, base_url, show_progress=False):
    try:
        available = set(get_ollama_models(base_url))
    except requests.exceptions.RequestException:
        raise ConnectionError(f"Could not reach Ollama at {base_url}. Is `ollama serve` running?")

    variants = {model, model if ":" in model else f"{model}:latest"}
    if variants & available:
        return

    placeholder = st.empty() if show_progress else None
    if placeholder:
        placeholder.info(f"Model `{model}` isn't downloaded yet. Pulling it via Ollama now...")
    try:
        pull_ollama_model(model, base_url, placeholder)
        if placeholder:
            placeholder.success(f"✅ `{model}` downloaded and ready.")
    except Exception as e:
        if placeholder:
            placeholder.error(f"Failed to download `{model}`: {e}")
        raise


def query_ollama(model, prompt, system=None, base_url=OLLAMA_BASE):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "30m",
        "options": {"num_ctx": 2048},
    }
    if system:
        payload["system"] = system
    try:
        # A separate connect/read timeout works for every Ollama model, whether small,
        # large, CPU-only, or GPU-backed. Large local models need longer first-token time.
        resp = requests.post(
            f"{base_url}/api/generate",
            json=payload,
            timeout=(10, LOCAL_OLLAMA_TIMEOUT_SECONDS),
        )
    except requests.exceptions.ReadTimeout as exc:
        raise LocalModelTimeout(model) from exc
    except requests.exceptions.RequestException as exc:
        raise LocalModelRequestError(f"Ollama could not complete a request for `{model}`: {exc}") from exc
    resp.raise_for_status()
    return resp.json().get("response", "").strip()


def check_hf_model_exists(model):
    resp = requests.get(f"https://huggingface.co/api/models/{model}", timeout=15)
    return resp.status_code == 200


def query_huggingface_api(model, prompt, token, system=None):
    if not check_hf_model_exists(model):
        raise ValueError(f"Model `{model}` was not found on Hugging Face.")
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    payload = {
        "inputs": full_prompt,
        "parameters": {"return_full_text": False},
        "options": {"wait_for_model": True},
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=(10, HOSTED_MODEL_TIMEOUT_SECONDS))
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"].strip()
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"].strip()
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(data["error"])
    return str(data).strip()

# History (session only)
if "model_history" not in st.session_state:
    st.session_state.model_history = []  # list of {"tier", "provider", "model"}
if "session_result" not in st.session_state:
    st.session_state.session_result = None
if "active_backend_kind" not in st.session_state:
    st.session_state.active_backend_kind = None
if "active_job" not in st.session_state:
    st.session_state.active_job = None
if "active_job_details" not in st.session_state:
    st.session_state.active_job_details = None
if "active_job_executor" not in st.session_state:
    st.session_state.active_job_executor = None


def reset_next_session_settings():
    """Reset fields for future use without touching a running job snapshot."""
    for key in [
        "paid_platform", "paid_model_input", "paid_api_key", "local_provider",
        "ollama_model_input", "ollama_endpoint", "hf_model_input", "hf_token",
        "active_backend_kind", "user_message", "model_history", "session_result",
    ]:
        st.session_state.pop(key, None)
    st.cache_data.clear()
    st.cache_resource.clear()


def activate_paid_backend():
    """Mark paid API as the next selected backend after any paid setting changes."""
    if st.session_state.get("paid_platform") != "None (skip paid API)":
        st.session_state.active_backend_kind = "paid"
    else:
        st.session_state.active_backend_kind = None


def activate_local_backend():
    """Mark the currently selected local method as the next selected backend."""
    st.session_state.active_backend_kind = (
        "ollama" if st.session_state.get("local_provider") == "Ollama (local)" else "huggingface"
    )


def add_to_history(tier, provider, model):
    entry = {"tier": tier, "provider": provider, "model": model}
    st.session_state.model_history = [
        e for e in st.session_state.model_history
        if not (e["tier"] == tier and e["provider"] == provider and e["model"] == model)
    ]
    st.session_state.model_history.insert(0, entry)
    st.session_state.model_history = st.session_state.model_history[:6]


def recall_history_entry(entry):
    if entry["tier"] == "Paid":
        st.session_state["paid_platform"] = entry["provider"]
        st.session_state["paid_model_input"] = entry["model"]
    else:
        st.session_state["local_provider"] = entry["provider"]
        if entry["provider"] == "Ollama (local)":
            st.session_state["ollama_model_input"] = entry["model"]
        else:
            st.session_state["hf_model_input"] = entry["model"]




# Task 1: The UI Shell
st.markdown('<div class="eyebrow">Prompt workspace</div>', unsafe_allow_html=True)
st.title("✨ Mono Void")
st.markdown(
    '<div class="hero-copy">A calm space to compare your original prompt with a refined version. '
    'Your work stays on screen while you adjust the workspace—send only when you are ready.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    # Provider settings update immediately. Completed results remain in session state.
    st.markdown("### Workspace")
    st.button("Reset", on_click=reset_next_session_settings, use_container_width=True,
              help="Resets fields for the next session. A running rewrite continues unchanged.")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 💳 Paid API")
    paid_platform = st.selectbox(
        "Platform",
        ["None (skip paid API)", "OpenAI", "Anthropic", "Gemini"],
        key="paid_platform",
        on_change=activate_paid_backend,
    )
    paid_model, api_key = "", ""
    if paid_platform != "None (skip paid API)":
        model_placeholders = {"OpenAI": "e.g. gpt-4o-mini", "Anthropic": "e.g. claude-haiku-4-5-20251001", "Gemini": "e.g. gemini-2.0-flash"}
        paid_model = st.text_input(
            f"{paid_platform} model name",
            placeholder=model_placeholders[paid_platform],
            key="paid_model_input",
            on_change=activate_paid_backend,
        )
        api_key = st.text_input(
            f"{paid_platform} API key",
            type="password",
            key="paid_api_key",
            help="Used only for this session. Never stored or logged.",
            on_change=activate_paid_backend,
        )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 🖥️ Local or hosted LLM")
    local_provider = st.radio(
        "Run via",
        ["Ollama (local)", "Hugging Face (API)"],
        key="local_provider",
        on_change=activate_local_backend,
    )
    ollama_endpoint, hf_token = OLLAMA_BASE, ""
    if local_provider == "Ollama (local)":
        local_model = st.text_input(
            "Ollama model name",
            value="",
            key="ollama_model_input",
            placeholder="e.g. llama3.2:3b",
            help="Choose any installed Ollama model. No model is selected by default.",
            on_change=activate_local_backend,
        )
        ollama_endpoint = st.text_input(
            "Ollama endpoint",
            value=OLLAMA_BASE,
            key="ollama_endpoint",
            on_change=activate_local_backend,
        )
    else:
        local_model = st.text_input(
            "Hugging Face model repo",
            value="",
            placeholder="e.g. HuggingFaceH4/zephyr-7b-beta",
            key="hf_model_input",
            on_change=activate_local_backend,
        )
        hf_token = st.text_input(
            "Hugging Face API token",
            type="password",
            key="hf_token",
            on_change=activate_local_backend,
        )
    active_kind = st.session_state.active_backend_kind
    active_labels = {
        "paid": f"{paid_platform}: {paid_model or 'model needed'}",
        "ollama": f"Ollama: {st.session_state.get('ollama_model_input', '') or 'model needed'}",
        "huggingface": f"Hugging Face: {st.session_state.get('hf_model_input', '') or 'model needed'}",
    }
    st.caption(f"Active for the next transmission: {active_labels.get(active_kind, 'Choose an LLM')}")
    if st.session_state.model_history:
        st.markdown("### Recently used")
        for entry in st.session_state.model_history:
            st.caption(f"{entry['provider']} · {entry['model']}")

st.markdown("<hr>", unsafe_allow_html=True)

# Task 2: Multi-Data Collection. The form keeps normal typing from rerunning the workspace.
st.markdown('<div class="composer"><p class="composer-title">Compose a transmission</p><p class="composer-help">This is your input space. Add context, then write the message you want to optimize.</p>', unsafe_allow_html=True)
with st.form("transmission_form", border=False):
    st.markdown('<div class="message-label">Your message <span>required</span></div>', unsafe_allow_html=True)
    user_message = st.text_area("Message", placeholder="Write the message you would like to transmit…", label_visibility="collapsed", key="user_message")
    transmit_clicked = st.form_submit_button("🚀 Transmit", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
stop_clicked = st.button("Stop current session", type="secondary", help="Explicitly clears the active comparison from this workspace.")
if stop_clicked:
    job = st.session_state.active_job
    if job is not None:
        job.cancel()  # Cancels if the request has not started; an in-flight HTTP call is ignored on completion.
    st.session_state.active_job = None
    st.session_state.active_job_details = None
    executor = st.session_state.active_job_executor
    st.session_state.active_job_executor = None
    if executor is not None:
        executor.shutdown(wait=False, cancel_futures=True)
    st.session_state.session_result = None
    st.toast("Session stopped. Your composer text is still available.")

# Selected-backend helpers. The active kind changes only when the user changes a provider field.
def snapshot_selected_backend():
    """Freeze the last selected provider and credentials for one transmission."""
    kind = st.session_state.active_backend_kind
    if kind is None:
        raise ValueError("Choose an LLM in the sidebar before transmitting.")

    if kind == "paid":
        platform = st.session_state.get("paid_platform", "None (skip paid API)")
        model = st.session_state.get("paid_model_input", "").strip()
        key = st.session_state.get("paid_api_key", "").strip()
        if platform == "None (skip paid API)" or not model or not key:
            raise ValueError("Enter the paid provider, model name, and API key to use that selected LLM.")
        return {"kind": kind, "tier": "Paid", "provider": platform, "model": model, "api_key": key}

    if kind == "ollama":
        model = st.session_state.get("ollama_model_input", "").strip()
        endpoint = st.session_state.get("ollama_endpoint", OLLAMA_BASE).strip() or OLLAMA_BASE
        if not model:
            raise ValueError("Enter an Ollama model name to use that selected LLM.")
        return {"kind": kind, "tier": "Local", "provider": "Ollama (local)", "model": model, "endpoint": endpoint}

    model = st.session_state.get("hf_model_input", "").strip()
    token = st.session_state.get("hf_token", "").strip()
    if not model:
        raise ValueError("Enter a Hugging Face model repo to use that selected LLM.")
    return {"kind": kind, "tier": "Hosted", "provider": "Hugging Face (API)", "model": model, "token": token}


def dispatch_selected(backend, prompt, system=None):
    """Use only the frozen backend selection; never reroute or fall back."""
    if backend["kind"] == "paid":
        return query_paid(backend["provider"], backend["model"], prompt, backend["api_key"], system=system)
    if backend["kind"] == "ollama":
        ensure_ollama_model(backend["model"], backend["endpoint"])
        return query_ollama(backend["model"], prompt, system=system, base_url=backend["endpoint"])
    return query_huggingface_api(backend["model"], prompt, backend["token"], system=system)


def show_refined_prompt(result):
    """Render the token comparison and refined prompt with Streamlit's copy control."""
    token_left, token_right = st.columns(2)
    with token_left:
        st.metric("Your prompt", f"~{format_token_count(result['original_tokens'])} tokens")
    with token_right:
        st.metric("Refined prompt", f"~{format_token_count(result['optimized_tokens'])} tokens")
    st.markdown("### Refined prompt")
    st.code(result["optimized"], language=None)


@st.fragment(run_every=1)
def render_active_rewrite():
    """Poll only the background job; sidebar edits never cancel or replace its snapshot."""
    job = st.session_state.active_job
    if job is None:
        if st.session_state.session_result:
            show_refined_prompt(st.session_state.session_result)
        return
    if not job.done():
        st.info("Refining prompt with the selected LLM… You can prepare settings for the next session while this runs.")
        return

    details = st.session_state.active_job_details
    executor = st.session_state.active_job_executor
    st.session_state.active_job = None
    st.session_state.active_job_details = None
    st.session_state.active_job_executor = None
    if executor is not None:
        executor.shutdown(wait=False)
    try:
        optimized_message = clean_optimized_output(job.result()) or details["original"]
        if estimate_tokens(optimized_message) < details["minimum_tokens"]:
            # Preserve the user's full prompt rather than returning an over-compressed rewrite.
            optimized_message = details["original"]
        result = {
            "name": details["name"],
            "original": details["original"],
            "optimized": optimized_message,
            "original_tokens": details["original_tokens"],
            "optimized_tokens": estimate_tokens(optimized_message),
            "backend": details["backend_label"],
        }
        st.session_state.session_result = result
        add_to_history(details["backend"]["tier"], details["backend"]["provider"], details["backend"]["model"])
        show_refined_prompt(result)
    except LocalModelTimeout as e:
        st.error(f"{e} The same timeout policy applies to every Ollama model.")
    except LocalModelRequestError as e:
        st.error(str(e))
    except (ConnectionError, ValueError, RuntimeError, requests.exceptions.RequestException) as e:
        st.error(str(e))
    except Exception:
        st.error("The transmission could not be completed. Please check the selected model settings and try again.")


# Task 3: The Action Gate
if transmit_clicked and not stop_clicked:
    if user_message.strip() == "":
        st.warning("Please type a message to transmit.")
    elif st.session_state.active_job is not None and not st.session_state.active_job.done():
        st.warning("A rewrite is already running. Only Stop current session can cancel it.")
    else:
        try:
            backend = snapshot_selected_backend()
            original_tokens = estimate_tokens(user_message)
            minimum_tokens = max(1, math.ceil(original_tokens / 2))
            executor = ThreadPoolExecutor(max_workers=1)
            st.session_state.active_job_executor = executor
            st.session_state.active_job = executor.submit(
                dispatch_selected,
                backend,
                user_message,
                refinement_system_prompt(minimum_tokens),
            )
            st.session_state.active_job_details = {
                "name": "Guest",
                "original": user_message,
                "original_tokens": original_tokens,
                "minimum_tokens": minimum_tokens,
                "backend": backend,
                "backend_label": f"{backend['provider']} ({backend['model']})",
            }
            st.info("Rewrite started. You can change LLM settings for the next session without affecting this one.")
        except ValueError as e:
            st.error(str(e))
        except Exception:
            st.error("The rewrite could not be started. Please check the selected model settings and try again.")

render_active_rewrite()
