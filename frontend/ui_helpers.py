"""Formatting and data-shaping helpers for the AgroSenseAI UI. No API or model logic lives here."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

METRICS_PATH = Path(__file__).resolve().parents[1] / "models" / "metrics.json"

# Feature names as defined by the backend request schemas (backend/app/schemas.py).
CROP_FEATURES = ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", "Temperature", "Humidity", "pH", "Rainfall"]
YIELD_FEATURES = ["State", "District", "Crop", "Crop Year", "Season", "Area"]

FIELD_LABELS = {
    "N": "Nitrogen (N)", "P": "Phosphorus (P)", "K": "Potassium (K)", "temperature": "Temperature (°C)",
    "humidity": "Humidity (%)", "ph": "pH level", "rainfall": "Rainfall (mm)", "state": "State",
    "district": "District", "crop": "Crop", "crop_year": "Crop year", "season": "Season",
    "area": "Area (hectares)", "recommended_crop": "Recommended crop", "confidence": "Confidence",
    "predicted_yield": "Predicted yield", "unit": "Unit", "model_version": "Model version",
}

PERIODS = {"All time": None, "Last 24 hours": timedelta(hours=24), "Last 7 days": timedelta(days=7),
           "Last 30 days": timedelta(days=30)}


def fmt_number(value, max_decimals: int = 4) -> str:
    """Thousands separators, up to `max_decimals` decimals (at least 2), no trailing noise."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    text = f"{number:,.{max_decimals}f}".rstrip("0")
    head, _, tail = text.partition(".")
    return f"{head}.{tail.ljust(2, '0')}"


def fmt_field(key: str, value) -> str:
    if key == "confidence":
        try:
            return f"{float(value) * 100:.1f}%"
        except (TypeError, ValueError):
            return str(value)
    if isinstance(value, bool) or value is None:
        return str(value)
    if isinstance(value, float):
        return fmt_number(value)
    return str(value)


def friendly_error(exc: Exception, what: str) -> tuple[str, str]:
    """Return (user message, short technical detail). Never a stack trace."""
    if isinstance(exc, requests.HTTPError):
        return f"The prediction service could not complete this request ({what}).", str(exc)
    return "Unable to reach the prediction service. Please make sure the backend is running.", str(exc)


def parse_created(raw):
    """Return (display string, aware datetime or None), matching the original display format."""
    if not raw:
        return raw, None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return raw, None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%d %b %Y, %H:%M"), dt


def build_entries(rows: list[dict]) -> list[dict]:
    entries = []
    for row in rows:
        output = row.get("output", {}) or {}
        inputs = row.get("input", {}) or {}
        created_str, created_dt = parse_created(row.get("created_at"))
        if row.get("model_type") == "crop_recommendation":
            kind, prediction, crop = "Crop Recommendation", output.get("recommended_crop", "-"), output.get("recommended_crop")
            prediction = str(prediction).title()
        else:
            kind, crop = "Yield Prediction", inputs.get("crop")
            raw = output.get("predicted_yield", "-")
            prediction = fmt_number(raw) if raw != "-" else raw
        conf = output.get("confidence")
        entries.append({
            "id": row.get("id"), "kind": kind, "prediction": prediction, "crop": str(crop).title() if crop else "-",
            "confidence": float(conf) * 100 if conf is not None else None,
            "created": created_str, "created_dt": created_dt, "input": inputs, "output": output,
        })
    return entries


def filter_entries(entries, kind="All", crop="All", period="All time"):
    window = PERIODS.get(period)
    cutoff = datetime.now(timezone.utc) - window if window else None
    out = []
    for e in entries:
        if kind != "All" and e["kind"] != kind:
            continue
        if crop != "All" and e["crop"] != crop:
            continue
        if cutoff and (e["created_dt"] is None or e["created_dt"] < cutoff):
            continue
        out.append(e)
    return out


def load_model_metrics():
    """Read metrics stored next to the trained models. Returns None when unavailable."""
    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
