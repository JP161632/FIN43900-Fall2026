"""Audit saved sensitivity evidence independently of reporting calculations."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
runs = data["runs"]
base = runs["base_before"]
assert len(runs) == 8
assert data["source_sha256"] == hashlib.sha256(
    (HERE.parent / "lab-10-nvda-proforma/nvda_proforma.py").read_bytes()).hexdigest()
assert base["inputs"] == runs["base_after"]["inputs"]
assert base["statements"] == runs["base_after"]["statements"]


def close(a, b):
    return math.isclose(a, b, rel_tol=0, abs_tol=1e-6)


for label, result in runs.items():
    assert result["valid"] and len(result["checks"]) == 5
    differences = [k for k in base["inputs"] if result["inputs"][k] != base["inputs"][k]]
    expected = [] if label in ("base_before", "base_after") or label.endswith(" / base") else [label.split(" / ")[0]]
    assert differences == expected
    assert result["value_per_share"] is None
    for year, row in result["statements"].items():
        assert close(row["Total assets"], row["Total liabilities & equity"])
        assert row["Cash"] >= result["inputs"]["MINIMUM_CASH"]
        assert close(row["Operating income"], row["Revenue"] *
                     (result["inputs"]["GROSS_MARGIN"][year] *
                      (1-result["inputs"]["SGA_TO_GROSS_PROFIT"])
                      - result["inputs"]["R_AND_D_TO_REVENUE"]))
        assert close(row["FCFE before shareholder payouts"],
                     row["Net change in cash"] + row["Dividends"] + row["Share repurchases"])
    for metric, column in (("operating_profit", "Operating income"),
                           ("fcfe", "FCFE before shareholder payouts")):
        assert close(result[metric], result["statements"]["2031"][column])
        if "delta_" + metric in result:
            assert close(result["delta_" + metric], result[metric] - base[metric])
for span in data["spans"]:
    assert span["valid_runs"] == 3
    for metric in ("operating_profit", "fcfe"):
        values = [runs[span["driver"] + " / " + level][metric]
                  for level in ("lower", "base", "higher")]
        assert close(span[metric], max(values)-min(values))
selected = runs["GROSS_MARGIN / higher"]["statements"]["2031"]
original = base["statements"]["2031"]
profit_effect = (selected["Operating income"] - original["Operating income"]) * (1-base["inputs"]["TAX_RATE"])
wc_effect = -(selected["Change in inventory"] - original["Change in inventory"]) + (selected["Change in accounts payable"] - original["Change in accounts payable"])
assert close(profit_effect + wc_effect, runs["GROSS_MARGIN / higher"]["delta_fcfe"])
print("PASS: 8 runs, 40 annual statements; inputs, accounting, FCFE bridge, signed deltas, spans and exact restored base.")
print(f"Higher-margin final-year FCFE bridge: after-tax profit {profit_effect:.6f} + working capital {wc_effect:.6f}")
print("Student-authored locked prediction not supplied; no claim of full classroom-requirement completion.")
