# Project 1 rubric audit

Audit date October 19, 2026. Target Salesforce / NYSE CRM. Scope: every authored file in this project folder, the supplied course brief, shared seven-part/12-row checklist and six analytic criteria totaling300 points. This is an evidence audit, not a guaranteed grade. **No honest audit can certify maximum points while the human evidence below is absent.**

## Criterion by criterion

| Criterion and weight | Evidence delivered and audited | Open requirement / effect on maximum points |
|---|---|---|
| Problem definition and decision usefulness45 |README, two-page memo, Edition B and results explicitly state buy-side user, no position, security, USD/diluted basis,12-24 month horizon, historical cutoff, conditional watch/defer and reversal triggers. Screening is excluded. |Authentic Salesforce Edition A PDF/first receipt and instructor ruling on target change were not supplied. The retained NVIDIA candidate is byte-identical but cannot prove a Salesforce baseline. Full A-to-B credit cannot be assured. The course directs that the missing baseline itself is not penalized twice elsewhere. |
| Data integrity and traceability45 |Frozen numerical inputs and source catalog; primary-filing dates/locators; field-level lineage; normalized-versus-reported LTM bridge; contamination catalog; cash/debt/share definitions; licensing/revision/privacy policy. Beta/ERP and forecasts explicitly assumptions. |Market debt and balance/share dates remain dated proxies; quantified and conditional on refresh before initiation. These limitations are disclosed, not silently repaired with future facts. Student must navigate/check primary evidence during defense. |
| Financial soundness and judgment60 |Five-year linked statements for three cases and three stresses; personalized subscription/billing/commission drivers; economic SBC retained; FCFF/WACC/reinvestment terminal; full equity bridge; EV and equity multiples under predeclared policy; transaction exclusion explained; no mechanical method average; ranges and triggers. |WACC/ROIC/realization and marginal retention are underwriting hypotheses. Pending M&A/PPA and full award valuation are conditions before trade. Student must own the final judgment. These are practical limitations rather than invented precision. |
| Technical execution and usability45 |Offline Python>=3.10, no model dependencies or credentials; deterministic JSON/Markdown/HTML results; README-only reproduction; fail-loud accounting/date/denominator/domain errors; fresh-copy/new-venv run reproduced four outputs exactly; six viewer selections tested. |Student code/validation Video2 and recorded cold-run ownership are not supplied. GitHub/recipient access must be verified after upload. A working engine alone cannot establish personal ownership. |
| Validation, sensitivity and reproducibility75 |22 meaningful checks: official DCF/bridge and nine grid answers; independent source/definition check; AI-authored before-run WACC prediction with actual decision effect;30 articulations; DCF boundaries/monotonicity; peer definitions; SBC counterexample; compensation propagation; downside action change; share/bridge robustness; reverse-DCF round trip; clean-run hashes. |Human-authored AI-off locked prediction/precommit and AI-closed run are missing; AI tests do not substitute. Authentic partner fresh-eyes challenge and recorded clean run remain open. Full criterion evidence cannot be claimed from test count. |
| Professional communication30 |Three PDFs with identical repository copies and Markdown source; two-page memo; clear executed report/dashboard;12-row manifest; eight rendered PDF pages checked; distinct bounded video guides/scripts; explicit transcript status files. |Three actual student recordings, corrected transcripts, observed durations/indices, stable video URLs, logged-out instructional access and final Brightspace receipt are missing. Scripts/status files are not passed off as completed videos/transcripts. |

No numeric self-award is assigned. The rubric belongs to the instructor, and a score estimate would hide the material ownership gaps. Human actions are collected in `STUDENT-ACTIONS.md`; mechanical completeness is recorded in `outputs/submission-audit.json` and must remain NOT READY until genuine missing evidence is supplied.

## Project task coverage

| Required task | Audited location | Status |
|---|---|---|
| Investment user/action/horizon/date/currency/share basis/exclusions |README; memo; output decision and bridge |Analysis complete |
| Filing traceability and normalized base |data/inputs.json; sources.json; data-lineage.md |Analysis complete |
| Five-year income/BS/CF with personalized drivers |model.forecast; all cases/stresses in results.json; visible-output.md |Executed;30 annual articulation checks |
| Driver value/basis/challenge/change-evidence |evidence/assumption-challenges.md |AI-assisted record complete; human partner entry missing |
| FCFF DCF/WACC/terminal/full equity bridge |model.valuation; memo; output |Executed and checked |
| Causal low/base/high, sensitivity, terminal share, reverse DCF |results.json and visible-output.md |Executed and checked |
| Policy before peer calculations; EV and equity multiples |evidence/peer-policy.md; model.comparables; output |Complete with two qualified peers and leave-one-out |
| Transaction context and method disagreement |transaction-qualification.md; memo; output |Qualified transaction excluded numerically; no averaging |
| Downside and Weeks5-6 credit transfer |what_if output; evidence/project1-credit-check.md |Executed; first failure and decision effect explained |
| Known answer / independent definition / written direction |tests.py; directional-test-precommit.md; output |Complete as AI-assisted validation |
| Human Locked Changed-Input Record |evidence/locked-changed-input-record.md |Missing; not forged |
| High-risk failure and clean run |tests.py; cold-run-log.md and receipt |Assistant execution complete; student recording missing |
| Accepted/corrected/qualified/rejected AI output |Validation PDF and Markdown; research-evolution |Independently anchored dispositions recorded; student review required |
| Unchanged Edition A + Edition B |Research-Evolution.pdf; unchanged NVIDIA text |Edition B complete; Salesforce baseline/receipt unavailable |
| Memo/deck |Decision-Memo.pdf and docs copy |Two pages; numerical/semantic consistency audited |
| Videos1/2/3 + actual corrected transcripts |recording-guide and prep scripts; transcript status files |Human actions missing |
| Manifest, frozen version, access, Brightspace receipt |submission-manifest.csv; integrity inventory; student actions |Local manifest/integrity prepared; external/human checks open |

## Repairs made during the audit

1. Connected the recurring compensation rate to EBIT, cash and terminal margin. An input that only appeared in a report did not satisfy the driver requirement. The8%-to9% test now proves propagation.
2. Added finance-lease principal repayments and separated finance from operating leases. The original draft had a financial claim without a principal run-off schedule.
3. Corrected pending acquisition timing so the cash roll does not presume a future closing had already occurred before the cutoff.
4. Added disaggregated cost/R&D/S&M/G&A/restructuring presentation and exposed S&M as the expense budget implied by the aggregate margin hypothesis. This makes the margin forecast challengeable instead of disguising a percentage as an explained business forecast.
5. Moved named shock values into the visible input file. They are no longer hidden in engine code.
6. Preserved the existing NVIDIA candidate unchanged, identified the company/date mismatch and removed any implication of a verified Salesforce baseline or receipt.
7. Labeled AI directional tests, assistant clean run and preparation scripts distinctly from human AI-off evidence, student recording and actual transcripts.
8. Removed a sparse fifth validation-PDF page and improved number/date spacing. The final documents occupy2 research pages,2 memo pages and4 validation pages; all eight rendered pages have readable layout, repeating table headers, no overlapping text and no out-of-page blocks.
9. Added scoped Git attributes after the staging audit detected that ASCII-encoded PDFs could undergo Windows line-ending conversion. PDFs are now binary; generated text has explicit LF endings, and the preserved NVIDIA candidate bypasses normalization. A fresh Git checkout is checked against all frozen byte hashes, not just the working-folder copies.

## File-level review

All inputs/source fields were checked against the cited filing sections or explicitly labeled assumptions. Model functions and financial data flow were reviewed for units, sign, timing, lease/SBC/commission treatment, fiscal basis and enterprise/equity objects. All required historical aggregates reconcile; current awards/debt and pending M&A uncertainty remain visible. Markdown and JSON outputs were checked against the memo and preparation scripts; no method average or unqualified buy number is present.

All three root PDFs and identical `docs/` copies were rendered. All eight pages were visually inspected in a contact sheet; the memo is within two pages. `outputs/pdf-qa.json` records page bounds, nonempty text, page counts and PDF hashes. The exact generated dashboard script was exercised for all six selections, including the downside action, five-year columns and check rows. This is a script smoke test, not a claim that a student browser demonstration was recorded.

README setup commands were executed in a copied project/new venv with no third-party model packages, and all four deterministic output files matched hashes. Required manifest columns and12 rows are checked. Frozen hashes cover the project source, evidence, PDFs and outputs, excluding self-referential/volatile files and ignored build/cache directories. No unrelated workspace file is staged for upload. Private account data, API secrets, original paid data feeds and false evidence are excluded.

## Publication and final audit

Initial package publication and post-upload access/integrity verification are recorded after the GitHub push. Missing human evidence remains openly flagged throughout. A public repository push is not a Brightspace receipt. The final tag `project-1-2026-10-19` identifies the frozen project snapshot; subsequent genuine human completion requires an explicit new version and updated hashes/manifest rather than silently changing the frozen artifacts.
