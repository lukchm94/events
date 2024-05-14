from fastapi import status

from kafka_events.__app_configs import Paths
from tests.conftest import client


def test_health() -> None:
    resp = client.get(Paths.health.value)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"status": "healthy"}
