# Lab 12 — NVIDIA presentation and partner review

**My company:** NVIDIA (NVDA). **Partner's company:** NVIDIA (NVDA).

**Review date:** October 1, 2026. Financial statement and forecast amounts are USD millions unless stated otherwise. Answers below record the discussion; subsequent clarifications distinguish supported results from unresolved claims.

## D — Conclusion and decision question

How did I get from selecting NVIDIA to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?

**Conditional conclusion: watch-defer under my saved assumptions.** My September 10, 2026 FCFF DCF produced $62.72 per diluted share, with a $55.59–$72.40 sensitivity range, in USD using 24,514 million FY2026 weighted-average diluted shares. These are saved estimates, not October 1 market values. Lab 11 supports operating-profit and FCFE comparisons but withholds a new pro-forma value per share until investment classification, the discount rate, and terminal cash flow are reconciled.

## Existing analysis and outputs

- [Lab 5: DCF, sensitivity grid, and reverse DCF](../lab-05-nvda-dcf/nvda-dcf-lab.md) · [Python](../lab-05-nvda-dcf/dcf.py)
- [Lab 8: Peer comparison and conditional conclusion](../lab-08-nvda-pe/lab-08-writeup.md) · [Python](../lab-08-nvda-pe/nvda_pe_comps.py)
- [Lab 10: Integrated pro-forma](../lab-10-nvda-proforma/nvda-proforma-lab.md) · [Python](../lab-10-nvda-proforma/nvda_proforma.py)
- [Lab 11: Operating sensitivity, cash-flow correction, and valuation limitations](../lab-11-nvda-sensitivity/lab-11-writeup.md) · [Python](../lab-11-nvda-sensitivity/nvda_sensitivity.py)

These are my existing files; the partner's model and source links have not yet been supplied.

## R and I — Full analysis route

### 1. Target selection

My stated selection rationale was NVIDIA's AI accelerator exposure and CUDA ecosystem relative to AMD's broader business. This makes demand growth, profitability, export restrictions, and reinvestment useful company-specific assumptions to test. My initial business thesis emphasized competitive strength; the valuation work makes the investment conclusion conditional on the price and cash flows that strength can support. The market-share percentage in my spoken answer below still needs a dated source and market definition.

### 2. Company and evidence

NVIDIA sells accelerated-computing platforms, networking, graphics products, and related software, using outsourced manufacturing. My historical statements cover FY2024–FY2026; the latest annual base ends January 25, 2026. The primary source is the [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm): Item 1 for the business, Item 1A for risks, Item 7 for operating context, and the financial statements and notes for model inputs. Lab 10 links the earlier filings and historical ratios. Forecasts are judgments anchored in this history, not filing promises.

### 3. Pro-forma

For FY2027–FY2031, revenue growth fades through 30%, 25%, 20%, 15%, and 10%; gross margin follows 72%, 72.5%, 73%, 73%, and 73%. The fade recognizes a larger revenue base and demand/export risk; modest margin recovery remains below the saved FY2025 75% historical margin. Receivable days of 65, inventory days of 125, and payable days of 57.3 connect income-statement activity to working capital. Capex follows revenue, depreciation follows opening PP&E, and cash follows cash flows and financing rather than an arbitrary balancing plug.

Lab 11 corrects Lab 10's cash-after-payouts label to FCFE **before** shareholder distributions. The FY2031 base bridge is $221,034.19 cash after payouts + $974 dividends + $20,000 repurchases = $242,008.19 FCFE. The $20,000 repurchase amount is a forecast assumption. Saved checks pass for balance-sheet equality, cash/PP&E/equity rollforwards, payout reconciliation, and the $10,000 cash floor; restoring the base produces zero difference. These checks establish internal consistency, not forecast accuracy.

### 4. Valuation

Lab 5 grows starting FCFF of $96,895.891 through 35%, 25%, 18%, 12%, and 8%, discounts at 15.88% WACC, and uses 3% perpetual growth. The FCFF growth path is separate from the later pro-forma revenue-growth path. WACC uses a 15.90% cost of equity from 4.80% + 2.22 × 5%, weighted with after-tax debt cost; the saved calculation and sources are linked above.

Enterprise value of $1,483,391.03 + non-operating cash/securities of $62,556 − debt of $8,468 = equity value of $1,537,479.03; dividing by 24,514 million diluted shares gives $62.72. The terminal value contributes 60.21% of enterprise value. The $55.59–$72.40 range tests WACC of 14.88%–16.88% and terminal growth of 2%–4%; it is not a confidence interval.

The saved reverse DCF targets **$224.35 per share, September 10, 2026, 1:37:33 p.m. EDT**. It has no solution within a uniform −5 to +10 percentage-point shift to the five FCFF growth rates: the upper endpoint gives $87.37. Starting FCFF, WACC, terminal growth, cash, debt, shares, and forecast length stay fixed. The failed bracket indicates a limitation of that test, not proof of mispricing.

Lab 8 uses AMD and qualified peer Broadcom. AMD's broader product mix and Broadcom's software/acquisition effects weaken consolidated P/E transferability. Using September 10, 2026 closing prices and annual GAAP diluted EPS, the peer-implied NVIDIA references are **$370.66–$931.18 per share**, versus NVIDIA's **$218.36 close**. These use NVIDIA's $4.90 FY2026 GAAP diluted EPS; peer fiscal year-ends differ. Their market expectations differ from my fading cash-flow forecast. I do not average the peer references with the DCF or call the peer range intrinsic fair value.

The later pro-forma has unresolved investment-asset treatment, cost-of-equity support, and sustainable terminal cash flow. I therefore do not reuse Lab 10's superseded valuation. Any FCFE valuation must retain signed cash flows, discount at a supported cost of equity, count investments once, and avoid subtracting debt again. Its 24,304 million base-date outstanding shares also differ from Lab 5's weighted-average diluted basis.

### 5. Sensitivity and drivers

Lab 11 shifts the full revenue-growth path by ±5 percentage points or the full margin path by ±2 percentage points, resetting other independent assumptions to base. These judgment-based ranges have different widths.

| FY2031E output, USD millions | Lower growth | Base | Higher growth | Lower margin | Higher margin |
|---|---:|---:|---:|---:|---:|
| Operating profit | 267,645.75 | 331,370.93 | 406,682.51 | 321,037.23 | 341,704.64 |
| FCFE before payouts | 208,417.19 | 242,008.19 | 279,077.11 | 233,055.24 | 250,961.14 |

Growth has the larger tested operating-profit span ($139,036.76 versus $20,667.40) and FCFE span ($70,659.93 versus $17,905.89). Growth compounds revenue and changes investment needs; margin changes profitability on unchanged revenue. The ranking depends on the ranges and output year. It measures impact, not probability, uncertainty, or valuation sensitivity. The margin input-to-cash-flow trace appears in my third answer below; it stops at FCFE because valuation remains unresolved.

### 6. Interpretation

The saved DCF's conditional price threshold is $72.40 under its September 10 assumptions; it is not a refreshed trading recommendation. A higher supported cash-flow path or revised discount rate could change the result, but requires recalculation. My next research priorities are sustainable revenue growth and separating operating investment from non-operating assets. Compared with the initial competitive-strength thesis, I now need to establish how much of that strength reaches equity cash flow and how much is already reflected in price.

## As presenter — Questions received and my answers

### 1. Selection and evidence

**Partner's question:** “Why did you choose NVIDIA rather than a broader competitor like AMD, and which specific section of the FY2026 10-K details the revenue risk posed by U.S. export restrictions to China?”

**My answer:**

> We selected NVIDIA over AMD because NVIDIA holds over 80% market share in AI accelerators and benefits from high developer switching costs around its proprietary CUDA software stack. In the FY2026 10-K, 'Item 1A — Risk Factors' and Note 17 explicitly disclose that U.S. export licensing rules caused China to fall from over 20% of Data Center sales to mid-single digits. Although surging North American hyperscaler demand offset that decline, any further tightening of export controls represents an immediate threat to our revenue growth path.

**Post-review source correction:** In the [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), Note 17 is **Leases**, so my spoken citation was incorrect. Item 1A is the relevant risk discussion. My precise China percentages and the “over 80%” market-share claim still need dated evidence and defined denominators; I do not rely on them as verified forecast inputs. Geographic revenue and Data Center end-market exposure must not be conflated.

### 2. Model and valuation

**Partner's question:** “How did your model capture the working capital drain from surging Accounts Receivable and Inventory during high-growth years? Did that create a visible lag between reported operating profit and actual free cash flow?”

**My answer:**

> Yes, our pro-forma balance sheet showed that rapid growth initially consumes substantial cash because receivables and inventory absorb billions of dollars upfront before customer payments are collected. Because of this, FY2027 free cash flow expanded much slower than operating income, only accelerating into cash once annual growth faded toward 10% by FY2031. This mechanical lag proved that high accounting profits do not translate into immediate liquidity when scaling physical chip manufacturing so quickly.

**Clarification from my saved model:** Receivables are linked to revenue through receivable days; inventory and accounts payable are linked to cost of revenue through their respective days assumptions. Increases in receivables and inventory consume cash, while increases in payables provide financing. The [Lab 11 discussion](../lab-11-nvda-sensitivity/lab-11-writeup.md) shows higher-growth FY2027 ending cash of $84,526.19 million versus $86,433.67 million at base, a $1,907.48 million reduction despite higher profit. That supports an initial cash-absorption effect, but it is an ending-cash scenario comparison, not proof of the stated year-over-year FCFE growth comparison. Other assets also absorb cash and contain an unresolved investment classification. The model does not establish that conversion to cash occurs only when growth reaches 10%.

### 3. Sensitivity and interpretation

**Partner's question:** “If major customers developing in-house AI chips (custom ASICs) compress NVIDIA’s gross margin by 2 percentage points, how does that translate into cash flow in your model? Why does a margin shift impact cash flow differently than a revenue growth shift?”

**My answer:**

> In our Lab 11 trace, a 2-percentage-point gross margin change creates an immediate $10.3 billion swing in operating profit and an $8.95 billion swing in annual FCFE. Unlike revenue growth—which requires heavy upfront cash reinvestment in inventory and receivables—gross margin changes flow almost directly to cash with virtually zero working capital drag. Therefore, if custom ASICs force NVIDIA to cut prices and push gross margins toward 70%, that cash loss hits equity holders directly without any offsetting capital savings.

**Clarification from my saved results:** The quoted dollar effects are **FY2031E**, not an immediate loss or a constant annual effect. Lab 11 lowers the full FY2027–FY2031 margin path by 2 percentage points, ending at **71% versus 73% base**; a 70% FY2031 margin is not the same scenario. FY2031 operating profit falls $10,333.70 million and FCFE before shareholder payouts falls $8,952.95 million, with revenue and other independent assumptions held fixed.

The lower-margin trace, in USD millions, is:

```text
Gross profit change                       -10,653.30
Less change in SG&A                           -319.60
Operating profit change                   -10,333.70
After-tax profit effect (15.1% tax)         -8,773.31
Net inventory/payables cash effect           -179.63
FCFE change                                -8,952.95
```

Higher cost of revenue raises inventory investment but also provides an offset through payable financing. Thus the working-capital effect is small relative to profit, but not zero. Capex and depreciation remain unchanged in this margin scenario. The test assumes margin compression; it does not estimate the likelihood of custom ASIC competition or its independent effects on revenue, investment, or valuation. Value per share remains unresolved for the reasons recorded in Lab 11.

## V — Questions asked and partner answers

### 1. Selection and evidence

**Question asked:** “What specific evidence in NVIDIA’s FY2026 Form 10-K supports your base revenue forecast, and which filing disclosure best shows that this data center demand is sustainable rather than a temporary backlog?”

**Partner's reported answer:**

> Our base forecast is anchored in NVIDIA’s FY2026 Form 10-K, where Data Center revenue expanded total sales to $215.9 billion, supported by record multi-year capex commitments from major cloud hyperscalers. We confirmed sustainability by cross-referencing supply-chain commitments and customer purchase obligations, which show demand remaining backordered into the Blackwell architecture. However, because a handful of hyperscalers represent a massive portion of revenue, customer concentration remains our biggest disclosed risk.

**Open evidence gap:** The answer does not identify the exact filing passages supporting multi-year hyperscaler capex commitments or Blackwell backlog. Identify whose obligations are being cited and distinguish NVIDIA's supply commitments from customers' commitments to buy NVIDIA products. The reported answer does not by itself establish sustainable demand. Also record why the partner selected NVIDIA; the question above addresses forecast evidence but not the selection rationale.

### 2. Model and valuation

**Question asked:** “Why did your DCF model and peer P/E multiples produce conflicting valuation conclusions, and how did you handle NVIDIA’s massive cash holdings and share buybacks in your equity bridge?”

**Partner's reported answer:**

> The methods diverged because peer P/E multiples price the entire industry on historical earnings, whereas our DCF model explicitly prices a multi-year growth fade as competition arrives. In our valuation bridge, we added back non-operating cash and marketable securities while ensuring annual share repurchases (around $20 billion) were not mistakenly deducted as operating expenses. This isolated true Free Cash Flow to Equity (FCFE) before shareholder distributions, preventing the model from artificially understating equity value.

**Open model gap:** Obtain the partner's calculation to establish whether the DCF uses FCFF/WACC or FCFE/cost of equity, whether non-operating investments are counted once, and whether the $20 billion repurchase figure is a forecast assumption or a reported historical amount. The answer does not establish that the full valuation bridge is correct. My own Lab 11 still identifies unresolved investment-asset classification, discount-rate, and terminal-cash-flow issues; the partner's answer does not resolve those issues in my model. Record the actual peers and earnings basis rather than treating their multiples as a valuation of the entire industry.

### 3. Sensitivity and interpretation

**Question asked:** “Did Revenue Growth appear as the dominant driver in Lab 11 simply because its tested range was wider than Gross Margin's, and what specific real-world event would cause you to reverse your recommendation?”

**Partner's reported answer:**

> Partially yes: testing a ±5 percentage-point spread that compounds over five years naturally generates a larger dollar swing ($139B operating profit span) than a flat ±2 point gross margin test ($21B span). However, revenue growth is also structurally more powerful because it sets the size of the whole pie and dictates how much cash gets absorbed by inventory and receivables. We would reverse our investment recommendation if hyperscaler AI capex budgets flatten out, or if gross margin drops below 70%, which would immediately erase over $10 billion in annual operating profit.

**Interpretation qualification:** The ranking applies to the tested ranges, not every range or scenario probability. The partner's starting recommendation is Watch/Defer; weaker demand or margins would reinforce caution rather than trigger a buy. Their stated conditions for initiating are recorded below. The claimed immediate loss above $10 billion requires a forecast year, base margin, revenue, and expense assumptions; it cannot be inferred for every year from the rounded spans.

### Evidence checked together and result

We opened NVIDIA's [FY2026 Form 10-K, Consolidated Statements of Income](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) and checked revenue of **$215,938 million** and gross margin of **71.1%** (gross profit divided by revenue, rounded). These match the historical baseline; the forecast margin path is a separate assumption.

We then traced the **+2 percentage-point margin path** in Lab 11 to **FY2031E**, holding other independent inputs fixed. Additional gross profit of $10,653.301230 million, less additional SG&A of $319.599037 million, produces $10,333.702193 million additional operating profit. After 15.1% tax, the profit contribution to FCFE is $8,773.313162 million; the net inventory/payables contribution adds $179.633498 million. The total FCFE increase is **$8,952.946660 million**, or **$8,952.95 million rounded**.

**Result: verified and reconciled.** The statement trace agrees with $250,961.135907 million changed FCFE minus $242,008.189247 million base FCFE. No discrepancy was identified at the saved precision. Rounded endpoints are $250,961.14 million and $242,008.19 million. This check supports the historical baseline and the conditional cash-flow mechanism; it does not verify sustainable demand, a repaired valuation, or an immediate effect in every year.

## E — Explain-back and feedback

**Partner's recommendation:** Conditional **Watch/Defer**. They withheld an immediate buy because they interpreted market pricing as requiring aggressive multi-year growth and little margin of safety if hyperscaler capex cools. Their 30%-to-10% growth fade is a forecast assumption, not a demonstrated market-implied path; that interpretation would require a successful reverse DCF.

**What I explained back:** “You are recommending Watch/Defer because NVIDIA's fundamental moat is intact, but the valuation leaves no room for execution error. You would only initiate if the stock pulls back to reflect a slower growth fade or if hyperscalers formally commit to another multi-year capex expansion cycle.” The main driver in the supplied analysis is revenue growth over the tested ranges; the biggest stated limitation is concentrated demand and uncertainty over sustained customer spending. No correction to my explanation was reported in the discussion notes.

**Feedback I gave:**

- **Strength:** Accounting precision in separating FCFE before distributions from cash remaining after assumed $20 billion annual repurchases. The joint FCFE trace supports the cash-flow explanation; it does not establish that every valuation issue is resolved.
- **Improvement:** Test a scenario in which a major hyperscaler temporarily reduces orders. My suggestion referred to “top 4 hyperscalers” representing “over 40% of demand”; that percentage needs a source and a defined demand measure before it becomes a model input. Specify the customer's exposure, reduction size, duration, and effects on margins and working capital.

**Feedback my partner gave me:**

- **Strength:** My explanation of the working-capital “tug-of-war” connected rapid revenue growth with cash absorbed into receivables and inventory before liquidity improves. The saved higher-growth FY2027 cash comparison supports that mechanism.
- **Improvement:** Rerun sensitivity using standardized relative shocks, such as ±5% on both growth and margin, to address the unequal ranges in the ranking.

## Response and revision

- **Keep:** The linked models and saved sensitivity results, with ranges and units, because they permit an input-to-output trace.
- **Revise:** My wording of the margin result to FY2031, 73% versus 71%, and a nonzero inventory/payables effect; correct Note 17 and distinguish cash after payouts from FCFE. These are documentation corrections, not a newly repaired model.
- **Investigate:** Source the market-share/China assertions, verify the partner's demand evidence, separate investment assets from operating reinvestment, support cost of equity, and reconcile terminal cash flow before reporting a new valuation.
- **Follow-up test:** Accept the suggestion to compare equal relative shocks as a complement to the original economically motivated ranges. For example, ±5% relative to 30% growth means 28.5%–31.5%, while ±5% relative to 73% margin means 69.35%–76.65%; neither is ±5 percentage points. Equal relative shocks improve comparability but do not eliminate dependence on base rates, compounding, economic plausibility, or output horizon. This test has not been run.

These corrections leave the saved conditional Watch/Defer conclusion unchanged: no new supported valuation has been computed. The review changes my research priority toward comparing driver ranges and cash conversion, alongside resolving the valuation conventions. I will not claim that a new sensitivity test or model repair has been completed.

## Reflection

The question that changed my thinking was whether growth looked dominant because I tested a 10-percentage-point total growth range against a 4-percentage-point total margin range. I now understand that “growth is by far the most important driver” overstates what the test establishes: the wider range and five-year compounding contribute to the ranking.

Competition from custom chips could motivate a separate 4–5 percentage-point margin-compression scenario. That is a research hypothesis, not a computed result or evidence that margin would affect equity value as much as a demand slowdown. I would first compare the resulting signed cash flows, and compare equity values only after resolving the valuation method. My improved conclusion is that growth dominates **over the original tested ranges**, while margin risk deserves a separately justified test.
