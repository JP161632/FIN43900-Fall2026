"""Download Yahoo daily adjusted closes; retain completed month-end observations.

Run from any directory. No third-party download package or credentials needed.
61 month-end prices produce 60 monthly returns, October 2021–September 2026.
"""
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
TICKERS = ("NVDA", "MSFT", "TSM", "QCOM")
START = datetime(2021, 9, 1, tzinfo=timezone.utc)
END = datetime(2026, 10, 1, tzinfo=timezone.utc)  # exclusive; no partial October
EXPECTED_MONTHS = [f"{2021 + (8 + i) // 12}-{(8 + i) % 12 + 1:02d}" for i in range(61)]


def main():
    records, raw_files, provenance = {}, {}, []
    for ticker in TICKERS:
        query = urlencode({"period1": int(START.timestamp()), "period2": int(END.timestamp()),
                           "interval": "1d", "events": "div,splits", "includeAdjustedClose": "true"})
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{query}"
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=30) as response:
            raw = response.read()
        fetched = datetime.now(timezone.utc).isoformat()
        document = json.loads(raw)
        if document["chart"]["error"]:
            raise ValueError(document["chart"]["error"])
        result = document["chart"]["result"][0]
        if result["meta"]["symbol"] != ticker or result["meta"]["currency"] != "USD":
            raise ValueError(f"Unexpected symbol/currency for {ticker}.")
        times = result["timestamp"]
        adjusted = result["indicators"]["adjclose"][0]["adjclose"]
        if len(times) != len(adjusted):
            raise ValueError(f"Mismatched timestamps and adjusted prices for {ticker}.")
        monthly = {}
        for stamp, value in zip(times, adjusted):
            date = datetime.fromtimestamp(stamp, timezone.utc).date()
            if value is None:
                raise ValueError(f"Missing adjusted close for {ticker} on {date}.")
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"Invalid adjusted close for {ticker} on {date}.")
            if START.date() <= date < END.date():
                month = date.isoformat()[:7]
                if month not in monthly or date.isoformat() > monthly[month][0]:
                    monthly[month] = (date.isoformat(), value)
        if sorted(monthly) != EXPECTED_MONTHS:
            raise ValueError(f"Incomplete five-year coverage for {ticker}: {sorted(monthly)}")
        # Prevent a truncated response from masquerading as a complete final month.
        if monthly["2026-09"][0] != "2026-09-30":
            raise ValueError(f"Final complete month missing its final session for {ticker}.")
        records[ticker] = monthly
        raw_name = f"sources/{ticker}-yahoo-daily.json"
        raw_files[raw_name] = raw
        provenance.append({"ticker": ticker, "source": "Yahoo Finance", "currency": "USD",
                           "history_url": f"https://finance.yahoo.com/quote/{ticker}/history/",
                           "download_url": url, "retrieved_at_utc": fetched,
                           "field": "indicators.adjclose[0].adjclose",
                           "aggregation": "Last actual trading-day adjusted close in each calendar month",
                           "raw_file": raw_name, "raw_sha256": hashlib.sha256(raw).hexdigest(),
                           "price_rows": len(monthly), "first_price_date": monthly[EXPECTED_MONTHS[0]][0],
                           "last_price_date": monthly[EXPECTED_MONTHS[-1]][0]})
        print(f"{ticker}: {len(monthly)} complete month-end adjusted closes; retrieved {fetched}")
    for month in EXPECTED_MONTHS:
        if len({records[ticker][month][0] for ticker in TICKERS}) != 1:
            raise ValueError(f"Trading-date mismatch across assets in {month}.")
    # Write only after every source passes; keep exact raw responses for audit.
    (ROOT / "sources").mkdir(exist_ok=True)
    for name, raw in raw_files.items():
        (ROOT / name).write_bytes(raw)
    with (ROOT / "prices.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Date", *TICKERS])
        for month in EXPECTED_MONTHS:
            writer.writerow([records[TICKERS[0]][month][0], *[records[t][month][1] for t in TICKERS]])
    manifest = {"complete_months_only": True, "omitted_partial_month": "2026-10",
                "return_months": 60, "prices_sha256": hashlib.sha256((ROOT / "prices.csv").read_bytes()).hexdigest(),
                "sources": provenance}
    (ROOT / "price-provenance.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Saved prices.csv and auditable source responses; 61 prices / 60 monthly returns.")


if __name__ == "__main__":
    main()
