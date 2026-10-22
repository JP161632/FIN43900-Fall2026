"""Lab 14 risk engine extended for Lab 15; rates and weights are decimals.

The original report uses only the standard library. CSV estimation uses pandas.
"""

import math
import sys

# Editable course-authored training inputs, not market estimates.
# Row/column order in CORRELATIONS is the insertion order of SLEEVES.
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005, "reserve_eligible": True},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070, "reserve_eligible": True},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060, "reserve_eligible": False},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160, "reserve_eligible": False},
}
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
CPI_ESTIMATE = 0.025  # Labelled classroom estimate, not an observed CPI release.
REAL_RETURN_TARGET = 0.040
OBJECTIVE_RETURN = CPI_ESTIMATE + REAL_RETURN_TARGET  # 6.5%, lab convention.
BENCHMARK_WEIGHTS = {
    "Treasury bills": 0.0,
    "Treasury 10-year note": 0.0,
    "Investment-grade bond fund": 0.4,
    "Global equity index fund": 0.6,
}


def validate_inputs(sleeves, correlations):
    """Reject malformed rates, correlations and an invalid correlation matrix."""
    names = list(sleeves)
    count = len(names)
    if not count or len(correlations) != count or any(
        len(row) != count for row in correlations
    ):
        raise ValueError("Correlation table must have one row and column per sleeve.")
    for name, inputs in sleeves.items():
        if not math.isfinite(inputs["return"]):
            raise ValueError(f"Expected return must be finite: {name}.")
        if not math.isfinite(inputs["volatility"]) or inputs["volatility"] <= 0:
            raise ValueError(f"Volatility must be finite and positive: {name}.")
    for i in range(count):
        for j in range(count):
            value = correlations[i][j]
            label = f"{names[i]} / {names[j]}"
            if not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation for {label} must be between -1 and 1; got {value}.")
            if not math.isclose(value, correlations[j][i], rel_tol=0, abs_tol=1e-12):
                raise ValueError(f"Correlation table must be symmetric: {label}.")
        if not math.isclose(correlations[i][i], 1, rel_tol=0, abs_tol=1e-12):
            raise ValueError(f"Self-correlation must be 1: {names[i]}.")
    # A symmetric table inside [-1, 1] can still imply impossible joint risks.
    # An LDL decomposition checks positive semidefiniteness without dependencies.
    lower = [[0.0] * count for _ in names]
    diagonal = [0.0] * count
    for i in range(count):
        lower[i][i] = 1.0
        diagonal[i] = correlations[i][i] - sum(
            lower[i][k] ** 2 * diagonal[k] for k in range(i)
        )
        if diagonal[i] < -1e-12:
            raise ValueError("Correlation table must be positive semidefinite.")
        for j in range(i + 1, count):
            residual = correlations[j][i] - sum(
                lower[j][k] * lower[i][k] * diagonal[k] for k in range(i)
            )
            if abs(diagonal[i]) <= 1e-12:
                if abs(residual) > 1e-12:
                    raise ValueError("Correlation table must be positive semidefinite.")
            else:
                lower[j][i] = residual / diagonal[i]


def covariance_matrix(sleeves, correlations):
    """Cov(i,j) = correlation(i,j) * volatility(i) * volatility(j)."""
    validate_inputs(sleeves, correlations)
    volatilities = [inputs["volatility"] for inputs in sleeves.values()]
    return [
        [correlations[i][j] * vol_i * vol_j for j, vol_j in enumerate(volatilities)]
        for i, vol_i in enumerate(volatilities)
    ]


def validate_weights(weights, sleeves):
    """Require exactly the labelled sleeves, long-only, and a total of one."""
    if set(weights) != set(sleeves):
        raise ValueError("Weight labels must match the sleeve labels exactly.")
    if any(not math.isfinite(weight) or weight < 0 for weight in weights.values()):
        raise ValueError("Weights must be finite and nonnegative.")
    if not math.isclose(sum(weights.values()), 1, rel_tol=0, abs_tol=1e-12):
        raise ValueError("Weights must sum to 1 (100%).")


def equal_weights(sleeves):
    """Allocate the same fraction to every sleeve."""
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_weights(sleeves):
    """Normalize inverse standalone volatilities; this is not optimization."""
    inverse = {name: 1 / inputs["volatility"] for name, inputs in sleeves.items()}
    total = sum(inverse.values())
    return {name: value / total for name, value in inverse.items()}


def expected_return(weights, sleeves):
    """Weighted average of expected sleeve returns."""
    validate_weights(weights, sleeves)
    return sum(weights[name] * inputs["return"] for name, inputs in sleeves.items())


def portfolio_variance(weights, sleeves, covariance):
    """Sum all weighted covariance pairs, including both off-diagonal terms."""
    validate_weights(weights, sleeves)
    ordered_weights = [weights[name] for name in sleeves]
    count = len(ordered_weights)
    if len(covariance) != count or any(len(row) != count for row in covariance):
        raise ValueError("Covariance dimensions must match the sleeve order.")
    variance = 0.0
    for i, weight_i in enumerate(ordered_weights):
        for j, weight_j in enumerate(ordered_weights):
            variance += weight_i * weight_j * covariance[i][j]
    return variance


def portfolio_volatility(weights, sleeves, covariance):
    """Convert variance to volatility in the same units as the input rates."""
    variance = portfolio_variance(weights, sleeves, covariance)
    if not math.isfinite(variance) or variance < -1e-12:
        raise ValueError("Portfolio variance must be finite and nonnegative.")
    return math.sqrt(max(0.0, variance))  # Tolerate tiny floating-point error.


def reserve_eligible_weight(weights, sleeves):
    """Add weights in the reserve-eligible sleeves: bills and 10-year note."""
    validate_weights(weights, sleeves)
    return sum(weights[name] for name, inputs in sleeves.items() if inputs["reserve_eligible"])


def meets_objective(portfolio_return, objective):
    """Compare unrounded expected return against the objective."""
    return portfolio_return >= objective


def baseline_portfolios(sleeves):
    """Return the three required baselines with full-precision weights."""
    return {
        "Benchmark": dict(BENCHMARK_WEIGHTS),
        "Equal weight": equal_weights(sleeves),
        "Inverse volatility": inverse_volatility_weights(sleeves),
    }


def search_mix(sleeves, correlations, objective=0.065, reserve_minimum=0.03):
    """Exhaust every fully invested, long-only 5-point mix; return best or None.

    Rates/weights are decimals. Ties keep the first mix in enumeration order.
    The minimum is on estimated volatility within this grid, not all portfolios.
    """
    if not 3 <= len(sleeves) <= 6:
        raise ValueError("Use three to six assets.")
    if not math.isfinite(objective) or not math.isfinite(reserve_minimum):
        raise ValueError("Objective and reserve minimum must be finite.")
    if not 0 <= reserve_minimum <= 1:
        raise ValueError("Reserve minimum must be between 0 and 100%.")
    covariance = covariance_matrix(sleeves, correlations)
    names = list(sleeves)
    best = None

    def allocations(remaining, count):
        if count == 1:
            yield [remaining]
        else:
            for units in range(remaining + 1):
                for tail in allocations(remaining - units, count - 1):
                    yield [units] + tail

    for units in allocations(20, len(names)):
        weights = dict(zip(names, (unit / 20 for unit in units)))
        result_return = expected_return(weights, sleeves)
        reserve = reserve_eligible_weight(weights, sleeves)
        # Tiny tolerance handles decimal representation, never display rounding.
        if result_return + 1e-12 < objective or reserve + 1e-12 < reserve_minimum:
            continue
        risk = portfolio_volatility(weights, sleeves, covariance)
        if best is None or risk < best["volatility"] - 1e-12:
            best = {"weights": weights, "return": result_return,
                    "volatility": risk, "reserve": reserve}
    return best


def estimate_from_csv(source, last_36=False):
    """Estimate annual arithmetic means, sample volatilities and correlations.

    CSV: date then 3–6 positive monthly adjusted-price columns, oldest first.
    No filling, dropping or fabricated prices. Last 36 selects RETURNS, so it
    uses 37 prices. Returns are historical estimates, not forecasts.
    """
    import pandas as pd
    import csv
    import io
    from pathlib import Path

    try:
        raw = source.read() if hasattr(source, "read") else Path(source).read_bytes()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8-sig")
        headers = next(csv.reader(io.StringIO(raw)), [])
        if not headers or any(not name.strip() for name in headers) or len(set(headers)) != len(headers):
            raise ValueError("CSV column names must be present and unique.")
        frame = pd.read_csv(io.StringIO(raw))
        if not 4 <= len(frame.columns) <= 7 or len(set(frame.columns)) != len(frame.columns):
            raise ValueError("CSV needs a date column followed by three to six unique tickers.")
        dates = pd.to_datetime(frame.iloc[:, 0], errors="raise")
        if dates.isna().any() or not dates.is_monotonic_increasing or dates.duplicated().any():
            raise ValueError("Dates must be present, unique and oldest first.")
        months = dates.dt.year * 12 + dates.dt.month
        if not months.diff().iloc[1:].eq(1).all():
            raise ValueError("Use one price per consecutive month; missing/duplicate months are rejected.")
        prices = frame.iloc[:, 1:].apply(pd.to_numeric, errors="raise")
        if prices.isna().any().any() or not prices.map(lambda x: math.isfinite(x) and x > 0).all().all():
            raise ValueError("Every adjusted price must be finite and positive; no missing values.")
        if len(prices) < 37:
            raise ValueError("At least 37 monthly prices are required for 36 monthly returns; supply five years for the lab.")
        returns = prices.pct_change(fill_method=None).iloc[1:]
        if last_36:
            returns = returns.tail(36)
        means = returns.mean() * 12
        vols = returns.std(ddof=1) * math.sqrt(12)
        correlations = returns.corr().values.tolist()
        sleeves = {name: {"return": float(means[name]), "volatility": float(vols[name]),
                          "reserve_eligible": False} for name in prices.columns}
        validate_inputs(sleeves, correlations)
        metadata = {"price_start": str(dates.iloc[0].date()),
                    "price_end": str(dates.iloc[-1].date()),
                    "return_start": str(dates.iloc[returns.index[0]].date()),
                    "return_end": str(dates.iloc[returns.index[-1]].date()),
                    "price_rows": len(prices), "return_months": len(returns)}
        return sleeves, correlations, metadata
    except (ValueError, TypeError, IndexError) as error:
        raise ValueError(f"Cannot estimate monthly prices: {error}") from error


def main():
    try:
        covariance = covariance_matrix(SLEEVES, CORRELATIONS)
        print("Lab 14 - course-authored annual training values, not market estimates")
        print(f"CPI estimate: {CPI_ESTIMATE:.1%}; objective: {OBJECTIVE_RETURN:.2%}")
        print("Expected-return test only; full mandate compliance needs mandate.py.")
        print("Weights use full precision; displayed rounded weights may not total 100.0%.")
        for name, weights in baseline_portfolios(SLEEVES).items():
            result = expected_return(weights, SLEEVES)
            risk = portfolio_volatility(weights, SLEEVES, covariance)
            reserve = reserve_eligible_weight(weights, SLEEVES)
            print(f"\n{name}")
            for sleeve in SLEEVES:
                print(f"  {sleeve}: {weights[sleeve]:.1%}")
            print(f"  Expected return: {result:.2%}")
            print(f"  Volatility: {risk:.2%}")
            print(f"  Reserve-eligible weight: {reserve:.1%}")
            print(f"  Meets {OBJECTIVE_RETURN:.1%} objective? {'yes' if meets_objective(result, OBJECTIVE_RETURN) else 'no'}")
    except (ValueError, TypeError, KeyError) as error:
        print(f"Cannot run portfolio engine: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
