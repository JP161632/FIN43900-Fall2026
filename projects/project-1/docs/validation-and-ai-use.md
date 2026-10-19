# NVIDIA: validation and AI use

Frozen technical evidence prepared October 19 2026. Valuation cutoff September 10 close; annual and interim reporting periods, sources and publication dates are in data/source-map.md. Facts, normalizations, analyst forecasts and outputs are separated in inputs.json, that source map, the contamination catalog below and outputs/results.json. The latest financial date is July 26; no October market facts enter valuation.

## Observed technical validation

Engine status **PASS**, 15/15 tests. run.py --all exits nonzero on failure. Official Week 3 answers come from lessons/week-03/teach-dcf-worked-example.md, including all nine grid cells; Week 2 fixture is lessons/week-02/starter/mini_case.csv. These are independently published known answers, not expected values generated from this implementation. Independent source check compares issuer release with SEC balance/notes and Treasury column definitions.

| Test / highest-risk claim | Result | Observed details |
|---|---|---|
| Official training DCF and nine cells | PASS | {"ev": 1624.8685199098418, "grid": [[28.598850582928744, 32.942594335725296, 39.02383558964048], [24.356422648726173, 27.497370398196836, 31.68530073082439], [21.057925415989104, 23.41403273251337, 26.443313568044573]], "benchmark": "lessons/week-03/teach-dcf-worked-example.md"} |
| Official Week 2 FCFF and bridge | PASS | {"fcff": 77.5, "equity": 820, "price": 8.2, "benchmark": "lessons/week-02/starter/mini_case.csv"} |
| Historical source reconciliations | PASS | {"income_cash_periods": 3, "balance_dates": 2, "max_income_cash_error": 0} |
| Independent source / definition check | PASS | {"evidence": "Issuer Q2 release BS independently compared with 10-Q BS/Notes 5,10,11; Treasury Sep 10 10 Yr (not real yield)", "cash_like": 56586, "marketable_equity_excluded": 42783, "book_debt": 33366, "fair_debt": 31400, "risk_free": 0.0495} |
| 25 forecast statement articulations | PASS | {"years": 25, "maximum_error_millions": 2.3283064365386963e-10, "no_plug": "Cash from cash flow; equity from retained earnings; minimum cash enforced"} |
| Prewritten directional changed input | PASS | {"prediction": "evidence/directional-test-precommit.md (AI-authored; not human lock)", "old_wacc": 0.13896509736724513, "new_wacc": 0.14896509736724514, "old_price": 118.58486735166377, "new_price": 108.37851365729144, "expected_direction": "lower", "actual_direction": "lower", "old_action": "WATCH / DEFER", "new_action": "WATCH / DEFER", "decision_effect": "Deferral persists because price remains above the base entry ceiling; discount-rate risk strengthens caution"} |
| WACC / growth monotonicity | PASS | "Higher WACC lowers value; higher g raises it even after terminal reinvestment; full bridge recomputed" |
| Invalid terminal / units rejected | PASS | ["Require 0 <= g < WACC", "WACC must be a decimal below 1", "Terminal growth must be below terminal ROIC"] |
| EV / equity / share bridge | PASS | {"equity": 2874734.3543390334, "dilution_test": "2% more shares lowers value; dividend cash also recomputed"} |
| Corrupt source / liquidity failure injection | PASS | ["BS_Jul 26 assets: 320273 != 320272", "base year 1 cash below floor; explicit funding needed"] |
| Highest-risk investment contamination experiment | PASS | {"financial_portfolio_excluded_from_nwc": 103021, "wrong_scaling_explicit_ev_drag": 126463.72972160792, "minimum_wrong_price_drag": 5.21672014361884, "diagnosis": "Repeats the Lab 10/11 investment-classification failure; false operating reinvestment is not economic capex"} |
| Signed cash-flow regression | PASS | "Negative year 1 FCFF reduces EV by 90.9091; no nonpositive-flow filter" |
| SBC free-cash-flow overstatement challenge | PASS | {"cost_treatment": "SBC expense retained, cash substitute, no addback, fixed shares", "minimum_wrong_five_year_value_inflation_per_share": 1.0450018556651153, "warning": "Terminal inflation would make the full error larger"} |
| Peer policy and consistent definitions | PASS | {"policy": "Retained from Lab 8; AMD use / AVGO qualify before new multiple calculations", "annual_gaap_only": true, "no_lease_debt": "Operating leases treated as operating in all EV calculations"} |
| Highest-risk causal downside and reverse DCF | PASS | {"base_action": "WATCH / DEFER", "downside_action": "DO NOT INITIATE", "minimum_low_case_cash_after_hypothetical_year 3_claim": 376201.3647226627, "cause": "Demand/collection/margin deterioration plus guarantee losses breaches the risk gate", "reverse_dc_shift": 0.1981961962529647} |

## Clean-environment cold run and first failure

Evidence/cold-run-log.md and cold-run-receipt.json record an actual assistant run: copied project, new venv --without-pip, no inherited third-party packages/network/credentials. Four deterministic outputs reproduce byte-for-byte: results.json, validation-results.json, visible-output.md, dashboard.html. First failure: none observed in this run; no fabricated repair story. This is technical reproduction evidence, not a student recording. Student must show an actual clean run and explain ownership in Video 2. Runtime Python version and timestamps are in the receipt. Finance engine is standard library only; optional pinned PDF dependencies are separate.

## Prewritten directional test versus required human lock

AI-authored prediction committed before first rebuilt execution: commit 7 c 404 d 5, evidence/directional-test-precommit.md. Test changes WACC from 0.138965097 to 0.148965097 decimal (+1 pp). Expected lower EV/share value and continued deferral; actual numbers/actions are recorded in the table and validation-results.json. This prewritten AI test **does not satisfy the required human-authored AI-off Locked Changed-Input Record**.

The complete truthful current locked-record status is in evidence/locked-changed-input-record.md: **INCOMPLETE / NOT EXECUTED AS A HUMAN LOCK**. Human author, AI-off prediction, immutable precommit timestamp, human chosen old/new inputs and units, expected direction/action, actual direction/action, and diagnosis must be supplied from an authentic new exercise. We have not backdated or filled these as completed. The procedural handoff is Student next steps.md. Final evidence must preserve both prediction and run artifact; unexpected outcomes require diagnosis, and unchanged action requires an explicit threshold explanation.

## Contamination catalog and financial limits

Annual FY26 H20 net 4,320 is a one-time normalization; normalizedEBIT134,707, GM 73.07%. It rolls out of LTM, so is not added again. Investment gains and interest income are excluded from operating FCFF. Equity holdings are not cash, financing acquisitions are not operating working capital, annual diluted weighted shares are not exact current shares, and old intraday price 224.35 is not September 10 close 218.36. New debt and pending acquisition are recognized. Stock compensation retains its owner cost through cash substitution, without addback or assumed future buyback benefit. Acquisition retention is expense, not purchase consideration; all purchase assets temporarily in goodwill is a disclosed allocation simplification. Market/peer annual denominators are qualified for timing/mix; no invented transaction multiple.

Interim balance roll-forward is interpolated, not reported. ROIC/terminal/WACC and investment recovery/default losses are assumptions. Uniform operating cash timing, constant lease/DT balances, refinancing debt, rounded equity-method classification and unknown guarantee-recourse probabilities constrain precision. Actual guarantee calls would require a funded cash/NI update; current loss assumptions are valuation bridge claims, not booked filing liabilities. The downside and entry gates ensure these limits affect action.

## Assumption-challenge and review record

Evidence/assumption-challenges.md contains every load-bearing driver with value, basis, challenge and evidence that changes it. Prior Lab 12 reported responses are preserved as historical, authenticity/attribution unverified; no partner name or AI model was supplied. The separate fictional rehearsal paragraph is explicitly AI-written and earns no human-review credit. Codex's independent review corrected source classification, cash-flow labels, dated inputs, acquisition funding, terminal reinvestment and peer definitions. No source statement is treated as proof merely because AI repeated it.

## Material AI uses and dispositions

Tool/interface: Codex based on GPT-6 (system-exposed identity); exact backend build/version not exposed. Interaction date October 19 2026. No claim is made about hidden reasoning, unseen chats or the model used in older labs.

| AI use | Independent check / disposition | Effect on decision |
|---|---|---|
| Inspect/reuse NVIDIA Labs 5/8/10/11/12 and existing Edition A | Prior files indexed with hashes and Git commits; original baseline unchanged. ACCEPTED WITH QUALIFICATION, checkpoint receipt missing. | Historical admission thesis distinguished from buy recommendation. |
| Research SEC/issuer/Treasury and extract facts | Definitions reconciled against statements and notes; issuer-release/SEC check. CORRECTED old cash/securities/debt classification. | Prevents inflated cash bridge and false reinvestment. |
| Build statements, FCFF/WACC/bridge/terminal and UI | Published known answers, articulation, boundary, sign and failure injection. ACCEPTED after 15 passing tests. | Conditional range, no price precision claim. |
| Draft forecast assumptions and stress/peer narrative | Full driver challenges; guidance not five-year fact; mixed peers qualified. QUALIFIED. | WATCH/DEFER; downside DO NOT INITIATE; no averaging. |
| Draft partner-style practice response | No authentic human source. FICTIONAL REHEARSAL ONLY; REJECTED as actual partner evidence. | Human-review requirement remains open. |
| Draft memo/scripts, run technical audit/cold run and prepare freeze | Cross-check financial numbers against results, PDFs rendered/reviewed, file hashes/access recorded. ACCEPTED as AI assistance, not student authorship/recording. | Student must understand/defend and complete missing evidence. |

## Freeze and access status

File-integrity.json hashes the stable artifact set with explicit exclusions to avoid self-reference. Submission-manifest.csv lists exactly 11 required rows plus optional deployment; videos/transcripts remain pending, not false links. Publication-audit.json records anonymous public access and hash checks after upload. A later final-video freeze must update the manifest, transcript artifacts and hashes under a new tag; do not move an existing frozen tag. GitHub upload is not Brightspace submission. Original Edition A checkpoint belongs at its designated checkpoint location; final assignment requires the seven-part bundle and receipt by October 19 2026 11:59 PM course time.
