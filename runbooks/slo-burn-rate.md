# Runbook: SLO error budget burn

**Alerts:** `SLOErrorBudgetBurnFast`, `SLOErrorBudgetBurnSlow` · **Severity:** page

## 1. Confirm impact (≤ 5 min)
- Open the Grafana dashboard **SRE → SLO & Error Budget** and select the service.
- Is the error ratio still above the SLO threshold line? If it has already recovered, ack and monitor for 15 minutes.

## 2. Find what changed
- Deploys in the last 2 hours (Argo CD history, or `kubectl rollout history deploy/<svc>`)
- Config or feature-flag changes
- Dependency health: database, cache and downstream APIs (check their dashboards)

## 3. Mitigate first, debug later
| Signal | Action |
|-------|--------|
| Started right after a deploy | **Roll back**: `kubectl rollout undo deploy/<svc>` or revert in Git |
| Saturation (CPU, connection pools) | Scale out: raise the HPA `minReplicas` |
| A single bad node or AZ | Cordon and drain the node, or shift traffic away from the AZ |
| A downstream dependency | Enable the circuit breaker or degrade gracefully, and page the owning team |

## 4. Communicate
- SEV1: open an incident channel, post updates every 30 minutes and update the status page.

## 5. Close out
- Confirm burn rate is below 1× for 30 minutes before resolving.
- File a postmortem using [postmortem-template.md](postmortem-template.md) for any SEV1 or SEV2.
