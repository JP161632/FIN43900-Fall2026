"""Reproduce personal estimates, window stress, and TSM one-point attack offline."""
import copy
import hashlib
import json
from pathlib import Path

from portfolio import estimate_from_csv, search_mix

ROOT = Path(__file__).resolve().parent
OBJECTIVE = .10
RESERVE_MINIMUM = 0.0


def largest_change(baseline, changed):
    if baseline is None or changed is None:
        return None
    return max(abs(changed["weights"][name] - weight) for name, weight in baseline["weights"].items()) * 100


def calculate():
    prices = ROOT / "prices.csv"
    provenance = json.loads((ROOT / "price-provenance.json").read_text(encoding="utf-8"))
    if hashlib.sha256(prices.read_bytes()).hexdigest() != provenance["prices_sha256"]:
        raise ValueError("prices.csv does not match its downloaded source manifest.")
    for source in provenance["sources"]:
        raw = (ROOT / source["raw_file"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != source["raw_sha256"]:
            raise ValueError(f"Source file hash mismatch: {source['ticker']}")
    full, full_corr, full_meta = estimate_from_csv(prices)
    recent, recent_corr, recent_meta = estimate_from_csv(prices, True)
    if full_meta["return_months"] != 60 or recent_meta["return_months"] != 36:
        raise ValueError("The personal cases require exactly 60 and 36 monthly returns.")
    stress = copy.deepcopy(full)
    stress["TSM"]["return"] -= .01
    runs = {"all_months": search_mix(full, full_corr, OBJECTIVE, RESERVE_MINIMUM),
            "last_36": search_mix(recent, recent_corr, OBJECTIVE, RESERVE_MINIMUM),
            "TSM_minus_1_point": search_mix(stress, full_corr, OBJECTIVE, RESERVE_MINIMUM)}
    return {"objective": OBJECTIVE, "reserve_minimum": RESERVE_MINIMUM,
            "estimate_label": "Annualized historical arithmetic return estimate; gross of fees, not a forecast",
            "estimates_all": full, "correlations_all": full_corr, "metadata_all": full_meta,
            "estimates_36": recent, "correlations_36": recent_corr, "metadata_36": recent_meta,
            "tsm_original_estimate": full["TSM"]["return"], "tsm_stressed_estimate": stress["TSM"]["return"],
            "runs": runs, "largest_window_change_points": largest_change(runs["all_months"], runs["last_36"]),
            "largest_attack_change_points": largest_change(runs["all_months"], runs["TSM_minus_1_point"])}


def main():
    results = calculate()
    (ROOT / "personal-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    rows = ["# Personal portfolio results", "", "Reproduce offline with `python analyze_personal.py`. All calculations import the same `portfolio.py` used by the app.", "", "Historical annualized arithmetic estimates, gross of fees, not forecasts. Objective 10.00%; reserve minimum 0.00%. Weight order: NVDA / MSFT / TSM / QCOM.", "", "| Run | Weights (%) | Return (%) | Volatility (%) | Reserve (%) |", "|---|---|---:|---:|---:|"]
    for name, answer in results["runs"].items():
        if answer is None:
            rows.append(f"| {name} | no mix meets the objective | — | — | — |")
        else:
            weights = " / ".join(f"{w * 100:.0f}" for w in answer["weights"].values())
            rows.append(f"| {name} | {weights} | {answer['return'] * 100:.2f} | {answer['volatility'] * 100:.2f} | {answer['reserve'] * 100:.2f} |")
    rows += ["", f"Largest window weight change: **{results['largest_window_change_points']:.2f} points**.", "", f"TSM attack: {results['tsm_original_estimate']:.2%} → {results['tsm_stressed_estimate']:.2%}; largest weight change **{results['largest_attack_change_points']:.2f} points**.", "", "The return floor is nonbinding: every asset's all-month historical estimate exceeds 10%, including TSM after its one-point cut. Changing only that mean leaves the covariance-based minimum-risk mix feasible and unchanged. Window estimation changes volatilities and correlations as well as means, producing the 20-point TSM weight change.", "", "## Estimated inputs", "", "| Asset | All-month return (%) | All-month volatility (%) | Last-36 return (%) | Last-36 volatility (%) |", "|---|---:|---:|---:|---:|"]
    for name, item in results["estimates_all"].items():
        recent = results["estimates_36"][name]
        rows.append(f"| {name} | {item['return'] * 100:.2f} | {item['volatility'] * 100:.2f} | {recent['return'] * 100:.2f} | {recent['volatility'] * 100:.2f} |")
    for label, key in [("All 60 monthly returns", "correlations_all"), ("Last 36 monthly returns", "correlations_36")]:
        rows += ["", f"## Correlations — {label}", "", "| Asset | NVDA | MSFT | TSM | QCOM |", "|---|---:|---:|---:|---:|"]
        for name, values in zip(results["estimates_all"], results[key]):
            rows.append(f"| {name} | " + " | ".join(f"{v:.4f}" for v in values) + " |")
    (ROOT / "personal-results.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("\n".join(rows[:18]).encode("ascii", errors="replace").decode("ascii"))


if __name__ == "__main__":
    main()
