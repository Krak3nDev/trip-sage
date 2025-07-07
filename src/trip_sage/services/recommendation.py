from sqlalchemy.ext.asyncio import AsyncSession

from trip_sage.openai import (
    OpenAIAdapter,
    RecommendationRequest,
)
from trip_sage.persistence.models import Recommendation
from trip_sage.persistence.repositories import RecommendationRepository
from trip_sage.schemas import (
    HistoryRecommendationItem,
    HistoryResponse,
    PlaceSchema,
    RecommendationResponse,
)


class RecommendationService:
    def __init__(
        self,
        session: AsyncSession,
        recommendation_repo: RecommendationRepository,
        openai_adapter: OpenAIAdapter,
    ) -> None:
        self._session = session
        self._recommendation_repo = recommendation_repo
        self._ai = openai_adapter

    async def recommend(
        self, payload: RecommendationRequest
    ) -> RecommendationResponse:
        places = await self._ai.generate(payload)
        places_dict = [place.model_dump() for place in places]

        recommendation = Recommendation(
            text=payload.text,
            num_places=payload.num_places or 4,
            exclude=payload.exclude,
            response_json={"places": places_dict},
        )

        self._recommendation_repo.add(recommendation)
        await self._session.commit()
        await self._session.refresh(recommendation)

        return RecommendationResponse(
            id=recommendation.id,
            places=places,
            created_at=recommendation.created_at,
        )

    async def get_history(
        self, limit: int = 50, offset: int = 0
    ) -> HistoryResponse:
        recommendations = await self._recommendation_repo.get_all(
            limit=limit, offset=offset
        )

        total = await self._recommendation_repo.get_total_count()

        history_items = []

        for rec in recommendations:
            places_data = rec.response_json.get("places", [])

            places = [
                PlaceSchema.model_validate(place_data)
                for place_data in places_data
            ]

            history_item = HistoryRecommendationItem(
                id=rec.id,
                text=rec.text,
                exclude=rec.exclude,
                num_places=rec.num_places,
                places=places,
                created_at=rec.created_at,
            )
            history_items.append(history_item)

        return HistoryResponse(recommendations=history_items, total=total)
