import os

import pandas as pd
import requests
import streamlit as st

import ui_helpers as ui
from components import (
    CHECK, DISCLAIMER, card_html, flat, kv_html, metric_html, pills, render_banner, render_brand,
    render_empty_state, render_footer, render_grid, render_group_title, render_header, render_helper,
    render_loading, render_section_title, render_workflow,
)
from styles import inject_css

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AgroSenseAI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="auto",
)
inject_css()

# Newer Streamlit versions replace use_container_width with width="stretch".
_NEW_API = tuple(int(x) for x in st.__version__.split(".")[:2]) >= (1, 50)
STRETCH = {"width": "stretch"} if _NEW_API else {"use_container_width": True}


def api_get(path: str, params=None):
    response = requests.get(f"{API_URL}{path}", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload: dict):
    response = requests.post(f"{API_URL}{path}", json=payload, timeout=20)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=20, show_spinner=False)
def get_health():
    """Read-only call to the existing /health endpoint. Returns None if the backend is unreachable."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


# ---------------------------------------------------------------- navigation
PAGES = [
    ("Home", "home"),
    ("Crop Recommendation", "spa"),
    ("Yield Prediction", "trending_up"),
    ("Prediction History", "history"),
    ("Model Information", "analytics"),
    ("About", "info"),
]

if "page" not in st.session_state:
    st.session_state.page = "Home"


def go(page_name: str) -> None:
    st.session_state.page = page_name


with st.sidebar:
    render_brand()
    for name, icon in PAGES:
        st.button(
            name, key=f"nav_{name}", icon=f":material/{icon}:", on_click=go, args=(name,),
            type="primary" if st.session_state.page == name else "secondary", **STRETCH,
        )
    health = get_health()
    if health is None:
        pill = '<span class="dot bad"></span>Service offline'
    elif health.get("status") == "ok":
        pill = '<span class="dot ok"></span>Service online'
    else:
        pill = '<span class="dot bad"></span>Service needs attention'
    st.markdown(flat(f'<div style="margin-top:1.4rem"><span class="status-pill">{pill}</span></div>'), unsafe_allow_html=True)

page = st.session_state.page


def show_error(container, exc: Exception, what: str) -> None:
    message, detail = ui.friendly_error(exc, what)
    with container:
        render_banner("error", message)
        with st.expander("Technical details"):
            st.code(detail, language=None)


def placeholder_html(title: str, text: str) -> str:
    return f'<div class="placeholder"><b>{title}</b><span>{text}</span></div>'


# ---------------------------------------------------------------- pages
def page_home():
    with st.container(key="hero"):
        st.markdown(flat(
            '<div class="hero-brand">AgroSenseAI</div>'
            '<div class="hero-title">Smarter Farming Through Data Intelligence.</div>'
            '<div class="hero-copy">Use machine learning to recommend suitable crops, estimate agricultural yield, '
            "and maintain a structured prediction history.</div>"
        ), unsafe_allow_html=True)
        c1, c2, _ = st.columns([1.1, 1, 2.2])
        c1.button("Crop Recommendation", key="hero_crop", type="primary", on_click=go, args=("Crop Recommendation",), **STRETCH)
        c2.button("Yield Prediction", key="hero_yield", on_click=go, args=("Yield Prediction",), **STRETCH)

    entries, error = [], False
    with st.spinner("Connecting to AgroSenseAI..."):
        try:
            entries = ui.build_entries(api_get("/history", params={"limit": 100}).get("predictions", []))
        except requests.RequestException:
            error = True
    if error:
        render_banner("info", "Unable to reach the prediction service. Please make sure the backend is running.")
    elif entries:
        capped = len(entries) >= 100
        crop_n = sum(e["kind"] == "Crop Recommendation" for e in entries)
        total = "100+" if capped else str(len(entries))
        scope = "Among the 100 most recent records" if capped else ""
        latest = entries[0]
        render_grid([
            metric_html("Total Predictions", total),
            metric_html("Crop Recommendations", crop_n, scope),
            metric_html("Yield Predictions", len(entries) - crop_n, scope),
            metric_html("Latest Prediction", latest["kind"], latest["created"] or "", small=True),
        ], "g4")

    render_section_title("What you can do")
    render_grid([
        card_html("Crop Recommendation", "Recommend suitable crops using soil nutrients and environmental conditions.", "feature"),
        card_html("Yield Prediction", "Estimate crop yield using location, season, crop, year and area.", "feature alt"),
        card_html("Prediction History", "Review previously generated predictions stored through PostgreSQL.", "feature alt2"),
    ])
    render_section_title("How it works")
    render_workflow()


def crop_result_html(result: dict) -> str:
    crop = str(result["recommended_crop"]).title()
    conf_html = ""
    if result.get("confidence") is not None:
        pct = float(result["confidence"]) * 100
        conf_html = (
            '<div class="r-label">Confidence</div>'
            f'<div class="r-value" style="font-size:1.7rem;margin-bottom:.2rem">{pct:.1f}%</div>'
            f'<div class="meter"><div style="width:{min(max(pct, 0), 100):.1f}%"></div></div>'
        )
    saved = f"Saved to prediction history as record #{result['prediction_id']}. " if result.get("prediction_id") else ""
    from html import escape
    return (
        f'<div class="result"><div class="r-head">{CHECK}Recommendation ready</div>'
        f'<div class="r-label">Recommended Crop</div><div class="r-value">{escape(crop)}</div>{conf_html}'
        f'<div class="note">{saved}{DISCLAIMER}</div></div>'
    )


def page_crop():
    render_header("Crop Recommendation", "Enter soil nutrients and climate conditions to get a suitable crop recommendation.")
    form_col, result_col = st.columns([3, 2], gap="large")
    slot = result_col.empty()
    slot.markdown(flat(placeholder_html("Your recommendation will appear here", "Fill in the conditions and select Recommend Crop.")), unsafe_allow_html=True)

    with form_col:
        with st.form("crop_form"):
            with st.container(key="grp_soil"):
                render_group_title("Soil Nutrients")
                c1, c2, c3 = st.columns(3)
                with c1:
                    nitrogen = st.number_input("Nitrogen (N)", min_value=0.0, max_value=300.0, value=45.0, step=1.0)
                    render_helper("Soil nitrogen level (0–300)")
                with c2:
                    phosphorus = st.number_input("Phosphorus (P)", min_value=0.0, max_value=300.0, value=32.0, step=1.0)
                    render_helper("Soil phosphorus level (0–300)")
                with c3:
                    potassium = st.number_input("Potassium (K)", min_value=0.0, max_value=300.0, value=38.0, step=1.0)
                    render_helper("Soil potassium level (0–300)")
            with st.container(key="grp_climate"):
                render_group_title("Climate Conditions")
                c1, c2, c3 = st.columns(3)
                with c1:
                    temperature = st.number_input("Temperature (°C)", min_value=-20.0, max_value=70.0, value=26.5, step=0.1)
                    render_helper("Air temperature (−20 to 70)")
                with c2:
                    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=65.0, step=0.1)
                    render_helper("Relative humidity (0–100)")
                with c3:
                    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=5000.0, value=120.0, step=1.0)
                    render_helper("Rainfall in mm (0–5000)")
            with st.container(key="grp_chem"):
                render_group_title("Soil Chemistry")
                c1, _, _ = st.columns(3)
                with c1:
                    ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
                    render_helper("Soil acidity or alkalinity (0–14)")
            crop_submit = st.form_submit_button("Recommend Crop", type="primary", **STRETCH)

    if crop_submit:
        payload = {
            "N": nitrogen,
            "P": phosphorus,
            "K": potassium,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall,
        }
        slot.markdown(render_loading("Analyzing soil and environmental conditions..."), unsafe_allow_html=True)
        try:
            result = api_post("/predict/crop", payload)
            slot.markdown(crop_result_html(result), unsafe_allow_html=True)
        except (requests.RequestException, KeyError) as exc:
            slot.empty()
            show_error(result_col, exc, "crop recommendation")


def yield_result_html(result: dict, ctx: dict) -> str:
    from html import escape
    saved = f"Saved to prediction history as record #{result['prediction_id']}. " if result.get("prediction_id") else ""
    pairs = [
        ("Crop", ctx["crop"]), ("Location", f"{ctx['state']} • {ctx['district']}"), ("Season", ctx["season"]),
        ("Crop Year", ctx["crop_year"]), ("Area (hectares)", ctx["area"]),
    ]
    return (
        f'<div class="result"><div class="r-head">{CHECK}Estimate ready</div>'
        f'<div class="r-label">Predicted Yield</div><div class="r-value number">{escape(ui.fmt_number(result["predicted_yield"]))}</div>'
        f'{kv_html(pairs)}'
        f'<div class="note">Reported in the yield units of the training dataset. {saved}{DISCLAIMER}</div></div>'
    )


def page_yield():
    render_header("Yield Prediction", "Enter location, crop and cultivation details to estimate expected crop yield.")
    try:
        options = api_get("/options")
        options_ok = True
    except requests.RequestException:
        options = {"states": [], "districts": [], "crops": [], "seasons": []}
        options_ok = False
    if not options_ok:
        render_banner("error", "Unable to reach the prediction service. Please make sure the backend is running.")

    states = options.get("states") or [""]
    districts = options.get("districts") or [""]
    crops = options.get("crops") or [""]
    seasons = options.get("seasons") or [""]

    form_col, result_col = st.columns([3, 2], gap="large")
    slot = result_col.empty()
    slot.markdown(flat(placeholder_html("Your yield estimate will appear here", "Fill in the details and select Predict Yield.")), unsafe_allow_html=True)

    with form_col:
        with st.form("yield_form"):
            with st.container(key="grp_location"):
                render_group_title("Location")
                c1, c2 = st.columns(2)
                state = c1.selectbox("State", states)
                district = c2.selectbox("District", districts)
            with st.container(key="grp_crop"):
                render_group_title("Crop Details")
                c1, c2 = st.columns(2)
                crop = c1.selectbox("Crop", crops)
                season = c2.selectbox("Season", seasons)
            with st.container(key="grp_cultivation"):
                render_group_title("Cultivation")
                c1, c2 = st.columns(2)
                crop_year = c1.number_input("Crop Year", min_value=1990, max_value=2100, value=2024, step=1)
                area = c2.number_input("Area (hectares)", min_value=0.01, value=1.0, step=0.1)
            yield_submit = st.form_submit_button("Predict Yield", type="primary", **STRETCH)

    if yield_submit:
        if not all([state, district, crop, season]):
            slot.empty()
            with result_col:
                render_banner("warning", "Start the FastAPI backend first so the available values can be loaded.")
        else:
            payload = {
                "state": state,
                "district": district,
                "crop": crop,
                "crop_year": int(crop_year),
                "season": season,
                "area": float(area),
            }
            slot.markdown(render_loading("Estimating expected crop yield..."), unsafe_allow_html=True)
            try:
                result = api_post("/predict/yield", payload)
                ctx = {"state": state, "district": district, "crop": crop, "season": season,
                       "crop_year": int(crop_year), "area": f"{float(area):g}"}
                slot.markdown(yield_result_html(result, ctx), unsafe_allow_html=True)
            except (requests.RequestException, KeyError) as exc:
                slot.empty()
                show_error(result_col, exc, "yield prediction")


def detail_card(entry: dict) -> str:
    inputs = [(ui.FIELD_LABELS.get(k, k.replace("_", " ").title()), ui.fmt_field(k, v)) for k, v in entry["input"].items()]
    outputs, alts = [], ""
    for k, v in entry["output"].items():
        if k == "alternatives" and isinstance(v, list):
            alts = pills([f"{str(a.get('crop', '')).title()} ({float(a.get('probability', 0)) * 100:.1f}%)" for a in v if isinstance(a, dict)])
            continue
        outputs.append((ui.FIELD_LABELS.get(k, k.replace("_", " ").title()), ui.fmt_field(k, v).title() if k == "recommended_crop" else ui.fmt_field(k, v)))
    alt_html = f'<div class="sub-label">Top alternatives</div>{alts}' if alts else ""
    return (
        f'<div class="grid g2"><div class="card"><h4>Inputs</h4>{kv_html(inputs)}</div>'
        f'<div class="card"><h4>Output</h4>{kv_html(outputs)}{alt_html}</div></div>'
    )


def page_history():
    render_header("Prediction History", "Previously generated AgroSenseAI predictions stored in PostgreSQL.")
    try:
        data = api_get("/history", params={"limit": 25})
        rows = data.get("predictions", [])
    except requests.RequestException as exc:
        render_banner("error", "Prediction history is currently unavailable.")
        message, detail = ui.friendly_error(exc, "history")
        st.caption(message)
        with st.expander("Technical details"):
            st.code(detail, language=None)
        return

    if not rows:
        render_empty_state("No predictions have been recorded yet.", "Run a crop recommendation or a yield prediction and it will be saved here automatically.")
        st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)
        c1, c2, _ = st.columns([1.2, 1, 2])
        c1.button("Crop Recommendation", key="empty_crop", type="primary", on_click=go, args=("Crop Recommendation",), **STRETCH)
        c2.button("Yield Prediction", key="empty_yield", on_click=go, args=("Yield Prediction",), **STRETCH)
        return

    entries = ui.build_entries(rows)
    f1, f2, f3 = st.columns(3)
    kind = f1.selectbox("Prediction Type", ["All", "Crop Recommendation", "Yield Prediction"])
    crop = f2.selectbox("Crop", ["All"] + sorted({e["crop"] for e in entries if e["crop"] != "-"}))
    period = f3.selectbox("Date", list(ui.PERIODS))
    shown = ui.filter_entries(entries, kind, crop, period)

    if not shown:
        render_empty_state("No records match these filters.", "Try a different prediction type, crop or date range.")
        return

    st.caption(f"Showing {len(shown)} of the {len(entries)} most recent records.")
    frame = pd.DataFrame([
        {"ID": e["id"], "Type": e["kind"], "Crop": e["crop"], "Prediction": e["prediction"],
         "Confidence": e["confidence"], "Created": e["created"]} for e in shown
    ])
    st.dataframe(
        frame, hide_index=True, **STRETCH,
        column_config={
            "ID": st.column_config.NumberColumn("ID", format="%d", width="small"),
            "Confidence": st.column_config.ProgressColumn("Confidence", format="%.1f%%", min_value=0, max_value=100),
        },
    )

    render_section_title("Record details")
    by_id = {e["id"]: e for e in shown}
    chosen = st.selectbox(
        "Select a record", list(by_id),
        format_func=lambda i: f"#{i}  {by_id[i]['kind']}  ({by_id[i]['created']})",
    )
    st.markdown(flat(detail_card(by_id[chosen])), unsafe_allow_html=True)


def page_model_info():
    render_header("Model Information", "The two trained models behind AgroSenseAI and the metrics stored with them.")
    health = get_health()
    if health is None:
        render_banner("error", "Unable to reach the prediction service. Please make sure the backend is running.")
    else:
        models = health.get("models", {})
        def status(label, ok, good, bad):
            return f'<span class="pill {"ok" if ok else "bad"}">{label}: {good if ok else bad}</span>'
        st.markdown(flat(
            status("Prediction service", health.get("status") == "ok", "online", "needs attention")
            + status("Crop model", models.get("crop_recommendation"), "available", "missing")
            + status("Yield model", models.get("crop_yield"), "available", "missing")
            + status("PostgreSQL", health.get("postgresql"), "connected", "unavailable")
        ), unsafe_allow_html=True)

    metrics = ui.load_model_metrics()
    if metrics is None:
        render_banner("warning", "Stored model metrics are not available.")
    metrics = metrics or {}
    rec, yld = metrics.get("recommendation", {}), metrics.get("yield", {})

    rec_pairs = []
    if "accuracy" in rec:
        rec_pairs.append(("Accuracy", f"{rec['accuracy'] * 100:.2f}%"))
    if "rows" in rec:
        rec_pairs.append(("Dataset rows", f"{rec['rows']:,}"))
    yld_pairs = []
    for key, label, fmt in [("r2", "R²", "{:.3f}"), ("mae", "MAE", "{:.2f}"), ("rmse", "RMSE", "{:.2f}"),
                            ("source_rows", "Source dataset rows", "{:,}"), ("training_rows", "Training rows", "{:,}")]:
        if key in yld:
            yld_pairs.append((label, fmt.format(yld[key])))

    def model_card(title, desc, kind, features, pairs):
        metrics_html = f'<div class="sub-label">Stored metrics</div>{kv_html(pairs)}' if pairs else ""
        return (
            f'<div class="card"><h4>{title}</h4><p>{desc}</p>'
            f'<div class="sub-label">Model type</div>{pills([kind], "neutral")}'
            f'<div class="sub-label">Input features</div>{pills(features)}{metrics_html}</div>'
        )

    render_section_title("Models")
    st.markdown(flat('<div class="grid g2">' + model_card(
        "Crop Recommendation Model",
        "Crop recommendation estimates a suitable crop using soil nutrient and environmental variables.",
        "Classification", ui.CROP_FEATURES, rec_pairs,
    ) + model_card(
        "Yield Prediction Model",
        "Yield prediction estimates expected agricultural yield using location, crop, season, year and cultivation area.",
        "Regression", ui.YIELD_FEATURES, yld_pairs,
    ) + "</div>"), unsafe_allow_html=True)
    st.markdown("<div style=\"height:.6rem\"></div>", unsafe_allow_html=True)
    st.caption("Metrics are read from the file stored alongside the trained models. They describe past model performance and do not imply causation.")


def page_about():
    render_header("About AgroSenseAI", "AI-powered crop recommendation and yield prediction with persistent prediction history.")
    render_section_title("Workflow")
    render_workflow()
    render_section_title("How each part works")
    render_grid([
        card_html("Crop Recommendation", "Uses classification to predict a crop label from soil and environmental inputs.", "feature"),
        card_html("Yield Prediction", "Uses regression to estimate numeric yield from agricultural and seasonal inputs.", "feature alt"),
        card_html("PostgreSQL", "Stores prediction history for later reference.", "feature alt2"),
    ])
    render_section_title("Built with")
    st.markdown(flat(f'<div class="card">{pills(["Streamlit", "FastAPI", "Scikit-learn", "Joblib", "PostgreSQL", "SQLAlchemy"])}'
                     f'<div class="note" style="margin-top:.4rem">{DISCLAIMER}</div></div>'), unsafe_allow_html=True)


{
    "Home": page_home,
    "Crop Recommendation": page_crop,
    "Yield Prediction": page_yield,
    "Prediction History": page_history,
    "Model Information": page_model_info,
    "About": page_about,
}[page]()

render_footer()
