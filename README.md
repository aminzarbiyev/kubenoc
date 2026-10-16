# KubeNOC

Network monitoring and automation platform on Kubernetes (k3s) for a telecom/NOC use case.

## Stack
Docker, k3s, Helm, Prometheus, Grafana, Alertmanager

## Status
- [x] k3s single-node cluster
- [x] Prometheus + Grafana (kube-prometheus-stack)
- [x] Blackbox probes (ping/uptime)
- [x] Alertmanager alerts to Telegram
- [ ] SNMP monitoring of virtual network devices
- [ ] Syslog with Loki
- [ ] CI/CD (GitHub Actions) + GitOps (ArgoCD)
