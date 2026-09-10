"""NVIDIA five-year FCFF DCF. Currency values are USD millions unless noted."""

# Editable inputs
starting_fcff = 96895.891
growth_rates = [0.35, 0.25, 0.18, 0.12, 0.08]
wacc = 0.1588
terminal_growth = 0.03
non_operating_cash = 62556.0
debt = 8468.0
diluted_shares = 24514.0

# Editable sensitivity and reverse-DCF controls
wacc_values = [0.1488, 0.1588, 0.1688]
terminal_growth_values = [0.02, 0.03, 0.04]
target_share_price = 224.35
reverse_lower_shift = -0.05
reverse_upper_shift = 0.10


def calculate_dcf(
    fcff_start: float,
    annual_growth_rates: list[float],
    discount_rate: float,
    perpetual_growth: float,
    cash: float,
    total_debt: float,
    shares: float,
) -> dict[str, float | list[float]]:
    """Return the full five-year DCF calculation without printing."""
    if len(annual_growth_rates) != 5:
        raise ValueError("Enter exactly five annual growth rates.")
    if any(growth <= -1.0 for growth in annual_growth_rates):
        raise ValueError("Every annual growth rate must be greater than -100%.")
    if perpetual_growth >= discount_rate:
        raise ValueError(
            "Terminal growth must be less than WACC for the Gordon-growth formula."
        )
    if shares <= 0:
        raise ValueError("Diluted shares must be positive.")

    fcff_values = []
    fcff = fcff_start
    for growth in annual_growth_rates:
        fcff *= 1 + growth
        fcff_values.append(fcff)

    pv_explicit_fcff = sum(
        value / (1 + discount_rate) ** year
        for year, value in enumerate(fcff_values, start=1)
    )
    terminal_value_year_5 = (
        fcff_values[-1]
        * (1 + perpetual_growth)
        / (discount_rate - perpetual_growth)
    )
    pv_terminal_value = terminal_value_year_5 / (1 + discount_rate) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + cash - total_debt
    value_per_diluted_share = equity_value / shares
    pv_terminal_value_share_of_ev = pv_terminal_value / enterprise_value

    return {
        "fcff_values": fcff_values,
        "pv_explicit_fcff": pv_explicit_fcff,
        "terminal_value_year_5": terminal_value_year_5,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_diluted_share": value_per_diluted_share,
        "pv_terminal_value_share_of_ev": pv_terminal_value_share_of_ev,
    }


def value_per_share(
    annual_growth_rates: list[float],
    discount_rate: float,
    perpetual_growth: float,
) -> float:
    result = calculate_dcf(
        starting_fcff,
        annual_growth_rates,
        discount_rate,
        perpetual_growth,
        non_operating_cash,
        debt,
        diluted_shares,
    )
    return float(result["value_per_diluted_share"])


def solve_uniform_growth_shift(
    target: float, lower: float, upper: float, tolerance: float = 1e-10
) -> float | None:
    """Solve for one shift added to all five explicit annual growth rates."""
    if lower >= upper:
        raise ValueError("Reverse-DCF lower bound must be less than the upper bound.")
    if any(growth + lower <= -1.0 for growth in growth_rates):
        raise ValueError("Bracket invalid: it pushes an annual growth rate to -100% or below.")

    def difference(shift: float) -> float:
        shifted_growth = [growth + shift for growth in growth_rates]
        return value_per_share(shifted_growth, wacc, terminal_growth) - target

    low_value = difference(lower)
    high_value = difference(upper)
    if low_value == 0:
        return lower
    if high_value == 0:
        return upper
    if low_value * high_value > 0:
        return None

    low, high = lower, upper
    for _ in range(200):
        midpoint = (low + high) / 2
        mid_value = difference(midpoint)
        if abs(mid_value) <= tolerance:
            return midpoint
        if low_value * mid_value <= 0:
            high = midpoint
        else:
            low = midpoint
            low_value = mid_value
    return (low + high) / 2


def validate_training_case() -> None:
    """Silently reproduce the instructor grid and reverse-DCF checkpoint."""
    training_fcff = 100.0
    training_growth = [0.08, 0.06, 0.05, 0.04, 0.03]
    training_grid = [
        [28.60, 32.94, 39.02],
        [24.36, 27.50, 31.69],
        [21.06, 23.41, 26.44],
    ]

    for row, training_wacc in enumerate([0.09, 0.10, 0.11]):
        for column, training_terminal_growth in enumerate([0.02, 0.03, 0.04]):
            result = calculate_dcf(
                training_fcff,
                training_growth,
                training_wacc,
                training_terminal_growth,
                50.0,
                300.0,
                50.0,
            )
            actual = float(result["value_per_diluted_share"])
            assert round(actual, 2) == training_grid[row][column]

    def training_difference(shift: float) -> float:
        result = calculate_dcf(
            training_fcff,
            [growth + shift for growth in training_growth],
            0.10,
            0.03,
            50.0,
            300.0,
            50.0,
        )
        return float(result["value_per_diluted_share"]) - 30.0

    low, high = -0.05, 0.10
    low_value = training_difference(low)
    for _ in range(200):
        midpoint = (low + high) / 2
        mid_value = training_difference(midpoint)
        if abs(mid_value) <= 1e-10:
            break
        if low_value * mid_value <= 0:
            high = midpoint
        else:
            low = midpoint
            low_value = mid_value
    assert round(midpoint * 100, 2) == 1.78


def main() -> None:
    validate_training_case()
    result = calculate_dcf(
        starting_fcff,
        growth_rates,
        wacc,
        terminal_growth,
        non_operating_cash,
        debt,
        diluted_shares,
    )

    fcff_values = result["fcff_values"]
    for year, value in enumerate(fcff_values, start=1):
        print(f"FCFF Year {year}: {value:.4f}")
    print(f"PV of explicit FCFF: {result['pv_explicit_fcff']:.4f}")
    print(f"Terminal value at Year 5: {result['terminal_value_year_5']:.4f}")
    print(f"PV of terminal value: {result['pv_terminal_value']:.4f}")
    print(f"Enterprise value: {result['enterprise_value']:.4f}")
    print(f"Equity value: {result['equity_value']:.4f}")
    print(f"Value per diluted share: {result['value_per_diluted_share']:.4f}")
    print(
        "PV of terminal value as share of enterprise value: "
        f"{result['pv_terminal_value_share_of_ev']:.4f}"
    )

    print("\nSensitivity grid: value per diluted share ($)")
    header = "WACC \\ terminal growth | " + " | ".join(
        f"{growth:.2%}" for growth in terminal_growth_values
    )
    print(header)
    print("-" * len(header))
    for discount_rate in wacc_values:
        cells = []
        for perpetual_growth in terminal_growth_values:
            if perpetual_growth >= discount_rate:
                cells.append("invalid")
            else:
                cells.append(
                    f"{value_per_share(growth_rates, discount_rate, perpetual_growth):.2f}"
                )
        print(f"{discount_rate:.2%}                  | " + " | ".join(cells))

    print("\nReverse DCF")
    solved_shift = solve_uniform_growth_shift(
        target_share_price, reverse_lower_shift, reverse_upper_shift
    )
    print("Solved variable: uniform shift added to all five explicit growth rates")
    print(f"Target share price: ${target_share_price:.2f}")
    print(
        "Held fixed: starting FCFF, WACC, terminal growth, non-operating cash, "
        "debt, diluted shares, and five-year forecast structure"
    )
    if solved_shift is None:
        print(
            "Solved shift: no solution in bracket "
            f"[{reverse_lower_shift * 100:.2f}, {reverse_upper_shift * 100:.2f}] percentage points"
        )
    else:
        print(f"Solved shift: {solved_shift * 100:+.2f} percentage points")
        shifted = [growth + solved_shift for growth in growth_rates]
        print("Implied growth path: " + ", ".join(f"{growth:.2%}" for growth in shifted))


if __name__ == "__main__":
    main()
