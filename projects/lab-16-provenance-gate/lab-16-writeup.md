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

## Quiz and partner work — awaiting student responses

- Month measured versus publication date, explained by student: **pending**.
- Least-understood line, AI quiz, student's answer before explanation: **pending**.
- No-AI line-by-line explanation of rule 4, partner's question, and student's answer: **pending**.
- Partner-file original run, April 15 change and results, and restoration: **pending**.

## Learn on your own — awaiting student responses

1. What is look-ahead bias? **Pending student answer.**
2. How do event time, publication time, and revisions cause it? **Pending student answer.**
3. Explain with AAA why +5.83% looks better than anything knowable on March 31. **Pending student answer.**

## Reflection — awaiting student responses

1. Which rule removed the row that mattered most, and why? **Pending student answer.**
2. What would a backtest built on the naive column claim? **Pending student answer.**

## Checkout links

- [Lab 16 writeup](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/lab-16-writeup.md)
- [asof.py](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/asof.py)
- [Reproducible verification](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/verify_lab16.py)
- [Executed results](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/verification-results.txt)
- [Requirement audit](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-16-provenance-gate/rubric-audit.md)
