# Lab 11 - NVIDIA operating-driver sensitivity

## Operating assumptions and tested ranges

Paths list FY2027, FY2028, FY2029, FY2030 and FY2031 in order.

| Independent input | Lower | Base | Higher |
|---|---|---|---|
| Revenue growth | 25%, 20%, 15%, 10%, 5% | 30%, 25%, 20%, 15%, 10% | 35%, 30%, 25%, 20%, 15% |
| Gross margin | 70%, 70.5%, 71%, 71%, 71% | 72%, 72.5%, 73%, 73%, 73% | 74%, 74.5%, 75%, 75%, 75% |

**Range reasons (AI-selected judgments):** growth shifts +/-5 percentage points in every year to test a sustained faster/slower fade while retaining the declining path. Margin shifts +/-2 percentage points in every year to test gross profitability around the base recovery. FY2025 margin was 75.0% and FY2026 was 71.1%, providing context for the margin range rather than a statistical interval. [NVIDIA FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm).

A percentage-point shift is additive: 30% + 5 percentage points = 35%; a 5% relative increase gives 31.5%. Machine rates are decimal fractions. Each run resets all other independent inputs to base and recalculates all linked statements for five years.

## Sensitivity results

Outputs are **FY2031E, USD millions**. Changes are changed output minus base. Free cash flow is **FCFE before shareholder payouts**, under the inherited aggregate reinvestment convention.

| Driver / case | Operating profit | Signed change | FCFE | Signed change |
|---|---:|---:|---:|---:|
| Growth / lower | 267,645.75 | -63,725.18 | 208,417.19 | -33,591.00 |
| Growth / base | 331,370.93 | 0.00 | 242,008.19 | 0.00 |
| Growth / higher | 406,682.51 | +75,311.58 | 279,077.11 | +37,068.92 |
| Margin / lower | 321,037.23 | -10,333.70 | 233,055.24 | -8,952.95 |
| Margin / base | 331,370.93 | 0.00 | 242,008.19 | 0.00 |
| Margin / higher | 341,704.64 | +10,333.70 | 250,961.14 | +8,952.95 |

## Main driver over the tested ranges

| Driver | Operating-profit span | FCFE span |
|---|---:|---:|
| Revenue growth | 139,036.76 | 70,659.93 |
| Gross margin | 20,667.40 | 17,905.89 |

**Revenue growth has the larger span for both outputs over these ranges.** Growth differences compound across five revenue levels; margin varies on the unchanged base revenue path. Growth also has a wider input range in percentage points. This does not establish that growth is inherently more important under every range selection.

## Accounting checks and restored base

All 40 annual checks across the initial base, six sensitivity cases and restored base pass. Every base statement cell and independent input matches after restoration; maximum difference is zero against a 0.000001 USD million tolerance. Balance-sheet gaps must be below 0.05 USD million and annual cash at least 10,000 USD million. The visible run below includes every case and annual check. Run the Python file with `--details` to print full annual statements for every case.

## Trace of the higher-margin result

Revenue remains at base. Extra gross profit equals 2% of revenue; SG&A consumes 3% of that extra gross profit and R&D is unchanged. FY2031 operating profit increases 10,333.702193. After the 15.1% tax rate, its contribution to FCFE is 8,773.313162. Lower cost of revenue reduces inventory investment but also reduces payable financing; the net contribution is 179.633498. Together these explain the FCFE increase of 8,952.946660. Capex and depreciation remain unchanged. Direct subtraction confirms 250,961.135907 - 242,008.189247 = +8,952.946660.

Growth increases both profit and investment requirements. Higher growth can reduce first-year cash despite higher profit because receivables and the other-assets aggregate absorb cash; final-year compounding ultimately produces the positive effects shown above. Revenue assumptions and the classification of other assets therefore merit further research.

## Cash-flow correction and valuation

Lab 10's line labeled FCFE deducts common dividends and repurchases. This extension preserves it as **legacy cash after payouts** and independently computes FCFE before distributions. The base bridge is 221,034.189247 + 974 + 20,000 = 242,008.189247. Original cash and statement values remain unchanged. FCFE is cash available to equity after reinvestment and net debt repayment, before shareholder distributions. [Damodaran's definitions](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/definitions.html).

**Value per share is unavailable.** Lab 10 discounts cash after payouts and filters negative explicit cash flows. Its other-assets aggregate includes financial investments, requiring reconciliation for defensible valuation. This extension retains signed flows and introduces no terminal value. These sensitivities cannot support a revised valuation conclusion until those issues are resolved; the valuation method is a research priority.

## Model implementation and execution

From this folder:

```powershell
python nvda_sensitivity.py
python nvda_sensitivity.py --details
```

The standalone script contains the separate base inputs, chosen ranges, complete linked model, sensitivity runs and accounting checks. It creates no additional files. The existing Lab 10 file remains unchanged. All statement details are retained in the `analyze()` return value; `--details` prints them.

## Changed-result verification

All six sensitivity cases reset the other independent assumptions to base. Each lower or higher case changes only its selected input path; each base case changes none. Signed output differences, spans across valid runs and the higher-margin profit/tax/working-capital bridge were independently recomputed.

## Prediction record

A student-authored prediction saved before the changed runs was not supplied, so a prediction-error reconciliation is unavailable.

## Visible terminal output

```text
LAB 11 - NVIDIA SENSITIVITY
Final-year FY2031E outputs: USD millions. FCFE before shareholder payouts.
Value per share: Unavailable: Lab 10 discounts cash after dividends/buybacks and filters negative cash flows. Other assets also combine operating assets and marketable securities. Valuation needs reconciliation; no terminal value or per-share value is generated here. FCFE below is before shareholder payouts, under the inherited aggregate reinvestment convention.

INPUT PATHS: FY2027, FY2028, FY2029, FY2030, FY2031
REVENUE_GROWTH - decimal fraction of prior-year revenue; endpoints shift base by minus/plus 5 percentage points in each FY2027-FY2031
lower [0.25, 0.2, 0.15, 0.1, 0.05]
base [0.3, 0.25, 0.2, 0.15, 0.1]
higher [0.35, 0.3, 0.25, 0.2, 0.15]
Judgment reason: Judgment: test a sustained faster or slower growth fade while preserving the existing declining path. Five percentage points each year creates a meaningful compounding test without extending recent historical growth rates. Endpoints are scenarios, not confidence bounds.
GROSS_MARGIN - decimal fraction of current-year revenue; endpoints shift base by minus/plus 2 percentage points in each FY2027-FY2031
lower [0.7, 0.705, 0.71, 0.71, 0.71]
base [0.72, 0.725, 0.73, 0.73, 0.73]
higher [0.74, 0.745, 0.75, 0.75, 0.75]
Judgment reason: Judgment: a two-percentage-point deviation tests weaker or stronger gross profitability while leaving the base recovery shape intact. It is a moderate variation relative to the filed FY2025 75.0% and FY2026 71.1% gross margins, not a statistically estimated interval.

Run | Operating profit | Change | FCFE | Change | Status
Base before | 331370.934759 | +0.000000 | 242008.189247 | +0.000000 | PASS
REVENUE_GROWTH / lower | 267645.754998 | -63725.179761 | 208417.187134 | -33591.002113 | PASS
REVENUE_GROWTH / base | 331370.934759 | +0.000000 | 242008.189247 | +0.000000 | PASS
REVENUE_GROWTH / higher | 406682.510841 | +75311.576082 | 279077.113521 | +37068.924274 | PASS
GROSS_MARGIN / lower | 321037.232566 | -10333.702193 | 233055.242587 | -8952.946660 | PASS
GROSS_MARGIN / base | 331370.934759 | +0.000000 | 242008.189247 | +0.000000 | PASS
GROSS_MARGIN / higher | 341704.636952 | +10333.702193 | 250961.135907 | +8952.946660 | PASS
Base restored | 331370.934759 | +0.000000 | 242008.189247 | +0.000000 | PASS

SPANS OVER THESE RANGES (max minus min of valid results)
REVENUE_GROWTH {'operating_profit': 139036.75584300002, 'fcfe': 70659.92638678529, 'valid_runs': 3}
GROSS_MARGIN {'operating_profit': 20667.40438620001, 'fcfe': 17905.893319286522, 'valid_runs': 3}
Restored base: PASS; max difference 0.000000000; tolerance 1e-06.

ANNUAL CHECKS: BS gap must be <0.05; other residuals <=0.000001; cash >=10000.
Base before, FY2027: PASS; cash 86433.667510; max residual 1.364e-12
Base before, FY2028: PASS; cash 195926.874401; max residual 2.910e-11
Base before, FY2029: PASS; cash 343632.050372; max residual 2.910e-11
Base before, FY2030: PASS; cash 528935.367246; max residual 1.164e-10
Base before, FY2031: PASS; cash 749969.556493; max residual 5.821e-11
REVENUE_GROWTH / lower, FY2027: PASS; cash 88341.146029; max residual 5.821e-11
REVENUE_GROWTH / lower, FY2028: PASS; cash 195165.168320; max residual 0.000e+00
REVENUE_GROWTH / lower, FY2029: PASS; cash 332674.463640; max residual 2.728e-12
REVENUE_GROWTH / lower, FY2030: PASS; cash 497426.339590; max residual 1.164e-10
REVENUE_GROWTH / lower, FY2031: PASS; cash 684869.526724; max residual 5.821e-11
REVENUE_GROWTH / base, FY2027: PASS; cash 86433.667510; max residual 1.364e-12
REVENUE_GROWTH / base, FY2028: PASS; cash 195926.874401; max residual 2.910e-11
REVENUE_GROWTH / base, FY2029: PASS; cash 343632.050372; max residual 2.910e-11
REVENUE_GROWTH / base, FY2030: PASS; cash 528935.367246; max residual 1.164e-10
REVENUE_GROWTH / base, FY2031: PASS; cash 749969.556493; max residual 5.821e-11
REVENUE_GROWTH / higher, FY2027: PASS; cash 84526.188991; max residual 5.821e-11
REVENUE_GROWTH / higher, FY2028: PASS; cash 196503.279716; max residual 2.910e-11
REVENUE_GROWTH / higher, FY2029: PASS; cash 354459.054120; max residual 5.821e-11
REVENUE_GROWTH / higher, FY2030: PASS; cash 561431.764888; max residual 2.328e-10
REVENUE_GROWTH / higher, FY2031: PASS; cash 819534.878409; max residual 3.638e-12
GROSS_MARGIN / lower, FY2027: PASS; cash 80768.696950; max residual 5.821e-11
GROSS_MARGIN / lower, FY2028: PASS; cash 184222.044252; max residual 5.821e-11
GROSS_MARGIN / lower, FY2029: PASS; cash 324731.456397; max residual 2.910e-11
GROSS_MARGIN / lower, FY2030: PASS; cash 501824.729469; max residual 1.164e-10
GROSS_MARGIN / lower, FY2031: PASS; cash 713905.972057; max residual 2.328e-10
GROSS_MARGIN / base, FY2027: PASS; cash 86433.667510; max residual 1.364e-12
GROSS_MARGIN / base, FY2028: PASS; cash 195926.874401; max residual 2.910e-11
GROSS_MARGIN / base, FY2029: PASS; cash 343632.050372; max residual 2.910e-11
GROSS_MARGIN / base, FY2030: PASS; cash 528935.367246; max residual 1.164e-10
GROSS_MARGIN / base, FY2031: PASS; cash 749969.556493; max residual 5.821e-11
GROSS_MARGIN / higher, FY2027: PASS; cash 92098.638069; max residual 2.910e-11
GROSS_MARGIN / higher, FY2028: PASS; cash 207631.704550; max residual 1.164e-10
GROSS_MARGIN / higher, FY2029: PASS; cash 362532.644348; max residual 1.164e-10
GROSS_MARGIN / higher, FY2030: PASS; cash 556046.005022; max residual 1.164e-10
GROSS_MARGIN / higher, FY2031: PASS; cash 786033.140929; max residual 2.328e-10
Base restored, FY2027: PASS; cash 86433.667510; max residual 1.364e-12
Base restored, FY2028: PASS; cash 195926.874401; max residual 2.910e-11
Base restored, FY2029: PASS; cash 343632.050372; max residual 2.910e-11
Base restored, FY2030: PASS; cash 528935.367246; max residual 1.164e-10
Base restored, FY2031: PASS; cash 749969.556493; max residual 5.821e-11
```
