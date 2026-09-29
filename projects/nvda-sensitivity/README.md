# NVIDIA operating-driver sensitivity

**Question:** Which assumptions drive my company's forecast and value, and what explains their effects?

This analysis extends NVDA Lab 10 without modifying it. Ranges and technical explanations are AI-assisted at the student's request. They are scenarios, not guidance or probabilities. No student-authored pre-run prediction was supplied; this report does not claim to satisfy that separate requirement.

## Inputs

Paths list FY2027, FY2028, FY2029, FY2030 and FY2031 in order.

| Independent input | Lower | Base | Higher |
|---|---|---|---|
| Revenue growth | 25%, 20%, 15%, 10%, 5% | 30%, 25%, 20%, 15%, 10% | 35%, 30%, 25%, 20%, 15% |
| Gross margin | 70%, 70.5%, 71%, 71%, 71% | 72%, 72.5%, 73%, 73%, 73% | 74%, 74.5%, 75%, 75%, 75% |

**Range reasons (AI-selected judgments):** growth shifts +/-5 percentage points in every year to test a sustained faster/slower fade while retaining the declining path. Margin shifts +/-2 percentage points in every year to test gross profitability around the base recovery. FY2025 margin was 75.0% and FY2026 was 71.1%, providing context for the margin range rather than a statistical interval. [NVIDIA FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm).

A percentage-point shift is additive: 30% + 5 percentage points = 35%; a 5% relative increase gives 31.5%. Machine rates are decimal fractions. Each run resets all other independent inputs to base and recalculates all linked statements for five years.

## Results

Outputs are **FY2031E, USD millions**. Changes are changed output minus base. Free cash flow is **FCFE before shareholder payouts**, under the inherited aggregate reinvestment convention.

| Driver / case | Operating profit | Signed change | FCFE | Signed change |
|---|---:|---:|---:|---:|
| Growth / lower | 267,645.75 | -63,725.18 | 208,417.19 | -33,591.00 |
| Growth / base | 331,370.93 | 0.00 | 242,008.19 | 0.00 |
| Growth / higher | 406,682.51 | +75,311.58 | 279,077.11 | +37,068.92 |
| Margin / lower | 321,037.23 | -10,333.70 | 233,055.24 | -8,952.95 |
| Margin / base | 331,370.93 | 0.00 | 242,008.19 | 0.00 |
| Margin / higher | 341,704.64 | +10,333.70 | 250,961.14 | +8,952.95 |

| Driver | Operating-profit span | FCFE span |
|---|---:|---:|
| Revenue growth | 139,036.76 | 70,659.93 |
| Gross margin | 20,667.40 | 17,905.89 |

**Revenue growth has the larger span for both outputs over these ranges.** Growth differences compound across five revenue levels; margin varies on the unchanged base revenue path. Growth also has a wider input range in percentage points. This does not establish that growth is inherently more important under every range selection.

All 40 annual checks across the initial base, six sensitivity cases and restored base pass. Every base statement cell and independent input matches after restoration; maximum difference is zero against a 0.000001 USD million tolerance. Balance-sheet gaps must be below 0.05 USD million and annual cash at least 10,000 USD million. [Visible output](visible-output.md) includes all runs and checks; [results.json](results.json) retains full annual statements.

## Trace of the higher-margin result

Revenue remains at base. Extra gross profit equals 2% of revenue; SG&A consumes 3% of that extra gross profit and R&D is unchanged. FY2031 operating profit increases 10,333.702193. After the 15.1% tax rate, its contribution to FCFE is 8,773.313162. Lower cost of revenue reduces inventory investment but also reduces payable financing; the net contribution is 179.633498. Together these explain the FCFE increase of 8,952.946660. Capex and depreciation remain unchanged. Direct subtraction confirms 250,961.135907 - 242,008.189247 = +8,952.946660.

Growth increases both profit and investment requirements. Higher growth can reduce first-year cash despite higher profit because receivables and the other-assets aggregate absorb cash; final-year compounding ultimately produces the positive effects shown above. Revenue assumptions and the classification of other assets therefore merit further research. This technical observation is not presented as a student's personal surprise or pre-run prediction.

## Cash-flow correction and valuation

Lab 10's line labeled FCFE deducts common dividends and repurchases. This extension preserves it as **legacy cash after payouts** and independently computes FCFE before distributions. The base bridge is 221,034.189247 + 974 + 20,000 = 242,008.189247. Original cash and statement values remain unchanged. FCFE is cash available to equity after reinvestment and net debt repayment, before shareholder distributions. [Damodaran's definitions](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/definitions.html).

**Value per share is unavailable.** Lab 10 discounts cash after payouts and filters negative explicit cash flows. Its other-assets aggregate includes financial investments, requiring reconciliation for defensible valuation. This extension retains signed flows and introduces no terminal value. The archived legacy price is not endorsed as a sensitivity output. These sensitivities cannot support a revised valuation conclusion until those issues are resolved; the valuation method is a research priority.

## Learning reference

1. One-at-a-time sensitivity changes one independent assumption and reruns the linked model with all other independent assumptions held at base.
2. Wider input ranges can create larger output spans. Rankings depend on ranges, affected years, and nonlinearities and apply **over these ranges**.
3. Sensitivity supplies no likelihoods or probability weights, and omits joint changes and correlations. It is not a forecast probability distribution.

## Reproduce and inspect

From the repository root:

```powershell
python projects/nvda-sensitivity/sensitivity.py --ranges projects/nvda-sensitivity/ranges.json
python projects/nvda-sensitivity/verify.py
```

If `python` is not on PATH in this workspace, replace it with `& "$env:USERPROFILE/.local/bin/python3.13.exe"`.

- [sensitivity.py](sensitivity.py): fresh model and deep-copied base for every run.
- [ranges.json](ranges.json): paths, units and judgment reasons.
- [base-inputs.json](base-inputs.json): separate complete base assumptions.
- [visible-output.md](visible-output.md): results readable without running code.
- [results.json](results.json): statements, assumptions and provenance hashes.
- [legacy-base-output.txt](legacy-base-output.txt): original run, with valuation warning.
- [audit.md](audit.md), [verify.py](verify.py): audit and independent arithmetic checks.
- [Preserved Lab 10 source](../lab-10-nvda-proforma/nvda_proforma.py).
