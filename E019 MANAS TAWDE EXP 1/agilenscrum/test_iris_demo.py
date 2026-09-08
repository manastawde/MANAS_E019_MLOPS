from pathlib import Path

from src.iris_demo import save_model, train_model


def test_train_model_reaches_sprint_target():
    _, accuracy = train_model()

    assert accuracy >= 0.95


def test_save_model_creates_artifact(tmp_path: Path):
    model, _ = train_model()
    output_path = tmp_path / "iris_model.joblib"

    saved_path = save_model(model, output_path)

    assert saved_path == output_path
    assert output_path.exists()
