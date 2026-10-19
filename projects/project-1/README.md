# Project 1 Salesforce corporate finance application

**Watch/defer Salesforce at the historical August 27, 2026 close of $252.05.** Causal FCFF scenarios support approximately $75-$300 per diluted share, with base near $195. Intended user: a buy-side PM and committee with no current CRM position; horizon 12-24 months. USD; current diluted-share proxy 824 million; five explicit rolling years end July 31, 2027-2031. This is a frozen historical analysis, not an October live quote or a guaranteed return.

**Submission status: analysis and automated checks complete; human course evidence incomplete.** No Salesforce AI-closed baseline PDF/receipt, human AI-off locked prediction/run, authentic Salesforce partner review, student videos or corrected actual transcripts were supplied. See [student actions](STUDENT-ACTIONS.md). The existing NVIDIA Markdown candidate is preserved unchanged with its limitations disclosed. No file claims a nonexistent receipt, recording or attestation.

## Review without running

- [Decision-Memo.pdf](Decision-Memo.pdf): two-page committee decision, assumptions, range, risks and triggers.
- [Research-Evolution.pdf](Research-Evolution.pdf): Edition B and accurate baseline/company-switch disclosure.
- [Validation-and-AI-Use.pdf](Validation-and-AI-Use.pdf): checks, AI dispositions, missing human lock and limitations.
- [Full executed result](outputs/visible-output.md): material inputs, source cutoff, all three five-year statements, cases, bridge, sensitivity, reverse DCF, comps and test evidence.
- [Offline dashboard](outputs/dashboard.html): download this folder and open the HTML locally; GitHub displays HTML source instead of running it. The selector shows cases and decision-changing stresses.
- [Rubric audit](docs/rubric-audit.md) and [12-row manifest](submission-manifest.csv): evidence locations and unresolved requirements.

## Reproduce

Requirements: Python 3.10 or newer, standard library only. No internet, credentials, API key, pip install, pandas, finance-provider access or `.env` file is needed to run the model. Use a terminal in this project folder:

```text
python --version
python run.py --all
```

On Windows, `py -3` can replace `python` when that launcher is installed. In this course workspace the existing interpreter is also available from the repository root:

```text
.\.venv\Scripts\python.exe .\projects\project-1\run.py --all
```

Expected: watch/defer; causal range $74.36 to $298.02, base $194.86; 22 checks passed and 0 failed. Machine outputs retain precision; committee prose rounds economic estimates. `outputs/results.json`, `validation-results.json`, `visible-output.md` and `dashboard.html` are regenerated. `run-receipt.json` intentionally gets a new runtime timestamp. Outputs are generated relative to the script, regardless of your working directory.

To explore an editable input or preserve a separate changed result:

```text
python run.py --case base --wacc 0.10 --output .build/wacc-example
python run.py --shock churn_and_collections --output .build/downside-example
python run.py --input data/inputs.json --all --output .build/reproduced
```

Rates are decimals; `.10` means 10%, not 0.10%. Bad accounting totals, missing/future sources, nonpositive shares/peer earnings, duplicate peers, invalid terminal boundaries and impossible expense budgets produce explicit errors. Input/result units are USD millions and shares millions except per-share values. Do not overwrite the frozen submission when performing a required human AI-closed exercise; follow the instructor's process and retain exact before/after files.

## Architecture and evidence map

| Location | Purpose |
|---|---|
| `data/inputs.json` | Filing facts, normalizations and editable forecasts; all values visible |
| `data/sources.json` | URLs, publication/as-of dates, definitions and source locators |
| `model.py` | Validation, normalized base, subscription forecast, articulated statements, FCFF/WACC/terminal/bridge, peers and reverse DCF |
| `tests.py` | Published known answers, financial invariants, source checks, changed inputs, counterexamples and rejection tests |
| `run.py` | Offline command-line application and static output viewer generation |
| `evidence/` | Data lineage/contamination catalog, peer policy, transaction qualification, driver challenges, credit transfer, clean-run log and missing human-lock status |
| `docs/` | Content-equivalent PDF/Markdown records, recording preparation and explicit transcript status files |
| `cold_run.py` | Fresh-copy/new-venv execution with deterministic output hash comparison |
| `submission_audit.py` | File/manifest/integrity checks; reports missing ownership evidence rather than certifying a grade |
| `file-integrity.json` | Frozen file SHA256 inventory; excludes itself and volatile run receipt |

Data flow: frozen facts -> LTM reconstruction and explicit normalizations -> company drivers -> income statement/balance sheet/cash flow -> operating FCFF -> discounted EV -> cash/investment/debt/share bridge -> conditional action. Each what-if runs the same linked engine. Scenario selection does not change historical actuals.

The source cutoff is August 27 US close. Primary data: Salesforce FY2026 10-K and July2026 10-Q, Treasury ten-year par yield, Adobe FY2025 and May2026 filings, ServiceNow FY2025/June2026 filings and aligned US historical prices. Retrieval occurred October 19. Source IDs link to full URLs in the source catalog; [data lineage](evidence/data-lineage.md) maps each field. Beta, ERP, forecasts, private-investment realization and risk floors are explicitly analyst assumptions, not provider facts.

## Judgment and limitations

No method average is used. The DCF carries the committee decision; qualified Adobe/ServiceNow P/E and EV/revenue ranges are wide because economics and earnings bases differ. The examined Informatica transaction does not supply a clean comparable EV numerator. Screening is not valuation evidence.

Recurring stock compensation stays an economic expense, with future cash substitution. Operating leases remain operating; finance leases are deducted and amortized. Capitalized commissions and acquired intangible amortization have separate schedules. Deferred revenue funds the operating cycle. Terminal cash flow requires growth reinvestment at 20% incremental ROIC; about 72% of base EV is terminal. The share denominator, rate assumptions, mixed peer fiscal ends, fixed tax/lease balances and dated bond/cash observations remain material limitations. The core scope excludes both pending acquisition costs and benefits; the adverse cash-cost/no-benefit case is separately visible.

Before initiation, require a price <= 80% of the refreshed base value, two quarters with organic subscription growth >=8% and GAAP EBIT margin >=22%, and verified acquisition/ASR/debt/share evidence. Do not initiate if weak growth and margin jointly breach the stated floors, coverage <3x, cash <USD2,000M or new financing is needed. These are analyst rules, not covenants. The named churn/collections case changes the action to do not initiate.

## Checks, PDFs and final submission

The clean-environment run reproduced all four deterministic outputs byte for byte; see [cold-run log](evidence/cold-run-log.md). It is an assistant run, not a student-recorded defense. No points or authorship are certified by automatic test count.

Only PDF rebuilding/rendering needs optional packages:

```text
python -m pip install -r requirements-docs.txt
python build_documents.py
python render_pdf_qa.py
```

`build_documents.py` renders the three `docs/*.md` sources and creates identical root/subfolder PDF copies; it enforces a two-page memo. Update the Markdown first if genuine human evidence becomes available. Full-page PNG previews are placed in ignored `.build/pdf-qa/`; `outputs/pdf-qa.json` records checks. The prepared PDFs were rendered and visually reviewed. Source and document package versions are pinned separately from the dependency-free model.

After genuine evidence and actual corrected transcripts exist, update the manifest, rebuild the PDFs, run `python submission_audit.py --freeze`, then `python submission_audit.py`. The bundle should continue to say NOT READY while required human evidence is missing. Preserve an immutable commit/tag, verify grader/video access, submit the frozen seven-part bundle to Brightspace and retain the receipt. **A GitHub push is not a Brightspace submission.**

All material AI uses/dispositions are disclosed in the single validation record. No private data, credentials or paid-feed copies are required or committed. Earlier NVIDIA labs and unrelated workspace files are left unchanged.
