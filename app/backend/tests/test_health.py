from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Legacy Retail Operations System" in data["service"]


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "legacyops_http_requests_total" in response.text
