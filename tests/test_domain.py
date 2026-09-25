import pytest

from observability_domain import SpanMetric, aggregate


def test_aggregate():
    result = aggregate(
        [
            SpanMetric("a", 10, False, 100, 0.2),
            SpanMetric("a", 20, True, 50, 0.1),
        ]
    )
    assert result["error_rate"] == 0.5
    assert result["p50_latency_ms"] == 15
    assert result["tokens"] == 150
    assert result["cost"] == 0.3


def test_empty_aggregate():
    assert aggregate([])["count"] == 0


@pytest.mark.parametrize(
    "metric",
    [
        SpanMetric("a", -1, False),
        SpanMetric("a", 1, False, -1),
        SpanMetric("a", 1, False, 0, -0.1),
    ],
)
def test_metrics_reject_negative_values(metric):
    with pytest.raises(ValueError):
        aggregate([metric])
