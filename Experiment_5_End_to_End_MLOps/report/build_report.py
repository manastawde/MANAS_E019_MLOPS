"""Builds architecture.png, Exp5_Report.docx, Exp5_Presentation.pptx from ../evidence (real captures)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from docx import Document
from docx.shared import Inches, Pt
from pptx import Presentation
from pptx.util import Inches as PI, Pt as PP

os.chdir(os.path.dirname(os.path.abspath(__file__)))
EV = "../evidence/"


def txt(n):
    return open(EV + n, encoding="utf-8").read().strip()


# ---- architecture diagram
fig, ax = plt.subplots(figsize=(12, 5.2))
ax.axis("off")
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.2)


def box(x, y, w, h, t, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=c, ec="#333"))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=9)


def arr(a, b):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", color="#333"))


box(0.1, 3.7, 1.8, 0.9, "Developer\nVS Code + Git", "#e8eaf6")
box(2.5, 3.7, 1.9, 0.9, "GitHub repo\nfeature branch + PR", "#e8eaf6")
box(5.0, 3.7, 2.2, 0.9, "GitHub Actions\ntest -> build -> push", "#fff3e0")
box(7.8, 3.7, 2.0, 0.9, "Docker Hub\nparthmangrulkar2004/\niris-mlops", "#e0f2f1")
box(0.1, 0.3, 11.8, 2.9, "", "#fafafa")
ax.text(0.3, 2.9, "Local Kubernetes (Docker Desktop)", fontsize=10, weight="bold")
box(0.5, 0.7, 3.2, 1.6, "ns: mlops-exp5\nDeployment iris (2 pods)\nFastAPI + scikit-learn\n/predict /health /metrics\nService iris:8000", "#e8f5e9")
box(4.6, 0.7, 2.6, 1.6, "ns: monitoring\nPrometheus\nscrapes /metrics\nAlert rules", "#fce4ec")
box(8.2, 0.7, 2.6, 1.6, "Grafana\nIris dashboard\n(8 panels)", "#f3e5f5")
for a, b in [((1.9, 4.15), (2.5, 4.15)), ((4.4, 4.15), (5.0, 4.15)), ((7.2, 4.15), (7.8, 4.15)),
             ((8.8, 3.7), (2.1, 2.3)), ((4.6, 1.5), (3.7, 1.5)), ((8.2, 1.5), (7.2, 1.5))]:
    arr(a, b)
ax.text(5.5, 2.85, "image pull", fontsize=8)
ax.text(3.75, 1.6, "scrape", fontsize=8)
ax.text(7.25, 1.6, "query", fontsize=8)
fig.savefig("architecture.png", dpi=150, bbox_inches="tight")
plt.close(fig)

SHOTS = [
    ("01_grafana_healthy.png", "Grafana dashboard under live traffic (requests by species, p95 latency, errors, health, CPU, memory, replicas, restarts)."),
    ("02_prometheus_targets.png", "Prometheus 'iris' scrape job: both pods UP."),
    ("03_prometheus_query.png", "Prometheus query of iris_predictions_total by species."),
    ("04_github_pr.png", "Pull request #1 into main."),
    ("12_github_actions.png", "GitHub Actions runs for the feature branch."),
    ("05_dockerhub.png", "Docker Hub repository parthmangrulkar2004/iris-mlops with tags (a cookie banner partly covers the 'latest' row)."),
    ("06_alert_error_firing.png", "Alert test 1: IrisHighErrorRate FIRING after sustained requests to /boom."),
    ("07_grafana_errors.png", "Grafana error-rate panel during the error test."),
    ("08_alert_down_firing.png", "Alert test 2: IrisDown FIRING with the deployment scaled to 0 replicas."),
    ("09_grafana_outage.png", "Grafana during the outage (health and replica panels)."),
    ("10_alert_recovered.png", "Recovery: both alerts inactive after scaling back to 2 replicas."),
    ("11_grafana_recovered.png", "Grafana after recovery."),
]
SHOTS = [s for s in SHOTS if os.path.exists(EV + s[0])]

d = Document()
d.styles["Normal"].font.size = Pt(11)
d.add_heading("Experiment 5: End-to-End MLOps Pipeline", 0)
d.add_paragraph("Name: Manas Tawde    Roll No: E019    Subject: MLOps\n"
                "Repository: https://github.com/manastawde/MANAS_E019_MLOPS (branch feature/exp5-end-to-end-mlops, PR #1)")


def sec(t, body=None):
    d.add_heading(t, 1)
    if body:
        d.add_paragraph(body)


def mono(t):
    p = d.add_paragraph()
    r = p.add_run(t)
    r.font.name = "Consolas"
    r.font.size = Pt(8)


sec("1. Aim", "To build, test, containerise, automatically publish and deploy a machine-learning service on Kubernetes, and monitor it with Prometheus and Grafana.")
sec("2. Architecture")
d.add_picture("architecture.png", width=Inches(6.4))
sec("3. Application", "A RandomForest classifier trained on the Iris dataset at start-up is served by FastAPI. Endpoints: POST /predict (validated input), GET /health, GET /metrics (Prometheus) and GET /boom (deliberate HTTP 500 used only for the alert test). Custom metrics: iris_predictions_total{species}, http_requests_total{method,path,status}, http_request_duration_seconds{path}.")
sec("4. Testing", "Five pytest tests cover model accuracy, health, a setosa prediction, input validation (422) and metrics exposure. They run locally and in CI.")
mono(txt("terminal_ci.txt"))
sec("5. Docker and CI/CD", "The Dockerfile uses python:3.11-slim and a non-root user. The workflow .github/workflows/exp5-mlops.yml runs on push and pull request: job 'test' runs pytest; job 'docker' builds the image and, on push events only, logs in to Docker Hub using repository secrets DOCKERHUB_USERNAME and DOCKERHUB_TOKEN and pushes :latest and :<commit sha>. The first push run failed at the Docker Hub login because the secrets had not yet been added; after adding them, all runs succeeded. The image was then pulled from Docker Hub and run locally (/health and /predict answered correctly).")
sec("6. Kubernetes deployment", "The published image was deployed to namespace mlops-exp5 (2 replicas, readiness/liveness probes on /health, CPU/memory requests and limits, ClusterIP service).")
mono(txt("terminal_k8s.txt"))
sec("7. Monitoring", "kube-prometheus-stack was installed with Helm into namespace 'monitoring'. An extra scrape job discovers the iris service endpoints and scrapes /metrics/. A Grafana dashboard (provisioned from a ConfigMap) shows prediction requests, p95 latency, error rate, application health, CPU, memory, replicas and restarts. Local access used kubectl port-forward on ports 19090 (Prometheus), 13000 (Grafana) and 18080 (app), chosen to avoid the existing Devops project.")
mono(txt("terminal_prometheus.txt"))
sec("8. Alert and recovery tests", "Test 1: sustained /boom requests drove the 5xx ratio above 20% and IrisHighErrorRate fired, then cleared when the load stopped. Test 2: scaling the deployment to 0 should fire IrisDown. The first attempt did NOT fire: with no targets, sum(up) returns no series rather than 0. The rule was corrected to (sum(up{job=\"iris\"}) or vector(0)) < 1, and the repeated test fired IrisDown and cleared after scaling back to 2 replicas. Deleting one pod showed Kubernetes self-healing (a replacement started automatically).")
sec("9. Screenshots")
for f, cap in SHOTS:
    d.add_picture(EV + f, width=Inches(6.2))
    d.add_paragraph("Figure: " + cap).runs[0].italic = True
sec("10. Limitations", "The cluster is a single-node local Docker Desktop cluster; Grafana uses a demo password and is reachable only through localhost port-forwards; Alertmanager has no receiver configured, so alerts are visible in Prometheus rather than sent as notifications; GitHub Actions cannot reach the laptop cluster, so deployment is a manual kubectl step from the published image.")
sec("11. Conclusion", "A change committed to a feature branch is tested and built by GitHub Actions, published to Docker Hub, deployed to Kubernetes and observed with Prometheus and Grafana, with alerting and recovery verified.")
d.save("Exp5_Report.docx")

pr = Presentation()
pr.slide_width, pr.slide_height = PI(13.33), PI(7.5)


def slide(title, bullets=None, img=None):
    s = pr.slides.add_slide(pr.slide_layouts[5])
    s.shapes.title.text = title
    s.shapes.title.text_frame.paragraphs[0].font.size = PP(30)
    if bullets:
        tb = s.shapes.add_textbox(PI(0.6), PI(1.5), PI(12), PI(5)).text_frame
        tb.word_wrap = True
        for i, b in enumerate(bullets):
            p = tb.paragraphs[0] if i == 0 else tb.add_paragraph()
            p.text = "- " + b
            p.font.size = PP(20)
    if img:
        s.shapes.add_picture(img, PI(1.2), PI(1.4), height=PI(5.8))


slide("Experiment 5: End-to-End MLOps", ["Manas Tawde, E019", "FastAPI + scikit-learn -> Docker -> GitHub Actions -> Docker Hub -> Kubernetes -> Prometheus/Grafana"])
slide("Architecture", img="architecture.png")
slide("CI/CD", ["Feature branch + PR #1 into main", "Jobs: pytest (5 tests) -> docker build -> push on push events", "Secrets: DOCKERHUB_USERNAME / DOCKERHUB_TOKEN", "First push run failed (no secrets yet); all runs green afterwards", "Image: parthmangrulkar2004/iris-mlops (:latest, :sha)"])
slide("Kubernetes + Monitoring", ["Namespace mlops-exp5: 2 replicas, probes, resource limits", "kube-prometheus-stack via Helm; scrape job for /metrics/", "Dashboard: predictions, p95 latency, errors, health, CPU, memory, replicas, restarts"])
for f, cap in SHOTS:
    s = pr.slides.add_slide(pr.slide_layouts[5])
    s.shapes.title.text = cap[:70]
    s.shapes.title.text_frame.paragraphs[0].font.size = PP(20)
    s.shapes.add_picture(EV + f, PI(2.4), PI(1.3), height=PI(6.0))
slide("Findings and limits", ["Alert test found a real bug: IrisDown never fired with 0 pods; fixed with 'or vector(0)'", "Single-node local cluster; port-forward access only", "No Alertmanager receiver configured"])
pr.save("Exp5_Presentation.pptx")
print("built", len(SHOTS), "screenshots")
