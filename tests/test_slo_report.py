import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location(
    "slo_report", pathlib.Path(__file__).parents[1] / "scripts" / "slo_report.py"
)
slo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(slo)


def test_within_budget():
    r = slo.error_budget(99.9, 0.0002)
    assert r["status"] == "OK"
    assert r["budget_remaining_pct"] == 80.0


def test_at_risk():
    assert slo.error_budget(99.9, 0.0008)["status"] == "AT_RISK"


def test_breached():
    r = slo.error_budget(99.9, 0.002)
    assert r["status"] == "BREACHED"
    assert r["budget_remaining_pct"] == 0.0
