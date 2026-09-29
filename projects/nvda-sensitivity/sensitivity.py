"""One-at-a-time extension of Lab 10; no third-party dependencies.

Run without arguments to save base evidence; supply --ranges for sensitivity.
"""
import argparse
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import math
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "lab-10-nvda-proforma" / "nvda_proforma.py"
YEARS = list(range(2027, 2032))
TOLERANCE = 1e-6  # USD millions; balance-sheet acceptance remains <0.05.
LIMITATION = (
    "Unavailable: Lab 10 discounts cash after dividends/buybacks and filters "
    "negative cash flows. Other assets also combine operating assets and "
    "marketable securities. Valuation needs reconciliation; no terminal value "
    "or per-share value is generated here. FCFE below is before shareholder "
    "payouts, under the inherited aggregate reinvestment convention."
)


def fresh_model():
    spec = importlib.util.spec_from_file_location("lab10", SOURCE)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    return model


def inputs(model):
    return {k: copy.deepcopy(v) for k, v in vars(model).items()
            if k.isupper() and k != "YEARS"}


def run(base, driver=None, replacement=None):
    model = fresh_model()
    assumptions = copy.deepcopy(base)
    if driver is not None:
        assumptions[driver] = copy.deepcopy(replacement)
    for key, value in assumptions.items():
        setattr(model, key, copy.deepcopy(value))
    changed = [key for key in base if base[key] != assumptions[key]]
    if changed not in ([], [driver]):
        raise AssertionError("More than one independent input changed")
    forecast = model.build_projection()
    checks = []
    opening_cash, opening_ppe, opening_equity = (
        base["OPENING"][k] for k in ("cash", "ppe", "equity"))
    for year, row in forecast.items():
        # Preserve Lab 10's cash linkage while correcting the payout label.
        row["Legacy cash after payouts"] = row.pop("Free cash flow to equity")
        row["FCFE before shareholder payouts"] = (
            row["Net income"] + row["Depreciation"] - row["Capital spending"]
            - row["Change in accounts receivable"] - row["Change in inventory"]
            - row["Change in other assets"] + row["Change in accounts payable"]
            + row["Change in other liabilities"] - row["Debt repayment"])
        residuals = {
            "balance_sheet": row["Total assets"] - row["Total liabilities & equity"],
            "cash_rollforward": row["Cash"] - opening_cash - row["Net change in cash"],
            "fcfe_payout_bridge": row["FCFE before shareholder payouts"]
                - row["Dividends"] - row["Share repurchases"] - row["Net change in cash"],
            "ppe_rollforward": row["PP&E"] - opening_ppe
                - row["Capital spending"] + row["Depreciation"],
            "equity_rollforward": row["Equity"] - opening_equity - row["Net income"]
                + row["Dividends"] + row["Share repurchases"],
        }
        valid = (all(math.isfinite(v) for v in row.values())
                 and abs(residuals["balance_sheet"]) < 0.05
                 and all(abs(v) <= TOLERANCE for k, v in residuals.items()
                         if k != "balance_sheet")
                 and row["Cash"] + 1e-9 >= base["MINIMUM_CASH"])
        checks.append({"year": year, "pass": valid, "residuals": residuals,
                       "cash": row["Cash"], "minimum_cash": base["MINIMUM_CASH"]})
        opening_cash, opening_ppe, opening_equity = (
            row[k] for k in ("Cash", "PP&E", "Equity"))
    final = forecast[2031]
    return {"inputs": assumptions, "changed_inputs": changed,
            "statements": forecast, "checks": checks,
            "valid": all(c["pass"] for c in checks),
            "operating_profit": final["Operating income"],
            "fcfe": final["FCFE before shareholder payouts"], "value_per_share": None}


def validate_config(config, base):
    drivers = config["drivers"]
    if len(drivers) != 2 or len({d["input"] for d in drivers}) != 2:
        raise ValueError("Exactly two different independent operating inputs required")
    allowed = {"REVENUE_GROWTH", "GROSS_MARGIN", "R_AND_D_TO_REVENUE",
               "SGA_TO_GROSS_PROFIT", "INVENTORY_DAYS", "AR_DAYS", "AP_DAYS",
               "OTHER_ASSETS_TO_REVENUE", "OTHER_LIABILITIES_TO_REVENUE",
               "DEPRECIATION_TO_OPENING_PPE", "CAPEX_TO_REVENUE"}
    locked = None
    if config.get("locked_record"):
        locked = (HERE / config["locked_record"]).resolve()
        if not locked.is_file():
            raise ValueError("Specified prediction record does not exist")
    for d in drivers:
        name = d["input"]
        if name not in allowed or not d.get("reason") or not d.get("units"):
            raise ValueError("Choose an existing operating input, units, and range reason")
        for level in ("lower", "base", "higher"):
            value = d[level]
            if isinstance(base[name], dict):
                value = {int(k): v for k, v in value.items()}
                if set(value) != set(YEARS):
                    raise ValueError("Paths must list all five forecast years")
                d[level] = value
            vals = value.values() if isinstance(value, dict) else [value]
            if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in vals):
                raise ValueError("Input values must be finite numbers")
        if d["base"] != base[name]:
            raise ValueError(f"{name}: supplied base differs from Lab 10")
        for y in YEARS:
            lo, mid, hi = [d[k][y] if isinstance(d[k], dict) else d[k]
                           for k in ("lower", "base", "higher")]
            if not lo <= mid <= hi:
                raise ValueError("Lower <= base <= higher required in every year")
        if d["lower"] == d["base"] or d["higher"] == d["base"]:
            raise ValueError("Each endpoint must change at least one forecast year")
    return locked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ranges", type=Path)
    args = parser.parse_args()
    model = fresh_model()
    base = inputs(model)
    original = io.StringIO()
    with contextlib.redirect_stdout(original):
        model.main()
    (HERE / "legacy-base-output.txt").write_text(
        "ARCHIVE ONLY: legacy FCFE label and valuation are unresolved.\n"
        + original.getvalue(), encoding="utf-8")
    (HERE / "base-inputs.json").write_text(json.dumps(base, indent=2), encoding="utf-8")
    before = run(base)
    results = {"base_before": before}
    report = ["# NVDA sensitivity: visible output", "",
              "Units: USD millions. Final forecast year: FY2031E.", "",
              "FCFE = modeled free cash flow to equity before dividends/buybacks.",
              "", LIMITATION, "",
              "| Run | Operating profit | Signed change | FCFE | Signed change | Checks |",
              "|---|---:|---:|---:|---:|---|"]

    def add_row(label, result):
        for metric in ("operating_profit", "fcfe"):
            result["delta_" + metric] = result[metric] - before[metric]
        report.append(f"| {label} | {result['operating_profit']:,.6f} | "
                      f"{result['delta_operating_profit']:+,.6f} | {result['fcfe']:,.6f} | "
                      f"{result['delta_fcfe']:+,.6f} | {'PASS' if result['valid'] else 'INVALID'} |")

    add_row("Base before", before)
    config = None
    if args.ranges:
        config = json.loads(args.ranges.read_text(encoding="utf-8"))
        locked = validate_config(config, base)
        prediction_hash = hashlib.sha256(locked.read_bytes()).hexdigest() if locked else None
        spans = []
        for d in config["drivers"]:
            group = []
            for level in ("lower", "base", "higher"):
                label = d["input"] + " / " + level
                result = run(base, d["input"], d[level])
                results[label] = result
                add_row(label, result)
                group.append(result)
            valid = [r for r in group if r["valid"]]
            spans.append({"driver": d["input"], "valid_runs": len(valid),
                          **{m: max(r[m] for r in valid) - min(r[m] for r in valid)
                             if valid else None for m in ("operating_profit", "fcfe")}})
        report += ["", "## Actual ranges and units", "", "```json",
                   json.dumps(config["drivers"], indent=2), "```", "",
                   "## Output spans over these ranges", "",
                   "Maximum minus minimum across valid runs only; incomplete groups are not ranked.",
                   "```json", json.dumps(spans, indent=2), "```"]
    else:
        prediction_hash, spans = None, []
        report += ["", "PENDING: input ranges.",
                   "No changed-input runs or driver ranking have been produced."]
    after = run(base)
    # Compare every statement cell and all inputs, not just selected outputs.
    largest = max(abs(before["statements"][y][k] - after["statements"][y][k])
                  for y in YEARS for k in before["statements"][y])
    restored = before["inputs"] == after["inputs"] and largest <= TOLERANCE
    results["base_after"] = after
    add_row_after = (f"Restored base: {'PASS' if restored and after['valid'] else 'FAIL'}; "
                     f"maximum statement difference = {largest:.9f} USD million; "
                     f"tolerance = {TOLERANCE} USD million. Inputs identical: "
                     f"{before['inputs'] == after['inputs']}.")
    report += ["", add_row_after, "", "## All annual checks", ""]
    for label, result in results.items():
        report.append(f"### {label}")
        for c in result["checks"]:
            report.append(f"- FY{c['year']}: {'PASS' if c['pass'] else 'INVALID'}; "
                          f"cash {c['cash']:,.6f} >= {c['minimum_cash']:,.6f}; "
                          f"residuals {json.dumps(c['residuals'])}")
    report += ["", "Full annual statements and independent inputs for every run: results.json."]
    evidence = {"generated_utc": datetime.now(timezone.utc).isoformat(),
                "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                "locked_prediction_sha256": prediction_hash, "config": config,
                "valuation_limitation": LIMITATION, "restored_base_pass": restored,
                "spans": spans, "runs": results}
    (HERE / "results.json").write_text(json.dumps(evidence, indent=2, allow_nan=False), encoding="utf-8")
    text = "\n".join(report) + "\n"
    (HERE / "visible-output.md").write_text(text, encoding="utf-8")
    print(text)
    if not restored or not all(r["valid"] for r in results.values()):
        raise SystemExit("Audit failed: investigate INVALID runs; do not rank them.")


if __name__ == "__main__":
    main()
