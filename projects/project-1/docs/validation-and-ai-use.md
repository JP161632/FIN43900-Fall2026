# Salesforce validation and AI use

Project 1. Economic cutoff 2026-08-27 at 16:00 US Eastern; preparation 2026-10-19. Security NYSE CRM US common share; USD millions and shares millions; price USD/share. Committee no position;12-24 month decision horizon. The root `Validation-and-AI-Use.pdf` and repository `docs/validation-and-ai-use.pdf` are generated from this exact Markdown source. Final frozen hashes are listed in `file-integrity.json`; use the Git commit referenced by the final manifest/repository history.

## Status and boundary

The model and automatic validation are executed. **The package is not a fully completed course submission.** Missing human evidence is explicitly preserved: authenticated Salesforce Edition A/receipt, human-authored AI-off locked prediction and run, credited Salesforce partner review, three student videos, corrected actual transcripts and logged-out instructional access checks. No statement below treats AI-assisted tests as substitutes.

The existing NVIDIA Markdown candidate is copied unchanged and hashed in the research-evolution brief. A Git tag/commit cannot substitute for the designated Brightspace checkpoint. The student must resolve the company switch and missing evidence with the instructor; no course approval is asserted.

## Data and definition controls

Every historical numerical input is in data/inputs.json; source IDs, public dates, period ends, links and locators are in data/sources.json. evidence/data-lineage.md supplies field mappings, transformations and contamination exclusions. evidence/assumption-challenges.md gives each material hypothesis's value, basis, challenge and evidence that changes it. Historical facts, analyst normalizations, forecasts and model outputs are distinguished.

Primary facts public by the cutoff come from Salesforce FY26 Form 10-K and July 2026 Form 10-Q; Adobe FY25 filing and May 2026 Form 10-Q; ServiceNow FY25 release and June 2026 Form 10-Q; Treasury Aug 27 daily ten-year yield. Historical common-share prices use aligned Aug 27 US closes from named providers. No dividend-adjusted CRM price, foreign CDR, future earnings release or provider-defined EV is silently substituted.

Independent source/definition check: Salesforce gross cash plus marketable debt securities is 8310+3093=11403M in the interim filing and issuer earnings release. Financial borrowings are 36800M fair value (30800 senior notes plus 6000 floating term loan), distinct from 39288M carrying value. Finance leases 633M are a separate financial claim; operating leases remain operating. Treasury's10 Yr row value 4.67%, rather than adjacent 7 Yr 4.52%, is the risk-free input. Sources/locators: CRM_Q p.3/note 8, CRM_RELEASE balance sheet, UST Aug 27 row.

Research occurred October 19 and is disclosed; facts published later than August 27 are excluded. The latest July cash/debt values are rolled or qualified, not represented as contemporaneous observed August balances. A no-cash-roll and book-debt-basis sensitivity quantify the date/basis gap. Original source PDFs were used temporarily for extraction where available and are excluded from Git; limited numeric facts, source links and model transformations remain reproducible. No credentials, private receipt, private prompt transcript or paid-feed redistribution is included.

## Finance conventions

The base uses LTM revenue 43938M, normalized to 44439M after annualizing partial Informatica revenue. EBIT normalizes 8735M to 9358.055M through a497.805M restructuring adjustment and 125.25M incremental contribution. Compensation remains a cost. Forecast statements cash-substitute future equity compensation and keep the share proxy fixed, avoiding an addback without offsetting dilution. They are normalized economic pro-formas, not management GAAP guidance.

Commission additions and amortization are separate from PP&E capex/D&A. PP&E depreciation, acquired amortization and operating rent are not conflated. Operating ROU/liabilities use a replacement convention; finance leases are in debt and have principal repayments. Net income rolls equity; CFO/CFI/CFF roll cash. There is no arbitrary equity balancing plug. A funding shortfall appears explicitly as hypothetical new borrowing and blocks initiation; it is not evidence of available committed credit.

FCFF = EBIT after normalized tax + PP&E depreciation + acquired amortization + commission amortization - commission cash additions - change in operating NWC - capex - modeled acquisition cash costs. Interest is excluded from FCFF and added back after tax only in the CFO reconciliation. Debt repayment/dividends are financing cash flows, not FCFF deductions. Terminal cash flow uses next-year NOPAT times(1-g/ROIC), with acquired amortization faded out. g<WACC and g<ROIC are enforced.

The first forecast year ends July 31 2027. July 31-Aug 27 2026 is 27/365 of a year; the first remaining FCFF is prorated and discounted over 1-27/365 years. An estimated operating/financing cash roll moves surplus cash to the valuation date. A pending acquisition cannot be presumed paid before cutoff. Uniform timing, constant ratios and the first-year-end acquisition stress are approximations; no daily cash observations are claimed. Forecast future surplus cash is not added twice at terminal.

## Executed validation register

`outputs/validation-results.json` is the detailed machine-readable evidence; all 22 checks pass. `outputs/results.json` preserves inputs/results/statement lines, and `outputs/visible-output.md` shows results without execution. Model/test source is fully inspectable.

| Claim | Test and expected behavior | Executed disposition |
|---|---|---|
| Official course DCF |FCFF 100 grows 8/6/5/4/3%; WACC 10%,g3%; compare official EV 1624.87, price 27.50 and all nine published grid cells. |PASS within published rounding tolerance. Fixture lessons/week-03/teach-dcf-worked-example.md; does not use an AI-invented benchmark. |
| Official Week 2 bridge |EBIT 150,tax 25%,D&A40,capex 60,NWC 15 gives FCFF 77.5; EV 1000+cash 100-debt 250-NCI 20-pension 10 gives equity 820/share 8.20. |PASS; fixture lessons/week-02/starter/mini_case.csv. |
| Base-year filings |Three historical income/cash-flow periods and two actual balance sheets reconcile to public totals. |PASS; arithmetic does not assert an external audit opinion. |
| Pro-forma articulation |Three causal cases plus three what-if scenarios, five years each: balance sheets balance and cash-flow ending cash equals balance-sheet cash. |PASS 30 annual forecast articulations; errors must be within 1e-7M. |
| Direction before execution |AI-authored plan saved before first run: WACC+100bp lowers EV/price with forecast/bridge fixed. |PASS; base about 195 to 165, watch/defer unchanged because entry condition remains unmet. This is not the human locked record. |
| Terminal boundaries and direction |g=WACC, g>WACC and zero WACC reject; positive-cash-flow sensitivities rise with g and fall with WACC. |PASS all tested cells, including reinvestment-aware terminal. |
| Traceability failure |Remove a source availability date or supply a future date. |PASS: model explicitly rejects missing/look-ahead evidence. |
| Accounting failure |Inject 1M into base-year cash without changing published assets. |PASS: asset-sum error raises ModelError. |
| Share/peer definitions |Zero diluted shares, duplicate peer and negative peer EPS must fail; peer EV/revenue and P/E are independently checked. |PASS; no bridge on P/E. Leave-one-out yields a one-peer reference, not a range. |
| Highest-risk economic failure |Add recurring SBC back without a cash/dilution offset. Expected value rises incorrectly. |PASS detection; rejected value about 285 versus accepted 195, overstatement about 90/share. At the observed price the action remains defer; inflated headroom is not allowed to become evidence. |
| Connected compensation driver |Raise recurring compensation 8% to 9%. |PASS: earnings, cash and value fall; corrects an earlier disconnected input. |
| Funding failure |Raise analyst cash floor to 50000M. |PASS: new funding is visible and action becomes do not initiate. No covenant/default claim is made. |
| Decision-altering downside |Churn, hosting margin and collections pressure propagate through statements. |PASS: churn/collections changes watch/defer to do not initiate, value about 83. First failure is joint growth/margin underwriting rule; coverage remains above 3x initially. |
| Bridge robustness |Add 33M shares, omit cash roll, use book rather than market financial debt. |PASS: dilution lowers value to about 187; omit roll lowers value about 0.7/share; book debt lowers it about 3/share. |
| Reverse DCF |Solve parallel five-year/terminal EBITA margin shift, then rerun at the solution. |PASS: reproduced 252.05 within 1e-7. Base other policies held fixed; implied margins are not unique market expectations. |

## Highest-risk claim and cold run

Highest-risk claim: durable operating cash earnings support an equity purchase without treating recurring stock compensation as free. Independent filing definitions and the deliberate wrong-answer test target that claim. The rejected model still runs and balances; therefore passing accounting invariants is necessary but insufficient.

A new temporary directory and new Python virtual environment are used for the assistant's clean end-to-end run with no installed model dependencies, network calls or credentials. Exact commands, runtime, first failure/resolution and hash comparison are preserved in `evidence/cold-run-log.md` and its receipt. This is an assistant-executed clean run; **no student recorded cold run is claimed**. Video 2 must demonstrate technical ownership and provide the required recorded evidence.

## Locked Changed-Input Record

**MISSING HUMAN EVIDENCE.** See evidence/locked-changed-input-record.md. The following required fields are all NOT PROVIDED: human author; material old/new input with units; finance-grounded predicted direction and predicted decision effect; precommit timestamp/timezone; immutable commit/snapshot; AI-closed run timestamp/environment/command; preserved before/after outputs; actual direction and actual decision effect; reconciliation; failure diagnosis or no-action-change reason. No AI-authored text is substituted for these fields.

Existing authentic evidence can be supplied unchanged. Otherwise the student must ask the instructor for the permitted recovery path after disclosing that AI-assisted Salesforce work has occurred. A newly backdated record cannot repair chronology. The AI-assisted WACC test and its prediction are separately labeled throughout this package.

## Named AI-use register

Tool: Codex in the shared course workspace, identified in the session as based on GPT-6. A finer model build/version was not exposed and is not invented. Interaction date 2026-10-19. Web research used the exposed web search/open tool; implementation and checks used file/shell tools and local Python 3.13.15. PDF authoring used ReportLab 5.0.1; rendering used PyMuPDF 2.0; these are deterministic software dependencies, not additional AI opinions. No second AI partner was used. Material dispositions below are the assistant's reviewed dispositions pending the student's own verification.

| Material AI use | Output considered | Independent evidence and disposition |
|---|---|---|
| Source discovery and transcription |Company/peer input candidates, filing periods and provider definitions. |MODIFY/QUALIFY against opened SEC/issuer documents and Treasury table. Do not accept provider labels or post-cutoff facts automatically. Field lineage and source-definition tests retained. |
| Forecast/model architecture and code |Subscription cohorts, economic compensation, linked statements, FCFF and terminal engine. |QUALIFY: required architecture follows course brief; published training-case answers, filing reconciliation and fail-loud invariants independently test arithmetic. Driver values remain contestable analyst hypotheses. |
| Early compensation implementation |SBC rate initially appeared without affecting earnings. |CORRECT: link a rate change to EBIT/cash/terminal margin; dedicated 8%-to 9% test confirms actual propagation. Filing recurring expense supports the economic correction. |
| Lease and acquisition timing implementation |Draft omitted finance-lease principal schedule and could roll pending deal cash before cutoff. |CORRECT against 10-Q notes 5/6/8; total 633M lease principal is allocated over future periods; pending cash excluded from pre-cutoff roll. Output regenerated. |
| Highest-risk counterexample |Recurring SBC addback without offsetting dilution/cash cost. |REJECT: filing distinguishes expense and CFO addback; incorrect result about 90/share higher. Running/balancing does not cure the economic error. |
| Research and memo preparation |Conditional watch/defer, method disagreement, monitoring thresholds and recording scripts. |QUALIFY: numbers are traced to executed outputs; no promised return, fabricated baseline, peer review, transcript, receipt or student attestation. Student must defend and accept responsibility. |
| Rubric audit and packaging |Checklists, manifest, integrity hashes, PDFs and audit. |ACCEPT as mechanical assistance only. It cannot guarantee points, certify human authorship or turn missing evidence into completion. |

## Limitations and monitoring

Provisional beta/ERP, private-investment realization, diluted-share proxy, uniform stub cash timing, static tax/lease balances, mixed fiscal-end peer denominators and pending M&A limit precision. At about 72% terminal share, terminal economics require more scrutiny than an attractive five-year chart. Additional full acquisition/PPA and award-valuation work could narrow the range; it is a condition before initiation. No transaction multiple is used with an indefensible numerator. The process preserves a fair-value range and conditional action rather than averaging weak methods.

Monitor each quarterly release: organic subscription growth, GAAP EBIT margin, compensation/revenue, billing/collections, debt/ASR shares, cash and deal integration. Revisit within five business days. Initiation requires the stated price discount plus operating and bridge confirmation. Weak growth<3% with EBIT margin<21% across two quarters, coverage<3x, cash<2000M or new funding need blocks initiation. These analyst conditions do not claim covenant breach, payment default or realized loss.
