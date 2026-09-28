import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AgroSense AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container {max-width: 1000px; padding-top: 2rem; padding-bottom: 3rem;}
        [data-testid="stSidebar"] {background: #f7faf7;}
        .agro-title {font-size: 2.15rem; font-weight: 750; color: #12324a; margin-bottom: 0.15rem;}
        .agro-subtitle {color: #667085; margin-bottom: 1.4rem;}
        .simple-card {
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.1rem;
            background: white;
            min-height: 130px;
        }
        .result-box {
            border: 1px solid #dcebdd;
            border-radius: 12px;
            padding: 1.2rem;
            background: #f7fbf7;
            margin-top: 1rem;
        }
        .result-label {color: #667085; font-size: 0.9rem; margin-bottom: 0.2rem;}
        .result-value {color: #176b3a; font-size: 2rem; font-weight: 750;}
        .small-note {color: #667085; font-size: 0.9rem;}
        div.stButton > button, div.stFormSubmitButton > button {
            border-radius: 9px;
            font-weight: 650;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def api_get(path: str, params=None):
    response = requests.get(f"{API_URL}{path}", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload: dict):
    response = requests.post(f"{API_URL}{path}", json=payload, timeout=20)
    response.raise_for_status()
    return response.json()


def show_header(title: str, subtitle: str):
    st.markdown(f'<div class="agro-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="agro-subtitle">{subtitle}</div>', unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "Home"

pages = ["Home", "Prediction", "History", "About"]

with st.sidebar:
    st.markdown("## 🌱 AgroSense AI")
    st.caption("Smart Farming, Better Tomorrow")
    st.divider()
    selected = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = selected

page = st.session_state.page

if page == "Home":
    show_header("Welcome to AgroSense AI", "A simple crop recommendation and yield prediction system.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="simple-card">
                <h3>🌿 Crop Recommendation</h3>
                <p>Uses soil and environmental inputs to recommend a suitable crop.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="simple-card">
                <h3>📈 Yield Prediction</h3>
                <p>Uses agricultural and seasonal inputs to estimate crop yield.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("Get Started", use_container_width=True):
        st.session_state.page = "Prediction"
        st.rerun()

elif page == "Prediction":
    show_header("Prediction", "Choose one of the two AgroSense AI modules.")

    crop_tab, yield_tab = st.tabs(["🌿 Crop Recommendation", "📈 Yield Prediction"])

    with crop_tab:
        st.caption("Enter the soil and environmental conditions.")
        with st.form("crop_form"):
            c1, c2 = st.columns(2)
            with c1:
                temperature = st.number_input("Temperature (°C)", min_value=-20.0, max_value=70.0, value=26.5, step=0.1)
                humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=65.0, step=0.1)
                ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
                rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=5000.0, value=120.0, step=1.0)
            with c2:
                nitrogen = st.number_input("Nitrogen (N)", min_value=0.0, max_value=300.0, value=45.0, step=1.0)
                phosphorus = st.number_input("Phosphorus (P)", min_value=0.0, max_value=300.0, value=32.0, step=1.0)
                potassium = st.number_input("Potassium (K)", min_value=0.0, max_value=300.0, value=38.0, step=1.0)

            crop_submit = st.form_submit_button("Recommend Crop", use_container_width=True)

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
            try:
                with st.spinner("Generating recommendation..."):
                    result = api_post("/predict/crop", payload)
                confidence = float(result.get("confidence", 0)) * 100
                st.markdown(
                    f"""
                    <div class="result-box">
                        <div class="result-label">Recommended Crop</div>
                        <div class="result-value">{str(result['recommended_crop']).title()}</div>
                        <div class="small-note">Confidence: {confidence:.1f}%</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except requests.RequestException as exc:
                st.error(f"Could not get a prediction. Make sure the FastAPI backend is running.\n\n{exc}")

    with yield_tab:
        st.caption("Enter the agricultural and seasonal details.")
        try:
            options = api_get("/options")
        except requests.RequestException:
            options = {"states": [], "districts": [], "crops": [], "seasons": []}

        states = options.get("states") or [""]
        districts = options.get("districts") or [""]
        crops = options.get("crops") or [""]
        seasons = options.get("seasons") or [""]

        with st.form("yield_form"):
            c1, c2 = st.columns(2)
            with c1:
                state = st.selectbox("State", states)
                district = st.selectbox("District", districts)
                crop = st.selectbox("Crop", crops)
            with c2:
                crop_year = st.number_input("Crop Year", min_value=1990, max_value=2100, value=2024, step=1)
                season = st.selectbox("Season", seasons)
                area = st.number_input("Area (hectares)", min_value=0.01, value=1.0, step=0.1)

            yield_submit = st.form_submit_button("Predict Yield", use_container_width=True)

        if yield_submit:
            if not all([state, district, crop, season]):
                st.warning("Start the FastAPI backend first so the available values can be loaded.")
            else:
                payload = {
                    "state": state,
                    "district": district,
                    "crop": crop,
                    "crop_year": int(crop_year),
                    "season": season,
                    "area": float(area),
                }
                try:
                    with st.spinner("Generating yield prediction..."):
                        result = api_post("/predict/yield", payload)
                    st.markdown(
                        f"""
                        <div class="result-box">
                            <div class="result-label">Predicted Yield</div>
                            <div class="result-value">{result['predicted_yield']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                except requests.RequestException as exc:
                    st.error(f"Could not get a prediction. Make sure the FastAPI backend is running.\n\n{exc}")

elif page == "History":
    show_header("Prediction History", "Recent prediction records stored in PostgreSQL.")

    try:
        data = api_get("/history", params={"limit": 25})
        rows = data.get("predictions", [])
        if not rows:
            st.info("No predictions have been saved yet.")
        else:
            table_rows = []
            for row in rows:
                output = row.get("output", {}) or {}
                created = row.get("created_at")
                if created:
                    try:
                        created = datetime.fromisoformat(created.replace("Z", "+00:00")).strftime("%d %b %Y, %H:%M")
                    except ValueError:
                        pass

                if row.get("model_type") == "crop_recommendation":
                    kind = "Crop Recommendation"
                    prediction = output.get("recommended_crop", "-")
                else:
                    kind = "Yield Prediction"
                    prediction = output.get("predicted_yield", "-")

                table_rows.append(
                    {
                        "ID": row.get("id"),
                        "Type": kind,
                        "Prediction": prediction,
                        "Created": created,
                    }
                )

            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
    except requests.RequestException as exc:
        st.error(f"Could not load history. Make sure the FastAPI backend is running.\n\n{exc}")

elif page == "About":
    show_header("About AgroSense AI", "The project uses a simple connected workflow.")
    st.markdown(
        """
        `Streamlit → FastAPI → Machine Learning Model → PostgreSQL`

        **Crop Recommendation** uses classification to predict a crop label from soil and environmental inputs.

        **Yield Prediction** uses regression to estimate numeric yield from agricultural and seasonal inputs.

        **PostgreSQL** stores prediction history for later reference.
        """
    )
