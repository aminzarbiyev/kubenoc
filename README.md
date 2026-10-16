# KubeNOC

Telekom/şəbəkə mühiti üçün Kubernetes üzərində monitorinq və avtomatlaşdırma platforması (test laboratoriyası, yalnız pulsuz alətlər).

## Arxitektur
Blackbox Exporter (ICMP ping) → Prometheus → Alertmanager → Telegram; Grafana dashboard; `noc-api` (FastAPI) Prometheus-dan status oxuyub JSON verir.

## Stack
Ubuntu Server 26.04, Docker, k3s, Helm, kube-prometheus-stack, Blackbox Exporter, Alertmanager, Grafana, FastAPI, GitHub Actions, GHCR.

## Tamamlanıb
- [x] k3s klaster, Helm, Prometheus, Grafana
- [x] Blackbox Exporter ilə ping monitorinqi (Probe CRD)
- [x] `HostUnreachable` alert qaydası (PrometheusRule)
- [x] Alertmanager → Telegram (Firing və Resolved)
- [x] Öz FastAPI servisi (`/healthz`, `/status`), multi-stage Dockerfile, non-root
- [x] Kubernetes Deployment/Service, resource limit, health probe
- [x] GitHub Actions: pytest + image build və GHCR push

## Yol xəritəsi
- [ ] SNMP exporter və virtual şəbəkə cihazları
- [ ] Loki ilə syslog
- [ ] Config backup
- [ ] ArgoCD (GitOps), Trivy, NetworkPolicy

## İşə salmaq
```
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack -n monitoring -f helm/monitoring-values.yaml
helm upgrade --install blackbox prometheus-community/prometheus-blackbox-exporter -n monitoring -f helm/blackbox-values.yaml
kubectl apply -f k8s/probe-ping.yaml -f k8s/alerts-noc.yaml -f k8s/noc-api.yaml
```
Telegram token Kubernetes Secret-də saxlanılır və Git-ə yazılmır.
