# NVIDIA recording evidence - reading aid

Generated from actual saved results, validation output and indexed earlier lab. Historical valuation September 10,2026; build/review October 19. This aid makes underlying evidence readable; it is not a substitute for original filings, code, test execution or authentic student events. USD millions unless marked USD/share.

## R1 Before and after

| Item | Earlier Lab 5 | Revised Project 1 / why comparison needs care |
|---|---|---|
| Decision | Watch-defer, after initial research admission | WATCH / DEFER remains; structural downside -> DO NOT INITIATE |
| Base estimate / USD per share | $62.72 | $118.58; not a controlled single-input change |
| Interval | $55.59-$72.40 WACC/g grid | $55.93-$212.08 causal low/base/high; DIFFERENT definition |
| Operating starting point | FY26 revenue 215,938 M; startingFCFF96,895.891 M | LTM revenue 302,970 M; five linked statements generate operatingFCFF |
| Year 1 forecastFCFF / USD millions | 130,809.4529 (Lab 5 Year 1) | 191,481.4896 full rollingyear before valuationstub; different forecastwindows, not a realized cash-flow gain |
| Discount rate / terminal | 15.88% WACC /3% g; FCFF Gordon continuation | 13.8965% WACC /3% g /25% ROIC; mature reinvestment explicit |
| Share basis / millions | 24,514 annual weighted-average diluted | 24,242 proxy =24,147 period-end basic+95 incremental quarter dilution |
| Market comparison | 224.35 intraday Sep 10,1:37:33 pmEDT | 218.36 Sep 10 US close; neither is an October quote |
| Evidence date versus build date | Annual fiscal 2026 endedJan 25 | LTM endedJul 26; publicAug 26; valuationSep 10; rebuiltOct 19 |

Original earlier evidence: [Lab 5 valuation and sensitivity](../../lab-05-nvda-dcf/nvda-dcf-lab.md); earlier file SHA256 `a40f09d61551323ef6fb2920d2106e7629ac590ca59f8b523d6d8c69b4ede7a3`. Original baseline text: [unchanged EditionA](../evidence/edition-a-existing-nvidia-unchanged.md); [research evolution](../Research-Evolution.pdf), baseline reading appendix page 3. Current numbers: [executed results](../outputs/results.json). Do not claim a new typeset appendix proves the original Brightspace checkpoint.

## R2 Why it changed / attribution

| Cause | Supported contribution | Limit on attribution |
|---|---|---|
| Course instruction | Five-year FCFF/enterprise-equity architecture, validation and decision standard | Instruction supplies method, not NVIDIA fair value |
| Existing student-supplied materials | Target/research-admission question and saved earlier lab outputs | Does not establish authorship of each older passage or original checkpoint receipt |
| Prior lab analysis/review | Lab 11 withholds a new value until classification/discount/terminal issues are resolved | Lab 12 reports partner questions; authenticity/credit unconfirmed here |
| AI assistance Oct 19 | Source organization, rebuild, assumptions/scenarios, tests and documentation | Not all changes were caused by AI; no claim AI-generated assumptions are reported facts |
| Primary evidence + numerical challenge | Latest filing definitions and test results support accepting/correcting/qualifying outputs | Passing accounting checks cannot establish forecast truth |

Lab 11 states: “Value-per-share spans are unavailable because valuation remains unresolved.” Read [Main driver over the tested ranges](../../lab-11-nvda-sensitivity/lab-11-writeup.md). It also states that the growth ranking depends on chosen ranges. The recorded limitation existed before the rebuild; internal balance alone did not justify a valuation. The new base is not simply Lab 5 plus one correction: data base, forecast method, WACC, terminal economics, bridge and shares all changed. The revised beta 1.8 and ERP 5% are explicit analyst assumptions, not a newly verified empirical beta; Treasury 4.95% is sourced. The lower WACC must be challenged, not presented as automatic model improvement.

## R3 Independent correction and test

| Primary-source fact / July 26,2026 | Amount USD millions | Model implication |
|---|---|---|
| Cash and equivalents | 22,443 | Cash balance; retains 10,000 operating reserve separately |
| Marketable debt securities | 34,143 | Cash+debt securities=56,586 |
| Marketable equity securities | 42,783 | Not cash; separate recovery assumption/bridge |
| Financial portfolio excluded from operatingNWC | 103,021 | Public 47,740 + private/other 55,281; counted separately once |
| Carrying debt / fair-value debt | 33,366 /31,400 | Book debt in statements; fair value in DCF bridge/WACC |

Primary check: [NVIDIA Q2 Form 10-Q, balance sheet and Notes 5/6/11](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm); [independent issuer release balance sheet](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027). Find 42,783 and read the row label/date; the current source map is our index, not independent proof by itself.

AI output disposition: **CORRECTED** financial-investment/operatingNWC classification; **QUALIFIED** forecast growth, beta, recoveries and guarantees. A deliberately wrong scaling diagnostic creates 126.46 bn of false discounted explicit-period investment, equivalent to$5.22/share in that calculation. This is a bounded illustrative subtraction exercise, not a full alternate forecast/terminal/stub-consistent valuation or attribution of the historical price change. It supports taking classification seriously; the source definitions justify the correction.

## R4 What changed the judgment

Final base **$118.58**, causal range **$55.93-$212.08**, dated market **218.36**, action **WATCH / DEFER**. Later action held from Lab 5 to finalB even though estimated value changed; EditionA was research admission. Base DCgrowth 40/30/22/15/10% is a forecast, not filing guidance. It is challenged by customer funding, collections and deployment/power constraints. Next filings showing sustainable demand with collection/margin conversion could justify revising it; supplier commitments are not customer orders. Entry ceiling$94.87 is conditional on refreshed evidence. [Full driver challenge record](../evidence/assumption-challenges.md).

## V1 Known answer and company arithmetic

| Check / units | Independent expected answer | Actual engine result |
|---|---|---|
| Training EV / USD millions | 1,624.87 rounded | 1,624.86852 |
| Training share value / USD | 27.50 rounded | 27.49737 |
| All nine sensitivity cells | Published Week 3 grid | Each tested within 0.006 USD/share |
| Company full year 1 FCFF / USD millions | NOPAT+D&A-capex-deltaoperatingNWC | 215,665.83+4,450.75-12,535.95-16,099.14=191,481.49 |
| Three-statement articulation | Assets=liabilities+equity; cash ties; no plug | 25 forecastyears; max error 2.33 e-10 M |

Independent expected answers: **course repository** lessons/week-03/teach-dcf-worked-example.md, published training EV 1,624.87 and price 27.50 (not invented company data). [Actual test results](../outputs/validation-results.json), “Official training DCF and nine cells”; [test implementation](../tests.py), functionknown. Company year 1 endsJuly 26,2027; the full-yearFCFF above precedes the elapsed 46-day valuation-stub adjustment. [Statement-to-FCFF code](../model.py), forecast; [all company statements](../outputs/visible-output.md).

## V2 Highest-risk failure evidence

Financial assets excluded from operatingNWC:103,021 M. Deliberately scaling them with sales creates false operating reinvestment: the bounded diagnostic's discounted amount is 126,463.73 M /$5.22 per share. This does not calculate the complete valuation error. Source grouping plus the diagnostic challenges the prior-lab classification rather than only checking whether the statements balance.

Two deliberately bad inputs are also rejected. A1 M asset corruption produces **“BS_Jul 26 assets:320273 !=320272.”** A forced first-year investment purchase 10,000,000 M produces **“base year 1 cash below floor; explicit funding needed.”** A passing test means the expected rejection happened, not that the corrupted run was financially viable. [Actual failures captured by tests](../outputs/validation-results.json), “Corrupt source / liquidity failure injection”; [test code](../tests.py), functionbroken.

## V3 Changed input: prediction versus result

| Item | Before | After / observed effect |
|---|---|---|
| WACC / decimal | 0.138965097 | 0.148965097; +0.01 =+1 percentagepoint |
| Estimated USD/share | $118.58 | $108.38 |
| Prediction / direction | Lower EV/per-share; continued deferral | Lower; WATCH/DEFER remains; price 218.36 still above the entry ceiling |
| Chronology | AI prediction committed in 7 c 404 d 5 before rebuilt model execution | Later humanized draft is retrospective; cannot backdate new wording |
| Human-lock evidence | Separate record currently INCOMPLETE | Use actual completed record or truthful instructor-permitted designation |

The current test recomputes discount-dependent bridge claim PVs, holding operating forecasts/terminalgrowth/bridge assumptions fixed. It is not a forecast-change scenario. [Original AI prewritten prediction](../evidence/directional-test-precommit.md); [actual result](../outputs/validation-results.json), “Prewritten directional changed input.” Correctly anticipating direction supports implementation; it does not validate the selected WACC as true.

## V4 Evidence boundary

[Current human-lock record](../evidence/locked-changed-input-record.md) remains markedINCOMPLETE; [humanized response draft](../docs/changed-input-response-draft.md) was written after the test. Use your actual completed artifact if saved elsewhere. A reported instructor exception can change which exercise is permitted, but cannot create a past AI-off prediction. Original checkpointPDF/receipt and confirmed partner attribution are also not supplied in this local package. These limits are separate from 15 passing financial tests and a reproducible assistant cold run. A new recorded student run must show what actually happened.

## C1 Dated action and causal range

| Causal case | USD/share | Action / economics |
|---|---|---|
| Low | $55.93 | DO NOT INITIATE: demand/financing/margin/collection deterioration, extra losses; declared risk gate |
| Base | $118.58 | WATCH / DEFER at 218.36; no 20% marginofsafety |
| High | $212.08 | Stronger sustained adoption/collections; not a probability-weighted target |

Base operatingEV$2,793,797.33 M + netbridge$80,937.03 M =common equity$2,874,734.35 M; divide 24,242 M proxy diluted shares ->$118.58/share. Forecast basic/awards are not exact September fully diluted cap-table facts. [Dashboard](../outputs/dashboard.html); [memo](../Decision-Memo.pdf).

## C2 Method disagreement

Historical annual GAAP P/E peer references:$370.66-$931.18. EV/annualsales references:$213.26-$251.76. AMD's lower margins and product mix, AVGO's software/acquisition mix, two-peer instability and stale annual denominators limit inference. Each method uses its disclosed consistent numerator/bridge convention; noncash investments are not added twice. Do not average these into the DCF range. [Peer policy](../evidence/peer-policy.md); [full method output](../outputs/visible-output.md); memo page 2.

## C3 Market expectation and terminal dependence

Base terminal-value share:65.1%. BaseWACC13.8965%,g 3%,ROIC 25% ->reinvest 12% of terminalNOPAT. At fixed other base inputs, the 218.36 marketprice requires+19.82 percentagepoints to **each** DCgrowth assumption: 59.8%, 49.8%, 41.8%, 34.8%, 29.8%. Year 5 sales 1,691.9 bn. This is one conditional solution, not a unique market forecast. It differs from Lab 5's limited-bracket failedreverseDCF because the underlying engine/base/shiftedvariable changed. [ReverseDCF output](../outputs/results.json).

## C4 Committee monitoring

**Ask:** WATCH / DEFER; no current position;12-24 month decisionhorizon. Consider initiation only below the refreshed 20%-discount entry ceiling (currently$94.87) with evidence supporting demand, collections, margins and funded commitments. Price alone is insufficient.

**Review every quarterly filing:** two consecutive quarters of DCgrowth below 20% challenge durability; collectiondays above 95 or reportedGMbelow 70% challenge conversion/profitability; material guarantee/capacity losses require immediate reassessment and a funded cash/NI model update. BaseforecastGM>=72% and collection assumption 75 days need support before initiation. DSOconvention here is endingreceivables/LTMsales*365, not an unqualified provider label. Current guarantees are valuationbridge expected-loss assumptions, not booked filing debt; the adverse-regime riskgate is a declared policy condition.

Durable faster growth with collection/margin intact could justify an upward revision, rather than a fixed permanent rejection. Refresh price,rates,awards,debt,investmentrealizations,pending-acquisitionfinancing and guarantee terms before any trade. [Memo page 2](../Decision-Memo.pdf); [monitoring section](../outputs/visible-output.md).
