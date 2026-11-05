"""Shared SEC facts and deterministic investor checks; memos remain model judgments."""
import argparse
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location("lab18_edgar", ROOT / ".agents/skills/buffett-edgar/scripts/edgar_facts.py")
edgar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edgar)
EXTRA = {"liabilities": "Liabilities", "current_assets": "AssetsCurrent", "current_liabilities": "LiabilitiesCurrent"}
INVESTORS = ("Buffett", "Graham", "Burry")


def threshold():
    config = ROOT / ".agents/skills/graham-edgar/settings.json"
    value = float(json.loads(config.read_text(encoding="utf-8"))["current_ratio_threshold"])
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Graham threshold must be finite and positive.")
    return value


def select_instant(facts, tag, end):
    records = [r for r in edgar.observations(facts, tag)
               if r.get("form") == "10-K" and r.get("end") == end
               and not r.get("start") and r.get("val") is not None]
    if not records:
        return {"value": None, "tag": "not found", "end": end, "searched_tags": [tag]}
    r = max(records, key=lambda r: (r.get("filed", ""), r.get("accn", "")))
    return {"value": r["val"], "tag": tag, "end": end, "form": "10-K",
            "filed": r.get("filed"), "accession": r.get("accn")}


def ratio(numerator, denominator, formula):
    n, d = numerator["value"], denominator["value"]
    return {"value": n / d if n is not None and d is not None and d > 0 else None,
            "tag": formula, "missing": "not known"}


def check(values, predicate, complete=True):
    if not complete or any(v is None for v in values):
        return "not known"
    return "pass" if predicate(values) else "fail"


def graham_checks(rows, hurdle):
    """Latest liquidity needs one input ratio; annual earnings need all five years."""
    latest = rows[-1]["current_ratio"]["value"] if rows else None
    income = [row["net_income"]["value"] for row in rows]
    complete = len(rows) == 5
    return {
        f"Current ratio >= {hurdle:.1f}, latest year": check([latest], lambda v: v[0] >= hurdle),
        "Net income positive every year": check(income, lambda v: all(x > 0 for x in v), complete),
        "Net income grew, first to last": check(income, lambda v: v[-1] > v[0], complete),
    }


def burry_checks(rows):
    pairs = [row[f]["value"] for row in rows for f in ("operating_cash_flow", "net_income")]
    leverage = rows[-1]["liabilities_to_equity"]["value"] if rows else None
    return {
        "Operating cash flow >= net income every year": check(
            pairs, lambda v: all(v[i] >= v[i+1] for i in range(0, len(v), 2)), len(rows) == 5),
        "Liabilities <= twice equity, latest year": check([leverage], lambda v: v[0] <= 2),
    }


def extend(base, facts, hurdle=None):
    result = deepcopy(base)
    hurdle = threshold() if hurdle is None else hurdle
    if not math.isfinite(hurdle) or hurdle <= 0:
        raise ValueError("Graham threshold must be finite and positive.")
    for row in result["rows"]:
        row.update({field: select_instant(facts, tag, row["fiscal_year_end"]) for field, tag in EXTRA.items()})
        row["current_ratio"] = ratio(row["current_assets"], row["current_liabilities"], "AssetsCurrent / LiabilitiesCurrent")
        row["liabilities_to_equity"] = ratio(row["liabilities"], row["equity"], "Liabilities / StockholdersEquity")
    result["graham_threshold"] = hurdle
    result["panel"] = {"Buffett": result["checks"], "Graham": graham_checks(result["rows"], hurdle),
                       "Burry": burry_checks(result["rows"])}
    return result


def run(ticker, refresh=False, offline=True, hurdle=None):
    base = edgar.run(ticker, refresh=refresh, offline=offline)
    path = edgar.LAB / "evidence" / f'{base["ticker"]}-companyfacts.json'
    # Verify the same archived bytes and metadata used by Lab 18 before extending.
    facts, _ = edgar.download(base["source"]["url"], path, offline=True)
    return extend(base, facts, hurdle)


def shown(cell, field):
    if field in ("current_ratio", "liabilities_to_equity"):
        return "not known" if cell["value"] is None else str(Decimal(str(cell["value"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    return edgar.display(cell, field == "roe")


def summary(checks):
    values = list(checks.values())
    return f'{values.count("pass")} of {len(values)} pass; {values.count("fail")} fail; {values.count("not known")} not known'


def report_text(result):
    text = [edgar.report_text(result), "## Added balance-sheet facts and ratios", "Amounts: USD millions. Ratios: times."]
    fields = list(EXTRA) + ["current_ratio", "liabilities_to_equity"]
    text += ["| Fiscal-year end | " + " | ".join(fields) + " |", "|---|" + "---|" * len(fields)]
    for row in result["rows"]:
        text.append("| " + row["fiscal_year_end"] + " | " + " | ".join(shown(row[f], f) for f in fields) + " |")
    text += [f'\nGraham current-ratio threshold: {result["graham_threshold"]:.1f}. Burry maximum liabilities/equity: 2.0.',
             "\n## Panel", "| Investor | Check | Result |", "|---|---|---|"]
    for investor, checks in result["panel"].items():
        text += [f"| {investor} | {name} | {outcome} |" for name, outcome in checks.items()]
    for investor, checks in result["panel"].items():
        text.append(f"\n{investor}: {summary(checks)}.\n")
    text += ["\n## Added provenance"]
    for row in result["rows"]:
        for f in fields:
            text.append(f'- {row["fiscal_year_end"]} {f}: {shown(row[f], f)}; {json.dumps(row[f], sort_keys=True)}')
    text += ["\nRatios are checked before rounding. Missing inputs or nonpositive denominators remain not known.",
             f'Original SEC retrieval: {result["source"]["retrieved_utc"]}; SHA256: {result["source"]["sha256"]}.']
    return "\n".join(text) + "\n"


def memo_path(ticker, investor):
    return HERE / "memos" / ticker / f"{investor.lower()}.md"


def load_memos(ticker):
    return {i: memo_path(ticker, i).read_text(encoding="utf-8") if memo_path(ticker, i).exists() else "" for i in INVESTORS}


def memo_flags(memos, report):
    return {i: edgar.unsupported_numbers(text, report) for i, text in memos.items()}


def verdict(memo):
    import re
    match = re.search(r"\*\*Verdict: (.*?)\*\*", memo)
    return match.group(1) if match else "pending memo"


def save(result, label=None):
    folder = HERE / "evidence"
    folder.mkdir(parents=True, exist_ok=True)
    name = label or result["ticker"]
    (folder / f"{name}-computed.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (folder / f"{name}-report.md").write_text(report_text(result), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--offline", action="store_true")
    mode.add_argument("--refresh", action="store_true")
    parser.add_argument("--graham-threshold", type=float, help="Temporary probe; does not edit the retained skill setting")
    parser.add_argument("--check-memos", action="store_true")
    args = parser.parse_args()
    try:
        result = run(args.ticker, refresh=args.refresh, offline=not args.refresh, hurdle=args.graham_threshold)
        save(result, f'{result["ticker"]}-probe' if args.graham_threshold is not None else None)
        report = report_text(result)
        print(report)
        if args.check_memos:
            memos = load_memos(result["ticker"])
            flags = memo_flags(memos, report)
            print("Unprinted-number flags across all memos:", json.dumps(flags))
            return int(any(flags.values()) or any(not text.strip() for text in memos.values()))
        return 0
    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
