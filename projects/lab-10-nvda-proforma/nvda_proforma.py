"""NVIDIA five-year integrated pro forma and FCFE valuation (USD millions)."""

YEARS = range(2027, 2032)

# Editable forecast assumptions.  See nvda-proforma-lab.md for labels and reasons.
REVENUE_GROWTH = {2027: 0.30, 2028: 0.25, 2029: 0.20, 2030: 0.15, 2031: 0.10}
GROSS_MARGIN = {2027: 0.720, 2028: 0.725, 2029: 0.730, 2030: 0.730, 2031: 0.730}
R_AND_D_TO_REVENUE = 0.086
SGA_TO_GROSS_PROFIT = 0.030
INTEREST_EXPENSE = 259.0
TAX_RATE = 0.151
INVENTORY_DAYS = 125.0
AR_DAYS = 65.0
AP_DAYS = 57.3
OTHER_ASSETS_TO_REVENUE = 0.5832
OTHER_LIABILITIES_TO_REVENUE = 0.1446
DEPRECIATION_TO_OPENING_PPE = 2_843.0 / 10_383.0
CAPEX_TO_REVENUE = 6_042.0 / 215_938.0
ANNUAL_DEBT_REPAYMENT = 999.0
ANNUAL_DIVIDENDS = 974.0
ANNUAL_SHARE_REPURCHASES = 20_000.0
MINIMUM_CASH = 10_000.0
COST_OF_EQUITY = 0.1588
TERMINAL_GROWTH = 0.030
SHARES_OUTSTANDING = 24_304.0

# FY2026 opening balance sheet, from the FY2026 Form 10-K, Consolidated Balance Sheets.
OPENING = {
    "revenue": 215_938.0,
    "cash": 10_605.0,
    "accounts_receivable": 38_466.0,
    "inventory": 21_403.0,
    "ppe": 10_383.0,
    "other_assets": 125_946.0,
    "accounts_payable": 9_812.0,
    "other_liabilities": 31_230.0,
    "debt": 8_468.0,
    "equity": 157_293.0,
}


def assert_balanced(year: int, gap: float, cash: float) -> None:
    """Stop valuation when a forecast balance sheet is broken or illiquid."""
    if abs(gap) >= 0.05:
        raise ValueError(f"FY{year}E balance-sheet gap: {gap:.1f}")
    if cash + 1e-9 < MINIMUM_CASH:
        raise ValueError(
            f"FY{year}E cash {cash:.1f} is below the {MINIMUM_CASH:.1f} minimum"
        )


def build_projection() -> dict[int, dict[str, float]]:
    """Build integrated income statement, balance sheet, and cash-flow statement."""
    forecast: dict[int, dict[str, float]] = {}
    opening = OPENING.copy()

    for year in YEARS:
        revenue = opening["revenue"] * (1 + REVENUE_GROWTH[year])
        gross_profit = revenue * GROSS_MARGIN[year]
        cost_of_revenue = revenue - gross_profit
        research_and_development = revenue * R_AND_D_TO_REVENUE
        sga = gross_profit * SGA_TO_GROSS_PROFIT
        operating_income = gross_profit - research_and_development - sga
        pretax_income = operating_income - INTEREST_EXPENSE
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        accounts_receivable = revenue * AR_DAYS / 365.0
        inventory = cost_of_revenue * INVENTORY_DAYS / 365.0
        accounts_payable = cost_of_revenue * AP_DAYS / 365.0
        other_assets = revenue * OTHER_ASSETS_TO_REVENUE
        other_liabilities = revenue * OTHER_LIABILITIES_TO_REVENUE
        depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
        capital_spending = revenue * CAPEX_TO_REVENUE
        ppe = opening["ppe"] + capital_spending - depreciation
        debt_repayment = min(ANNUAL_DEBT_REPAYMENT, opening["debt"])
        debt = opening["debt"] - debt_repayment
        dividends = ANNUAL_DIVIDENDS
        share_repurchases = ANNUAL_SHARE_REPURCHASES
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
            "Interest expense": INTEREST_EXPENSE, "Pretax income": pretax_income,
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


def print_table(title: str, rows: list[str], forecast: dict[int, dict[str, float]]) -> None:
    print(f"\n{title}")
    print(f"{'Line':<34}" + "".join(f"FY{year}E".rjust(14) for year in YEARS))
    print("-" * 104)
    for row in rows:
        print(f"{row:<34}" + "".join(f"{forecast[y][row]:14,.1f}" for y in YEARS))


def main() -> None:
    if TERMINAL_GROWTH >= COST_OF_EQUITY:
        raise ValueError("Terminal growth must be below cost of equity.")
    forecast = build_projection()
    print_table("INCOME STATEMENT (USD millions)", [
        "Revenue", "Cost of revenue", "Gross profit", "R&D", "SG&A",
        "Operating income", "Interest expense", "Pretax income", "Tax", "Net income"], forecast)
    print_table("BALANCE SHEET (USD millions)", [
        "Cash", "Accounts receivable", "Inventory", "PP&E", "Other assets",
        "Total assets", "Accounts payable", "Other liabilities", "Debt", "Equity",
        "Total liabilities & equity"], forecast)
    print_table("CASH FLOW STATEMENT (USD millions)", [
        "Net income", "Depreciation", "Capital spending", "Change in accounts receivable",
        "Change in inventory", "Change in other assets", "Change in accounts payable",
        "Change in other liabilities", "Debt repayment", "Dividends", "Share repurchases",
        "Free cash flow to equity", "Net change in cash"], forecast)

    print("\nCHECKS")
    for year in YEARS:
        gap, cash = forecast[year]["Balance-sheet gap"], forecast[year]["Cash"]
        assert_balanced(year, gap, cash)
        print(f"FY{year}E: assets - liabilities - equity = {gap:.1f}; "
              f"cash >= minimum: {cash:.1f} >= {MINIMUM_CASH:.1f} PASS")

    positive_fcfe = {year: forecast[year]["Free cash flow to equity"] for year in YEARS
                     if forecast[year]["Free cash flow to equity"] > 0}
    pv_fcfe = sum(value / (1 + COST_OF_EQUITY) ** (year - 2026)
                  for year, value in positive_fcfe.items())
    terminal_fcfe = forecast[2031]["Free cash flow to equity"]
    terminal_value = terminal_fcfe * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1 + COST_OF_EQUITY) ** 5
    equity_value = pv_fcfe + pv_terminal
    print("\nVALUATION")
    print(f"Equity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2031: {pv_terminal / equity_value:.1%}")
    print(f"Value per share: ${equity_value / SHARES_OUTSTANDING:.2f}")


if __name__ == "__main__":
    main()
