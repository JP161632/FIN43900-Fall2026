"""Lab 16: point-in-time provenance gate; Python standard library only."""

# Editable inputs: row number is provenance, not part of duplicate identity.
DECISION_DATE = "2026-03-31"
TABLE = """row,ticker,month,published,index
1,AAA,2026-01,2026-02-10,101.0
2,AAA,2026-02,2026-03-10,104.0
3,AAA,2026-03,2026-04-10,109.0
4,AAA,2026-02,2026-03-25,103.0
5,BBB,2026-01,2026-02-10,98.0
6,BBB,2026-02,2026-03-10,97.0
7,BBB,2026-02,2026-03-10,97.0
8,BBB,2026-03,2026-04-10,92.0
9,CCC,2026-01,2026-02-10,110.0
10,CCC,2026-02,2026-04-05,112.0
11,,2026-02,2026-03-10,99.0
12,CCC,2026-02,2026-03-10,111.0
"""

import csv
from datetime import date
from decimal import Decimal
from io import StringIO


def load_rows(table):
    rows = []
    for item in csv.DictReader(StringIO(table)):
        month = date.fromisoformat(item["month"] + "-01")
        value = Decimal(item["index"])
        if not value.is_finite():
            raise ValueError("Index must be finite")
        rows.append(dict(row=int(item["row"]), ticker=item["ticker"].strip(),
                         month=month, published=date.fromisoformat(item["published"]),
                         index=value))
    if len({r["row"] for r in rows}) != len(rows):
        raise ValueError("Row numbers must be unique")
    return rows


def latest_vintages(rows):
    """Rule 4: caller supplies only publications eligible for its cutoff."""
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        previous = latest.get(key)
        if previous is None or row["published"] > previous["published"]:
            latest[key] = row
        elif (row["published"] == previous["published"]
              and row["index"] != previous["index"]):
            raise ValueError(f"Conflicting same-day publications for {key}")
    kept = sorted(latest.values(), key=lambda r: r["row"])
    kept_ids = {row["row"] for row in kept}
    removed = [row for row in rows if row["row"] not in kept_ids]
    return kept, removed


def filter_rows(rows, decision_date):
    cutoff = date.fromisoformat(decision_date)
    funnel = []
    missing = [r for r in rows if not r["ticker"]]
    identified = [r for r in rows if r["ticker"]]
    funnel.append(("Quarantined: no ticker", missing))
    seen, unique, duplicates = set(), [], []
    for row in identified:
        key = (row["ticker"], row["month"], row["published"], row["index"])
        if key in seen:
            duplicates.append(row)
        else:
            seen.add(key)
            unique.append(row)
    funnel.append(("Exact duplicate", duplicates))
    late = [r for r in unique if r["published"] > cutoff]
    eligible = [r for r in unique if r["published"] <= cutoff]
    funnel.append(("Published after decision date", late))
    panel, replaced = latest_vintages(eligible)
    funnel.append(("Older vintage replaced by a revision", replaced))
    # Naive comparison retains identity/dedup rules but ignores the cutoff.
    naive, _ = latest_vintages(unique)
    return panel, naive, funnel


def signals(panel):
    result = {}
    for ticker in sorted({r["ticker"] for r in panel}):
        history = sorted((r for r in panel if r["ticker"] == ticker),
                         key=lambda r: r["month"])
        latest = history[-1]
        month = latest["month"]
        previous_month = date(month.year - (month.month == 1),
                              12 if month.month == 1 else month.month - 1, 1)
        previous = next((r for r in history if r["month"] == previous_month), None)
        change = None
        if previous is not None and previous["index"] != 0:
            change = (latest["index"] / previous["index"] - 1) * 100
        result[ticker] = (month, change)
    return result


def report(table=TABLE, decision_date=DECISION_DATE):
    rows = load_rows(table)
    panel, naive, funnel = filter_rows(rows, decision_date)
    print(f"Decision date: {decision_date}; input rows: {len(rows)}")
    remaining = len(rows)
    for label, removed in funnel:
        remaining -= len(removed)
        ids = ", ".join(str(r["row"]) for r in removed) or "none"
        print(f"{label}: removed {len(removed)}; rows {ids}; remaining {remaining}")
    print("\nAs-of panel")
    print("Row | Ticker | Month measured | Published on | Index")
    for r in panel:
        print(f"{r['row']} | {r['ticker']} | {r['month']:%Y-%m} | "
              f"{r['published']} | {r['index']}")
    print("\nSignals: percent change from the immediately previous calendar month")
    asof_signals, naive_signals = signals(panel), signals(naive)
    for ticker in sorted(set(asof_signals) | set(naive_signals)):
        parts = []
        for label, values in (("As-of", asof_signals), ("Naive", naive_signals)):
            if ticker not in values:
                parts.append(f"{label}: unavailable (no eligible rows)")
                continue
            month, value = values[ticker]
            formatted = "unavailable (missing prior month or zero base)" if value is None else f"{value:+.2f}%"
            parts.append(f"{label}: {formatted} ({month:%B %Y})")
        print(f"{ticker} | " + " | ".join(parts))


if __name__ == "__main__":
    report()
