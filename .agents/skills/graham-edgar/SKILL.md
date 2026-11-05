---
name: graham-edgar
description: Run Lab 19 Graham liquidity and earnings checks on shared SEC facts, then write a conservative business-screen memo. Excludes valuation and prices.
---

From the repository root run `.venv/Scripts/python.exe projects/lab-19-legend-panel/panel.py TICKER --offline` and read its printed report before judging. For a new ticker use `--refresh`; identification belongs only in the runtime SEC_USER_AGENT, never in saved files. The shared Lab 18 selector uses five annual USD 10-K periods, permitted tags and latest eligible filings, preserving provenance and gaps.

The executable checks are `graham_checks` in `projects/lab-19-legend-panel/panel.py`: latest current assets/current liabilities meets the hurdle; net income is positive every year; final net income exceeds initial net income. Missing inputs remain not known. A nonpositive ratio denominator is not known. Annual checks require five complete years.

The retained current-ratio threshold is **2.0**, read by code from [settings.json](settings.json). To perform the lab probe, temporarily change that setting to 1.0, run COST, and restore 2.0. The CLI `--graham-threshold 1.0` is a reproducible temporary override. Keep the retained setting and the line below the memo consistent; never silently lower it to fit a company.

Write `projects/lab-19-legend-panel/memos/TICKER/graham.md`, labeled an educational AI simulation, with a first-person Graham-style judgment and a `**Verdict: ...**` line. Use only numbers literally printed by the script, in its displayed units. Explain liquidity protection and earnings stability/growth. No estimates, stock prices, forecasts, scores or unsupported qualitative assertions. Do not claim the panel establishes intrinsic value or a margin of safety. End with one line recording the threshold kept and why; distinguish a proposed rationale from a student-supplied choice. Never invent partner activities or student decisions.

Run `panel.py TICKER --offline --check-memos` and repair every unsupported number. The flag tests numeric occurrence, not correct metric attribution: read each statement for semantic accuracy.

Read [FAskills Graham](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md) for philosophy only. Adapt conservative financing and stable earnings. The lab's exact checks override its broader valuation, growth, data-feed and prediction framework; do not install the plugin or estimate missing facts.
