---
name: burry-edgar
description: Run Lab 19 Burry cash-backing and liabilities checks on shared SEC facts, then write a skeptical accounting memo. Excludes prices, short recommendations and valuation.
---

From the repository root run `.venv/Scripts/python.exe projects/lab-19-legend-panel/panel.py TICKER --offline`. Read actual printed output before writing a conclusion. A new ticker uses `--refresh` with SEC_USER_AGENT supplied only in the process environment; never save identity or request headers.

Use the shared Lab 18 five-year annual USD 10-K selector and `burry_checks` in `projects/lab-19-legend-panel/panel.py`: operating cash flow at least net income every year, and latest liabilities no more than twice positive equity. The annual comparison requires five complete years. Missing facts remain not found; checks and ratios with missing inputs/nonpositive denominators remain not known. Do not substitute debt for Liabilities or bank-specific estimates.

Write `projects/lab-19-legend-panel/memos/TICKER/burry.md`, labeled an educational AI simulation, in a skeptical first-person voice with a `**Verdict: ...**` line. Use only numbers literally printed in the script's displayed units. Explain cash backing, balance-sheet risk and what the checks cannot detect. Passing does not establish clean accounting or absence of hidden liabilities; failing does not prove fraud. No forecasts, price targets, scores, new arithmetic or invented facts. Keep unknowns explicit and leave student decisions and partner work to the student.

Run `panel.py TICKER --offline --check-memos`; fix unsupported numbers and read for correct metric attribution because occurrence checking cannot establish semantic accuracy.

Read [FAskills Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md) for philosophy only: skepticism, cash-backed earnings and bear-case construction. The assigned lab checks replace the page's paid feeds, price targets, holdings and predictive outputs. Do not install it, guess missing data or claim to have read footnotes absent from the evidence.
