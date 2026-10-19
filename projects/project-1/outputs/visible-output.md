# NVIDIA - executed investment decision

Historical valuation: **2026-09-10 US close**, prepared 2026-10-19. USD millions except shares (millions) and USD/share. Intended user: buy-side committee, no existing position; 12-24 month decision horizon.

**WATCH / DEFER** at $218.36. Causal intrinsic range $56-$212; base reference $119. These are assumptions, not probability-weighted targets. Entry ceiling with 20% margin of safety: $95, subject to evidence gates.

No post-September10 fact is used in the valuation. October19 is the build/review date. Read data/source-map.md and evidence/assumption-challenges.md for definitions and evidence that changes each driver.

## Causal cases

| Case | Year1 / Year5 sales | WACC / g | EV | Equity | USD/share | TV share | Action |
|---|---|---|---|---|---|---|---|
| low | 359,788.20 / 486,685.62 | 15.40% / 2.0% | 1,326,962.72 | 1,355,862.97 | 55.93 | 56.1% | DO NOT INITIATE |
| base | 417,865.00 / 821,108.48 | 13.90% / 3.0% | 2,793,797.33 | 2,874,734.35 | 118.58 | 65.1% | WATCH / DEFER |
| high | 474,683.20 / 1,162,568.07 | 12.40% / 4.0% | 5,028,835.23 | 5,141,192.01 | 212.08 | 72.7% | WATCH / DEFER |

Low: deployment/financing slowdown, weaker margin, longer collections, excess inventory, $10bn supply charge and $25bn guarantee-call assumption. Base: strong DC growth fading with competition. High: sustained platform adoption, execution and collection improvement. Scenario claims are analyst assumptions, not issuer guidance.

## Historical facts and normalization

| Item | FY26 | H1FY26 | H1FY27 | LTM July26 |
|---|---|---|---|---|
| revenue | 215,938.00 | 90,805.00 | 177,837.00 | 302,970.00 |
| ebit | 130,387.00 | 50,078.00 | 117,270.00 | 197,579.00 |
| net_income | 120,067.00 | 45,197.00 | 118,010.00 | 192,880.00 |
| cfo | 102,718.00 | 42,779.00 | 74,421.00 | 134,360.00 |
| capex | 6,042.00 | 3,122.00 | 4,434.00 | 7,354.00 |
| da | 2,843.00 | 1,280.00 | 2,124.00 | 3,687.00 |
| sbc | 6,386.00 | 3,099.00 | 3,954.00 | 7,241.00 |
| investment_gains | 8,918.00 | 2,073.00 | 23,707.00 | 30,552.00 |

LTM = FY26 + H1FY27 - H1FY26. The $4.32bn net H20 charge is an annual normalization only: FY26 reported EBIT130,387 -> normalized134,707 and GM73.07%. It rolls out of the LTM comparator; no second LTM addback. Investment markups/interest are excluded from operating EBIT/FCFF. Latest-quarter platform presentation is recast; annual legacy Gaming labels are not combined with recast Edge categories.

Share proxy = July26 period-end basic24,147 + Q2 incremental dilution95 = 24,242. Annual diluted weighted-average24,514 is used only in historical EPS. Forecast SBC is replaced by equal cash compensation; expense retained, no addback and no forecast dilution benefit. Additional 2% dilution is tested.

## WACC construction

| Component | Value |
|---|---|
| risk_free | 0.049500 |
| beta_assumption | 1.800000 |
| erp_assumption | 0.050000 |
| cost_equity | 0.139500 |
| pretax_cost_debt | 0.059500 |
| market_debt_weight | 0.005897 |
| equity_weight | 0.994103 |
| tax_rate | 0.180000 |
| wacc | 0.138965 |

Risk-free4.95% is Treasury Sep10 nominal10-year. Beta1.8, ERP5%, debt spread1% are explicit assumptions (not current provider estimates). Market equity uses diluted proxy * price, debt uses filing fair value31,400. Operating leases stay operating; rent in cost forecast, no second lease-debt deduction.

## Enterprise to common equity - base

| Bridge component | USD millions |
|---|---|
| Enterprise value | 2,793,797.33 |
| rolled_cash | 40,836.14 |
| debt_securities | 34,143.00 |
| less_operating_cash | -10,000.00 |
| less_cash_tax_reserve | -1,700.00 |
| public_investments_net | 42,966.00 |
| private_other_investments_net | 28,869.27 |
| less_debt_fair_value | -31,400.00 |
| less_purchase_consideration | -861.74 |
| less_future_investment_loss_pv | -9,574.81 |
| less_guarantee_claim_pv | -1,720.01 |
| less_pending_acquisition_cash_pv | -10,620.83 |
| Common equity | 2,874,734.35 |
| Diluted proxy shares | 24,242.00 |
| USD/share | 118.58 |

Financial date July26 precedes valuation by 46 days. Uniform within-year cash-flow interpolation rolls cash and purchases to September10; first FCFF is reduced by elapsed fraction. Dates to remaining payments: 0.873973, 1.873973, 2.873973, 3.873973, 4.873973 years. No interim reported balance sheet is implied. Test residual timing risk before trading.

Public investments:42,783+4,957 locked holdings; base90% recovery. Private/other:51,157+3,300 rounded equity-method+824 derivatives; base50% recovery. These haircuts include tax/illiquidity/realization uncertainty; not precision tax estimates. Future committed equity investments25,000 are financing assets in CFI, not operating NWC/capex; cost/recovery shortfall has a separate negative-PV bridge, once. Debt33,366 carrying versus31,400 fair value. Groq986 consideration is a separate claim. Cash reserve10,000 and foreign-cash tax reserve1,700 are withheld.

## Base five-year income statement

| USD millions | 2027-07-26 | 2028-07-26 | 2029-07-26 | 2030-07-26 | 2031-07-26 |
|---|---|---|---|---|---|
| revenue | 417,865.00 | 538,013.90 | 652,486.37 | 747,862.87 | 821,108.48 |
| cost_of_revenue | 108,644.90 | 139,883.61 | 172,908.89 | 201,922.97 | 229,910.37 |
| gross_profit | 309,220.10 | 398,130.28 | 479,577.48 | 545,939.89 | 591,198.11 |
| rd | 35,936.39 | 46,269.20 | 56,113.83 | 64,316.21 | 70,615.33 |
| sga | 10,276.60 | 11,943.91 | 14,387.32 | 16,378.20 | 17,735.94 |
| risk_charge | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| retention_included_in_sga | 1,000.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| ebit | 263,007.11 | 339,917.18 | 409,076.33 | 465,245.49 | 502,846.83 |
| interest_expense | 1,985.28 | 1,985.28 | 1,985.28 | 1,985.28 | 1,985.28 |
| pretax_income | 261,021.83 | 337,931.90 | 407,091.05 | 463,260.21 | 500,861.56 |
| tax | 46,983.93 | 60,827.74 | 73,276.39 | 83,386.84 | 90,155.08 |
| net_income | 214,037.90 | 277,104.16 | 333,814.66 | 379,873.37 | 410,706.48 |

## Base five-year balance sheet

| USD millions | 2027-07-26 | 2028-07-26 | 2029-07-26 | 2030-07-26 | 2031-07-26 |
|---|---|---|---|---|---|
| cash | 155,668.56 | 376,623.00 | 654,156.64 | 981,572.55 | 1,344,018.18 |
| debt_securities | 34,143.00 | 34,143.00 | 34,143.00 | 34,143.00 | 34,143.00 |
| public_investments | 47,740.00 | 47,740.00 | 47,740.00 | 47,740.00 | 47,740.00 |
| private_investments | 74,781.00 | 77,281.00 | 79,281.00 | 80,281.00 | 80,281.00 |
| ar | 85,862.67 | 110,550.80 | 134,072.54 | 153,670.45 | 168,720.92 |
| inventory | 37,207.16 | 47,905.35 | 59,215.37 | 69,151.70 | 78,736.43 |
| prepaid | 4,596.51 | 5,918.15 | 7,177.35 | 8,226.49 | 9,032.19 |
| ppe | 23,249.70 | 33,577.69 | 44,757.86 | 56,004.28 | 66,636.47 |
| rou | 5,390.00 | 5,390.00 | 5,390.00 | 5,390.00 | 5,390.00 |
| goodwill | 33,025.00 | 33,025.00 | 33,025.00 | 33,025.00 | 33,025.00 |
| intangibles | 2,118.50 | 1,400.00 | 815.00 | 317.00 | 41.50 |
| dta | 12,159.00 | 12,159.00 | 12,159.00 | 12,159.00 | 12,159.00 |
| other_operating_assets | 9,193.03 | 11,836.31 | 14,354.70 | 16,452.98 | 18,064.39 |
| ap | 17,859.44 | 22,994.57 | 28,423.38 | 33,192.82 | 37,793.49 |
| operating_accruals | 50,143.80 | 64,561.67 | 78,298.36 | 89,743.54 | 98,533.02 |
| purchase_consideration | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| debt | 33,366.00 | 33,366.00 | 33,366.00 | 33,366.00 | 33,366.00 |
| lease_long | 4,985.00 | 4,985.00 | 4,985.00 | 4,985.00 | 4,985.00 |
| equity | 418,779.90 | 671,642.06 | 981,214.72 | 1,336,846.10 | 1,723,310.57 |
| total_assets | 525,134.14 | 797,549.29 | 1,126,287.47 | 1,498,133.46 | 1,897,988.08 |
| total_liabilities | 106,354.24 | 125,907.23 | 145,072.74 | 161,287.36 | 174,677.50 |

## Base five-year cash flow and FCFF

| USD millions | 2027-07-26 | 2028-07-26 | 2029-07-26 | 2030-07-26 | 2031-07-26 |
|---|---|---|---|---|---|
| net_income | 214,037.90 | 277,104.16 | 333,814.66 | 379,873.37 | 410,706.48 |
| depreciation_amortization | 4,450.75 | 6,530.92 | 8,979.42 | 11,687.46 | 14,276.57 |
| delta_operating_nwc | 16,099.14 | 19,798.23 | 19,443.85 | 16,467.05 | 13,662.16 |
| cfo | 202,389.51 | 263,836.85 | 323,350.24 | 375,093.79 | 411,320.89 |
| capex | 12,535.95 | 16,140.42 | 19,574.59 | 22,435.89 | 24,633.25 |
| financial_investment_purchases | 19,500.00 | 2,500.00 | 2,000.00 | 1,000.00 | 0.00 |
| acquisition_cash | 11,900.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cfi | -43,935.95 | -18,640.42 | -21,574.59 | -23,435.89 | -24,633.25 |
| dividends | 24,242.00 | 24,242.00 | 24,242.00 | 24,242.00 | 24,242.00 |
| purchase_consideration_paid | 986.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| buybacks | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cff | -25,228.00 | -24,242.00 | -24,242.00 | -24,242.00 | -24,242.00 |
| cash_start | 22,443.00 | 155,668.56 | 376,623.00 | 654,156.64 | 981,572.55 |
| cash_change | 133,225.56 | 220,954.43 | 277,533.65 | 327,415.91 | 362,445.63 |
| cash_end | 155,668.56 | 376,623.00 | 654,156.64 | 981,572.55 | 1,344,018.18 |
| FCFF | 191,481.49 | 249,324.36 | 305,403.57 | 354,285.83 | 388,315.56 |

FCFF = EBIT*(1-tax) + D&A - operating capex - change in operating NWC. CFO + interest*(1-tax) - capex independently agrees. Dividends, buybacks and financial investments are excluded from FCFF. Cash is calculated from CFO+CFI+CFF; equity from retained earnings. No balancing equity plug. Full signed statements for all cases are in results.json.

Pending Hugging Face: September3 8-K discloses ~11,900 purchase consideration and up to1,000 equity retention, closing expected first half2027. Forecast assumes cash purchase11,900 and cash-equivalent retention1,000 in year1, no incremental revenue/synergies. Purchase cash is CFI; separate discounted bridge claim prevents treating acquisition as free. Retention cost is in SGA/FCFF once. Unallocated acquired assets are shown in goodwill as an illustrative purchase-allocation placeholder, not a GAAP purchase-price allocation. Closing/cancellation/allocation require a model revision. Neither pending payment is interpolated into elapsed pre-valuation cash.

## Terminal convention

Year6 normalized FCFF = Year5 NOPAT*(1+g)*(1-g/ROIC) = 373,739.90. Base terminal ROIC25%, g3%; reinvestment12% of NOPAT. D&A equals maintenance capex in steady state; incremental operating investment is g/ROIC. This deliberately replaces year5 growth reinvestment with a mature steady state; TV share 65.1% requires caution.

## WACC-growth sensitivity

| WACC | g | USD/share |
|---|---|---|
| 12.897% | 2.0% | 125.72 |
| 12.897% | 3.0% | 130.87 |
| 12.897% | 4.0% | 137.09 |
| 13.897% | 2.0% | 114.70 |
| 13.897% | 3.0% | 118.58 |
| 13.897% | 4.0% | 123.18 |
| 14.897% | 2.0% | 105.42 |
| 14.897% | 3.0% | 108.38 |
| 14.897% | 4.0% | 111.82 |

## Market-implied expectation

Holding all other base assumptions fixed, $218.36 implies adding 19.82 percentage points to EACH of the five DC growth rates: 59.8%, 49.8%, 41.8%, 34.8%, 29.8%. Implied year5 total revenue 1,691,867.98. One conditional solution, not a unique market forecast.

## Comparable companies

Same-date unadjusted closes; latest-quarter diluted share proxies and financial bridges; latest ANNUAL GAAP earnings/sales for every name. Fiscal years differ and are stale versus AI growth. Not a TTM, forward or clean pure-play valuation.

| Peer | P/E annual GAAP | EV/annual sales | Balance date | Share basis |
|---|---|---|---|---|
| AMD | 190.04x | 23.83x | 2026-06-27 | Q diluted 1,659 |
| AVGO | 75.65x | 28.16x | 2026-08-02 | Q diluted 4,887 |

NVIDIA on the same comparison convention: annual GAAP P/E 44.56x; EV/annual sales 24.41x. P/E target cross-check $371-$931; EV/sales target cross-check $213-$252. Do not average these with DCF. Annual earnings lag explosive growth, AMD has lower margins, and AVGO includes software. Two peers cannot establish a stable fair multiple; leave-one-out exposes the endpoint spread. See policy and transaction exclusions.

Peer EV/annual-sales backsolve uses the SAME narrow cash/debt-securities-minus-BOOK-debt bridge as each comparison numerator. Noncash equity holdings stay inside the broad comparison EV for all names; they are not added again. This proxy comparison is not the separately adjusted operating EV used in DCF. No DCF-specific investment/claim adjustment is silently applied to a peer proxy.

## Named what-if outcomes

| Scenario | USD/share | Action |
|---|---|---|
| demand_financing_downside | 55.93 | DO NOT INITIATE |
| margin_minus_2pp | 114.71 | WATCH / DEFER |
| dc_growth_minus_5pp | 101.22 | WATCH / DEFER |

## Monitoring and reversal

Revisit after each filing. Initiation requires price below the base entry ceiling AND evidence that 75-day collection, 125-day inventory, margin>=72%, and cash compensation economics are sustainable; refresh all market facts before trade. Failure conditions: sustained DC growth below20%, DSO>95 days, GM<70%, or material guarantee calls/capacity losses -> DO NOT INITIATE. Faster durable DC growth with collections and margins intact can justify revising toward high case. Supply commitments279bn are not customer backlog. $105bn SB Energy guarantee cap and $56bn additional cloud/third-party lease commitments are exposures, not certain present debt; scenario expected losses require review.

## Validation and submission status

Engine validation: **PASS**, 15/15 tests. Read validation-results.json for observed outcomes.

Student evidence remains incomplete: original EditionA PDF/first Brightspace receipt, authentic AI-off locked prediction/run, confirmation of partner attribution, three recordings and corrected actual transcripts. Scripts are preparation aids. This package does not claim a full score or a Brightspace submission.
