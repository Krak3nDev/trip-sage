from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from trip_sage.persistence.models import Recommendation


class RecommendationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, recommendation: Recommendation) -> None:
        self._session.add(recommendation)

    async def get_all(
        self, limit: int = 50, offset: int = 0
    ) -> Sequence[Recommendation]:
        stmt = (
            select(Recommendation)
            .order_by(Recommendation.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_total_count(self) -> int:
        stmt = select(func.count(Recommendation.id))
        result = await self._session.execute(stmt)
        return result.scalar()
