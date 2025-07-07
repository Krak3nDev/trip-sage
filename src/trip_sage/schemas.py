from datetime import datetime

from pydantic import BaseModel, Field


class Coords(BaseModel):
    lat: float = Field(..., description="Latitude in decimal degrees.")
    lng: float = Field(..., description="Longitude in decimal degrees.")


class PlaceSchema(BaseModel):
    name: str = Field(..., description="Human‑readable name of the location.")
    description: str = Field(
        ..., description="Short description of why the place is interesting."
    )
    coords: Coords


class RecommendationRequest(BaseModel):
    text: str = Field(..., example="Хочу в Рим, люблю історію та макарони")
    exclude: list[str] | None = Field(
        default=None, description="Список назв місць, які треба виключити"
    )
    num_places: int | None = Field(
        default=4,
        ge=1,
        le=20,
        description="Кількість локацій у відповіді (1–20)",
    )


class RecommendationResponse(BaseModel):
    id: int
    places: list[PlaceSchema]
    created_at: datetime


class HistoryRecommendationItem(BaseModel):
    id: int
    text: str
    exclude: list[str] | None
    num_places: int
    places: list[PlaceSchema]
    created_at: datetime


class HistoryResponse(BaseModel):
    recommendations: list[HistoryRecommendationItem]
    total: int
