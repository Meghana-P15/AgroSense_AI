from pydantic import BaseModel, Field


class CropRequest(BaseModel):
    N: float = Field(ge=0, le=300, description="Nitrogen content")
    P: float = Field(ge=0, le=300, description="Phosphorus content")
    K: float = Field(ge=0, le=300, description="Potassium content")
    temperature: float = Field(ge=-20, le=70)
    humidity: float = Field(ge=0, le=100)
    ph: float = Field(ge=0, le=14)
    rainfall: float = Field(ge=0, le=5000)


class YieldRequest(BaseModel):
    state: str = Field(min_length=2, max_length=100)
    district: str = Field(min_length=1, max_length=100)
    crop: str = Field(min_length=1, max_length=100)
    crop_year: int = Field(ge=1990, le=2100)
    season: str = Field(min_length=1, max_length=50)
    area: float = Field(gt=0, le=1_000_000_000)
