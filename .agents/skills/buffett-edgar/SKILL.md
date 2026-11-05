---
name: buffett-edgar
description: Evaluate a business using Buffett-style judgment after computing five fiscal years of SEC EDGAR 10-K facts and deterministic quality checks. Use for Lab 18 or a ticker business-quality memo; excludes stock-price and valuation analysis.
---

Run the bundled script before writing any financial conclusion. From the repository root:

```powershell
.venv/Scripts/python.exe .agents/skills/buffett-edgar/scripts/edgar_facts.py COST
```

For another ticker, replace COST. Live downloads require `SEC_USER_AGENT` set in the process environment to the operator's name and email. Never save that identity in source, evidence, or GitHub. Request it if absent. No API key is needed. The script saves raw SEC responses, retrieval metadata, computed JSON and a printed Markdown report in `projects/lab-18-legend-investor/evidence/`. `--offline` replays saved SEC responses without claiming a new download; `--refresh` requests new responses.

The code, not the model, selects the last five fiscal-year-end dates from annual 10-K contexts, filters one-year flows (350–380 elapsed days, including 52/53-week years), chooses the latest filed observation for the same annual period, and applies the lab's tag priority. Inspect the provenance in the computed JSON when explaining a number. Do not use quarter/YTD values, the XBRL `fy` field as the historical period label, or 10-Q/10-K/A records.

Revenue: RevenueFromContractWithCustomerExcludingAssessedTax, then Revenues. Net income: NetIncomeLoss. Operating cash flow: NetCashProvidedByUsedInOperatingActivities. Capital spending: PaymentsToAcquirePropertyPlantAndEquipment, then PaymentsToAcquireProductiveAssets. Equity: StockholdersEquity. ROE = net income / year-end equity. Owner earnings = operating cash flow - capital spending. Derived fields retain their input tags. Missing facts print `not found`; ROE for nonpositive equity prints `not known`. Checks with any missing/undefined input print `not known`. Never estimate or import a value from the answer key.

Read the script's actual printed report. It computes ROE >= 15% every year, owner earnings > 0 every year, and final owner earnings > initial owner earnings. The script also prints the fiscal years, all input tags and source filings. It does not choose the verdict.

Write a short, first-person Buffett-style educational memo to `projects/lab-18-legend-investor/memos/TICKER.md`: choose **own the business**, **watch it**, or **pass**. Use only numbers literally printed in the report, in its displayed units ($ millions, ROE percent). Explain evidence for earning power and consistency; distinguish those observations from judgments about moat durability, competence, management and allocation. Treat unverified qualitative claims as open questions. No scores, forecasts, prices, target prices, margin of safety, or new arithmetic. For missing owner earnings explicitly say you cannot judge owner earnings. Identify the text as a simulation, not Buffett's actual opinion. End with `Student decision: pending student response` unless the student has supplied their decision; never invent it.

Check the memo using `edgar_facts.py TICKER --offline --check-memo PATH`. Repair unsupported numbers before delivery. The numeric checker tests occurrence in printed output, not whether a number is assigned to the correct metric; read for semantic accuracy too. The Streamlit app loads the memo and performs the same check on edits.

Philosophy source (read only; never install FAskills or use its data feeds): [FAskills Buffett page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md). Adapt its durable advantage, understandable business, consistent earning power, owner-minded management and conservative financing lens. The lab's cash-flow-minus-total-capex definition overrides the page's maintenance-capex estimate. This lab excludes the page's valuation, prices, holdings, paid feeds and predictive outputs.

For Lab 19's investor panel, run `.venv/Scripts/python.exe projects/lab-19-legend-panel/panel.py TICKER --offline` instead. It reuses the unchanged Lab 18 engine and adds balance-sheet facts on the same fiscal periods. Read its actual output, then save this investor's memo to `projects/lab-19-legend-panel/memos/TICKER/buffett.md` with a `**Verdict: ...**` line and the same printed-number and honest-gap constraints above. Validate all investors with `panel.py TICKER --offline --check-memos`. Do not overwrite the original Lab 18 memo or invent a student decision.
