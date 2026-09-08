"""Train and evaluate the Iris Decision Tree model."""

from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "iris_decision_tree.joblib"


def train_model(random_state: int = 42) -> tuple[DecisionTreeClassifier, float]:
    """Train the classifier and return it with its holdout accuracy."""
    iris = load_iris()
    features_train, features_test, labels_train, labels_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.2,
        random_state=random_state,
    )

    model = DecisionTreeClassifier(random_state=random_state)
    model.fit(features_train, labels_train)
    predictions = model.predict(features_test)
    accuracy = accuracy_score(labels_test, predictions)
    return model, accuracy


def save_model(model: DecisionTreeClassifier, output_path: Path = MODEL_PATH) -> Path:
    """Persist a trained model and return the destination path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return output_path


def main() -> None:
    model, accuracy = train_model()
    model_path = save_model(model)
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    main()
