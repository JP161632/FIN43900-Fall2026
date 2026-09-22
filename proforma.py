"""ABG five-year integrated pro forma and equity valuation (USD millions)."""

YEARS = range(2026, 2031)

# Assumptions
ORGANIC_GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_TO_GROSS_PROFIT = {
    2026: 0.665,
    2027: 0.655,
    2028: 0.645,
    2029: 0.645,
    2030: 0.645,
}
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3_070.4
IMPAIRMENT = 120.0
CAPITAL_SPENDING = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365
FLOOR_PLAN_TO_INVENTORY = 2_027.0 / 2_135.8
OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349

OPENING = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "term_debt": 3_572.0,
    "revolver": 0.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
}


def assert_balanced(year, gap, cash):
    """Refuse a forecast year that does not balance or meet minimum cash."""
    if abs(gap) >= 0.05:
        raise ValueError(f"FY{year}E balance-sheet gap: {gap:.1f}")
    if cash + 1e-9 < MINIMUM_CASH:
        raise ValueError(
            f"FY{year}E cash {cash:.1f} is below the {MINIMUM_CASH:.1f} minimum"
        )


def build_projection():
    forecast = {}
    opening = OPENING.copy()

    for year in YEARS:
        revenue = opening["revenue"] * (1 + ORGANIC_GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        sga = gross_profit * SGA_TO_GROSS_PROFIT[year]
        depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
        impairment = IMPAIRMENT
        operating_income = gross_profit - sga - depreciation - impairment
        floor_plan_interest = opening["floor_plan"] * FLOOR_PLAN_RATE
        term_debt_interest = opening["term_debt"] * TERM_DEBT_RATE
        revolver_interest = opening["revolver"] * REVOLVER_RATE
        interest = floor_plan_interest + term_debt_interest + revolver_interest
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        cost_of_sales = revenue - gross_profit
        inventory = cost_of_sales * INVENTORY_DAYS / 365
        floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
        ppe = opening["ppe"] + CAPITAL_SPENDING - depreciation
        revenue_change = revenue - opening["revenue"]
        other_working_capital_change = (
            OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE * revenue_change
        )
        other_assets = (
            opening["other_assets"] + other_working_capital_change - impairment
        )
        term_debt = opening["term_debt"] - DEBT_REPAYMENT
        other_liabilities = opening["other_liabilities"]
        equity = opening["equity"] + net_income - SHARE_BUYBACK

        inventory_change = inventory - opening["inventory"]
        floor_plan_change = floor_plan - opening["floor_plan"]
        fcfe = (
            net_income
            + depreciation
            + impairment
            - CAPITAL_SPENDING
            - inventory_change
            - other_working_capital_change
            + floor_plan_change
            - DEBT_REPAYMENT
        )

        cash = opening["cash"] + fcfe - SHARE_BUYBACK
        revolver = opening["revolver"]
        if cash < MINIMUM_CASH:
            draw = min(MINIMUM_CASH - cash, REVOLVER_LIMIT - revolver)
            cash += draw
            revolver += draw
        elif cash > MINIMUM_CASH and revolver > 0:
            repayment = min(cash - MINIMUM_CASH, revolver)
            cash -= repayment
            revolver -= repayment

        assets = cash + inventory + ppe + other_assets
        liabilities_and_equity = (
            floor_plan + term_debt + revolver + other_liabilities + equity
        )
        gap = assets - liabilities_and_equity

        forecast[year] = {
            "Revenue": revenue,
            "Gross profit": gross_profit,
            "SG&A": sga,
            "Depreciation": depreciation,
            "Impairment": impairment,
            "Operating income": operating_income,
            "Interest expense": interest,
            "Pretax income": pretax_income,
            "Tax": tax,
            "Net income": net_income,
            "Cash": cash,
            "Inventory": inventory,
            "PP&E": ppe,
            "Other assets": other_assets,
            "Total assets": assets,
            "Floor plan": floor_plan,
            "Term debt": term_debt,
            "Revolver": revolver,
            "Other liabilities": other_liabilities,
            "Equity": equity,
            "Total liabilities & equity": liabilities_and_equity,
            "Capital spending": CAPITAL_SPENDING,
            "Change in inventory": inventory_change,
            "Change in other working capital": other_working_capital_change,
            "Change in floor plan": floor_plan_change,
            "Debt repayment": DEBT_REPAYMENT,
            "Share buyback": SHARE_BUYBACK,
            "Free cash flow to equity": fcfe,
            "Balance-sheet gap": gap,
        }

        opening = {
            "revenue": revenue,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "floor_plan": floor_plan,
            "term_debt": term_debt,
            "revolver": revolver,
            "other_liabilities": other_liabilities,
            "equity": equity,
        }

    return forecast


def print_table(title, rows, forecast):
    print(f"\n{title}")
    print(f"{'Line':<32}" + "".join(f"FY{year}E".rjust(12) for year in YEARS))
    print("-" * 92)
    for row in rows:
        print(f"{row:<32}" + "".join(f"{forecast[y][row]:12.1f}" for y in YEARS))


def main():
    forecast = build_projection()

    print_table(
        "INCOME STATEMENT (USD millions)",
        [
            "Revenue", "Gross profit", "SG&A", "Depreciation", "Impairment",
            "Operating income", "Interest expense", "Pretax income", "Tax",
            "Net income",
        ],
        forecast,
    )
    print_table(
        "BALANCE SHEET (USD millions)",
        [
            "Cash", "Inventory", "PP&E", "Other assets", "Total assets",
            "Floor plan", "Term debt", "Revolver", "Other liabilities",
            "Equity", "Total liabilities & equity",
        ],
        forecast,
    )
    print_table(
        "CASH FLOW STATEMENT (USD millions)",
        [
            "Net income", "Depreciation", "Impairment", "Capital spending",
            "Change in inventory", "Change in other working capital",
            "Change in floor plan", "Debt repayment", "Share buyback",
            "Free cash flow to equity",
        ],
        forecast,
    )

    print("\nCHECKS")
    for year in YEARS:
        gap = forecast[year]["Balance-sheet gap"]
        cash = forecast[year]["Cash"]
        assert_balanced(year, gap, cash)
        print(
            f"FY{year}E: assets - liabilities - equity = {gap:.1f}; "
            f"cash >= minimum: {cash:.1f} >= {MINIMUM_CASH:.1f} PASS"
        )

    pv_fcfe = sum(
        forecast[year]["Free cash flow to equity"] / (1 + COST_OF_EQUITY) ** n
        for n, year in enumerate(YEARS, start=1)
    )
    normalized_2030_fcfe = (
        forecast[2030]["Free cash flow to equity"] + DEBT_REPAYMENT
    )
    terminal_value = (
        normalized_2030_fcfe
        * (1 + TERMINAL_GROWTH)
        / (COST_OF_EQUITY - TERMINAL_GROWTH)
    )
    pv_terminal_value = terminal_value / (1 + COST_OF_EQUITY) ** 5
    equity_value = pv_fcfe + pv_terminal_value
    share_after_2030 = pv_terminal_value / equity_value
    value_per_share = equity_value / SHARES_OUTSTANDING

    print("\nVALUATION")
    print(f"Equity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {share_after_2030:.1%}")
    print(f"Value per share: ${value_per_share:.2f}")


if __name__ == "__main__":
    main()
