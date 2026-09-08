# Agile and Scrum MLOps Demo

## Aim

Simulate an Agile Scrum lifecycle while building and evaluating an Iris flower classification model.

## Scrum Team

| Student | Role |
| --- | --- |
| Student 1 | Product Owner |
| Student 2 | Scrum Master |
| Student 3 | ML Engineer |
| Student 4 | Data Engineer |
| Student 5 | Tester |

If one student performs the experiment, that student assumes all five roles.

## Sprint 1

- **Duration:** 1 week
- **Goal:** Build the first working ML model
- **Tasks:** Download dataset, clean data, train model, evaluate accuracy, save model

The ceremony notes and Sprint Review/Retrospective checklist are in `docs/scrum_ceremonies.md`. The prioritized stories are in `Product_Backlog.md`.

## Run the model

From this directory:

```bash
python -m pip install -r requirements.txt
python src/iris_demo.py
```

Expected output includes an accuracy of at least `0.95` and a saved model path under `models/`.

## Run tests

```bash
pytest -q
```

## Project structure

```text
agilenscrum/
|- data/                         # Dataset inputs, if external data is added
|- docs/scrum_ceremonies.md      # Planning, Daily Scrum, Review, Retrospective
|- models/                       # Generated model artifacts
|- src/iris_demo.py              # Training and evaluation code
|- Product_Backlog.md
|- requirements.txt
`- test_iris_demo.py
```
