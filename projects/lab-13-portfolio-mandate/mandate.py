"""Meridian Foundation Reserve mandate checker (all amounts in USD millions)."""

# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": "none", "days": 0, "reserve_eligible": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True},
    "Global equity index fund": {
        "issuer": "diversified fund", "days": 2, "reserve_eligible": False,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund", "days": 3, "reserve_eligible": False,
    },
    "Private real estate fund": {
        "issuer": "diversified fund", "days": 90, "reserve_eligible": False,
    },
    "Acme Corp bonds": {"issuer": "Acme Corp", "days": 4, "reserve_eligible": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "days": 1, "reserve_eligible": False},
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # Attack portfolio: it satisfies every coded constraint, but may not pursue S2.
    "D": {
        "Cash": 3, "Treasury bills": 97, "Treasury 10-year note": 0,
        "Global equity index fund": 0, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90
ISSUER_LIMIT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def verdict(value, passes):
    """Return a consistently formatted measured value and rule result."""
    return f"{value:.1f} {'pass' if passes else 'FAIL'}"


def check_candidate(name, weights, reserve_minimum):
    """Measure every checkable mandate rule for one candidate."""
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = sum(
        weight for holding, weight in weights.items()
        if HOLDINGS[holding]["reserve_eligible"]
    )
    liquid_weight = sum(
        weight for holding, weight in weights.items()
        if HOLDINGS[holding]["days"] <= LIQUIDITY_WINDOW_DAYS
    )

    company_weights = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] = company_weights.get(issuer, 0) + weight
    largest_company = max(company_weights.values(), default=0)

    results = [
        ("Weights sum to 100", total_weight, abs(total_weight - 100) < 1e-9),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0),
        (f"Reserve >= {reserve_minimum:.1f}%", reserve_weight, reserve_weight >= reserve_minimum),
        (
            f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days >= {MINIMUM_LIQUID_SHARE:.1f}%",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUID_SHARE,
        ),
        (
            f"Largest single company <= {ISSUER_LIMIT:.1f}%",
            largest_company,
            largest_company <= ISSUER_LIMIT,
        ),
    ]

    print(f"\nCandidate {name}")
    for rule, value, passes in results:
        print(f"{rule}: {verdict(value, passes)}")
    print("Calendar-year loss: requires CIO clarification")

    failures = sum(not passes for _, _, passes in results)
    if failures:
        print(f"Verdict: fails {failures} rule(s)")
    else:
        print("Verdict: passes every checkable rule")


def main():
    reserve_minimum = (
        QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    )
    print(f"Reserve minimum: {reserve_minimum:.1f}% of the portfolio")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
