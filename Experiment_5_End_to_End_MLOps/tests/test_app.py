from fastapi.testclient import TestClient
from app.main import app, model

c = TestClient(app)


def test_model_accuracy():
    from sklearn.datasets import load_iris
    X, y = load_iris(return_X_y=True)
    assert model.score(X, y) > 0.9


def test_health():
    assert c.get("/health").json() == {"status": "ok"}


def test_predict_setosa():
    r = c.post("/predict", json={"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2})
    assert r.status_code == 200 and r.json()["species"] == "setosa"


def test_predict_validation():
    assert c.post("/predict", json={"sepal_length": -1, "sepal_width": 3, "petal_length": 1, "petal_width": 1}).status_code == 422


def test_metrics_exposed():
    c.get("/health")
    body = c.get("/metrics/").text
    assert "iris_predictions_total" in body and "http_requests_total" in body
