# Production Observability & SRE Framework

> **About this repo:** my production work lives in private enterprise repositories, so this is a public reference build of the same patterns, written from scratch with sample data and placeholder account IDs.

A ready-to-run observability stack and SRE operating model for Linux and AWS production environments. It covers **metrics, logs, alerting and SLI/SLO tracking** with **Prometheus, Grafana, Alertmanager and CloudWatch**, together with the process side: **on-call, runbooks and blameless postmortems**.

```
  Linux hosts (RHEL/CentOS)       AWS services                Applications
  node_exporter (Ansible) ─┐      CloudWatch alarms ─┐        /metrics ─┐
                           ▼                         ▼                  ▼
                     ┌──────────────────────────────────────────────────────┐
                     │ Prometheus — recording rules (SLIs) + burn-rate alerts │
                     └──────────────────────────────────────────────────────┘
                              │                           │
                              ▼                           ▼
                     Grafana (SLO dashboard)     Alertmanager → PagerDuty / Slack
                                                          │
                                                          ▼
                                                 runbooks/ → postmortem template
```

## What's inside

| Path | Purpose |
|------|---------|
| `docker-compose.yml` | Prometheus, Alertmanager, Grafana, node_exporter and a demo app, started with one command |
| `prometheus/rules/slo.rules.yml` | SLI recording rules and **multi-window, multi-burn-rate** SLO alerts (Google SRE workbook method) |
| `prometheus/rules/infra.rules.yml` | Host alerts for CPU, memory, disk fill prediction and down targets |
| `alertmanager/alertmanager.yml` | Severity-based routing, grouping and inhibition |
| `grafana/` | Provisioned data source and an SLO / error budget dashboard |
| `terraform/cloudwatch/` | CloudWatch alarms and an SNS topic for AWS-managed services (ALB, RDS, EC2) |
| `ansible/` | Role that installs node_exporter as a hardened systemd service on RHEL/CentOS |
| `scripts/slo_report.py` | Calculates SLO attainment and remaining error budget from Prometheus |
| `scripts/healthcheck.sh` | Lightweight endpoint probe for cron or CI smoke tests |
| `runbooks/` | Alert runbooks, the on-call process and a blameless postmortem template |

## Quick start

```bash
docker compose up -d
# Prometheus  http://localhost:9090
# Alertmanager http://localhost:9093
# Grafana     http://localhost:3000  (admin / admin)
```

```bash
python scripts/slo_report.py --prometheus http://localhost:9090 --slo 99.9 --window 30d
```

## SLO alerting model

| Alert | Long window | Short window | Burn rate | Budget consumed | Action |
|------|------|------|------|------|------|
| `SLOErrorBudgetBurnFast` | 1h | 5m | 14.4× | 2% in 1h | Page |
| `SLOErrorBudgetBurnSlow` | 6h | 30m | 6× | 5% in 6h | Page |
| `SLOErrorBudgetBurnTicket` | 3d | 6h | 1× | 10% in 3d | Ticket |

## Tech

Prometheus · Grafana · CloudWatch · Linux (RHEL/CentOS) · AWS · Python · Bash · Ansible
