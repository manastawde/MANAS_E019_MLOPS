from pathlib import Path

import pandas as pd

from src.etl_mlflow import extract_data, load_features, run_experiments, transform_data


def test_transform_engineers_reusable_feature():
    features, labels = transform_data(extract_data())

    assert "petal_ratio" in features.columns
    assert len(features) == len(labels) == 150
    assert not features.isna().any().any()


def test_load_features_writes_target_column(tmp_path: Path):
    features, labels = transform_data(extract_data())
    output_path = load_features(features, labels, tmp_path / "iris_features.csv")
    stored = pd.read_csv(output_path)

    assert output_path.exists()
    assert "target" in stored.columns
    assert stored.shape == (150, 6)


def test_experiments_track_two_models(tmp_path: Path):
    features, labels = transform_data(extract_data())
    results = run_experiments(features, labels, tracking_uri=tmp_path.as_uri())

    assert {result["model"] for result in results} == {
        "LogisticRegression",
        "RandomForest",
    }
    assert all(result["accuracy"] >= 0.90 for result in results)
