"""Generates dashboard-configmap.yaml (Grafana sidecar picks up label grafana_dashboard=1)."""
import json
DS = {"type": "prometheus", "uid": "prometheus"}
def p(i, title, expr, x, y, kind="timeseries", unit="short", legend="{{pod}}"):
    return {"id": i, "title": title, "type": kind, "datasource": DS, "gridPos": {"x": x, "y": y, "w": 8, "h": 7},
            "fieldConfig": {"defaults": {"unit": unit}, "overrides": []},
            "targets": [{"expr": expr, "legendFormat": legend, "refId": "A"}]}
R = 'job="iris"'
panels = [
    p(1, "Prediction requests / s (by species)", 'sum(rate(iris_predictions_total[1m])) by (species)', 0, 0, legend="{{species}}", unit="reqps"),
    p(2, "p95 latency /predict", 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{path="/predict"}[1m])) by (le))', 8, 0, unit="s", legend="p95"),
    p(3, "Error rate (5xx / s)", 'sum(rate(http_requests_total{status=~"5.."}[1m]))', 16, 0, unit="reqps", legend="5xx"),
    p(4, "Application health (up)", f'up{{{R}}}', 0, 7, kind="stat", legend="{{pod}}"),
    p(5, "Pod CPU (cores)", 'sum(rate(container_cpu_usage_seconds_total{namespace="mlops-exp5",container="iris"}[1m])) by (pod)', 8, 7, unit="short"),
    p(6, "Pod memory", 'sum(container_memory_working_set_bytes{namespace="mlops-exp5",container="iris"}) by (pod)', 16, 7, unit="bytes"),
    p(7, "Ready replicas", 'kube_deployment_status_replicas_available{namespace="mlops-exp5",deployment="iris"}', 0, 14, kind="stat", legend="available"),
    p(8, "Pod restarts", 'sum(kube_pod_container_status_restarts_total{namespace="mlops-exp5"}) by (pod)', 8, 14, kind="stat"),
]
dash = {"uid": "iris-exp5", "title": "Iris MLOps - Experiment 5", "schemaVersion": 39, "refresh": "10s",
        "time": {"from": "now-15m", "to": "now"}, "panels": panels}
body = json.dumps(dash, indent=1).replace("\n", "\n    ")
open("dashboard-configmap.yaml", "w").write(
    "apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: iris-dashboard\n  namespace: monitoring\n"
    "  labels: {grafana_dashboard: \"1\"}\ndata:\n  iris.json: |\n    " + body + "\n")
