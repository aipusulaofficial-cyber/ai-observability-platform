from observability import PrincipalObservabilityMiddleware
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from pydantic import BaseModel, Field

from observability import configure_observability, get_logger, PrincipalObservabilityMiddleware
from observability_domain import SpanMetric, aggregate

configure_observability()
logger = get_logger(__name__)

app = FastAPI(title="ai-observability-platform", version="1.0.0")
app.add_middleware(PrincipalObservabilityMiddleware)
tracer = trace.get_tracer("ai-observability-platform")


class Request(BaseModel):
    key: str
    payload: dict = Field(default_factory=dict)


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/v1/observability")
def handle(request: Request) -> dict[str, float | int]:
    with tracer.start_as_current_span("ai-observability-platform.aggregate"):
        try:
            metric = SpanMetric(
                service=request.key,
                latency_ms=float(request.payload.get("latency_ms", 0)),
                error=bool(request.payload.get("error", False)),
                tokens=int(request.payload.get("tokens", 0)),
                cost=float(request.payload.get("cost", 0)),
            )
            result = aggregate([metric])
            logger.info(
                "observability_aggregate service=%s count=%d",
                request.key,
                result["count"],
            )
            return result
        except (ValueError, KeyError, TypeError) as exc:
            logger.warning(
                "observability_request_rejected service=%s reason=%s",
                request.key,
                exc,
            )
            raise HTTPException(status_code=400, detail=str(exc)) from exc
