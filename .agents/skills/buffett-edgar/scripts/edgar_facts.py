"""Lab 18: deterministic 10-K facts. No price feeds, estimates or model arithmetic."""
import argparse
from datetime import date, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[4]
LAB = ROOT / "projects/lab-18-legend-investor"
TAGS = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"),
    "net_income": ("NetIncomeLoss",),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capital_spending": ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"),
    "equity": ("StockholdersEquity",),
}
NUMBERS = re.compile(r"\d{4}-\d{2}-\d{2}|[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:\s*%)?")


def ticker_symbol(value):
    value = value.strip().upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9.-]{0,11}", value):
        raise ValueError("Enter a valid SEC ticker, for example COST or JPM.")
    return value


def download(url, destination, refresh=False, offline=False):
    """Persist public response plus hash; never persist the User-Agent identity."""
    metadata = destination.with_suffix(".source.json")
    if offline or (destination.exists() and not refresh):
        if not destination.exists() or not metadata.exists():
            raise ValueError(f"No archived SEC response: {destination.name}. Run online first.")
        body = destination.read_bytes()
        source = json.loads(metadata.read_text(encoding="utf-8"))
        if hashlib.sha256(body).hexdigest() != source["sha256"]:
            raise ValueError(f"Archived response hash mismatch: {destination.name}")
        return json.loads(body), source
    agent = os.environ.get("SEC_USER_AGENT", "").strip()
    if not re.search(r"\S+@\S+\.\S+", agent) or len(agent.split()) < 2:
        raise ValueError("Set SEC_USER_AGENT to your name and email in this session; do not commit it.")
    request = urllib.request.Request(url, headers={"User-Agent": agent, "Accept": "application/json"})
    time.sleep(0.2)  # Sequential requests, comfortably below SEC's request limit.
    with urllib.request.urlopen(request, timeout=45) as response:
        body = response.read()
    result = json.loads(body)
    source = {"url": url, "retrieved_utc": datetime.now(timezone.utc).isoformat(),
              "sha256": hashlib.sha256(body).hexdigest()}
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(body)
    metadata.write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
    return result, source


def annual(record):
    if record.get("form") != "10-K" or not record.get("start") or not record.get("end"):
        return False
    days = (date.fromisoformat(record["end"]) - date.fromisoformat(record["start"])).days
    return 350 <= days <= 380


def observations(facts, tag):
    return facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", [])


def select_fact(facts, field, end, start):
    """Tag priority is per fiscal year; within an eligible tag the latest filing wins."""
    for tag in TAGS[field]:
        eligible = [r for r in observations(facts, tag)
                    if r.get("form") == "10-K" and r.get("end") == end
                    and r.get("val") is not None
                    and ((field == "equity" and not r.get("start"))
                         or (field != "equity" and annual(r) and r["start"] == start))]
        if eligible:
            selected = max(eligible, key=lambda r: (r.get("filed", ""), r.get("accn", "")))
            return {"value": selected["val"], "tag": tag,
                    "start": selected.get("start"), "end": end,
                    "filed": selected.get("filed"), "accession": selected.get("accn"), "form": "10-K"}
    return {"value": None, "tag": "not found", "end": end, "searched_tags": list(TAGS[field])}


def year_row(facts, end, start):
    """One annual row: select facts, keep provenance, compute only with complete inputs."""
    row = {"fiscal_year_end": end, "period_start": start}
    row.update({field: select_fact(facts, field, end, start) for field in TAGS})
    income, equity = row["net_income"]["value"], row["equity"]["value"]
    ocf, capex = row["operating_cash_flow"]["value"], row["capital_spending"]["value"]
    row["roe"] = {"value": income / equity if income is not None and equity is not None and equity > 0 else None,
                  "tag": "NetIncomeLoss / StockholdersEquity", "missing": "not known"}
    row["owner_earnings"] = {"value": ocf - capex if ocf is not None and capex is not None else None,
                             "tag": f'{row["operating_cash_flow"]["tag"]} - {row["capital_spending"]["tag"]}'}
    return row


def compute(facts, ticker):
    periods = {}
    for field in ("net_income", "revenue"):
        for tag in TAGS[field]:
            for record in observations(facts, tag):
                if annual(record):
                    key = (record.get("filed", ""), record.get("accn", ""))
                    if record["end"] not in periods or key > periods[record["end"]][0]:
                        periods[record["end"]] = (key, record["start"])
    ends = sorted(periods)[-5:]
    if not ends:
        raise ValueError("No annual USD revenue/net-income contexts from 10-K filings found.")
    rows = [year_row(facts, end, periods[end][1]) for end in ends]
    roes = [r["roe"]["value"] for r in rows]
    owners = [r["owner_earnings"]["value"] for r in rows]
    def check(values, predicate):
        if len(rows) != 5 or any(v is None for v in values):
            return "not known"
        return "pass" if predicate(values) else "fail"
    checks = {"ROE >= 15% every year": check(roes, lambda v: all(x >= .15 for x in v)),
              "Owner earnings positive every year": check(owners, lambda v: all(x > 0 for x in v)),
              "Owner earnings grew, first to last": check(owners, lambda v: v[-1] > v[0])}
    return {"ticker": ticker, "company": facts.get("entityName", ticker), "cik": facts.get("cik"),
            "units": "USD; displayed amounts in USD millions", "rows": rows, "checks": checks}


def display(cell, percent=False):
    if cell["value"] is None:
        return cell.get("missing", "not found")
    number = Decimal(str(cell["value"]))
    if percent:
        return f'{(number * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP):.1f}%'
    millions = number / Decimal(1000000)
    return f"{millions:,.6f}".rstrip("0").rstrip(".")


def report_text(result):
    fields = list(TAGS) + ["roe", "owner_earnings"]
    text = [f'# {result["ticker"]} — {result["company"]}',
            "Amounts: USD millions. ROE: net income / fiscal-year-end equity.",
            "ROE threshold: 15%. Owner earnings: operating cash flow minus capital spending.",
            "| Fiscal-year end | " + " | ".join(fields) + " |",
            "|---|" + "---|" * len(fields)]
    for row in result["rows"]:
        text.append("| " + row["fiscal_year_end"] + " | " + " | ".join(
            display(row[f], f == "roe") for f in fields) + " |")
    text.append("\nXBRL tags and selected filing provenance:")
    for row in result["rows"]:
        text.append(f'\nFY{row["fiscal_year_end"][:4]} ends {row["fiscal_year_end"]}; starts {row["period_start"]}.')
        for field in fields:
            cell = row[field]
            detail = f'; filed {cell["filed"]}; accession {cell["accession"]}' if cell.get("filed") else ""
            searched = "; searched " + ", ".join(cell["searched_tags"]) if cell.get("searched_tags") else ""
            text.append(f'- {field}: {display(cell, field == "roe")} [{cell["tag"]}]{detail}{searched}')
    text.append("\nChecks:")
    text.extend(f"- {name}: {outcome}" for name, outcome in result["checks"].items())
    if len(result["rows"]) < 5:
        text.append("Incomplete five-year history: all checks are not known.")
    return "\n".join(text) + "\n"


def numeric_key(token):
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", token):
        return ("date", token)
    return ("percent" if "%" in token else "number", Decimal(token.replace(",", "").replace("%", "").strip()))


def unsupported_numbers(memo, printed_report):
    """Flag each occurrence absent from printed output, preserving percent units and sign."""
    allowed = {numeric_key(m.group()) for m in NUMBERS.finditer(printed_report)}
    return [{"token": m.group(), "start": m.start(), "end": m.end()}
            for m in NUMBERS.finditer(memo) if numeric_key(m.group()) not in allowed]


def run(ticker, refresh=False, offline=False):
    ticker = ticker_symbol(ticker)
    folder = LAB / "evidence"
    tickers, ticker_source = download("https://www.sec.gov/files/company_tickers.json", folder / "company_tickers.json", refresh, offline)
    matches = [v for v in tickers.values() if v["ticker"].upper() == ticker]
    if not matches:
        raise ValueError(f"Ticker {ticker} not found in SEC ticker mapping.")
    cik = int(matches[0]["cik_str"])
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
    facts, source = download(url, folder / f"{ticker}-companyfacts.json", refresh, offline)
    if int(facts["cik"]) != cik:
        raise ValueError("SEC response CIK does not match ticker mapping.")
    result = compute(facts, ticker)
    result["source"] = source
    result["ticker_source"] = ticker_source
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--refresh", action="store_true")
    group.add_argument("--offline", action="store_true")
    parser.add_argument("--check-memo", type=Path)
    args = parser.parse_args()
    try:
        result = run(args.ticker, args.refresh, args.offline)
        report = report_text(result)
        folder = LAB / "evidence"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f'{result["ticker"]}-computed.json').write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        (folder / f'{result["ticker"]}-report.md').write_text(report, encoding="utf-8")
        print(report)
        if args.check_memo:
            flags = unsupported_numbers(args.check_memo.read_text(encoding="utf-8"), report)
            print("Unsupported memo numbers:", json.dumps(flags))
            return 1 if flags else 0
        return 0
    except Exception as error:
        print(f"{type(error).__name__}: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
