# EXP 4: ETL, Feature Store, and MLflow Tracking

**Student:** E019 Manas Tawde

## Aim

Explore an ETL data pipeline, create reusable engineered features through a simple feature store, and compare machine-learning experiments using MLflow.

## Workflow

1. **Extract:** Load the Iris dataset with pandas-compatible scikit-learn output.
2. **Transform:** Validate the data and engineer `petal_ratio`.
3. **Load:** Save the prepared feature matrix to `feature_store/iris_features.csv`.
4. **Experiment:** Train Logistic Regression and Random Forest models on the same features.
5. **Track:** Log parameters, accuracy, and model artifacts to MLflow.
6. **Compare:** Print the best-performing run by accuracy.

## Setup and run

From this directory:

```powershell
python -m pip install -r requirements.txt
python src/etl_mlflow.py
```

The script creates the feature-store CSV and the local `mlruns/` tracking directory. Start the MLflow UI with:

```powershell
mlflow ui --backend-store-uri .\mlruns
```

Then open `http://127.0.0.1:5000` and select `ETL_FeatureStore_Experiment` to compare the two runs.

## Tests

```powershell
pytest -q
```

## Structure

```text
E019 MANAS TAWDE EXP 4/
|- data/                       # Raw-data location
|- feature_store/              # Reusable engineered features
|- artifacts/                  # Optional exported artifacts
|- src/etl_mlflow.py           # ETL and MLflow implementation
|- test_etl_mlflow.py          # Automated checks
|- requirements.txt
`- README.md
```

## Result

The pipeline extracts and transforms the Iris dataset, stores reusable features, tracks two model runs with MLflow, and identifies the best run by accuracy.
