"""Visual design tokens and global CSS for AgroSenseAI (presentation layer only)."""

import streamlit as st

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Inter:wght@400;500;600&family=Manrope:wght@600;700;800&display=swap');"
)

# Subtle "furrow lines" pattern used behind the hero panel (inline SVG, no external assets).
FURROWS = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='640' height='320' "
    "viewBox='0 0 640 320' fill='none' stroke='%2374C69D' stroke-width='1.2' opacity='0.22'%3E"
    "%3Cpath d='M-20 300 C 140 230, 300 300, 480 210 S 640 170, 700 150'/%3E"
    "%3Cpath d='M-20 260 C 140 190, 300 260, 480 170 S 640 130, 700 110'/%3E"
    "%3Cpath d='M-20 220 C 140 150, 300 220, 480 130 S 640 90, 700 70'/%3E"
    "%3Cpath d='M-20 180 C 140 110, 300 180, 480 90 S 640 50, 700 30'/%3E"
    "%3Cpath d='M-20 140 C 140 70, 300 140, 480 50 S 640 10, 700 -10'/%3E"
    "%3C/svg%3E\")"
)

CSS = FONT_IMPORT + """
:root {
  --green-900:#1B4332; --green-700:#2D6A4F; --green-500:#40916C; --green-300:#74C69D;
  --sage:#D8F3DC; --cream:#F8F7F2; --bg:#F7F9F7; --card:#FFFFFF;
  --text:#1F2937; --muted:#6B7280; --border:#E5E7EB;
  --success:#22C55E; --warning:#F59E0B; --error:#EF4444; --info:#3B82F6;
  --font-display:'Manrope','Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
  --font-body:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
}

html, body, [data-testid="stApp"] { font-family: var(--font-body); color: var(--text); }
[data-testid="stApp"] { background: var(--bg); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stAppDeployButton"], footer { display: none !important; }

.block-container { max-width: 1120px; padding: 2.2rem 2rem 3rem; }
h1, h2, h3, h4 { font-family: var(--font-display); color: var(--green-900); letter-spacing: -0.01em; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] { background: var(--cream); border-right: 1px solid var(--border); }
[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }
.brand { display:flex; align-items:center; gap:.75rem; margin-bottom:.25rem; }
.brand-mark { width:38px; height:38px; border-radius:11px; background:var(--green-900);
  display:flex; align-items:center; justify-content:center; flex:none; }
.brand-name { font-family:var(--font-display); font-weight:800; font-size:1.25rem; color:var(--green-900); line-height:1.1; }
.brand-sub { color:var(--muted); font-size:.85rem; margin:.15rem 0 1.1rem 0; }
[data-testid="stSidebar"] .stButton > button {
  justify-content:flex-start; width:100%; text-align:left; background:transparent; border:1px solid transparent;
  color:var(--text); font-weight:500; padding:.55rem .8rem; border-radius:10px; box-shadow:none;
}
[data-testid="stSidebar"] .stButton > button > div { justify-content:flex-start; width:100%; }
[data-testid="stSidebar"] .stButton > button p { text-align:left; }
[data-testid="stSidebar"] .stButton > button:hover { background:#EEF3EE; border-color:transparent; color:var(--green-900); }
[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
  background:var(--sage); color:var(--green-900); font-weight:600; border-color:#BFE6C7;
}
.status-pill { display:inline-flex; align-items:center; gap:.45rem; font-size:.82rem; color:var(--muted);
  border:1px solid var(--border); background:#fff; border-radius:999px; padding:.3rem .7rem; }
.dot { width:8px; height:8px; border-radius:50%; background:var(--muted); display:inline-block; }
.dot.ok { background:var(--success); } .dot.bad { background:var(--error); }

/* ---------- Hero ---------- */
.st-key-hero { background:var(--green-900) """ + FURROWS + """ right bottom/640px 320px no-repeat;
  border-radius:20px; padding:2.6rem 2.6rem 2rem; margin-bottom:1.6rem; }
.hero-brand { display:flex; align-items:center; gap:.6rem; color:var(--green-300); font-weight:600; font-size:1rem; margin-bottom:1rem; }
.hero-title { font-family:var(--font-display); font-weight:800; color:#fff; font-size:clamp(2rem,4.2vw,3.15rem);
  line-height:1.1; letter-spacing:-0.025em; max-width:16em; margin:0 0 1rem; }
.hero-copy { color:#D1E7DB; font-size:1.08rem; line-height:1.6; max-width:38em; margin:0 0 1.4rem; }
.st-key-hero .stButton > button { border-radius:10px; font-weight:600; padding:.65rem 1.2rem; }
.st-key-hero .stButton > button[kind="primary"],
.st-key-hero .stButton > button[data-testid="stBaseButton-primary"] { background:#fff; color:var(--green-900); border:1px solid #fff; }
.st-key-hero .stButton > button[kind="primary"]:hover,
.st-key-hero .stButton > button[data-testid="stBaseButton-primary"]:hover { background:var(--sage); border-color:var(--sage); }
.st-key-hero .stButton > button[kind="secondary"],
.st-key-hero .stButton > button[data-testid="stBaseButton-secondary"] { background:transparent; color:#fff; border:1px solid rgba(255,255,255,.45); }
.st-key-hero .stButton > button[kind="secondary"]:hover,
.st-key-hero .stButton > button[data-testid="stBaseButton-secondary"]:hover { background:rgba(255,255,255,.1); border-color:#fff; color:#fff; }

/* ---------- Page headers, sections, cards ---------- */
.page-title { font-family:var(--font-display); font-weight:800; font-size:clamp(1.6rem,3vw,2.05rem); color:var(--green-900);
  letter-spacing:-0.02em; margin:0 0 .3rem; }
.page-sub { color:var(--muted); font-size:1.02rem; line-height:1.55; max-width:44em; margin:0 0 1.6rem; }
.section-title { font-family:var(--font-display); font-weight:700; font-size:1.15rem; color:var(--green-900); margin:2rem 0 .9rem; }
.card { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1.3rem 1.4rem;
  box-shadow:0 1px 2px rgba(16,24,40,.04); }
.card h4 { margin:0 0 .4rem; font-size:1.05rem; font-weight:700; }
.card p { margin:0; color:var(--muted); font-size:.95rem; line-height:1.6; }
.grid { display:grid; gap:1rem; }
.grid.g3 { grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); }
.grid.g2 { grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); }
.grid.g4 { grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); }
.feature { border-left:4px solid var(--green-500); }
.feature.alt { border-left-color:var(--green-300); }
.feature.alt2 { border-left-color:var(--green-700); }
.pill { display:inline-block; background:var(--sage); color:var(--green-900); font-size:.82rem; font-weight:500;
  border-radius:999px; padding:.2rem .7rem; margin:0 .35rem .4rem 0; }
.pill.neutral { background:#F3F4F6; color:var(--text); }
.pill.ok { background:#DCFCE7; color:#166534; } .pill.bad { background:#FEE2E2; color:#991B1B; }

/* ---------- Metrics ---------- */
.metric { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1.1rem 1.3rem; }
.metric .m-label { color:var(--muted); font-size:.88rem; margin-bottom:.3rem; }
.metric .m-value { font-family:var(--font-display); font-weight:800; font-size:2.1rem; color:var(--green-900); line-height:1.1; }
.metric .m-note { color:var(--muted); font-size:.82rem; margin-top:.3rem; }
.metric .m-value.small { font-size:1.35rem; }

/* ---------- Workflow ---------- */
.flow { display:grid; grid-template-columns:repeat(5,1fr); gap:0; margin-top:.4rem; }
.flow-step { position:relative; padding:1.6rem .8rem 0 0; }
.flow-step::before { content:""; position:absolute; top:.45rem; left:0; right:0; height:2px; background:var(--green-300); }
.flow-step::after { content:""; position:absolute; top:0; left:0; width:12px; height:12px; border-radius:50%;
  background:var(--green-700); box-shadow:0 0 0 4px var(--sage); }
.flow-step:last-child::before { right:auto; width:0; }
.flow-step b { display:block; font-family:var(--font-display); color:var(--green-900); font-size:.98rem; margin-bottom:.2rem; }
.flow-step span { color:var(--muted); font-size:.87rem; line-height:1.5; display:block; }

/* ---------- Forms ---------- */
[class*="st-key-grp"] { background:var(--card); border:1px solid var(--border); border-radius:16px;
  padding:1.1rem 1.3rem .6rem; margin-bottom:.9rem; box-shadow:0 1px 2px rgba(16,24,40,.04); }
.grp-title { font-family:var(--font-display); font-weight:700; font-size:1.02rem; color:var(--green-900); margin:0 0 .1rem; }
.grp-sub { color:var(--muted); font-size:.87rem; margin:0 0 .7rem; }
.helper { color:var(--muted); font-size:.8rem; margin:-.55rem 0 .8rem; line-height:1.4; }
[data-testid="stForm"] { border:none; padding:0; background:transparent; }
[data-testid="stWidgetLabel"] p { font-size:.88rem; font-weight:500; color:var(--text); }
[data-baseweb="input"], [data-baseweb="select"] > div, [data-testid="stNumberInputContainer"] { border-radius:10px !important; }
div.stButton > button, div.stFormSubmitButton > button {
  border-radius:10px; font-weight:600; padding:.65rem 1.2rem; transition:background .15s ease, border-color .15s ease; }
div.stFormSubmitButton > button[kind="primaryFormSubmit"],
div.stFormSubmitButton > button[data-testid="stBaseButton-primaryFormSubmit"],
div.stFormSubmitButton > button[kind="secondaryFormSubmit"],
div.stFormSubmitButton > button[data-testid="stBaseButton-secondaryFormSubmit"] {
  background:var(--green-700); color:#fff; border:1px solid var(--green-700); font-size:1rem; padding:.8rem 1.2rem; }
div.stFormSubmitButton > button:hover { background:var(--green-900); border-color:var(--green-900); color:#fff; }
div.stFormSubmitButton > button:focus-visible, div.stButton > button:focus-visible { outline:3px solid var(--green-300); outline-offset:2px; }

/* ---------- Result / loading / empty ---------- */
.result { background:var(--card); border:1px solid #BFE6C7; border-radius:16px; padding:1.4rem 1.5rem; }
.result .r-head { display:flex; align-items:center; gap:.5rem; color:#166534; font-weight:600; font-size:.92rem; margin-bottom:.9rem; }
.result .r-label { color:var(--muted); font-size:.88rem; }
.result .r-value { font-family:var(--font-display); font-weight:800; font-size:2.5rem; color:var(--green-900); line-height:1.15; margin:.15rem 0 1rem; }
.result .r-value.number { font-size:2.8rem; }
.meter { height:8px; background:#EEF2EE; border-radius:99px; overflow:hidden; margin:.35rem 0 1rem; }
.meter > div { height:100%; background:var(--green-500); border-radius:99px; }
.kv { display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:.8rem 1.2rem; margin-top:.4rem; }
.kv .k { color:var(--muted); font-size:.8rem; } .kv .v { font-weight:600; font-size:.98rem; color:var(--text); word-break:break-word; }
.note { color:var(--muted); font-size:.82rem; line-height:1.5; margin-top:1rem; }
.placeholder { border:1.5px dashed #CBD5CB; border-radius:16px; padding:2rem 1.4rem; text-align:center; color:var(--muted); background:#FBFCFB; }
.placeholder b { display:block; color:var(--green-900); font-family:var(--font-display); font-size:1.02rem; margin:.5rem 0 .25rem; }
.placeholder span { font-size:.9rem; line-height:1.5; display:block; }
.loading { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:1.6rem 1.5rem; }
.loading b { font-family:var(--font-display); color:var(--green-900); }
.bar { height:6px; border-radius:99px; background:#EEF2EE; overflow:hidden; margin-top:1rem; position:relative; }
.bar::after { content:""; position:absolute; inset:0; width:40%; background:var(--green-500); border-radius:99px; animation:slide 1.3s ease-in-out infinite; }
@keyframes slide { 0%{transform:translateX(-100%)} 100%{transform:translateX(260%)} }
.banner { display:flex; gap:.7rem; border-radius:12px; padding:.85rem 1rem; font-size:.93rem; line-height:1.5; margin:0 0 1rem; border:1px solid; }
.banner.error { background:#FEF2F2; border-color:#FECACA; color:#991B1B; }
.banner.warning { background:#FFFBEB; border-color:#FDE68A; color:#92400E; }
.banner.info { background:#EFF6FF; border-color:#BFDBFE; color:#1E40AF; }

.sub-label { color:var(--muted); font-size:.82rem; margin:1.1rem 0 .45rem; }

/* ---------- Footer ---------- */
.footer { margin-top:3rem; padding-top:1.1rem; border-top:1px solid var(--border); color:var(--muted); font-size:.85rem; text-align:center; line-height:1.6; }

/* ---------- Responsive ---------- */
@media (max-width: 900px) { .flow { grid-template-columns:1fr; gap:1.1rem; }
  .flow-step { padding:0 0 0 1.8rem; } .flow-step::before { top:.3rem; bottom:-1.2rem; left:5px; right:auto; width:2px; height:auto; }
  .flow-step::after { top:.3rem; } .flow-step:last-child::before { display:none; } }
@media (max-width: 640px) {
  .block-container { padding:1.2rem 1rem 2rem; }
  .st-key-hero { padding:1.6rem 1.3rem 1.3rem; border-radius:16px; }
  .hero-copy { font-size:1rem; }
  .result .r-value { font-size:2rem; } .result .r-value.number { font-size:2.2rem; }
}
@media (prefers-reduced-motion: reduce) { .bar::after { animation:none; width:100%; opacity:.5; } }
"""


def inject_css() -> None:
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
