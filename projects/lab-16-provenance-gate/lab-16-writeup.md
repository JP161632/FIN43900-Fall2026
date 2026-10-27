# Lab 16 — Provenance Gate

## D — Decision

On the day you would have traded, what did this data actually say — and how much of what you see now came later?

Decision cutoff: **March 31, 2026**, inclusive. This exercise uses the professor's fictional card-spend index for AAA, BBB, and CCC, not investment data. The source is the 12-row training table pasted in the assignment, preserved as editable input in [asof.py](asof.py). No external data, personal records, or API credentials are used.

## R — Training table and rules

Each record contains its original row number, ticker, month measured, publication date, and index. The original row numbers stay attached to records throughout the funnel. A row number is provenance, not a data field for identifying exact duplicates.

Apply these rules in order: quarantine missing tickers; remove exact duplicates; exclude publications after the cutoff; retain the latest eligible publication for each ticker and measured month. Quarantined and excluded rows remain identifiable in the source and printed funnel; no missing identity is invented.

## I — Implementation

[asof.py](asof.py) uses only Python's standard library. Editable `TABLE` and `DECISION_DATE` appear at the top. Dates are parsed as dates and index values as decimal numbers. Every reported row and signal is computed from those inputs; the known answers appear only in the separate verifier.

From the repository root:

```powershell
python projects/lab-16-provenance-gate/asof.py
python projects/lab-16-provenance-gate/verify_lab16.py
```

Or change into this folder and run `python asof.py`.

The rule-4 block is `latest_vintages`. `filter_rows` passes only eligible records to it for the as-of panel. Its dictionary key is `(ticker, month)`: an eligible row replaces the stored row only when its publication date is later. The naive comparison applies the same identity and duplicate handling, then selects the latest publications without a cutoff. Conflicting different values for the same ticker, month, and publication day raise an error rather than silently choosing one.

Signals use `(latest index / previous index - 1) * 100`, where previous means the immediately preceding calendar month. A missing previous month or zero denominator produces an unavailable signal. Display rounding occurs only at the end.

## V — Known-answer proof

Executed output is preserved in [verification-results.txt](verification-results.txt). Reproduce the assertions and both cutoff reports with [verify_lab16.py](verify_lab16.py).

| Funnel step | Removed count | Original row numbers | Remaining |
|---|---:|---|---:|
| Input | — | 1–12 | 12 |
| Quarantined: no ticker | 1 | 11 | 11 |
| Exact duplicate | 1 | 7 | 10 |
| Published after March 31 | 3 | 3, 8, 10 | 7 |
| Older vintage replaced | 1 | 2 | 6 |
| As-of panel | — | 1, 4, 5, 6, 9, 12 | 6 |

| Row | Ticker | Month measured | Published on | Index |
|---:|---|---|---|---:|
| 1 | AAA | 2026-01 | 2026-02-10 | 101.0 |
| 4 | AAA | 2026-02 | 2026-03-25 | 103.0 |
| 5 | BBB | 2026-01 | 2026-02-10 | 98.0 |
| 6 | BBB | 2026-02 | 2026-03-10 | 97.0 |
| 9 | CCC | 2026-01 | 2026-02-10 | 110.0 |
| 12 | CCC | 2026-02 | 2026-03-10 | 111.0 |

| Ticker | As-of signal | Naive signal |
|---|---|---|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

AAA uses February's revised 103, published March 25: `(103 / 101 - 1) * 100`. Using the superseded 104 would produce +2.97%, the assignment's diagnostic error. Naive AAA uses `(109 / 103 - 1) * 100`; naive BBB uses `(92 / 97 - 1) * 100`. CCC's naive February value is 112, replacing the as-of value of 111 only after April 5.

The automated April 15 experiment yields +5.83%, -5.15%, and +1.82%, respectively, in **both** columns. This verifies this submitted implementation; it does not establish that a partner's separate file was run. The delivered date remains March 31.

## Quiz and partner work

The responses below are student-supplied reports; AI did not observe the partner activities.

**Month measured versus publication date — student's explanation:** The month measured (event time) represents when the economic activity happened, such as consumer card spending during January or February. The publication date (availability time) is the later calendar day when that data was released and became publicly knowable. A later revision can change the published value. The observation cannot support a trade before its publication date, regardless of when the activity occurred.

**Least-understood code:** replacing older revisions. The student initially described the key as ticker alone; the actual code uses `(ticker, month)`. The student's stated difficulty was tracking revision replacement without dropping valid records from other measured months.

**AI quiz — answer pending:** Suppose `latest_vintages()` receives AAA January published February 10 (row 1), AAA February published March 25 (row 4), and then AAA February published March 10 (row 2), in that order. With `key = (row["ticker"], row["month"])`, which rows remain, why does row 2 not overwrite row 4, and what would go wrong if the key were only the ticker? The student's answer must precede the AI explanation.

**No-AI explanation and partner question:** The student reports walking the partner through `latest_vintages()` line by line without AI. The partner asked what happens when two conflicting index values share the exact publication date for the same ticker and month. The student answered that the code checks for that collision and raises `ValueError`, since an unverified same-day contradiction cannot be silently resolved.

**Swap and break, reported by student:** The partner's `asof.py` matched the baseline: AAA +1.98%, BBB -1.02%, CCC +0.91%. Setting its `DECISION_DATE` to `2026-04-15` made the as-of and naive columns agree at +5.83%, -5.15%, and +1.82%, respectively. All supplied April releases were then eligible. The student reports immediately restoring `2026-03-31`.

## Learn on your own

**What is look-ahead bias? — student's response:** A backtest incorporates information that was impossible to know on the simulated trade date, making a strategy look artificially effective because it uses future knowledge.

**How does it work? — student's response:** Indexing data by the month measured can falsely treat March data as available on March 31. Publication time determines actual availability, while revisions can introduce changed values published weeks after the cutoff. A point-in-time backtest must use only the vintages available on each decision date.

**Explain with AAA — student's response:** The naive +5.83% relies on row 3's March index of 109.0, released April 10. On March 31, the latest knowable month was February, with a revised index of 103.0 and a +1.98% change from January. Claiming +5.83% on March 31 pretends April 10's release was available ten days early. The two percentages refer to different monthly intervals.

## Reflection

**Which rule removed the row that mattered most? — student's response:** Rule 3, excluding publications after the decision date, removed row 3 (AAA's March index of 109.0, published April 10). That row makes the naive calculation show a stronger +5.83% March signal instead of the knowable +1.98% February signal. Filtering it out prevents a March 31 decision from using April 10's release.

**What would a naive backtest claim? — student's response, edited for precision:** It could claim that the strategy identified AAA's strengthening card-spend trend and BBB's weakening trend on March 31, using signals that actually depended on April releases. If those signals were used to choose long or short positions, the historical results would rely on unavailable information. This table contains index observations, not security prices or realized trading returns, so it cannot establish extraordinary profits, a stock-price surge or drop, or inevitable live-trading losses. Those outcomes would require a defined trading rule, price data, and execution and cost assumptions.

## Checkout links

- [Lab 16 writeup](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/lab-16-writeup.md)
- [asof.py](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/asof.py)
- [Reproducible verification](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/verify_lab16.py)
- [Executed results](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/verification-results.txt)
- [Requirement audit](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/rubric-audit.md)
