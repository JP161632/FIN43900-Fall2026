# Lab 18 — Legend Investor as Skill

**Question:** Can an investor's philosophy become a skill your AI runs the same way every time—every number computed by code from the 10-K, the judgment the model's?

The reusable skill computes the financial evidence consistently; a model then judges the business and writes a memo. The Streamlit app displays the evidence, checks, and editable memo. This is a learning demonstration built with AI help, not investment advice.

## Run

From the repository root in PowerShell:

```powershell
# The repository's existing environment already has these packages.
.venv/Scripts/python.exe -m pip install -r projects/lab-18-legend-investor/requirements.txt

# Enter your name and email only into this process's environment, not a tracked file.
$env:SEC_USER_AGENT = Read-Host 'SEC User-Agent (your name and email)'
.venv/Scripts/python.exe .agents/skills/buffett-edgar/scripts/edgar_facts.py COST --refresh
.venv/Scripts/python.exe .agents/skills/buffett-edgar/scripts/edgar_facts.py JPM --refresh
.venv/Scripts/python.exe -m streamlit run projects/lab-18-legend-investor/app.py
```

Open the terminal's local URL. Saved SEC responses are the default, so later launches can replay preserved public evidence without internet or a User-Agent. Select live downloads and click **Download now** to update a ticker. Download failures are displayed; the app never replaces them with fabricated facts. The script uses its archived response on an ordinary online run if one already exists; use `--refresh` for a new download or `--offline` to require an archived response. Retrieval time is the original download time, never the replay time.

In Codex, invoke:

```text
Use $buffett-edgar on COST. Run the bundled script, then write the Buffett-style business memo using only its printed numbers.
```

The skill is checked into [the repository's .agents/skills folder](../../.agents/skills/buffett-edgar/SKILL.md), a location Codex scans for repository skills. If the selector has not refreshed, restart Codex and select it with `$` or `/skills`. Source: [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Files

| File | Purpose |
|---|---|
| [SKILL.md](../../.agents/skills/buffett-edgar/SKILL.md) | Discoverable trigger and reusable model workflow |
| [edgar_facts.py](../../.agents/skills/buffett-edgar/scripts/edgar_facts.py) | SEC downloads, annual context selection, numeric calculations, memo-number checker |
| [app.py](app.py) | Ticker chart, table, checks, provenance and editable memo |
| [request.md](request.md) | Original lab-specific build request |
| [verify_lab18.py](verify_lab18.py) | Separate instructor answer-key audit and controlled probes |
| [verify_app.py](verify_app.py) | Actual Streamlit page tests against archived SEC responses |
| [COST memo](memos/COST.md) / [JPM memo](memos/JPM.md) | Model judgments after reading computed output |
| [lab-18-writeup.md](lab-18-writeup.md) | Finance interpretation, code explanation and activity status |

The CLI creates `evidence/TICKER-companyfacts.json`, a source metadata file, `TICKER-computed.json`, and `TICKER-report.md`. The model saves memos to `memos/TICKER.md`. The raw source is public SEC company data. Request headers, operator identity and credentials are excluded.

## Data rules

Only USD facts in forms exactly equal to `10-K` qualify. The last five annual fiscal-period ends are identified from annual net-income/revenue contexts; older comparison values retain their actual fiscal-year-end dates even when their filing's XBRL `fy` labels a later filing year. Annual duration means 350–380 elapsed days, accommodating 52/53-week years. Flow start dates must match the selected annual period; instant equity must match its end date. Within each allowed tag and period, the latest filing date wins, with accession as a deterministic tie-breaker. Tag priority precedes recency across different tags, as required by the lab. There is no quarterly summation or annualization.

Revenue uses `RevenueFromContractWithCustomerExcludingAssessedTax`, falling back to `Revenues`; capital spending uses `PaymentsToAcquirePropertyPlantAndEquipment`, falling back to `PaymentsToAcquireProductiveAssets`. Net income, operating cash flow and equity use the exact assigned tags. Provenance retains tag, period, filing date, form and accession. ROE divides net income by year-end equity; owner earnings subtracts capital spending from operating cash flow. No maintenance-capex estimate is introduced.

Missing amounts print **not found**. ROE with missing inputs or zero/negative equity prints **not known**. A check with any missing input prints **not known**, including the growth check when an intervening year's owner earnings is missing. Fewer than five available annual rows produces **not known** checks; the code never invents years. The three checks use unrounded values; the displayed ROE is rounded to one decimal percent.

## Verify and probe

```powershell
.venv/Scripts/python.exe projects/lab-18-legend-investor/verify_lab18.py
.venv/Scripts/python.exe projects/lab-18-legend-investor/verify_lab18.py --source-audit
.venv/Scripts/python.exe projects/lab-18-legend-investor/verify_app.py
.venv/Scripts/python.exe .agents/skills/buffett-edgar/scripts/edgar_facts.py COST --offline --check-memo projects/lab-18-legend-investor/memos/COST.md
```

The first command runs explicitly synthetic selection and missing-data tests. The second separately compares all 35 supplied COST values with archived SEC-derived output, checks the three pass results and rising chart endpoints, probes JPM's gaps and tests the altered memo. It writes `verification-results.json` and fails on any mismatch. Instructor answers occur only in that verifier, never in production calculations or source responses. The third command exercises the actual Streamlit page: tables, checks, both chart series and endpoints, memo injection/reload, JPM gaps, invalid and unknown tickers. It writes `app-verification-results.json` without live network access or changing saved memos.

**Executed result:** All 35 COST comparisons, nine controlled tests, eight source/memo checks and six app checks pass on the November 3, 2026 download. Both saved model memos pass numeric validation. The student supplied the partner activity, trust decision and reflection. At the student's request, [a disclosed Codex response](codex-comparison.md) replaces the fresh-browser no-skill comparison; it is not an independent probe.

For the manual probe, append `Hand-entered ROE: 40.0%.` to the memo in the app. Expect an unsupported-number error; remove it after observing the flag. The text area checks on each rerun, and **Save memo edits** persists its contents. To pick up an edit made externally in the Markdown file, click **Reload memo from file**. A new ticker has no prewritten verdict; use the skill to create its memo, then reload it.

The numeric checker flags each numeric token absent from the printed report, normalizing comma separators and decimal spelling while preserving percent units, negative signs and dates. Its scope is numeric occurrence, not semantic proof: it cannot tell whether a printed number was assigned to the wrong metric or whether an asserted moat is real. The model must still read the memo for accuracy. Missing chart values stay missing rather than becoming zero.

## Sources and scope

- [Assigned FAskills Buffett page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md): read for philosophy only; never installed or used for financial data.
- [SEC ticker mapping](https://www.sec.gov/files/company_tickers.json) and [SEC companyfacts API](https://data.sec.gov/api/xbrl/companyfacts/CIK0000909832.json): public, keyless financial inputs. The companyfacts CIK is resolved from the ticker mapping and padded to ten digits.
- [SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) and [automated access guidance](https://www.sec.gov/about/webmaster-frequently-asked-questions): public dissemination API, runtime identification and conservative sequential requests.
- [Streamlit app-testing documentation](https://docs.streamlit.io/develop/api-reference/app-testing): framework for inspecting the real app's outputs and interactions.

The original Buffett page also requests valuation, paid-feed context, estimated maintenance spending and forecasts. The lab deliberately replaces those parts with its exact SEC-only calculations and a business-quality verdict. Historical profitability does not prove a durable moat, trustworthy management, sensible leverage, or an attractive stock price. Liabilities/equity is not displayed because the assigned app asks for no liabilities metric; if extended, nonpositive equity must make that ratio **not known** too.
