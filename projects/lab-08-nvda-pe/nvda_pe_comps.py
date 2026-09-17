"""Lab 08: NVIDIA P/E comparable-company valuation.

Prices are September 10, 2026 closes. Earnings are the latest annual GAAP
diluted EPS published by that date. The calculation uses no adjusted EPS.
"""

from statistics import median


TARGET = {
    "name": "NVIDIA",
    "ticker": "NVDA",
    "price": 218.36,
    "diluted_eps": 4.90,
}

PEERS = [
    {
        "name": "Advanced Micro Devices",
        "ticker": "AMD",
        "price": 503.60,
        "diluted_eps": 2.65,
    },
    {
        "name": "Broadcom",
        "ticker": "AVGO",
        "price": 360.83,
        "diluted_eps": 4.77,
    },
]


def ticker(company):
    return str(company.get("ticker", "")).strip().upper()


def positive_number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and value > 0
        and value != float("inf")
    )


def money(value):
    return f"${value:,.2f}"


def signed_money(value):
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.2f}"


def calculate(target, peers):
    print("NVIDIA P/E COMPARABLE-COMPANY ANALYSIS")
    print("Earnings basis: latest annual reported GAAP diluted EPS public by 2026-09-10")
    print("Price basis: unadjusted closing price on 2026-09-10 (USD per share)")
    print()

    valid = []
    print("Peer P/E multiples:")
    for peer in peers:
        if ticker(peer) == ticker(target):
            print(f"- {ticker(peer)}: excluded because it is the target")
        elif not positive_number(peer.get("price")):
            print(f"- {ticker(peer)}: unusable missing/nonpositive price")
        elif not positive_number(peer.get("diluted_eps")):
            print(f"- {ticker(peer)}: unusable missing/nonpositive diluted EPS")
        else:
            multiple = peer["price"] / peer["diluted_eps"]
            valid.append((peer, multiple))
            print(f"- {peer['name']} ({ticker(peer)}): {multiple:.6f}x")

    print()
    if not positive_number(target.get("diluted_eps")):
        print("Target implied prices: unusable missing/nonpositive target diluted EPS")
        return
    if not valid:
        print("Target implied prices: no usable peers")
        return

    multiples = [multiple for _, multiple in valid]
    full_estimate = median(multiples) * target["diluted_eps"]
    print(f"Peer median P/E: {median(multiples):.6f}x")
    if len(valid) == 1:
        print(f"Target reference estimate: {money(full_estimate)}")
        print("Target range: unavailable with one valid peer")
    else:
        print(f"Target implied minimum: {money(min(multiples) * target['diluted_eps'])}")
        print(f"Target implied median: {money(full_estimate)}")
        print(f"Target implied maximum: {money(max(multiples) * target['diluted_eps'])}")
        print(
            "Target implied range: "
            f"{money(min(multiples) * target['diluted_eps'])} to "
            f"{money(max(multiples) * target['diluted_eps'])}"
        )

    print()
    print("Leave-one-peer-out analysis:")
    for removed_peer, _ in valid:
        remaining = [multiple for peer, multiple in valid if peer is not removed_peer]
        if not remaining:
            print(f"- Remove {ticker(removed_peer)}: no estimate")
            continue
        estimate = median(remaining) * target["diluted_eps"]
        print(
            f"- Remove {ticker(removed_peer)}: {money(estimate)}; "
            f"change from full-peer estimate: {signed_money(estimate - full_estimate)}"
        )


if __name__ == "__main__":
    calculate(TARGET, PEERS)
