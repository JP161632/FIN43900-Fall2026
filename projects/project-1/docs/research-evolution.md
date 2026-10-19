# NVIDIA: research evolution

Edition B prepared October 19 2026; historical valuation September 10 US close. Intended user: buy-side committee with no position; decide initiate/watch-defer/do-not-initiate over 12-24 months, expressed as a range with reversal conditions.

## Baseline boundary and dated addendum

Existing NVIDIA Edition A Markdown is preserved byte-for-byte, SHA256 FF289D7D83BF56F977D5D3F85F7CDF13125841075D5E8A59AF03FA845D39ED6B. Its original September 1 date and wording remain unchanged. The Appendix reproduces its text for reading; this newly rendered appendix is **not the original submitted Edition A PDF**. The first successful Brightspace checkpoint receipt and original PDF have not been supplied. No Git tag substitutes for that receipt, and this AI session cannot reconstruct an AI-off baseline retroactively.

October 19 addendum: Edition B uses September 10 close to align the earlier DCF/comparables labs, with Q2 information already public August 26 and acquisition disclosure public September 3. This date change is explicit. No October market facts enter the model. Baseline's “initiate” means initiate valuation research, not a buy recommendation. B's WATCH/DEFER therefore reflects completed valuation, not a claim the student previously recommended buying.

## Edition B decision and architecture

At 218.36, WATCH/DEFER; intrinsic causal range$56-$212, base reference$119; approximately$95 entry ceiling with 20% margin of safety plus evidence gates. Five rolling statements feed FCFF, WACC 13.90%, g 3% and ROIC 25%; explicit cash/financial investments/debt/claims/share bridge. Finance engine in model.py, facts/assumptions in inputs.json, visible results in outputs. No network/credentials/packages needed at runtime.

## A-to-B and prior-lab evidence table

| Evidence / prior view | Challenge and disposition | Observable change in B / decision |
|---|---|---|
| Edition A: DC growth 193,737 versus 115,186 merits research | Screening is not valuation evidence; growth durability and price remain open. | LTM base 302,970, DC growthfade and reverseDCF. Research admission becomes conditional watch/defer. Original text unchanged. |
| Lab 5: annual-basis value 62.72; WACC 15.88%; reverse bracket fails | Stale annual growth path and inadequate bracket do not prove mispricing. | Latest-quarter operating base, explicit assumed WACCbuild, reinvestment terminal and solved reverseDCF; old output retained only as history. |
| Lab 8: annual GAAP P/E peer interval 370.66-931.18 | Two heterogeneous peers and stale annual EPS exaggerate confidence. | Preserve policy, add consistent EV/sales and latest balances; show leave-one-out; no mechanical averaging. |
| Lab 10: personalized GM/R&D/SG&A/days/PPE forecast | “Other assets” mix operating/investment holdings; FCFE/cash-after-payouts labeling and discount basis inconsistent. | Investments removed from operatingNWC, no markups in EBIT; FCFF from statements at WACC; all signed cash flows retained. |
| Lab 11: sensitivity depends on ranges; margin/WC effects not zero | +/-5 pp growth compounds; +/-2 pp margin has distinct timing. Dropping negative flows is wrong. | Named stress cases, margin/growth what-ifs, signed-flow regression and cash minimum failure test. |
| Lab 12: reported partner demand challenge and claim about commitments | Partner authorship/identity unconfirmed; supplier commitments are not orders. | Qualified historical review credit, independent Note 10 check, downside risk gate; fictional rehearsal sample clearly labeled. |
| Latest source definition: securities/cash and debt changed | Annual 62,556 includes equity holdings; debt 8,468 stale after new issuance. | Latest cash+debtsecurities 56,586, separate public/private recoveries, debt 33,366 book/31,400 fair. Definition check executed. |
| Pending acquisition headlines | Retention is service compensation; control synergy not public-share multiple. | Purchase cash 11,900 and retention 1,000 modeled conservatively, no incremental operating benefit. |

## Attribution of research changes

Course requirements supplied the five-year FCFF framework with articulated statements, evidence boundaries and validation standards. Existing student-supplied NVIDIA materials supplied the target, initial research-admission question and prior lab trail. Labs 10-12 already recorded investment classification, cash-flow labeling and sensitivity limitations before the October 19 rebuild; their existence is independently inspectable, but this package cannot establish who authored every older passage. The Lab 12 record reports partner questions; attribution remains qualified until confirmed.

Codex assisted the October 19 filing research, code rebuild, scenario assumptions, documentation and checks. The revised forecast and discount-rate choices are analyst assumptions that the student must evaluate and defend; they are not new reported facts or automatically the student's independently authored judgment. Sources and executed tests justify accepting or qualifying those outputs. The move from Lab 5's 62.72 to the current base 118.58 cannot be credited to AI alone: reporting base, operating forecast, WACC, reinvestment, bridge and share basis all changed. No controlled dollar-by-dollar historical attribution is asserted. The action stays watch/defer from Lab 5 to B, while Edition A was admission to research rather than a buy decision.

## AI output independently corrected

Material output at issue: prior forecast treated broad other-assets balances as operating reinvestment and labeled cash after payouts as FCFE. Independent evidence: Q2 balance and Notes 5/6 identify 42,783 marketable equity,51,157 private holdings and investment components in other assets. Disposition **CORRECTED**: financial investments are CFI/assets/bridge items; FCFF retains operating NWC only. Quantified deliberately wrong scaling is in validation-results.json. This is a check against primary financial definitions, not another AI's agreement.

Further corrections: reject “supplier commitments prove customer backlog”; reject dropping negative forecast flows; keep SBC owner cost; correct export-risk citation to Item 1 A rather than Note 17. AI was useful for code/source organization and locating possible contradictions; independently sourced tests decide whether output survives. The exposed interface identifies Codex based on GPT-6; exact backend build/version is not exposed and is not invented.

## Unresolved evidence that limits credit

The student must supply the original checkpoint PDF/receipt, complete a genuinely human-authored AI-off locked prediction before a new run, confirm authentic prior partner discussion or obtain real review, record three bounded videos and correct actual transcripts. No sample answer, generated script, or assistant cold-run receipt is relabeled as a human event. Student next steps.md gives exact preparations and recording routes. This package supports a defensible decision but cannot certify missing history or a score.

<!-- pagebreak -->
## Existing EditionA text - reading reproduction only

The source file below remains byte-identical in evidence/. This typeset reproduction was made October 19 and is not an original submission artifact.

# Project 1 — Edition A

**Company:** NVIDIA Corporation (`NVDA`; CIK 0001045810)  
**Valuation date:** September 1, 2026  
**Decision user:** Investment committee with no current NVDA position  
**Decision:** Decide whether to initiate, watch/defer, or not initiate a position after a defensible enterprise-value-to-equity-value valuation range is completed.

## Initial thesis — initiate

Initiate valuation research on NVIDIA. NVIDIA merits deeper valuation research because Data Center revenue increased from $115.186 billion in fiscal 2025 to $193.737 billion in fiscal 2026. This growth suggests that AI-computing demand may be an important driver of future operating value, subject to testing its durability, profitability, and valuation. This is a preliminary research-admission decision, not a buy recommendation.

## Known evidence

All company-specific facts below are from NVIDIA's [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), filed with the SEC.

| Item | Reported evidence |
| --- | --- |
| Entity | NVIDIA Corporation (`NVDA`; CIK 0001045810) |
| Primary filing | Form 10-K; accession `0001045810-26-000021`; filed February 25, 2026 |
| Reporting period | Fiscal year ended January 25, 2026 |
| Currency and units | U.S. dollars; financial-statement amounts in millions, except per-share data |
| Cash | Cash, cash equivalents, and marketable securities of $62,556 million at January 25, 2026 |
| Debt | Debt net carrying amount of $8,468 million: $999 million short-term and $7,469 million long-term |
| Diluted-share evidence | Diluted weighted-average shares of 24,514 million for fiscal 2026 |
| Operating-value driver | Data Center revenue of $193,737 million in fiscal 2026, up from $115,186 million in fiscal 2025 |

## Synthetic enterprise-to-equity bridge check

Using the class synthetic case, all monetary values and shares are in millions:

`Equity value = 1,000 + 100 - 250 - 20 - 10 = 820`

`Per-share value = 820 / 100 = $8.20 per diluted share`

This check confirms the direction of the bridge: add non-operating cash, subtract debt and senior/non-common claims, then divide common equity value by diluted shares. It is a mechanics check only, not a valuation of NVIDIA.

## Consequential assumptions

- Data Center demand can remain durable beyond the current AI-infrastructure buildout.
- NVIDIA can retain sufficient pricing power and operating margins to convert Data Center demand into future free cash flow to the firm.
- The eventual valuation will use a consistent bridge policy for cash, marketable securities, debt, lease liabilities, and diluted shares.

## Unknowns and uncertainties

- The degree of customer concentration and the risk that a small number of customers reduce purchases.
- The effect of export controls and competition on revenue growth, pricing, and margins.
- Whether current AI-infrastructure spending is sustainable or reflects an unsustainable buildout.
- The appropriate valuation range as of September 1, 2026, including forecast growth, margin, WACC, terminal growth, and the classification of cash and debt-like claims.

## Research plan

1. Build a filing-based evidence ledger for revenue, EBIT, tax rate, D&A, capital expenditures, operating net working capital, cash, debt, and diluted shares.
2. Identify and label any non-recurring, accounting-basis, or classification issue before forecasting FCFF.
3. Build an FCFF valuation, bridge enterprise value to common equity, and state the diluted-share convention used.
4. Test the conclusion with revenue-growth, operating-margin, WACC, and terminal-growth sensitivities.
5. Check the durability of Data Center revenue using later filings and disclosures on customer concentration, export controls, supply commitments, and competitive conditions.

## Partner-generated falsification question

> What evidence in NVIDIA's future filings would show that the Data Center revenue increase is not durable enough to support the initiate thesis?

No answer is proposed here.
