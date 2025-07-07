from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from starlette import status

from trip_sage.openai import RecommendationRequest
from trip_sage.schemas import HistoryResponse, RecommendationResponse
from trip_sage.services.recommendation import RecommendationService

recommendations_router = APIRouter(
    prefix="/api/v1", tags=["recommendations"], route_class=DishkaRoute
)


@recommendations_router.post(
    "",
    response_model=RecommendationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_recommendation(
    payload: RecommendationRequest, service: FromDishka[RecommendationService]
):
    return await service.recommend(payload)


@recommendations_router.get("/history", response_model=HistoryResponse)
async def get_recommendations_history(
    service: FromDishka[RecommendationService],
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
        description="Maximum number of records to return",
    ),
    offset: int = Query(
        default=0, ge=0, description="Number of records to skip"
    ),
):
    return await service.get_history(limit=limit, offset=offset)
