# Lab 19 — Legend Panel

**Question:** When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would you trust the panel?

The panel extends Lab 18 with Graham's liquidity/earnings checks and Burry's cash-backing/leverage checks. All investors share the same annual SEC facts; each memo is a disclosed model interpretation. The original Lab 18 app and evidence remain available.

**Verified:** COST matches all ten supplied ratios and all eight checks: Buffett 3 of 3, Graham 2 of 3 with current ratio failing at 1.06, Burry 2 of 2. Twenty calculation/source/memo probes and nine Streamlit app checks pass. The temporary 1.0 threshold makes Graham pass; the retained setting is 2.0. The confirmed Project 2 company and student responses are still pending; JPM is only an additional gap probe.

## Run

From the repository root:

```powershell
.venv/Scripts/python.exe -m pip install -r projects/lab-19-legend-panel/requirements.txt
.venv/Scripts/python.exe projects/lab-19-legend-panel/panel.py COST --offline --check-memos
.venv/Scripts/python.exe projects/lab-19-legend-panel/panel.py COST --offline --graham-threshold 1.0
.venv/Scripts/python.exe projects/lab-19-legend-panel/panel.py JPM --offline --check-memos
.venv/Scripts/python.exe -m streamlit run projects/lab-19-legend-panel/app.py
```

For a new confirmed holding, set `SEC_USER_AGENT` through an interactive `Read-Host` in your local process, then run `panel.py TICKER --refresh`. Never put operator identity in a source file, report or commit. The original downloader saves public SEC responses in Lab 18's evidence directory and records URL, retrieval time and hash without saving request headers. Normal runs replay that dated snapshot; they do not claim a fresh download. A company lacking eligible annual 10-K facts produces an error, not estimated results; choose and document the fund's next-largest qualifying holding.

Use the repository skills `$buffett-edgar`, `$graham-edgar` and `$burry-edgar` after printing the ticker's report. Each saves its memo under `memos/TICKER/`. The app reads those saved memos; it does not make a new model/API call on every rerun. A new ticker without memos displays pending judgments, never prewritten conclusions for a different company.

## Files

| File | Purpose |
|---|---|
| [lab-19-writeup.md](lab-19-writeup.md) | Question, known answer, interpretation, code explanation and activity status |
| [request.md](request.md) | AI-assisted lab build request |
| [panel.py](panel.py) | Reused Lab 18 facts, added instant facts/ratios, checks, CLI and shared memo checker |
| [app.py](app.py) | Chart, facts, investor/check table, verdicts and three editable memos side by side |
| [Graham skill](../../.agents/skills/graham-edgar/SKILL.md) / [Burry skill](../../.agents/skills/burry-edgar/SKILL.md) | Reusable source-informed memo workflows |
| [Buffett skill](../../.agents/skills/buffett-edgar/SKILL.md) | Existing workflow with a Lab 19 output-path option |
| [COST report](evidence/COST-report.md) / [probe report](evidence/COST-probe-report.md) | Printed baseline and temporary-threshold evidence |
| [COST memos](memos/COST) / [JPM memos](memos/JPM) | Separate judgments written after reading script output |
| [verify_lab19.py](verify_lab19.py) / [results](verification-results.json) | Independent known-answer audit and behavioral checks |
| [verify_app.py](verify_app.py) / [results](app-verification-results.json) | Actual Streamlit page interaction checks |
| [rubric-audit.md](rubric-audit.md) | Evidence and unresolved requirements by criterion |

## Data and gap rules

The [unchanged Lab 18 engine](../../.agents/skills/buffett-edgar/scripts/edgar_facts.py) chooses the last five annual fiscal-year ends from USD revenue/net-income contexts, exact form `10-K`, annual duration 350–380 days, matching annual starts, assigned tag priorities, then latest eligible filing/accession. No `10-Q`, `10-K/A`, annualization, XBRL `fy` relabeling or estimated capex enters the calculations. Revenue, net income, cash flow, capital spending, equity, ROE and owner earnings retain the Lab 18 definitions and provenance.

The added facts use exact `Liabilities`, `AssetsCurrent` and `LiabilitiesCurrent` tags, instant contexts at those same fiscal ends, and the latest eligible 10-K observation. Current ratio = current assets/current liabilities; liabilities/equity = total liabilities/year-end equity. Nonpositive denominators and missing ratio inputs give **not known**. Missing source amounts remain **not found**. Checks use unrounded values. Annual checks require five complete years, including the interior years of endpoint-growth tests; latest-year checks need only the latest available eligible row and its required inputs. Unknowns are counted separately from failures.

The retained Graham hurdle is read from [settings.json](../../.agents/skills/graham-edgar/settings.json). The CLI and app provide an explicit temporary 1.0 override; both preserve the saved setting. Probe output is saved separately and the app warns that baseline memos are not rewritten for a temporary probe.

The existing numeric checker applies to all three complete memo texts, preserving signs, dates and percent units. Both CLI and app identify the investor with an unsupported number. An absent memo is flagged as missing, not validated as a judgment. The checker tests numeric occurrence, not financial meaning: assigning an allowed number to the wrong metric can pass, so semantic review remains necessary. Numeric strings in source metadata also appear in the report; the checker is a diagnostic, not a proof of evidence quality.

## Verification

```powershell
.venv/Scripts/python.exe projects/lab-19-legend-panel/verify_lab19.py
.venv/Scripts/python.exe projects/lab-19-legend-panel/verify_app.py
```

The instructor key lives only in the independent verifier. Production ratios come from archived SEC inputs. Controlled mutations are synthetic tests, never company evidence. Tests cover missing interior income, missing/nonpositive denominators, inclusive boundaries, rounding, short/empty histories, exact instant-context selection, preserved JPM gaps and injection into every memo. App tests exercise the real page, three columns, tables, verdicts, chart/provenance, probe/restoration, per-memo injection/reload, invalid ticker and absent ticker. They are framework tests, not claims of a browser or partner session.

## Sources

- [FAskills Graham](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md): defensive liquidity and earnings discipline. The lab substitutes its exact five-year checks for the page's broader framework.
- [FAskills Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md): cash backing, skeptical accounting analysis and bear-case questions.
- [FAskills Buffett](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md): earning power and durable-business questions, with Lab 18's owner-earnings proxy.
- [SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces): public companyfacts data. Source snapshots and hashes remain in [Lab 18 evidence](../lab-18-legend-investor/evidence).
- [Streamlit columns](https://docs.streamlit.io/develop/api-reference/layout/st.columns) and [AppTest](https://docs.streamlit.io/develop/api-reference/app-testing): side-by-side display and executable interaction tests.

FAskills was read for philosophy only. Its plugin, price feeds, forecasts, holdings, valuation outputs and missing-data substitutions are outside this assignment. Agreement among personas on one snapshot does not provide independent source corroboration.
