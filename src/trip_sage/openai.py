import json
import logging

from openai import AsyncOpenAI, OpenAIError
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from trip_sage.config import OpenAIAPIConfig
from trip_sage.schemas import PlaceSchema, RecommendationRequest


class InvalidLLMResponse(Exception):
    pass


class OpenAIAdapter:
    def __init__(self, openai_config: OpenAIAPIConfig):
        self._openai_config = openai_config
        self._client = AsyncOpenAI(api_key=openai_config.key)

    _SYSTEM_PROMPT = (
        "You are a helpful travel planner. "
        'Return ONLY a JSON object with a single key "places", '
        "whose value is an array of objects. Each object has exactly "
        '"name", "description", "coords" (coords is {"lat": float, "lng": float}). '
        "Return no other keys or text."
    )

    def _build_messages(self, req: RecommendationRequest) -> list[dict]:
        parts: list[str] = [req.text]
        if req.exclude:
            parts.append(f"Please do NOT include: {', '.join(req.exclude)}.")
        if req.num_places:
            parts.append(f"Return exactly {req.num_places} places.")
            
        return [
            {"role": "system", "content": self._SYSTEM_PROMPT},
            {"role": "user", "content": " ".join(parts)},
        ]

    async def generate(self, req: RecommendationRequest) -> list[PlaceSchema]:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self._openai_config.max_retries),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=(
                retry_if_exception_type(OpenAIError)
                | retry_if_exception_type(InvalidLLMResponse)
            ),
            reraise=True,
        ):
            with attempt:
                resp = await self._client.chat.completions.create(
                    model=self._openai_config.model,
                    temperature=0.2,
                    response_format={"type": "json_object"},
                    messages=self._build_messages(req),
                )

                raw = resp.choices[0].message.content.strip()

                try:
                    data = json.loads(raw)

                    places = data["places"]

                    if req.num_places and len(places) != req.num_places:
                        raise InvalidLLMResponse(
                            f"Expected {req.num_places} places, got {len(data)}"
                        )

                    places = [
                        PlaceSchema.model_validate(item) for item in places
                    ]
                    
                    return places

                except json.JSONDecodeError as exc:
                    raise InvalidLLMResponse(f"Malformed JSON: {exc}") from exc
