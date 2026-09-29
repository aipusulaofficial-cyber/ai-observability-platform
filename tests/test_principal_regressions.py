import pytest

from observability_domain import SpanMetric, aggregate


def test_tail_latency_is_reported():
    spans = [SpanMetric("api", float(latency), False) for latency in range(1, 101)]
    result = aggregate(spans)
    assert result["p50_latency_ms"] == pytest.approx(50.5)
    assert result["p95_latency_ms"] == pytest.approx(95.05)
    assert result["p99_latency_ms"] == pytest.approx(99.01)


def test_empty_aggregate_exposes_stable_tail_latency_keys():
    result = aggregate([])
    assert result["p95_latency_ms"] == 0.0
    assert result["p99_latency_ms"] == 0.0
