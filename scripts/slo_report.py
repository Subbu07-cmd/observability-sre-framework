#!/usr/bin/env python3
"""SLO attainment and error budget report from Prometheus.

Usage: python scripts/slo_report.py --prometheus http://localhost:9090 --slo 99.9 --window 30d
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request


def error_budget(slo_pct: float, error_ratio: float) -> dict:
    """Pure calculation, unit-tested in tests/test_slo_report.py."""
    allowed = 1 - slo_pct / 100
    availability = 1 - error_ratio
    consumed = error_ratio / allowed if allowed else float("inf")
    return {
        "slo": slo_pct,
        "availability": round(availability * 100, 4),
        "budget_consumed_pct": round(consumed * 100, 2),
        "budget_remaining_pct": round(max(0.0, 1 - consumed) * 100, 2),
        "status": "OK" if consumed < 0.75 else ("AT_RISK" if consumed < 1 else "BREACHED"),
    }


def query(prom: str, expr: str) -> list[dict]:
    url = f"{prom.rstrip('/')}/api/v1/query?" + urllib.parse.urlencode({"query": expr})
    with urllib.request.urlopen(url, timeout=15) as r:
        body = json.load(r)
    if body.get("status") != "success":
        raise RuntimeError(body)
    return body["data"]["result"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prometheus", default="http://localhost:9090")
    ap.add_argument("--slo", type=float, default=99.9)
    ap.add_argument("--window", default="30d")
    a = ap.parse_args()

    expr = (
        f'sum by (service) (increase(http_requests_total{{code=~"5.."}}[{a.window}]))'
        f" / sum by (service) (increase(http_requests_total[{a.window}]))"
    )
    rows = query(a.prometheus, expr)
    if not rows:
        print("No data returned.", file=sys.stderr)
        return 1
    print(f"{'service':<24}{'availability':>14}{'budget used':>14}{'remaining':>12}  status")
    worst = 0
    for row in rows:
        r = error_budget(a.slo, float(row["value"][1]))
        print(f"{row['metric'].get('service', '-'):<24}{r['availability']:>13}%{r['budget_consumed_pct']:>13}%"
              f"{r['budget_remaining_pct']:>11}%  {r['status']}")
        worst = max(worst, {"OK": 0, "AT_RISK": 1, "BREACHED": 2}[r["status"]])
    return worst


if __name__ == "__main__":
    sys.exit(main())
