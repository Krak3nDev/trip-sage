import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from openai import OpenAIError
from starlette.requests import Request

from trip_sage.openai import InvalidLLMResponse

logger = logging.getLogger(__name__)


async def openai_error_handler(
    request: Request, exception: OpenAIError
) -> ORJSONResponse:
    if "rate_limit" in str(exception).lower():
        return ORJSONResponse(
            status_code=429,
            content={
                "detail": "OpenAI API rate limit exceeded. Please try again later.",
                "error_type": "rate_limit_error",
            },
        )

    if (
        "authentication" in str(exception).lower()
        or "unauthorized" in str(exception).lower()
    ):
        return ORJSONResponse(
            status_code=502,
            content={
                "detail": "External API authentication failed. Please contact support.",
                "error_type": "api_auth_error",
            },
        )

    return ORJSONResponse(
        status_code=502,
        content={
            "detail": "External AI service is temporarily unavailable. Please try again later.",
            "error_type": "external_api_error",
        },
    )


async def invalid_llm_response_handler(
    request: Request, exception: InvalidLLMResponse
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=502,
        content={
            "detail": "AI service returned invalid response. Please try again.",
            "error_type": "invalid_ai_response",
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(OpenAIError, openai_error_handler)
    app.add_exception_handler(InvalidLLMResponse, invalid_llm_response_handler)
