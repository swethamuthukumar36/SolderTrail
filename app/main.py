import json
import time
from collections.abc import AsyncIterator
from typing import Annotated

import psycopg
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

from app.config import Settings, get_settings
from app.cost import log_call
from app.llm.errors import LLMConfigurationError, LLMUnavailable
from app.llm.factory import create_provider
from app.llm.reliable import AsyncReliableLLM
from app.llm.types import LLMRequest, Message, Usage
from app.schemas import ChatRequest
from app.usage import usage_by_day

app = FastAPI(title="Examate RAG starter", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_llm(settings: SettingsDep) -> AsyncReliableLLM:
    return create_provider(settings)


LLMDep = Annotated[AsyncReliableLLM, Depends(get_llm)]


@app.get("/hello")
def say_hello():
    return "hello"


@app.get("/")
def say_root():
    return "You are on root page"


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness check: does not call the LLM or database."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.get("/ready")
def ready(settings: SettingsDep):
    """Readiness check: verifies database connectivity."""
    if not settings.database_url:
        return {
            "status": "ok",
            "database": "not configured",
        }

    try:
        with psycopg.connect(
            settings.database_url,
            connect_timeout=3,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

        return {
            "status": "ok",
            "database": "ok",
        }

    except psycopg.Error:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "database": "unavailable",
            },
        )


@app.get("/usage")
def usage(settings: SettingsDep) -> dict:
    """Return daily calls, tokens and cost from the cost log."""
    return usage_by_day(settings.cost_log_path)


def sse(data: dict, event: str | None = None) -> str:
    prefix = f"event: {event}\n" if event else ""
    return f"{prefix}data: {json.dumps(data)}\n\n"


@app.post("/chat")
async def chat(
    request: ChatRequest,
    provider: LLMDep,
    settings: SettingsDep,
) -> StreamingResponse:
    llm_request = LLMRequest(
        messages=tuple(Message(role=message.role, content=message.content) for message in request.messages),
        model=request.model,
    )

    async def event_stream() -> AsyncIterator[str]:
        start_time = time.perf_counter()
        usage = None
        ok = False

        try:
            async for chunk in provider.stream(llm_request):
                if chunk.text:
                    yield sse({"delta": chunk.text})
                if chunk.usage is not None:
                    usage = chunk.usage
            ok = True

        except (LLMUnavailable, LLMConfigurationError) as error:
            yield sse({"error": str(error)}, event="error")

        finally:
            latency_ms = (time.perf_counter() - start_time) * 1000

            recorded_usage = usage or Usage(
                input_tokens=0,
                output_tokens=0,
                estimated=False,
            )

            fallback_used = provider.fallback_used
            provider_name = "openai_compat" if fallback_used else settings.llm_provider

            active_model = (
                settings.llm_fallback_model
                if fallback_used
                else getattr(provider.primary, "model", request.model)
            )

            record = log_call(
                settings.cost_log_path,
                provider=provider_name,
                model=active_model,
                usage=recorded_usage,
                latency_ms=latency_ms,
                price_in_per_m=settings.price_input_per_million,
                price_out_per_m=settings.price_output_per_million,
                ok=ok,
                fallback_used=fallback_used,
            )

            usage_data = {
                "input_tokens": recorded_usage.input_tokens,
                "output_tokens": recorded_usage.output_tokens,
                "estimated": recorded_usage.estimated,
            }

            yield sse(
                {
                    "usage": usage_data,
                    "cost_usd": record["cost_usd"],
                },
                event="done",
            )

    return StreamingResponse(event_stream(), media_type="text/event-stream")
