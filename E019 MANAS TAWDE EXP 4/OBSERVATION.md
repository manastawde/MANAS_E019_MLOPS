# Observation Table

Run the program to populate the accuracy values and compare the MLflow runs.

| Run | Model | Key parameters | Accuracy | Remarks |
| --- | --- | --- | --- | --- |
| 1 | Logistic Regression | `max_iter=300` | Printed by program | Compare in MLflow |
| 2 | Random Forest | `n_estimators=100`, `max_depth=5` | Printed by program | Compare in MLflow |

## Viva points

- ETL means Extract, Transform, and Load; it makes data preparation repeatable.
- A feature store makes the same engineered features reusable for training and inference.
- An MLflow experiment groups related runs, while each run records one training execution.
- Parameters, metrics, and artifacts make experiments comparable and reproducible.
