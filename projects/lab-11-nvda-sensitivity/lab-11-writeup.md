# Lab 11 - NVIDIA operating-driver sensitivity

## Operating assumptions and tested ranges

Paths list FY2027, FY2028, FY2029, FY2030 and FY2031 in order. Revenue growth is the percentage change from prior-year revenue; gross margin is gross profit as a percentage of current-year revenue. Both are independent operating inputs, not calculated statement totals. They are stored as `REVENUE_GROWTH` and `GROSS_MARGIN` in `BASE_INPUTS` in [nvda_sensitivity.py](nvda_sensitivity.py); `DRIVERS` stores the tested paths. The full base assumption set is preserved separately and deep-copied for every run. The original Lab 10 model remains unchanged.

| Independent input | Lower | Base | Higher |
|---|---|---|---|
| Revenue growth | 25%, 20%, 15%, 10%, 5% | 30%, 25%, 20%, 15%, 10% | 35%, 30%, 25%, 20%, 15% |
| Gross margin | 70%, 70.5%, 71%, 71%, 71% | 72%, 72.5%, 73%, 73%, 73% | 74%, 74.5%, 75%, 75%, 75% |

**Range reasons:** the ranges are judgment-based. Growth shifts +/-5 percentage points in every year to test a sustained faster/slower fade while retaining the declining path. Margin shifts +/-2 percentage points in every year to test gross profitability around the base recovery. FY2025 margin was 75.0% and FY2026 was 71.1%, providing context for the margin range rather than a statistical interval. [NVIDIA FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm).

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

Each span is the maximum minus minimum across the three valid lower/base/higher outputs, calculated before rounding. Span units are USD millions. Value-per-share spans are unavailable because valuation remains unresolved.

| Driver | Operating-profit span | FCFE span |
|---|---:|---:|
| Revenue growth | 139,036.76 | 70,659.93 |
| Gross margin | 20,667.40 | 17,905.89 |

**Revenue growth has the larger span for both outputs over these ranges.** Growth differences compound across five revenue levels; margin varies on the unchanged base revenue path. Growth also has a wider input range in percentage points. This does not establish that growth is inherently more important under every range selection.

## Accounting checks and restored base

All 40 annual checks across the initial base, six sensitivity cases and restored base pass. Every base statement cell and independent input matches after restoration; maximum difference is zero against a 0.000001 USD million tolerance. Balance-sheet gaps must be below 0.05 USD million and annual cash at least 10,000 USD million. The sensitivity tables above retain the visible results; the Python model retains all annual statement details and accounting checks.


| Run | Annual checks | Largest absolute balance-sheet gap | Lowest annual cash |
|---|---|---:|---:|
| Base before | 5/5 PASS | 1.164e-10 | 86,433.667510 |
| REVENUE_GROWTH / lower | 5/5 PASS | 1.164e-10 | 88,341.146029 |
| REVENUE_GROWTH / base | 5/5 PASS | 1.164e-10 | 86,433.667510 |
| REVENUE_GROWTH / higher | 5/5 PASS | 2.328e-10 | 84,526.188991 |
| GROSS_MARGIN / lower | 5/5 PASS | 2.328e-10 | 80,768.696950 |
| GROSS_MARGIN / base | 5/5 PASS | 1.164e-10 | 86,433.667510 |
| GROSS_MARGIN / higher | 5/5 PASS | 2.328e-10 | 92,098.638069 |
| Base restored | 5/5 PASS | 1.164e-10 | 86,433.667510 |

Amounts above are USD millions; each annual check also verifies the cash, PP&E and equity rollforwards and the FCFE-to-cash payout bridge. No tested run failed. An invalid run is flagged by the code and must be investigated before comparing complete three-case spans; failed cases must not be ranked. Signed cash flows are retained even when negative. No terminal value is generated.

| FY2031 base comparison | Before sensitivity | After restoration | Difference |
|---|---:|---:|---:|
| Operating profit | 331,370.934759 | 331,370.934759 | 0.000000 |
| FCFE | 242,008.189247 | 242,008.189247 | 0.000000 |

Every original Lab 10 statement value was also compared with the new base and matched exactly, including cash after payouts. The FCFE label correction is reconciled below; it does not change the forecast statements.

## Trace of the higher-margin result

Revenue remains at base. Extra gross profit equals 2% of revenue; SG&A consumes 3% of that extra gross profit and R&D is unchanged. FY2031 operating profit increases 10,333.702193. After the 15.1% tax rate, its contribution to FCFE is 8,773.313162. Lower cost of revenue reduces inventory investment but also reduces payable financing; the net contribution is 179.633498. Together these explain the FCFE increase of 8,952.946660. Capex and depreciation remain unchanged. Direct subtraction confirms 250,961.135907 - 242,008.189247 = +8,952.946660.


Selected FY2031 statement evidence, USD millions:

| Statement line | Base | Higher margin | Signed change |
|---|---:|---:|---:|
| Revenue | 532,665.061500 | 532,665.061500 | +0.000000 |
| Gross profit | 388,845.494895 | 399,498.796125 | +10,653.301230 |
| SG&A | 11,665.364847 | 11,984.963884 | +319.599037 |
| R&D | 45,809.195289 | 45,809.195289 | +0.000000 |
| Operating income | 331,370.934759 | 341,704.636952 | +10,333.702193 |
| Tax | 49,997.902149 | 51,558.291180 | +1,560.389031 |
| Net income | 281,114.032611 | 289,887.345772 | +8,773.313162 |
| Change in inventory | 4,477.570567 | 4,145.898673 | -331.671894 |
| Change in accounts payable | 2,052.518348 | 1,900.479952 | -152.038396 |
| Capital spending | 14,904.103500 | 14,904.103500 | +0.000000 |
| Depreciation | 9,084.590320 | 9,084.590320 | +0.000000 |
| FCFE before shareholder payouts | 242,008.189247 | 250,961.135907 | +8,952.946660 |

Growth increases both profit and investment requirements. Higher growth can reduce first-year cash despite higher profit because receivables and the other-assets aggregate absorb cash; final-year compounding ultimately produces the positive effects shown above. For example, higher-growth FY2027 ending cash is 84,526.188991 versus 86,433.667510 at base, a decrease of 1,907.478519 USD million despite higher profit. Revenue assumptions and the classification of other assets therefore merit further research.

## Cash-flow correction and valuation

Lab 10's line labeled FCFE deducts common dividends and repurchases. This extension preserves it as **legacy cash after payouts** and independently computes FCFE before distributions. The base bridge is 221,034.189247 + 974 + 20,000 = 242,008.189247. Original cash and statement values remain unchanged. FCFE is cash available to equity after reinvestment and net debt repayment, before shareholder distributions.

### Why value per share is not yet reported

A number can be calculated, but the current model does not yet support reporting it as a defensible valuation. The original Lab 10 valuation discounted cash remaining after dividends and buybacks, rather than cash available to shareholders, and excluded negative forecast cash flows. Lab 11 corrects the payout definition and retains signed cash flows, but two valuation inputs and an accounting classification still need reconciliation:

- **Investment assets:** the revenue-linked other-assets balance includes marketable securities and other investments. Treating every increase as operating reinvestment can distort free cash flow. Operating assets and non-operating investments need separate treatment, with investment value counted once.
- **Discount rate:** Lab 5 labels 15.88% as WACC, while Lab 10 labels the same number as cost of equity. FCFF uses WACC; FCFE uses cost of equity. Reusing the number alone does not establish that it is appropriate for both.
- **Terminal cash flow:** Lab 10 assumes 3% perpetual growth, but final-year revenue growth is 10% in the base case, with continuing debt repayments and changing reinvestment. A sustainable terminal-year cash flow must be reconciled with the long-run growth and financing assumptions before applying the perpetuity formula.



### How the earlier valuation work can provide an answer

The DCF method already used in Lab 5 provides the framework. One route is to retain FCFE, separate non-operating investments from operating reinvestment, support the cost of equity, and forecast a sustainable FY2032 cash flow. Then:

```text
Terminal equity value at FY2031 = FCFE_2032 / (cost of equity - terminal growth)
Equity value at the FY2026 base date = present value of all signed FY2027-FY2031 FCFE
                                    + present value of terminal equity value
                                    + non-operating asset value not already included
Value per share = equity value / consistent base-date shares outstanding
```

The existing 3% terminal-growth assumption and 24,304 million base-date shares are starting inputs to review, not missing numbers that need to be invented. Debt must not be subtracted again from an FCFE valuation because interest and net debt repayments are already reflected in those cash flows. Alternatively, the model could use the Lab 5 FCFF/WACC approach, converting cash flows consistently and applying the enterprise-to-equity bridge once.

After those changes, the base and all six sensitivity cases would need to be rerun with the same valuation method. Until then, **value per share remains unavailable**, while the operating-profit and FCFE comparisons remain usable under the disclosed model assumptions. The results prioritize research on revenue growth and the investment-asset classification; they do not establish a revised valuation conclusion.

## Changed-result verification

All six sensitivity cases reset the other independent assumptions to base. Each lower or higher case changes only its selected input path; each base case changes none. Signed output differences, spans across valid runs and the higher-margin profit/tax/working-capital bridge were independently recomputed.
