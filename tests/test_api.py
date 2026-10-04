from fastapi.testclient import TestClient

from api.index import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_model_info():
    response = client.get("/api/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data.get("model_path") == "models/production/model-best"


def test_predict_contract():
    response = client.post(
        "/api/predict",
        json={"text": "Rumah Gadang berasal dari Sumatera Barat."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["model_loaded"] is True
    assert isinstance(data["entities"], list)
    for entity in data["entities"]:
        assert {"text", "label", "start", "end"}.issubset(entity)


def test_quiz_contract():
    response = client.post(
        "/api/quiz",
        json={"text": "Tari Saman berkembang dalam masyarakat Gayo di Aceh."},
    )
    assert response.status_code == 200
    assert isinstance(response.json()["questions"], list)
