import math
from dataclasses import dataclass


@dataclass(frozen=True)
class SpanMetric:
    service: str
    latency_ms: float
    error: bool
    tokens: int = 0
    cost: float = 0.0

    def __post_init__(self) -> None:
        if not self.service.strip():
            raise ValueError("service is required")
        if (
            not math.isfinite(self.latency_ms)
            or not math.isfinite(self.cost)
            or self.latency_ms < 0
            or self.tokens < 0
            or self.cost < 0
        ):
            raise ValueError("metrics must be finite and non-negative")


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    if not 0 <= percentile <= 1:
        raise ValueError("percentile must be between 0 and 1")
    position = (len(values) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)
    weight = position - lower
    return values[lower] + (values[upper] - values[lower]) * weight


def aggregate(spans: list[SpanMetric]) -> dict[str, float | int]:
    if not spans:
        return {
            "count": 0,
            "error_rate": 0.0,
            "p50_latency_ms": 0.0,
            "tokens": 0,
            "cost": 0.0,
        }

    latencies = sorted(span.latency_ms for span in spans)
    return {
        "count": len(spans),
        "error_rate": sum(span.error for span in spans) / len(spans),
        "p50_latency_ms": _percentile(latencies, 0.5),
        "tokens": sum(span.tokens for span in spans),
        "cost": round(sum(span.cost for span in spans), 6),
    }
