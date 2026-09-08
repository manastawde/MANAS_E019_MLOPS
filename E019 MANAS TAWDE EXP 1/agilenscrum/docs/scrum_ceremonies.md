# Scrum Ceremonies

## Sprint Planning

**Sprint goal:** Build the first working ML model.

| Task | Estimate |
| --- | --- |
| Download dataset | 20 min |
| Data cleaning | 30 min |
| Train model | 30 min |
| Test and evaluate accuracy | 20 min |
| Save model and document result | 20 min |

## Daily Scrum

| Role | Yesterday | Today | Blocker |
| --- | --- | --- | --- |
| Product Owner | Requirements finalized | Review Sprint progress | None |
| Scrum Master | Sprint planned | Conduct Daily Scrum | Git installation issue |
| ML Engineer | Selected Decision Tree | Train model | Dataset unavailable |
| Data Engineer | Downloaded Iris dataset | Split dataset | Missing library |
| Tester | Prepared test cases | Evaluate accuracy | None |

## Sprint Review

- [x] Dataset available through scikit-learn
- [x] Data prepared and split
- [x] Decision Tree model trained
- [x] Accuracy generated
- [x] Model artifact saved

**Discussion:** The Sprint Goal was achieved. The increment includes working Python source code, a trained model artifact, automated tests, and this documentation.

## Sprint Retrospective

| Question | Result |
| --- | --- |
| What went well? | The team used a small, testable increment and shared a clear Sprint Goal. |
| What problems occurred? | Missing Python packages and possible dataset access issues can block the Sprint. |
| What should improve? | Install dependencies and verify the environment before Sprint Planning begins. |
