"""Lab 07: P/E comparable-company valuation for Asbury Automotive.

Edit TARGET and PEERS below to reuse the calculator. This file uses only the
Python standard library and intentionally makes no cash/debt adjustment because
P/E is already an equity-value multiple.
"""

from statistics import median


# Editable inputs -----------------------------------------------------------
TARGET = {
    "name": "Asbury Automotive",
    "ticker": "ABG",
    "price": 243.03,
    "diluted_eps": 21.50,
}

PEERS = [
    {
        "name": "AutoNation",
        "ticker": "AN",
        "price": 169.84,
        "diluted_eps": 16.92,
    },
    {
        "name": "Group 1 Automotive",
        "ticker": "GPI",
        "price": 421.48,
        "diluted_eps": 36.81,
    },
]
# End editable inputs -------------------------------------------------------


def normalized_ticker(company):
    """Return a ticker normalized for comparison and deduplication."""
    return str(company.get("ticker", "")).strip().upper()


def positive_number(value):
    """Return True only for a numeric, finite, strictly positive value."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value > 0
        and value != float("inf")
    )


def peer_status(peer):
    """Explain whether a peer has the inputs needed for a meaningful P/E."""
    if not positive_number(peer.get("price")):
        return "not meaningful: missing or nonpositive price"
    if not positive_number(peer.get("diluted_eps")):
        return "not meaningful: missing or nonpositive diluted EPS"
    return "valid"


def prepare_peers(target, peers):
    """Exclude the target and duplicate tickers, retaining first occurrences."""
    target_ticker = normalized_ticker(target)
    seen = set()
    prepared = []
    exclusions = []

    for peer in peers:
        ticker = normalized_ticker(peer)
        label = ticker or str(peer.get("name", "unnamed peer"))
        if ticker and ticker == target_ticker:
            exclusions.append(f"{label}: excluded because it is the target")
        elif ticker and ticker in seen:
            exclusions.append(f"{label}: excluded as a duplicate peer")
        else:
            if ticker:
                seen.add(ticker)
            prepared.append(peer)
    return prepared, exclusions


def money(value):
    return f"${value:,.2f}"


def signed_money(value):
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.2f}"


def calculate(target, peers):
    prepared, exclusions = prepare_peers(target, peers)
    valid = []

    print("ASBURY AUTOMOTIVE P/E COMPARABLE-COMPANY ANALYSIS")
    print("Earnings basis: FY2024 total GAAP diluted EPS")
    print("Price date: December 31, 2024")
    print()

    if exclusions:
        print("Input exclusions:")
        for exclusion in exclusions:
            print(f"- {exclusion}")
        print()

    print("Peer P/E multiples:")
    for peer in prepared:
        status = peer_status(peer)
        label = f"{peer.get('name', 'Unnamed')} ({normalized_ticker(peer) or 'no ticker'})"
        if status == "valid":
            multiple = peer["price"] / peer["diluted_eps"]
            valid.append((peer, multiple))
            print(f"- {label}: {multiple:.6f}x")
        else:
            print(f"- {label}: {status}")

    print()
    target_eps = target.get("diluted_eps")
    if not positive_number(target_eps):
        print("Target implied prices: not meaningful: missing or nonpositive diluted EPS")
        print("Leave-one-peer-out analysis: not meaningful without a valid target EPS")
        return

    if not valid:
        print("Target implied prices: no usable peers")
        print("Leave-one-peer-out analysis: no usable peers")
        return

    multiples = [multiple for _, multiple in valid]
    median_multiple = median(multiples)
    full_estimate = median_multiple * target_eps

    print(f"Peer median P/E: {median_multiple:.6f}x")
    if len(valid) == 1:
        print(f"Target reference estimate: {money(full_estimate)}")
        print("Target range: unavailable with one valid peer")
    else:
        print(f"Target implied minimum: {money(min(multiples) * target_eps)}")
        print(f"Target implied median: {money(full_estimate)}")
        print(f"Target implied maximum: {money(max(multiples) * target_eps)}")
        print(
            "Target implied range: "
            f"{money(min(multiples) * target_eps)} to {money(max(multiples) * target_eps)}"
        )

    print()
    print("Leave-one-peer-out analysis:")
    for removed_peer, _ in valid:
        remaining = [
            multiple
            for peer, multiple in valid
            if peer is not removed_peer
        ]
        removed_label = normalized_ticker(removed_peer) or removed_peer.get("name", "peer")
        if not remaining:
            print(f"- Remove {removed_label}: no estimate (no usable peers remain)")
            continue
        remaining_estimate = median(remaining) * target_eps
        change = remaining_estimate - full_estimate
        print(
            f"- Remove {removed_label}: {money(remaining_estimate)}; "
            f"change from full-peer estimate: {signed_money(change)}"
        )


if __name__ == "__main__":
    calculate(TARGET, PEERS)
