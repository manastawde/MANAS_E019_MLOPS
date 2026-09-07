# EXP 3: Continuous Integration with GitHub Actions

**Student:** E019 Manas Tawde

## Aim

To demonstrate Continuous Integration (CI) by automatically installing dependencies and testing a Python application whenever code is pushed to GitHub.

## Objectives

- Understand Continuous Integration and GitHub Actions.
- Create a Python application with automated unit tests.
- Configure workflow triggers for pushes and pull requests to `main`.
- Observe successful and failed CI pipeline runs.

## Project Structure

```text
E019 MANAS TAWDE EXP 3/
|- app.py
|- test_app.py
|- requirements.txt
|- README.md
`- .github/workflows/ci.yml
```

## Run Locally

```bash
python -m pip install -r requirements.txt
pytest -v
python app.py
```

The test suite contains five tests for addition, subtraction, multiplication, division, and division by zero.

## GitHub Actions Workflow

The workflow in `.github/workflows/ci.yml` runs on:

- Pushes to the `main` branch.
- Pull requests targeting the `main` branch.

It checks out the repository, sets up Python 3.11, installs `pytest`, and runs the tests. A green check indicates that the CI job passed.

## CI Demonstration

1. Push the project to a GitHub repository.
2. Open the repository's **Actions** tab and select **Python CI**.
3. Temporarily change `add(a, b)` to return `a + b + 1`.
4. Commit and push the change to observe a failed test.
5. Restore `return a + b`, commit, and push again to observe a successful run.

## Result

Continuous Integration was demonstrated successfully using a Python application, automated tests, and a GitHub Actions workflow.