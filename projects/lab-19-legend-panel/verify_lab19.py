"""Independent known-answer audit and explicitly synthetic mutation probes."""
from copy import deepcopy
import json
from pathlib import Path
import panel

HERE = Path(__file__).resolve().parent
# Instructor answers appear only here, never in production facts or calculations.
EXPECTED = [
    ("2022-08-28", "1.02", "2.11"),
    ("2023-09-03", "1.07", "1.75"),
    ("2024-09-01", "0.97", "1.96"),
    ("2025-08-31", "1.03", "1.64"),
    ("2026-08-30", "1.06", "1.49"),
]


def run():
    checks = {}
    cost = panel.run("COST")
    panel.save(cost)
    comparisons = [{"end": end, "current_ratio": panel.shown(row["current_ratio"], "current_ratio"),
                    "liabilities_to_equity": panel.shown(row["liabilities_to_equity"], "liabilities_to_equity"),
                    "match": row["fiscal_year_end"] == end and panel.shown(row["current_ratio"], "current_ratio") == cr
                    and panel.shown(row["liabilities_to_equity"], "liabilities_to_equity") == le}
                   for row, (end, cr, le) in zip(cost["rows"], EXPECTED)]
    checks["COST_all_ten_ratios_match"] = len(comparisons) == 5 and all(r["match"] for r in comparisons)
    checks["COST_all_eight_checks_match"] = [list(v.values()) for v in cost["panel"].values()] == [
        ["pass", "pass", "pass"], ["fail", "pass", "pass"], ["pass", "pass"]]
    probe = panel.run("COST", hurdle=1.0)
    panel.save(probe, "COST-probe")
    checks["threshold_probe_changes_only_Graham_liquidity"] = (
        list(probe["panel"]["Graham"].values()) == ["pass"] * 3 and probe["rows"] == cost["rows"]
        and probe["panel"]["Buffett"] == cost["panel"]["Buffett"] and probe["panel"]["Burry"] == cost["panel"]["Burry"])
    checks["retained_skill_threshold_is_two"] = panel.threshold() == 2.0
    memos = panel.load_memos("COST")
    report = panel.report_text(cost)
    checks["all_COST_memos_present_and_supported"] = all(memos.values()) and not any(panel.memo_flags(memos, report).values())
    for investor in panel.INVESTORS:
        injected = dict(memos)
        injected[investor] += "\nInjected ratio 987654321.12345."
        flags = panel.memo_flags(injected, report)
        checks[f"injection_detected_in_{investor}_only"] = bool(flags[investor]) and not any(v for k, v in flags.items() if k != investor)
    rows = deepcopy(cost["rows"])
    rows[2]["net_income"]["value"] = None
    checks["interior_missing_income_blocks_both_Graham_annual_checks"] = list(panel.graham_checks(rows, 2).values())[1:] == ["not known"] * 2
    checks["interior_missing_income_blocks_Burry_cash_check"] = next(iter(panel.burry_checks(rows).values())) == "not known"
    for denominator in (None, 0, -1):
        checks[f"ratio_denominator_{denominator}_not_known"] = panel.ratio({"value": 1}, {"value": denominator}, "synthetic")["value"] is None
    rows = deepcopy(cost["rows"])
    rows[-1]["current_ratio"]["value"] = 2
    rows[-1]["liabilities_to_equity"]["value"] = 2
    checks["inclusive_ratio_boundaries"] = next(iter(panel.graham_checks(rows, 2).values())) == "pass" and list(panel.burry_checks(rows).values())[-1] == "pass"
    rows[-1]["current_ratio"]["value"] = 1.999999
    checks["threshold_uses_unrounded_value"] = next(iter(panel.graham_checks(rows, 2).values())) == "fail"
    short = rows[-1:]
    checks["short_history_keeps_latest_checks_but_blocks_annual_checks"] = (
        list(panel.graham_checks(short, 2).values())[1:] == ["not known"] * 2
        and list(panel.burry_checks(short).values()) == ["not known", "pass"])
    checks["empty_history_unknown"] = set(panel.graham_checks([], 2).values()) == {"not known"} and set(panel.burry_checks([]).values()) == {"not known"}
    jpm = panel.run("JPM")
    checks["JPM_real_gaps_preserved"] = (
        all(r["current_assets"]["value"] is None and r["current_liabilities"]["value"] is None and r["current_ratio"]["value"] is None for r in jpm["rows"])
        and list(jpm["panel"]["Graham"].values()) == ["not known", "pass", "pass"]
        and list(jpm["panel"]["Buffett"].values())[1:] == ["not known", "not known"])
    checks["JPM_memos_present_supported_and_disclose_gaps"] = (
        all(panel.load_memos("JPM").values()) and not any(panel.memo_flags(panel.load_memos("JPM"), panel.report_text(jpm)).values())
        and "cannot judge owner earnings" in panel.load_memos("JPM")["Buffett"])
    facts = {"facts": {"us-gaap": {"AssetsCurrent": {"units": {"USD": [
        {"form": "10-K", "end": "2025-12-31", "filed": "2026-02-01", "val": 1, "accn": "synthetic-A"},
        {"form": "10-K", "end": "2025-12-31", "filed": "2026-03-01", "val": 2, "accn": "synthetic-B"},
        {"form": "10-Q", "end": "2025-12-31", "filed": "2026-04-01", "val": 999},
        {"form": "10-K/A", "end": "2025-12-31", "filed": "2026-05-01", "val": 888},
        {"form": "10-K", "start": "2025-01-01", "end": "2025-12-31", "filed": "2026-06-01", "val": 777},
    ]}}}}}
    checks["instant_selection_latest_10K_excludes_duration_quarter_amendment"] = panel.select_instant(facts, "AssetsCurrent", "2025-12-31")["value"] == 2
    nvda = panel.run("NVDA")
    panel.save(nvda)
    checks["NVDA_all_eight_checks_and_no_unknowns"] = [list(v.values()) for v in nvda["panel"].values()] == [
        ["pass"] * 3, ["pass"] * 3, ["fail", "pass"]]
    checks["NVDA_cash_exceptions_retained"] = [r["fiscal_year_end"] for r in nvda["rows"]
        if r["operating_cash_flow"]["value"] < r["net_income"]["value"]] == ["2022-01-30", "2024-01-28", "2025-01-26", "2026-01-25"]
    checks["NVDA_all_memos_present_supported_and_have_verdicts"] = (
        all(panel.load_memos("NVDA").values())
        and not any(panel.memo_flags(panel.load_memos("NVDA"), panel.report_text(nvda)).values())
        and all(panel.verdict(m) != "pending memo" for m in panel.load_memos("NVDA").values()))
    results = {"checks": checks, "COST_comparisons": comparisons, "sources": {"COST": cost["source"], "JPM": jpm["source"], "NVDA": nvda["source"]},
               "probe": {"threshold": probe["graham_threshold"], "Graham": probe["panel"]["Graham"]}}
    (HERE / "verification-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checks, indent=2))
    return all(checks.values())


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
