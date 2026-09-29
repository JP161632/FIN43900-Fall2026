"""Lab 11: NVIDIA one-at-a-time sensitivity, USD millions.
Standalone extension of the preserved Lab 10 equations. No extra files required.
Run: python nvda_sensitivity.py (add --details for every annual statement).
"""
import argparse
import copy
import math

YEARS = list(range(2027, 2032))
TOLERANCE = 1e-6

BASE_INPUTS = {'REVENUE_GROWTH': {2027: 0.3, 2028: 0.25, 2029: 0.2, 2030: 0.15, 2031: 0.1},
 'GROSS_MARGIN': {2027: 0.72, 2028: 0.725, 2029: 0.73, 2030: 0.73, 2031: 0.73},
 'R_AND_D_TO_REVENUE': 0.086,
 'SGA_TO_GROSS_PROFIT': 0.03,
 'INTEREST_EXPENSE': 259.0,
 'TAX_RATE': 0.151,
 'INVENTORY_DAYS': 125.0,
 'AR_DAYS': 65.0,
 'AP_DAYS': 57.3,
 'OTHER_ASSETS_TO_REVENUE': 0.5832,
 'OTHER_LIABILITIES_TO_REVENUE': 0.1446,
 'DEPRECIATION_TO_OPENING_PPE': 0.27381296349802564,
 'CAPEX_TO_REVENUE': 0.027980253591308617,
 'ANNUAL_DEBT_REPAYMENT': 999.0,
 'ANNUAL_DIVIDENDS': 974.0,
 'ANNUAL_SHARE_REPURCHASES': 20000.0,
 'MINIMUM_CASH': 10000.0,
 'COST_OF_EQUITY': 0.1588,
 'TERMINAL_GROWTH': 0.03,
 'SHARES_OUTSTANDING': 24304.0,
 'OPENING': {'revenue': 215938.0,
             'cash': 10605.0,
             'accounts_receivable': 38466.0,
             'inventory': 21403.0,
             'ppe': 10383.0,
             'other_assets': 125946.0,
             'accounts_payable': 9812.0,
             'other_liabilities': 31230.0,
             'debt': 8468.0,
             'equity': 157293.0}}

DRIVERS = [{'input': 'REVENUE_GROWTH',
  'units': 'decimal fraction of prior-year revenue; endpoints shift base by minus/plus 5 '
           'percentage points in each FY2027-FY2031',
  'reason': 'Judgment: test a sustained faster or slower growth fade while preserving the existing '
            'declining path. Five percentage points each year creates a meaningful compounding '
            'test without extending recent historical growth rates. Endpoints are scenarios, not '
            'confidence bounds.',
  'lower': {2027: 0.25, 2028: 0.2, 2029: 0.15, 2030: 0.1, 2031: 0.05},
  'base': {2027: 0.3, 2028: 0.25, 2029: 0.2, 2030: 0.15, 2031: 0.1},
  'higher': {2027: 0.35, 2028: 0.3, 2029: 0.25, 2030: 0.2, 2031: 0.15}},
 {'input': 'GROSS_MARGIN',
  'units': 'decimal fraction of current-year revenue; endpoints shift base by minus/plus 2 '
           'percentage points in each FY2027-FY2031',
  'reason': 'Judgment: a two-percentage-point deviation tests weaker or stronger gross '
            'profitability while leaving the base recovery shape intact. It is a moderate '
            'variation relative to the filed FY2025 75.0% and FY2026 71.1% gross margins, not a '
            'statistically estimated interval.',
  'lower': {2027: 0.7, 2028: 0.705, 2029: 0.71, 2030: 0.71, 2031: 0.71},
  'base': {2027: 0.72, 2028: 0.725, 2029: 0.73, 2030: 0.73, 2031: 0.73},
  'higher': {2027: 0.74, 2028: 0.745, 2029: 0.75, 2030: 0.75, 2031: 0.75}}]

LIMITATION = (
    "Unavailable: Lab 10 discounts cash after dividends/buybacks and filters "
    "negative cash flows. Other assets also combine operating assets and "
    "marketable securities. Valuation needs reconciliation; no terminal value "
    "or per-share value is generated here. FCFE below is before shareholder "
    "payouts, under the inherited aggregate reinvestment convention."
)


def build_projection(assumptions) -> dict[int, dict[str, float]]:
    """Build integrated income statement, balance sheet, and cash-flow statement."""
    forecast: dict[int, dict[str, float]] = {}
    opening = assumptions['OPENING'].copy()

    for year in YEARS:
        revenue = opening["revenue"] * (1 + assumptions['REVENUE_GROWTH'][year])
        gross_profit = revenue * assumptions['GROSS_MARGIN'][year]
        cost_of_revenue = revenue - gross_profit
        research_and_development = revenue * assumptions['R_AND_D_TO_REVENUE']
        sga = gross_profit * assumptions['SGA_TO_GROSS_PROFIT']
        operating_income = gross_profit - research_and_development - sga
        pretax_income = operating_income - assumptions['INTEREST_EXPENSE']
        tax = max(0.0, pretax_income) * assumptions['TAX_RATE']
        net_income = pretax_income - tax

        accounts_receivable = revenue * assumptions['AR_DAYS'] / 365.0
        inventory = cost_of_revenue * assumptions['INVENTORY_DAYS'] / 365.0
        accounts_payable = cost_of_revenue * assumptions['AP_DAYS'] / 365.0
        other_assets = revenue * assumptions['OTHER_ASSETS_TO_REVENUE']
        other_liabilities = revenue * assumptions['OTHER_LIABILITIES_TO_REVENUE']
        depreciation = opening["ppe"] * assumptions['DEPRECIATION_TO_OPENING_PPE']
        capital_spending = revenue * assumptions['CAPEX_TO_REVENUE']
        ppe = opening["ppe"] + capital_spending - depreciation
        debt_repayment = min(assumptions['ANNUAL_DEBT_REPAYMENT'], opening["debt"])
        debt = opening["debt"] - debt_repayment
        dividends = assumptions['ANNUAL_DIVIDENDS']
        share_repurchases = assumptions['ANNUAL_SHARE_REPURCHASES']
        equity = opening["equity"] + net_income - dividends - share_repurchases

        change_ar = accounts_receivable - opening["accounts_receivable"]
        change_inventory = inventory - opening["inventory"]
        change_other_assets = other_assets - opening["other_assets"]
        change_ap = accounts_payable - opening["accounts_payable"]
        change_other_liabilities = other_liabilities - opening["other_liabilities"]
        fcfe = (
            net_income + depreciation - capital_spending - change_ar - change_inventory
            - change_other_assets + change_ap + change_other_liabilities
            - debt_repayment - dividends - share_repurchases
        )
        cash = opening["cash"] + fcfe
        assets = cash + accounts_receivable + inventory + ppe + other_assets
        liabilities_and_equity = accounts_payable + other_liabilities + debt + equity
        gap = assets - liabilities_and_equity

        forecast[year] = {
            "Revenue": revenue, "Cost of revenue": cost_of_revenue,
            "Gross profit": gross_profit, "R&D": research_and_development,
            "SG&A": sga, "Operating income": operating_income,
            "Interest expense": assumptions['INTEREST_EXPENSE'], "Pretax income": pretax_income,
            "Tax": tax, "Net income": net_income, "Cash": cash,
            "Accounts receivable": accounts_receivable, "Inventory": inventory,
            "PP&E": ppe, "Other assets": other_assets, "Total assets": assets,
            "Accounts payable": accounts_payable, "Other liabilities": other_liabilities,
            "Debt": debt, "Equity": equity,
            "Total liabilities & equity": liabilities_and_equity,
            "Depreciation": depreciation, "Capital spending": capital_spending,
            "Change in accounts receivable": change_ar,
            "Change in inventory": change_inventory,
            "Change in other assets": change_other_assets,
            "Change in accounts payable": change_ap,
            "Change in other liabilities": change_other_liabilities,
            "Debt repayment": debt_repayment, "Dividends": dividends,
            "Share repurchases": share_repurchases, "Free cash flow to equity": fcfe,
            "Net change in cash": cash - opening["cash"], "Balance-sheet gap": gap,
        }
        opening = {"revenue": revenue, "cash": cash,
                   "accounts_receivable": accounts_receivable, "inventory": inventory,
                   "ppe": ppe, "other_assets": other_assets,
                   "accounts_payable": accounts_payable,
                   "other_liabilities": other_liabilities, "debt": debt, "equity": equity}
    return forecast


def run(base, driver=None, replacement=None):
    assumptions = copy.deepcopy(base)
    if driver is not None:
        assumptions[driver] = copy.deepcopy(replacement)
    changed = [key for key in base if base[key] != assumptions[key]]
    if changed not in ([], [driver]):
        raise AssertionError("More than one independent input changed")
    forecast = build_projection(assumptions)
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



def analyze():
    base = copy.deepcopy(BASE_INPUTS)
    before = run(base)
    results = {"Base before": before}
    spans = {}
    for driver in DRIVERS:
        name = driver["input"]
        assert driver["base"] == base[name]
        for year in YEARS:
            assert driver["lower"][year] <= base[name][year] <= driver["higher"][year]
        group = []
        for level in ("lower", "base", "higher"):
            result = run(base, name, driver[level])
            expected = [] if level == "base" else [name]
            assert result["changed_inputs"] == expected
            for metric in ("operating_profit", "fcfe"):
                result["delta_" + metric] = result[metric] - before[metric]
            results[name + " / " + level] = result
            group.append(result)
        valid = [r for r in group if r["valid"]]
        spans[name] = {metric: max(r[metric] for r in valid) - min(r[metric] for r in valid)
                       if valid else None for metric in ("operating_profit", "fcfe")}
        spans[name]["valid_runs"] = len(valid)
    after = run(base)
    results["Base restored"] = after
    difference = max(abs(before["statements"][y][k] - after["statements"][y][k])
                     for y in YEARS for k in before["statements"][y])
    restored = (before["inputs"] == after["inputs"] == BASE_INPUTS
                and difference <= TOLERANCE)
    return results, spans, restored, difference


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", action="store_true", help="Print every statement line for every run")
    args = parser.parse_args()
    results, spans, restored, difference = analyze()
    print("LAB 11 - NVIDIA SENSITIVITY")
    print("Final-year FY2031E outputs: USD millions. FCFE before shareholder payouts.")
    print("Value per share: " + LIMITATION)
    print("\nINPUT PATHS: FY2027, FY2028, FY2029, FY2030, FY2031")
    for driver in DRIVERS:
        print(driver["input"], "-", driver["units"])
        for level in ("lower", "base", "higher"):
            print(level, [driver[level][y] for y in YEARS])
        print("Judgment reason:", driver["reason"])
    print("\nRun | Operating profit | Change | FCFE | Change | Status")
    before = results["Base before"]
    for label, result in results.items():
        print(f"{label} | {result['operating_profit']:.6f} | "
              f"{result['operating_profit']-before['operating_profit']:+.6f} | "
              f"{result['fcfe']:.6f} | {result['fcfe']-before['fcfe']:+.6f} | "
              f"{'PASS' if result['valid'] else 'INVALID'}")
    print("\nSPANS OVER THESE RANGES (max minus min of valid results)")
    for name, span in spans.items():
        print(name, span)
    print(f"Restored base: {'PASS' if restored else 'FAIL'}; max difference {difference:.9f}; tolerance {TOLERANCE}.")
    print("\nANNUAL CHECKS: BS gap must be <0.05; other residuals <=0.000001; cash >=10000.")
    for label, result in results.items():
        for check in result["checks"]:
            residual = max(abs(v) for v in check["residuals"].values())
            print(f"{label}, FY{check['year']}: {'PASS' if check['pass'] else 'INVALID'}; "
                  f"cash {check['cash']:.6f}; max residual {residual:.3e}")
    if args.details:
        for label, result in results.items():
            print("\nFULL STATEMENTS:", label)
            for line in result["statements"][2027]:
                print(line, " | ".join(f"{result['statements'][year][line]:.6f}" for year in YEARS))
    if not restored or not all(r["valid"] for r in results.values()):
        raise SystemExit("INVALID: investigate failures; do not rank incomplete groups.")


if __name__ == "__main__":
    main()
