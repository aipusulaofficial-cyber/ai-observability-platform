from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis import strategies as st

from service import app

client = TestClient(app)


def test_contract():
    assert client.get("/health/live").status_code == 200


@given(
    st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=1,
        max_size=32,
    ).filter(lambda value: bool(value.strip()))
)
def test_property(value: str):
    response = client.post(
        "/v1/observability",
        json={
            "key": value,
            "payload": {"latency_ms": 1, "tokens": 1, "cost": 0},
        },
    )
    assert response.status_code == 200, response.text
