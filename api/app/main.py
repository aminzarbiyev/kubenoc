import os
import httpx
from fastapi import FastAPI, HTTPException

PROM_URL = os.getenv(
    "PROMETHEUS_URL",
    "http://monitoring-kube-prometheus-prometheus.monitoring.svc:9090",
)
QUERY = os.getenv("PROBE_QUERY", 'probe_success{job="icmp-ping"}')

app = FastAPI(title="KubeNOC API", version="0.1.0")


def fetch_probes():
    r = httpx.get(f"{PROM_URL}/api/v1/query", params={"query": QUERY}, timeout=5)
    r.raise_for_status()
    return r.json()["data"]["result"]


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/status")
def status():
    try:
        result = fetch_probes()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Prometheus unreachable: {exc}")
    targets = [
        {"target": s["metric"].get("instance", "?"), "up": s["value"][1] == "1"}
        for s in result
    ]
    down = [t["target"] for t in targets if not t["up"]]
    return {
        "total": len(targets),
        "up": len(targets) - len(down),
        "down": len(down),
        "down_targets": down,
        "targets": sorted(targets, key=lambda t: t["target"]),
    }
