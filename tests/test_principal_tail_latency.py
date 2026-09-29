import pytest

from observability_domain import SpanMetric, aggregate


def test_aggregated_tail_latency_uses_sorted_samples():
    spans = [
        SpanMetric("svc", 100.0, False),
        SpanMetric("svc", 1.0, False),
        SpanMetric("svc", 10.0, False),
        SpanMetric("svc", 50.0, False),
    ]
    result = aggregate(spans)
    assert result["p50_latency_ms"] == pytest.approx(30.0)
    assert result["p95_latency_ms"] == pytest.approx(92.5)
    assert result["p99_latency_ms"] == pytest.approx(98.5)


def test_empty_aggregates_report_zero_tail_metrics():
    result = aggregate([])
    assert result["p95_latency_ms"] == 0.0
    assert result["p99_latency_ms"] == 0.0
