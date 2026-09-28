"""Reusable presentation components for AgroSenseAI. They only render HTML; no data logic lives here."""

from html import escape

import streamlit as st

LEAF = (
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#74C69D" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14"/>'
    '<path d="M5 19c2-4 5-7 9-9"/></svg>'
)
CHECK = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.6 2.6L16 9.5"/></svg>'
)
INBOX = (
    '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#40916C" stroke-width="1.6" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M3 13h5l1.5 3h5L16 13h5"/>'
    '<path d="M5.5 5h13L21 13v6H3v-6z"/></svg>'
)


def flat(markup: str) -> str:
    """Strip line indentation so Markdown never treats HTML as a code block."""
    return "".join(line.strip() for line in markup.strip().splitlines())


def html(markup: str) -> None:
    st.markdown(flat(markup), unsafe_allow_html=True)


def _e(value) -> str:
    return escape(str(value))


def render_brand() -> None:
    html(
        f'<div class="brand"><div class="brand-mark">{LEAF}</div><div class="brand-name">AgroSenseAI</div></div>'
        '<div class="brand-sub">Smart Agricultural Intelligence</div>'
    )


def render_header(title: str, subtitle: str) -> None:
    html(f'<div class="page-title">{_e(title)}</div><div class="page-sub">{_e(subtitle)}</div>')


def render_section_title(text: str) -> None:
    html(f'<div class="section-title">{_e(text)}</div>')


def render_group_title(title: str, subtitle: str = "") -> None:
    sub = f'<div class="grp-sub">{_e(subtitle)}</div>' if subtitle else ""
    html(f'<div class="grp-title">{_e(title)}</div>{sub}')


def render_helper(text: str) -> None:
    html(f'<div class="helper">{_e(text)}</div>')


def card_html(title: str, body: str, variant: str = "") -> str:
    return f'<div class="card {variant}"><h4>{_e(title)}</h4><p>{_e(body)}</p></div>'


def metric_html(label: str, value, note: str = "", small: bool = False) -> str:
    size = " small" if small else ""
    note_html = f'<div class="m-note">{_e(note)}</div>' if note else ""
    return (
        f'<div class="metric"><div class="m-label">{_e(label)}</div>'
        f'<div class="m-value{size}">{_e(value)}</div>{note_html}</div>'
    )


def render_grid(items: list[str], cols: str = "g3") -> None:
    html(f'<div class="grid {cols}">{"".join(items)}</div>')


def render_metric_card(label: str, value, note: str = "", small: bool = False) -> None:
    html(metric_html(label, value, note, small))


def pills(items, kind: str = "") -> str:
    return "".join(f'<span class="pill {kind}">{_e(i)}</span>' for i in items)


def kv_html(pairs: list[tuple[str, str]]) -> str:
    cells = "".join(f'<div><div class="k">{_e(k)}</div><div class="v">{_e(v)}</div></div>' for k, v in pairs)
    return f'<div class="kv">{cells}</div>'


def render_banner(kind: str, message: str) -> None:
    html(f'<div class="banner {kind}"><div>{_e(message)}</div></div>')


def render_empty_state(title: str, text: str) -> None:
    html(f'<div class="placeholder">{INBOX}<b>{_e(title)}</b><span>{_e(text)}</span></div>')


def render_loading(message: str) -> str:
    return f'<div class="loading"><b>{_e(message)}</b><div class="bar"></div></div>'


def render_workflow() -> None:
    steps = [
        ("Agricultural Inputs", "Soil, climate, location and crop details"),
        ("Validation", "Values are range-checked before prediction"),
        ("Machine Learning", "Trained models score the inputs"),
        ("Prediction", "The result is returned to the app"),
        ("PostgreSQL Storage", "Each prediction is saved to history"),
    ]
    body = "".join(f"<div class='flow-step'><b>{_e(t)}</b><span>{_e(d)}</span></div>" for t, d in steps)
    html(f'<div class="card"><div class="flow">{body}</div></div>')


def render_footer() -> None:
    html(
        '<div class="footer">AgroSenseAI • Machine Learning + FastAPI + PostgreSQL<br>'
        "Built for intelligent agricultural decision support.</div>"
    )


DISCLAIMER = (
    "Predictions are decision-support estimates and should be considered alongside local agricultural expertise."
)
