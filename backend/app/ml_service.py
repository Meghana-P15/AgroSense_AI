from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

MODEL_DIR = Path(__file__).resolve().parents[2] / "models"


@lru_cache(maxsize=2)
def _load_model(filename: str):
    path = MODEL_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")
    return joblib.load(path)


def model_status() -> dict[str, bool]:
    return {
        "crop_recommendation": (MODEL_DIR / "crop_recommendation.joblib").exists(),
        "crop_yield": (MODEL_DIR / "crop_yield.joblib").exists(),
    }


def predict_crop(payload: dict) -> dict:
    bundle = _load_model("crop_recommendation.joblib")
    features = bundle["features"]
    frame = pd.DataFrame([{feature: payload[feature] for feature in features}])

    probabilities = bundle["model"].predict_proba(frame)[0]
    classes = bundle["model"].classes_
    ranked = probabilities.argsort()[::-1]

    top_predictions = [
        {
            "crop": str(classes[index]),
            "probability": round(float(probabilities[index]), 6),
        }
        for index in ranked[:3]
    ]

    return {
        "recommended_crop": top_predictions[0]["crop"],
        "confidence": top_predictions[0]["probability"],
        "alternatives": top_predictions,
        "model_version": bundle.get("version", "unknown"),
    }


def predict_yield(payload: dict) -> dict:
    bundle = _load_model("crop_yield.joblib")
    features = bundle["features"]
    frame = pd.DataFrame([payload], columns=features)
    prediction = max(0.0, float(bundle["model"].predict(frame)[0]))

    return {
        "predicted_yield": round(prediction, 4),
        "unit": "dataset Yield units",
        "model_version": bundle.get("version", "unknown"),
    }


def model_options() -> dict:
    """Return safe UI choices learned by the fitted yield model."""
    bundle = _load_model("crop_yield.joblib")
    supported = dict(bundle.get("supported_values", {}))

    districts: list[str] = []
    try:
        preprocess = bundle["model"].named_steps["preprocess"]
        onehot = preprocess.named_transformers_["cat"].named_steps["onehot"]
        # Categorical transformer order: State, District, Crop, Season
        districts = [str(value) for value in onehot.categories_[1]]
    except Exception:
        districts = []

    return {
        "states": [str(v) for v in supported.get("states", [])],
        "districts": districts,
        "crops": [str(v) for v in supported.get("crops", [])],
        "seasons": [str(v) for v in supported.get("seasons", [])],
    }
