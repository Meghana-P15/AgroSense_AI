from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from .database import (
    database_status,
    fetch_predictions,
    get_db,
    init_db,
    save_prediction,
)
from .ml_service import model_options, model_status, predict_crop, predict_yield
from .schemas import CropRequest, YieldRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AgroSense AI API",
    version="1.0.0",
    description="FastAPI backend for crop recommendation, yield prediction and PostgreSQL history.",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "AgroSense AI backend is running.",
        "docs": "/docs",
        "health": "/health",
        "history": "/history",
    }


@app.get("/health")
def health():
    models = model_status()
    db_ok = database_status()
    return {
        "status": "ok" if all(models.values()) and db_ok else "dependency_error",
        "models": models,
        "postgresql": db_ok,
    }


@app.get("/options")
def options():
    return model_options()


@app.post("/predict/crop")
def crop_prediction(request: CropRequest, db: Session = Depends(get_db)):
    try:
        input_data = request.model_dump()
        result = predict_crop(input_data)
        row = save_prediction(db, "crop_recommendation", input_data, result)
        return {
            "recommended_crop": result["recommended_crop"],
            "confidence": result["confidence"],
            "prediction_id": row.id,
        }
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Crop prediction failed: {exc}") from exc


@app.post("/predict/yield")
def yield_prediction(request: YieldRequest, db: Session = Depends(get_db)):
    try:
        model_input = {
            "State": request.state.strip(),
            "District": request.district.strip(),
            "Crop": request.crop.strip(),
            "Crop_Year": request.crop_year,
            "Season": request.season.strip(),
            "Area": request.area,
        }
        result = predict_yield(model_input)
        row = save_prediction(db, "crop_yield", request.model_dump(), result)
        return {
            "predicted_yield": result["predicted_yield"],
            "prediction_id": row.id,
        }
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Yield prediction failed: {exc}") from exc


@app.get("/history")
def history(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    rows = fetch_predictions(db, limit=limit)
    return {
        "predictions": [
            {
                "id": row.id,
                "model_type": row.model_type,
                "input": row.input_data,
                "output": row.output_data,
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
            for row in rows
        ]
    }
