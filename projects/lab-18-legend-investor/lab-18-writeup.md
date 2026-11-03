# Lab 18 — Legend Investor as Skill

**Status:** Skill, calculation script, Streamlit app, both memos and student decision/reflection complete. All 35 COST known-answer values match SEC-derived output. Nine controlled tests, eight source/memo checks, six app checks and skill validation pass. The student reported the partner exercise and requested a current-context Codex comparison in place of the fresh-browser probe; that substitution is disclosed below.

## D — Decision question

Can an investor's philosophy become a skill your AI runs the same way every time—every number computed by code from the 10-K, the judgment the model's?

**Answer:** Its data selection, arithmetic and explicit checks can be repeatable for a fixed source snapshot. Its qualitative philosophy can guide judgment consistently, but the memo remains a model interpretation, not a mechanical proof of business quality. Refreshing SEC data can change results because later filings can restate earlier periods.

**Opening explanation to practice:** Code can compute ROE from annual net income and year-end equity. Deciding whether earning power reflects a durable competitive advantage requires judgment; passing a profitability threshold does not establish that competitors cannot erode it.

## R / I — Research and implementation

I asked the AI to create the workflow in [request.md](request.md). The [skill](../../.agents/skills/buffett-edgar/SKILL.md) lives in Codex's repository skill location and bundles the [calculation script](../../.agents/skills/buffett-edgar/scripts/edgar_facts.py). The [app](app.py) shows its facts, chart, three checks, provenance and saved memo, with the required SEC/AI/learning/not-investment-advice notice immediately under its title.

The philosophy reading is the instructor's [FAskills Buffett page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md). I use its focus on understandable businesses, durable advantages, consistent earning power and owner-minded management. This lab's owner-earnings proxy is operating cash flow minus total capital spending; it does not estimate maintenance capex. The app has no price data and cannot establish valuation or a margin of safety.

The numerical source is SEC EDGAR. Details of the exact tag priorities, annual-period selection, latest-filing rule and replay commands are in [README.md](README.md). No FAskills package or paid financial-data source is used.

## V — Verification

Nine controlled behavioral tests currently pass. They prove annual/quarter discrimination and latest filing selection, priority and fallback tags, an intervening missing cash input, nonpositive equity, threshold boundaries and failed checks, short histories, 53-week annual periods, numeric injection detection and invalid-ticker rejection. Synthetic fixtures are marked as synthetic and are never presented as downloaded facts.

Live SEC responses were downloaded November 3, 2026, using the required identifying User-Agent only at runtime. The public source bodies, exact retrieval timestamps and hashes are preserved in [evidence/](evidence/). No request identity is stored. No answer-key value is substituted into the calculation code. The independent [verification-results.json](verification-results.json) records **35 out of 35 matching COST values** and all eight source/memo checks passing.

| COST fiscal-year end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2022-08-28 | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3% | 3,501 |
| 2023-09-03 | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1% | 6,745 |
| 2024-09-01 | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2% | 6,629 |
| 2025-08-31 | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8% | 7,837 |
| 2026-08-30 | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8% | 9,382 |

Amounts are USD millions; ROE is percent. COST passes all three coded checks. Both chart series end above their initial values, although owner earnings decreases between FY2023 and FY2024. Full selected tags and filing provenance are in [COST-report.md](evidence/COST-report.md) and [COST-computed.json](evidence/COST-computed.json).

**JPM probe:** The five fiscal-year ends are December 31 of 2021–2025. Every capital-spending and owner-earnings entry is **not found**. Both owner-earnings checks are **not known**; the ROE check fails because FY2022 ROE is 12.9%. The [JPM memo](memos/JPM.md) explicitly says it cannot judge owner earnings. Source output: [JPM-report.md](evidence/JPM-report.md).

**Hand-entered number:** In the actual Streamlit app test, appending `Hand-entered ROE: 40.0%.` produces an unsupported-number error; reloading the saved memo clears it. All six [app checks](app-verification-results.json) pass: COST table/checks/memo/notice, both plotted series and endpoints, injection/reload, JPM gaps/memo, invalid ticker and unknown ticker. These are Streamlit AppTest runs against archived real SEC data, not browser screenshots. The original saved memos contain no unsupported numeric tokens.

**AI comparison — disclosed substitution:** At the student's request, [codex-comparison.md](codex-comparison.md) provides a Codex response to the assigned question using this conversation's existing computed evidence. Its five ROEs and fiscal-year-end labels match the table, and its sources are explicitly identified. This is not the requested fresh browser chat without the skill, so it does not test an unaided model's sourcing. No browser experiment or uncited-model error is claimed. Average-equity ROE can be legitimate elsewhere, but does not implement this lab's specified year-end-equity denominator.

## Explain the code — preparation, not a claim the exercise occurred

Open `year_row` in the bundled script. Its lines do the following:

1. Start a row carrying the actual fiscal-year-end date and annual start date.
2. Call `select_fact` for each raw field. That helper follows the tag priority, filters to eligible 10-K contexts and returns the latest filing's value plus provenance.
3. Read the selected net-income and year-end-equity values into local variables.
4. Read the operating-cash-flow and capital-spending values.
5. Compute ROE only when both inputs exist and equity is positive; otherwise retain `None` with the display label `not known`. Its formula identifies both XBRL input tags.
6. Compute owner earnings only when both cash inputs exist; otherwise retain `None`. Preserve the tags used for the subtraction.
7. Return the completed row.

**Where “not found” comes from:** If `select_fact` exhausts its permitted tags without an eligible observation, it returns `value=None` and records the searched tags. `display` converts a missing cell to `not found`, except a missing/undefined ROE whose explicit missing label is `not known`. Owner earnings stays missing when an input is missing. `compute` checks for missing values before evaluating any pass/fail predicate, so missing inputs do not silently become failed checks or zeros.

The script chooses the fiscal period before building each row. It ignores XBRL `fy` for historical labeling because a later 10-K can contain comparative facts from older fiscal years. Annual flow start/end dates and form determine eligibility.

**Actual partner exchange — student-reported:** The student reports explaining the fiscal dates, latest eligible 10-K facts, tag priorities and conditional calculations line by line. The partner asked why zero or negative equity sets ROE to `None` instead of producing a negative percentage. The student answered that this screen evaluates earning power on positive capital and must avoid misleading interpretations at the profitability hurdle. The student confirms the full role swap: the partner explained the missing-value path without AI, and the student asked how `select_fact` handles tie-breakers involving amended filings. The partner's answer to that final question has not been supplied.

**Technical clarification of that explanation:** Annual-period eligibility is established by `annual` and `compute` before `year_row` receives the dates; `select_fact` enforces those period dates again. Positive equity is required for ROE, not for owner earnings, whose only required inputs are operating cash flow and capital spending. A negative-equity ratio is mathematically calculable when equity is nonzero, but the lab defines it as **not known** because it is unsuitable for this screen; division by zero is mathematically undefined. Forms exactly equal to `10-K` qualify, so `10-K/A` amendments are excluded. Among eligible same-tag, same-period observations, filing date wins, with accession breaking a same-date tie. No partner response is invented for the amendment question.

## The call

The [COST memo](memos/COST.md) selects **watch it**: strong reported earning power merits further study, while the table cannot establish moat durability, trustworthy management or balance-sheet resilience. The model chose this verdict after reading the script's output; the script does not assign it.

**Student decision, supplied by the student and edited for printed units:** Yes, I trust the “watch it” verdict. COST passes the quantitative screen, with ROEs of 28.3%, 25.1%, 31.2%, 27.8% and 25.8% and final owner earnings of 9,382 million. Reported financial numbers alone cannot establish permanently defensible customer loyalty or wise reinvestment; passing the screen earns further study rather than a blind commitment. This decision also appears directly under the memo. The student's original rounded billions figure was expressed in the script's printed millions to preserve numeric traceability.

## Agent skills — learn on your own

**What is a skill?** A discoverable folder whose `SKILL.md` supplies a name, description, reusable instructions and optional scripts. This skill tells the model when to use SEC-backed business analysis and how to run the calculation before judging the results.

**Why read only name and description first?** The agent can select relevant capabilities without loading every skill's instructions into context. Once the request matches this skill, it loads the body; the script performs the deterministic work. This progressive loading keeps discovery cheap and leaves context available for the current task. [Official documentation](https://learn.chatgpt.com/docs/build-skills).

**Why put the numbers in code?** Code can enforce source forms, annual durations, tag priorities, missing-value handling and exact arithmetic, while preserving the chosen observation's provenance. A fluent model answer alone does not establish which filing, numerator or denominator produced a ratio. The model interprets earning power and acknowledges what the evidence cannot establish.

## Reflect — explanation to personalize

**What stays the same?** On the same saved SEC response, the selected annual periods, tags, missing-data rules, formulas, display rounding and checks repeat. The memo's verdict and reasoning remain model judgment; the skill constrains its evidence without guaranteeing identical wording or conclusions.

**Why is “not found” better than an estimate?** It makes a source limitation visible and prevents unsupported precision. For a bank such as JPM, substituting a different capital-spending proxy could silently change the economic meaning; `not known` correctly blocks the cash-flow checks until their required inputs exist.

**Student's own reflection:** “I can now confidently explain how deterministic Python scripts force AI to use audited, reproducible SEC 10-K facts rather than hallucinating ratios or using inconsistent accounting conventions like average equity. What still feels a bit uncertain is how to objectively split total capital expenditures into growth versus maintenance capex without relying on management’s subjective guesswork.”

**Accounting clarification:** Average-equity ROE is a valid alternative convention, but mixing it with year-end-equity ROE would make this lab's comparisons inconsistent. This workflow intentionally avoids a subjective maintenance/growth split by deducting total reported capital spending; it does not resolve the economic estimation question raised in the reflection.

## Checkout links

Submission repository: [JP161632/FIN43900-Fall2026](https://github.com/JP161632/FIN43900-Fall2026).

- [Skill](https://github.com/JP161632/FIN43900-Fall2026/blob/main/.agents/skills/buffett-edgar/SKILL.md)
- [Python calculation script](https://github.com/JP161632/FIN43900-Fall2026/blob/main/.agents/skills/buffett-edgar/scripts/edgar_facts.py)
- [Streamlit app](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-18-legend-investor/app.py)
- [Lab writeup](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-18-legend-investor/lab-18-writeup.md)
- [COST memo](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-18-legend-investor/memos/COST.md)
- [Verification results](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-18-legend-investor/verification-results.json)
- [Setup and reproducibility](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-18-legend-investor/README.md)

AI assistance: OpenAI Codex created the implementation, verification code, explanatory drafts and the explicitly labeled substitute comparison response. The student supplied the partner activity report, trust decision and reflection. The fresh-browser no-skill probe was replaced at the student's request, not represented as performed.
