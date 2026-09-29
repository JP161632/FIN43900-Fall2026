# Technical audit

Scope: requested model, sensitivities, visible outputs and technical explanation. This does not certify completion of every classroom activity. The student-authored locked prediction and reconciliation were not supplied and have not been fabricated.

| Requirement | Result | Evidence |
|---|---|---|
| Own company and working Lab 10 preserved | PASS | NVDA source imported without edits |
| Original base inputs and visible output | PASS | base-inputs.json; legacy-base-output.txt |
| Two existing independent drivers | PASS | Revenue growth and gross margin |
| Low/base/high, units, years and range reasons | PASS | ranges.json and README; AI-selected judgments labeled |
| Six complete linked-model runs | PASS | All annual statements in results.json |
| Only selected input changes; other inputs at base | PASS | verify.py compares every assumption |
| Fresh independent base copy per run | PASS | Fresh module plus deepcopy |
| Common signed operating-profit and FCFE outputs | PASS | FY2031E, USD millions |
| Changes recompute as changed minus base | PASS | Independent verification |
| Spans recompute as max minus min | PASS | Three valid runs per driver |
| Signed cash flows retained | PASS | No positive-only filter in extension |
| Valuation valid or explicitly unavailable | PASS | Unavailable; reasons disclosed |
| Accounting checks visible | PASS | 40 annual checks; balance sheet, cash, PP&E, equity and payout bridges |
| Invalid runs flagged, not ranked | CODE REVIEW | Invalid checks retained; failure exit; no invalid cases in tested ranges |
| Base restored and rerun | PASS | All inputs and statement cells identical; 0.000001 USD million tolerance |
| Actual statement trace | PASS | Higher-margin profit, tax and working-capital bridge |
| Main driver over stated ranges | PASS | Growth larger for both outputs over tested ranges |
| Learning explanations | PROVIDED | Reference explanations in README |
| Locked student prediction reconciled | NOT PROVIDED | No retrospective record represented as pre-run evidence |

## Factual scope

The FY2026 filing confirms the opening separately modeled assets, payables, debt and equity. Other modeled assets equal 206,803 - 10,605 - 38,466 - 21,403 - 10,383 = 125,946. Other liabilities equal 49,510 - 9,812 - 8,468 = 31,230. The asset aggregate includes marketable securities, so it is not purely operating working capital. [NVIDIA FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm).

Forecasts and ranges are judgments. Balanced accounts establish internal consistency, not forecast realism. This audit does not certify every narrative claim or old market-price comparison in Lab 10. The payout correction follows [Damodaran's FCFE definition](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/definitions.html); investment-asset classification remains a disclosed limitation.

## Debug record

Original command: `python projects/lab-10-nvda-proforma/nvda_proforma.py`.

Principal error: `python : The term 'python' is not recognized as the name of a cmdlet, function, script file, or operable program.`

Resolution: use installed Python 3.13 at `$env:USERPROFILE/.local/bin/python3.13.exe`. No packages required.
