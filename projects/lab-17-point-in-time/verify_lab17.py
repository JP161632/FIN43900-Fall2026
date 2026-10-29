"""Reproduce live evidence (--live) or re-audit the preserved public downloads."""

import argparse
import csv
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import hashlib
from io import StringIO
import json
from pathlib import Path
from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest

import asof_app as app

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
EXPECTED = {"BAA": ("2026-09-01", 6.47), "FEDFUNDS": ("2026-09-01", 3.75),
            "DGS10": ("2026-10-02", 5.28), "MORTGAGE30US": ("2026-10-01", 7.28)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Refresh public source snapshots")
    parser.add_argument("--series", help="Also audit the student's prework series")
    parser.add_argument("--live-ui", action="store_true", help="Also exercise the page with real HTTP downloads")
    args = parser.parse_args()
    today = date.today().isoformat()
    manifest_path = EVIDENCE / "downloads.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    loaded = {}

    def get(series_id, cutoff=None):
        key = f"{series_id}_{cutoff or 'current'}"
        if key in loaded:
            return loaded[key]
        if args.live:
            result = (app.download_vintage(series_id, cutoff, today) if cutoff
                      else app.download_current(series_id, today))
            EVIDENCE.mkdir(exist_ok=True)
            raw = result["csv"].encode("utf-8")
            (EVIDENCE / f"{key}.csv").write_bytes(raw)
            manifest[key] = {"url": result["url"], "downloaded_at_utc": result["downloaded_at_utc"],
                             "sha256": hashlib.sha256(raw).hexdigest(), "file": f"{key}.csv"}
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        else:
            entry = manifest[key]
            raw = (EVIDENCE / entry["file"]).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == entry["sha256"], f"Snapshot changed: {key}"
            column = f"{series_id}_{cutoff.replace('-', '')}" if cutoff else series_id
            result = {"data": app.parse_csv(raw.decode(), column), "csv": raw.decode(), **entry}
        loaded[key] = result
        return result

    results = {"audited_at_utc": datetime.now(timezone.utc).isoformat(),
               "mode": "live downloads" if args.live else "preserved source snapshots", "checks": []}

    def check(label, condition):
        results["checks"].append({"check": label, "passed": bool(condition)})

    known_rows = []
    for series_id, (expected_date, expected_value) in EXPECTED.items():
        current = get(series_id)
        vintage = get(series_id, "2026-10-05")
        row = app.compare(current["data"], vintage["data"])
        check(f"{series_id} October 5 known answer", row["Last measured date known then"] == pd.Timestamp(expected_date)
              and row["Value known then"] == expected_value)
        known_rows.append({"series": series_id, **row})
    results["known_answer"] = known_rows
    current, vintage = get("PAYEMS"), get("PAYEMS", "2025-01-15")
    probe = app.compare(current["data"], vintage["data"])
    then_dec = float(vintage["data"].loc["2024-12-01", "value"])
    now_dec = float(current["data"].loc["2024-12-01", "value"])
    check("PAYEMS vintage ends in December 2024 at 159536", probe["Last measured date known then"] == pd.Timestamp("2024-12-01")
          and then_dec == 159536)
    check("PAYEMS December 2024 lower today and many revisions", now_dec < then_dec and probe["Revised matching dates"] > 100)
    results["payems_probe"] = {**probe, "December 2024 then": then_dec, "December 2024 today": now_dec}

    # Synthetic counterexample, separate from the live known-answer evidence.
    now = app.parse_csv("observation_date,X\n2020-01-01,1\n2020-01-02,3\n2020-01-03,.\n2020-01-04,4\n", "X")
    then = app.parse_csv("observation_date,X_20200102\n2020-01-01,1\n2020-01-02,2\n", "X_20200102")
    row = app.compare(now, then)
    check("Missing dot is not a late value; matching-date revision counted", row["Later values today"] == 1
          and row["Revised matching dates"] == 1 and row["Matching dates compared"] == 2)
    empty = then.iloc[:0]
    check("Empty vintage has no invented last date", app.compare(now, empty)["Last measured date known then"] is None)
    check("Empty vintage counts available current observations", app.compare(now, empty)["Later values today"] == 3)
    try:
        app.parse_csv("observation_date,X\n2020-01-01,1\n", "X_20200102")
        rejected = False
    except ValueError:
        rejected = True
    check("Current CSV rejected when vintage header required", rejected)
    prior_release = app.parse_csv("observation_date,X_20200101\n2020-01-01,1\n", "X_20200102")
    check("ALFRED last-release header earlier than cutoff is accepted", prior_release.iloc[0, 0] == 1)
    try:
        app.parse_csv("observation_date,X_20200103\n2020-01-01,1\n", "X_20200102")
        rejected = False
    except ValueError:
        rejected = True
    check("Vintage header later than cutoff is rejected", rejected)

    if args.series:
        series_id = app.validate_id(args.series)
        month_end = (date.today().replace(day=1) - timedelta(days=1)).isoformat()
        current = get(series_id)
        comparisons = []
        for cutoff in (month_end, today):
            vintage = get(series_id, cutoff)
            comparisons.append({"cutoff": cutoff, **app.compare(current["data"], vintage["data"])})
        results["personal_series"] = {"series": series_id, "comparisons": comparisons}
        if series_id == "DGS10":
            # Read the actual source rows independently of the app's pandas parser.
            raw_rows = {r["observation_date"]: r["DGS10"]
                        for r in csv.DictReader(StringIO(current["csv"]))}
            checked_values = []
            for measured_date in ("2026-01-02", "2026-03-31", "2026-09-01"):
                source_text = raw_rows[measured_date]
                source_value = Decimal(source_text)
                app_value = Decimal(str(current["data"].loc[measured_date, "value"]))
                check(f"DGS10 {measured_date}: raw FRED row matches app", source_value == app_value)
                checked_values.append({"measured_date": measured_date, "percent": str(source_value),
                                       "source_row": f"{measured_date},{source_text}",
                                       "app_value": str(app_value), "matched": source_value == app_value})
            results["source_value_checks"] = {
                "series": series_id, "source_url": current["url"],
                "downloaded_at_utc": current["downloaded_at_utc"],
                "method": "AI verified actual public CSV rows with standard-library csv/Decimal independently of the app parser",
                "values": checked_values}

    # Exercise the real Streamlit page using archived responses, no additional HTTP requests.
    def fake_current(series_id, download_day):
        if series_id == "INVALID_LAB17_ID":
            raise ValueError("Unknown series ID (intentional isolation test)")
        return get(series_id)

    def fake_vintage(series_id, as_known_on, download_day):
        return get(series_id, "2025-01-15" if series_id == "PAYEMS" else "2026-10-05")

    with patch.object(app, "download_current", side_effect=fake_current), patch.object(app, "download_vintage", side_effect=fake_vintage):
        page = AppTest.from_string("from asof_app import main\nmain()", default_timeout=30).run()
        check("Page defaults: four charts, one table, no exceptions", not page.exception and len(page.get("vega_lite_chart")) == 4
              and len(page.dataframe) == 1 and len(page.dataframe[0].value) == 4)
        page.text_input[0].set_value("PAYEMS").run()
        check("Typed PAYEMS adds a fifth chart and table row", not page.exception and len(page.dataframe[0].value) == 5
              and len(page.get("vega_lite_chart")) == 5)
        page.text_input[0].set_value("INVALID_LAB17_ID").run()
        check("Unknown ID leaves four other series working", not page.exception and len(page.error) == 1
              and len(page.dataframe[0].value) == 4)
        page.text_input[0].set_value("bad&id").run()
        check("Malformed ID rejected without breaking page", not page.exception and len(page.error) == 1
              and len(page.dataframe[0].value) == 4)
        page.text_input[0].set_value("").run()
        page.multiselect[0].set_value([]).run()
        check("Empty selection is handled", not page.exception and len(page.dataframe) == 0)

    if args.live_ui:
        page = AppTest.from_string("from asof_app import main\nmain()", default_timeout=120).run()
        results["live_default_diagnostics"] = {"errors": [e.value for e in page.error],
                                               "exceptions": [e.message for e in page.exception],
                                               "charts": len(page.get("vega_lite_chart")),
                                               "rows": len(page.dataframe[0].value) if page.dataframe else 0}
        check("Live page: four charts and four rows without errors", not page.exception and not page.error
              and len(page.get("vega_lite_chart")) == 4 and len(page.dataframe[0].value) == 4)
        page.date_input[1].set_value(date(2026, 10, 5)).run()
        table = page.dataframe[0].value
        check("Live date widget reproduces all four October 5 answers", not page.exception and not page.error
              and all(table.iloc[i]["Value known then"] == EXPECTED[s][1]
                      and table.iloc[i]["Last measured date known then"] == pd.Timestamp(EXPECTED[s][0])
                      for i, s in enumerate(EXPECTED)))
        page.date_input[1].set_value(date(2025, 1, 15))
        page.text_input[0].set_value("PAYEMS").run()
        table = page.dataframe[0].value
        check("Live typed PAYEMS and date widget reproduce revision probe", not page.exception and not page.error
              and len(table) == 5 and table.iloc[-1]["Value known then"] == 159536
              and table.iloc[-1]["Revised matching dates"] > 100)
        results["live_ui"] = {"tested_at_utc": datetime.now(timezone.utc).isoformat(),
                              "payems_page_rows": table.to_dict(orient="records")}

    results["passed"] = all(row["passed"] for row in results["checks"])
    (ROOT / "verification-results.json").write_text(json.dumps(results, indent=2, default=str) + "\n", encoding="utf-8")
    lines = [f"Lab 17 audit: {results['mode']}", f"UTC: {results['audited_at_utc']}"]
    lines += [f"{'PASS' if row['passed'] else 'FAIL'}: {row['check']}" for row in results["checks"]]
    lines += [f"PAYEMS December 2024: then {then_dec:,.0f}; current {now_dec:,.0f}; revised dates {probe['Revised matching dates']}"]
    (ROOT / "verification-results.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if args.live_ui:
        print(json.dumps(results["live_default_diagnostics"], indent=2))
    raise SystemExit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
