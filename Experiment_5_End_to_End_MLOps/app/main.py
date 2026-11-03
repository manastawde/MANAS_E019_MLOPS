import time
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, make_asgi_app
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()
model = RandomForestClassifier(n_estimators=50, random_state=42).fit(iris.data, iris.target)

app = FastAPI(title="Iris Classifier")
app.mount("/metrics", make_asgi_app())

PREDICTIONS = Counter("iris_predictions_total", "Predictions served", ["species"])
HTTP_REQS = Counter("http_requests_total", "HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["path"])


class Flower(BaseModel):
    sepal_length: float = Field(gt=0, lt=20)
    sepal_width: float = Field(gt=0, lt=20)
    petal_length: float = Field(gt=0, lt=20)
    petal_width: float = Field(gt=0, lt=20)


@app.middleware("http")
async def observe(request: Request, call_next):
    path, start = request.url.path, time.perf_counter()
    status = 500
    try:
        resp = await call_next(request)
        status = resp.status_code
        return resp
    finally:
        if not path.startswith("/metrics"):
            HTTP_REQS.labels(request.method, path, status).inc()
            LATENCY.labels(path).observe(time.perf_counter() - start)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(f: Flower):
    species = iris.target_names[model.predict([[f.sepal_length, f.sepal_width, f.petal_length, f.petal_width]])[0]]
    PREDICTIONS.labels(species).inc()
    return {"species": str(species)}


@app.get("/boom")
def boom():  # deliberate 500 so the error panel/alert can be demonstrated
    raise HTTPException(status_code=500, detail="simulated failure")
