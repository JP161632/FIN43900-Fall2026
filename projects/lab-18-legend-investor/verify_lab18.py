"""Independent answer-key audit and controlled behavioral probes (no hidden data fixes)."""
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parents[1] / ".agents/skills/buffett-edgar/scripts/edgar_facts.py"
spec = importlib.util.spec_from_file_location("edgar", SCRIPT)
edgar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edgar)

# The instructor's answer key belongs ONLY in the independent verifier.
EXPECTED = [
    ("2022-08-28", 226954, 5844, 7392, 3891, 20642, 28.3, 3501),
    ("2023-09-03", 242290, 6292, 11068, 4323, 25058, 25.1, 6745),
    ("2024-09-01", 254453, 7367, 11339, 4710, 23622, 31.2, 6629),
    ("2025-08-31", 275235, 8099, 13335, 5498, 29164, 27.8, 7837),
    ("2026-08-30", 303154, 9226, 15817, 6435, 35803, 25.8, 9382),
]


def fixture():
    """Clearly synthetic contexts for adversarial selection tests, never live evidence."""
    facts = {"entityName": "Synthetic test company", "cik": 1, "facts": {"us-gaap": {}}}
    for field, tags in edgar.TAGS.items():
        records = []
        for year in range(2021, 2026):
            record = {"end": f"{year}-12-31", "form": "10-K", "filed": f"{year+1}-02-15",
                      "accn": f"synthetic-{year}", "val": 100_000_000}
            if field != "equity":
                record["start"] = f"{year}-01-01"
            record["val"] = {"revenue": 500_000_000, "net_income": 20_000_000,
                             "operating_cash_flow": (year-2020)*30_000_000,
                             "capital_spending": 10_000_000, "equity": 100_000_000}[field]
            records.append(record)
        facts["facts"]["us-gaap"][tags[0]] = {"units": {"USD": records}}
    return facts


class ControlledTests(unittest.TestCase):
    def test_annual_vs_quarter_and_latest_filing(self):
        facts = fixture()
        records = edgar.observations(facts, "NetIncomeLoss")
        restated = dict(records[-1], val=25_000_000, filed="2026-03-01", fy=2026)
        records += [restated, dict(restated, val=999, start="2025-10-01", filed="2027-01-01"),
                    dict(restated, val=888, form="10-Q", filed="2028-01-01"),
                    dict(restated, val=777, form="10-K/A", filed="2029-01-01")]
        row = edgar.compute(facts, "TEST")["rows"][-1]
        self.assertEqual(row["net_income"]["value"], 25_000_000)
        self.assertEqual(row["fiscal_year_end"], "2025-12-31")

    def test_priority_then_fallback(self):
        facts = fixture()
        facts["facts"]["us-gaap"]["Revenues"] = {"units": {"USD": [
            dict(edgar.observations(facts, edgar.TAGS["revenue"][0])[-1], val=999, filed="2027-01-01")]}}
        row = edgar.compute(facts, "TEST")["rows"][-1]
        self.assertEqual(row["revenue"]["value"], 500_000_000)
        edgar.observations(facts, edgar.TAGS["revenue"][0]).pop()
        row = edgar.compute(facts, "TEST")["rows"][-1]
        self.assertEqual(row["revenue"]["tag"], "Revenues")
        self.assertEqual(row["revenue"]["value"], 999)

    def test_missing_capex_and_interior_missing_growth(self):
        facts = fixture()
        edgar.observations(facts, edgar.TAGS["capital_spending"][0]).pop(2)
        result = edgar.compute(facts, "TEST")
        self.assertEqual(edgar.display(result["rows"][2]["capital_spending"]), "not found")
        self.assertEqual(edgar.display(result["rows"][2]["owner_earnings"]), "not found")
        self.assertEqual(list(result["checks"].values()), ["pass", "not known", "not known"])

    def test_nonpositive_equity(self):
        for value in [0, -100]:
            facts = fixture()
            edgar.observations(facts, "StockholdersEquity")[-1]["val"] = value
            result = edgar.compute(facts, "TEST")
            self.assertEqual(edgar.display(result["rows"][-1]["roe"], True), "not known")
            self.assertEqual(next(iter(result["checks"].values())), "not known")

    def test_checks_fail_and_boundary_pass(self):
        facts = fixture()
        edgar.observations(facts, "NetIncomeLoss")[-1]["val"] = 15_000_000
        self.assertEqual(next(iter(edgar.compute(facts, "TEST")["checks"].values())), "pass")
        edgar.observations(facts, "NetIncomeLoss")[-1]["val"] = 14_999_999
        edgar.observations(facts, "NetCashProvidedByUsedInOperatingActivities")[-1]["val"] = 10_000_000
        self.assertEqual(list(edgar.compute(facts, "TEST")["checks"].values()), ["fail", "fail", "fail"])

    def test_short_history(self):
        facts = fixture()
        for item in facts["facts"]["us-gaap"].values():
            item["units"]["USD"].pop()
        self.assertEqual(set(edgar.compute(facts, "TEST")["checks"].values()), {"not known"})

    def test_53_weeks(self):
        self.assertTrue(edgar.annual({"form": "10-K", "start": "2022-08-29", "end": "2023-09-03"}))
        self.assertFalse(edgar.annual({"form": "10-K", "start": "2023-06-01", "end": "2023-09-03"}))

    def test_numeric_injection_and_units(self):
        report = edgar.report_text(edgar.compute(fixture(), "TEST"))
        self.assertEqual(edgar.unsupported_numbers("ROE 20.0%", report), [])
        flags = edgar.unsupported_numbers("ROE 40.0%; ROE 40.0%; income -500; ROE 500%", report)
        self.assertEqual([x["token"] for x in flags], ["40.0%", "40.0%", "-500", "500%"])

    def test_invalid_ticker(self):
        with self.assertRaises(ValueError):
            edgar.ticker_symbol("../../COST")


def source_audit():
    cost = edgar.run("COST", offline=True)
    jpm = edgar.run("JPM", offline=True)
    fields = list(edgar.TAGS) + ["roe", "owner_earnings"]
    actual = {row["fiscal_year_end"]: row for row in cost["rows"]}
    comparison = []
    for expected in EXPECTED:
        row = actual.get(expected[0])
        for field, target in zip(fields, expected[1:]):
            value = None if row is None else row[field]["value"]
            shown = None if row is None else edgar.display(row[field], field == "roe")
            correct = (shown == f"{target:.1f}%" if field == "roe" else value == target * 1_000_000)
            comparison.append({"fiscal_year_end": expected[0], "field": field, "expected": target,
                               "expected_units": "percent" if field == "roe" else "USD millions",
                               "actual_display": shown, "match": correct})
    memo_flags = {}
    for result in (cost, jpm):
        path = HERE / "memos" / f'{result["ticker"]}.md'
        memo_flags[result["ticker"]] = edgar.unsupported_numbers(path.read_text(encoding="utf-8"), edgar.report_text(result)) if path.exists() else "memo missing"
    injected = edgar.unsupported_numbers("Hand-entered ROE 40.0%.", edgar.report_text(cost))
    jpm_gap = all(row["capital_spending"]["value"] is None and row["owner_earnings"]["value"] is None for row in jpm["rows"])
    checks = {
        "COST_all_35_answer_key_values_match": all(x["match"] for x in comparison),
        "COST_all_three_checks_pass": set(cost["checks"].values()) == {"pass"},
        "COST_owner_earnings_and_net_income_up": all(cost["rows"][-1][f]["value"] > cost["rows"][0][f]["value"] for f in ("owner_earnings", "net_income")),
        "JPM_capex_and_owner_earnings_missing_all_years": jpm_gap,
        "JPM_owner_earnings_checks_not_known": list(jpm["checks"].values())[1:] == ["not known", "not known"],
        "JPM_memo_discloses_owner_earnings_gap": "cannot judge owner earnings" in (HERE / "memos/JPM.md").read_text(encoding="utf-8").lower(),
        "hand_entered_40_percent_flagged": [x["token"] for x in injected] == ["40.0%"],
        "saved_memos_have_no_unsupported_numbers": all(value == [] for value in memo_flags.values()),
    }
    result = {"checks": checks, "COST_comparison": comparison,
              "actual_fiscal_year_ends": list(actual), "memo_flags": memo_flags, "injection_flags": injected,
              "sources": {"COST": cost["source"], "JPM": jpm["source"]}}
    (HERE / "verification-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checks, indent=2))
    print("Answer-key matches:", sum(x["match"] for x in comparison), "/", len(comparison))
    return all(checks.values())


if __name__ == "__main__":
    import sys
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ControlledTests)
    passed = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    if "--source-audit" in sys.argv:
        passed = source_audit() and passed
    raise SystemExit(0 if passed else 1)
