from fastapi.testclient import TestClient

from kafka_events.server.main import app

client = TestClient(app)
