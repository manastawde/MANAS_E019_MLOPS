"""ETL, feature-store, and MLflow tracking demo for the Iris dataset."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_STORE_PATH = PROJECT_ROOT / "feature_store" / "iris_features.csv"
MLRUNS_PATH = PROJECT_ROOT / "mlruns"
EXPERIMENT_NAME = "ETL_FeatureStore_Experiment"


def extract_data() -> pd.DataFrame:
    """Extract the Iris dataset into a DataFrame."""
    return load_iris(as_frame=True).frame


def transform_data(raw_data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Validate, clean, and engineer the model features."""
    if raw_data.empty or raw_data.isna().any().any():
        raise ValueError("The raw dataset must be non-empty and contain no missing values")

    features = raw_data.drop(columns=["target"]).copy()
    labels = raw_data["target"].copy()
    features["petal_ratio"] = (
        features["petal length (cm)"] / features["sepal length (cm)"]
    )
    return features, labels


def load_features(features: pd.DataFrame, labels: pd.Series, path: Path = FEATURE_STORE_PATH) -> Path:
    """Load reusable features and labels into the local feature store."""
    path.parent.mkdir(parents=True, exist_ok=True)
    stored_features = features.copy()
    stored_features["target"] = labels
    stored_features.to_csv(path, index=False)
    return path


def run_experiments(
    features: pd.DataFrame,
    labels: pd.Series,
    tracking_uri: str | None = None,
) -> list[dict[str, Any]]:
    """Train, evaluate, and track two models; return comparable run summaries."""
    if tracking_uri is None:
        tracking_uri = MLRUNS_PATH.as_uri()
    # MLflow 3 requires an explicit opt-in for its local tutorial-style store.
    os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)

    features_train, features_test, labels_train, labels_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )
    candidates = [
        (
            "LogisticRegression",
            LogisticRegression(max_iter=300),
            {"model": "LogisticRegression", "max_iter": 300},
        ),
        (
            "RandomForest",
            RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
            {"model": "RandomForest", "n_estimators": 100, "max_depth": 5},
        ),
    ]

    results: list[dict[str, Any]] = []
    for run_name, model, parameters in candidates:
        with mlflow.start_run(run_name=run_name) as run:
            model.fit(features_train, labels_train)
            predictions = model.predict(features_test)
            accuracy = accuracy_score(labels_test, predictions)
            mlflow.log_params(parameters)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.sklearn.log_model(model, artifact_path="model")
            results.append(
                {"run_id": run.info.run_id, "model": run_name, "accuracy": accuracy}
            )
    return results


def run_pipeline() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Execute ETL and tracked experiments, returning runs and the best run."""
    raw_data = extract_data()
    features, labels = transform_data(raw_data)
    feature_path = load_features(features, labels)
    results = run_experiments(features, labels)
    best_run = max(results, key=lambda result: result["accuracy"])
    print(f"Features stored at: {feature_path}")
    for result in results:
        print(f"{result['model']} Accuracy: {result['accuracy']:.4f}")
    print(f"Best model: {best_run['model']} ({best_run['accuracy']:.4f})")
    return results, best_run


if __name__ == "__main__":
    run_pipeline()
