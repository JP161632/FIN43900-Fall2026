# Project 1 Salesforce executed valuation

Valuation: 2026-08-27 US close. USD millions; shares millions; prices USD per diluted share. Historical analysis, not a current October quote.

**Committee action: watch/defer. Causal DCF range $74.36 to $298.02.** Base diagnostic $194.86; observed US common-share close $252.05. Do not average methods.

Required human ownership evidence remains incomplete. See `STUDENT-ACTIONS.md` and `docs/rubric-audit.md`. This package does not claim a Salesforce AI-off baseline or a completed human locked prediction.

## Material facts and normalized base

| Metric | Value | Basis |
|---|---|---|
| LTM revenue | 43,938 | FY26 + H1FY27 - H1FY26 |
| Normalized revenue | 44,439 | Informatica current run-rate annualization; analyst normalization |
| Reported LTM EBIT | 8,735 | filing arithmetic |
| Normalized EBIT | 9,358.06 | recurring restructuring reserve retained; SBC retained |
| Cash + debt securities | 11,403 | July31 10-Q; gross, before operating cash |
| Financial debt fair value | 36,800 | senior notes30800 + term loan6000 |
| Finance leases | 633 | separate senior claim; operating leases remain operating |
| Diluted share proxy | 824 | 823 outstanding Aug20 + Q2 incremental1 |
| WACC | 8.98% | market weights; Treasury4.67%, beta1.15 and ERP4.5% analyst assumptions |
| Terminal g / ROIC | 3.00% / 20% | perpetual reinvestment g/ROIC; no free-growth terminal |


## Causal cases

| Case | Price | EV USD M | TV share | WACC / g | Action |
|---|---|---|---|---|---|
| low | $74.36 | 85,029 | 64.63% | 10.50% / 2.00% | do not initiate |
| base | $194.86 | 181,251 | 72.10% | 8.98% / 3.00% | watch/defer |
| high | $298.02 | 263,312 | 75.43% | 8.25% / 3.50% | watch/defer |


Cases change subscription retention/expansion, operating margins, investment realization and discount/terminal assumptions together. They are causal states, not confidence intervals.

## Base enterprise to equity bridge

| Bridge component | USD M |
|---|---|
| Operating enterprise value | 181,251.03 |
| Excess cash after operating-cash reserve | 11,080.62 |
| Strategic investments after all-in realization haircut | 5,662.00 |
| Less debt market value + finance leases | -37,433.00 |
| Common equity | 160,560.66 |
| Shares million | 824 |
| Value USD/share | $194.86 |


Cash is estimated forward 27 days using the pro-forma. Operating cash stays in the business. No operating-lease deduction is taken because lease costs stay in operating earnings. Preferred, minority interest and other separately identified senior claims are zero on the disclosed basis; no pension deduction is inferred without evidence.

## WACC and growth sensitivity

| WACC / terminal g | 2% | 3% | 4% |
|---|---|---|---|
| 7.98% | $211.97 | $237.22 | $274.86 |
| 8.98% | $178.74 | $194.86 | $217.22 |
| 9.98% | $153.79 | $164.54 | $178.72 |


## Market-implied expectations

At $252.05, a parallel margin shift of 7.44 percentage points is needed under the base revenue/WACC/g path: year1 EBITA margin 33.94%, terminal EBITA margin 35.44%. revenue cohorts, WACC, g, tax, ROIC, capex/working-capital policies, share count, cash/debt/investment bridge policy; cash roll reacts to changed profitability. This is a conditional implication, not a unique market forecast.

## Comparable companies

| Peer | Close | Annual GAAP P/E | EV / annual revenue | Annual end | Balance date |
|---|---|---|---|---|---|
| ADBE | $289.15 | 17.3144x | 4.8967x | 2025-11-28 | 2026-05-29 |
| NOW | $138.43 | 82.8922x | 10.8410x | 2025-12-31 | 2026-06-30 |


P/E implied range: $135.05 to $646.56. EV/revenue implied range: $215.18 to $514.74. These are qualified cross-checks; two heterogeneous peers do not establish fair value. Salesforce annual reported P/E is 32.31x.

| Peer removed | Remaining reference | Meaning |
|---|---|---|
| ADBE | $646.56 | one-peer reference, no range |
| NOW | $135.05 | one-peer reference, no range |


P/E combines reported earnings with strategic-investment gains and a historical weighted share basis that predates substantial buybacks. Adobe has more creative/prosumer exposure; ServiceNow has much faster growth and a more depressed GAAP earnings denominator. EV/revenue ignores margins and stock compensation. Their very wide ranges explain why the DCF and explicit underwriting conditions carry the decision; no weighted average is used.

## Named what-if scenarios

| Scenario | Price | Action | Year1 EBIT / interest | Year1 end cash |
|---|---|---|---|---|
| churn_and_collections | $83.12 | do not initiate | 3.26x | 7,136 |
| ai_hosting_cost | $177.46 | watch/defer | 4.45x | 14,860 |
| cash_acquisitions_no_benefit | $189.14 | watch/defer | 5.11x | 10,867 |


Churn/collections: retention90%, expansion6%, new business2%, EBITA margins20/20/21/22/23%, 15 extra receivable days and deferred-revenue balance 5 points of revenue lower. Hosting: EBITA margin lower3 points; other operating drivers unchanged. Acquisition cash: $5100M paid with zero incremental benefits, added to goodwill, no inferred impairment; this is a deliberately adverse execution case, not an acquisition valuation. Flags are analyst diagnostics, not covenant or default findings.

## Five-year statements and checks

These are economically normalized statements with future stock compensation paid in cash at its assumed expense equivalent. Existing dilution is addressed in the bridge proxy and share stress. ROU assets and operating-lease liabilities remain flat under replacement leases; other deferred-tax/assets remain fixed; taxes use a normalized cash-tax proxy. No future discretionary buyback or unidentified M&A is assumed. July fiscal endpoints are analyst rolling years, not Salesforce's January fiscal year.

### Low case

| Income statement USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| Subscription/support | 42,716.94 | 43,144.11 | 43,575.55 | 43,575.55 | 43,575.55 |
| Services/other | 2,059.20 | 1,976.83 | 1,897.76 | 1,821.85 | 1,748.97 |
| Revenue | 44,776.14 | 45,120.94 | 45,473.31 | 45,397.40 | 45,324.52 |
| Subscription cost before acquired amortization | 7,475.46 | 7,550.22 | 7,625.72 | 7,625.72 | 7,625.72 |
| Services cost | 2,368.08 | 2,273.36 | 2,182.42 | 2,095.13 | 2,011.32 |
| Gross profit before acquired amortization | 34,932.60 | 35,297.37 | 35,665.17 | 35,676.55 | 35,687.48 |
| Research and development | 6,716.42 | 6,768.14 | 6,821.00 | 6,809.61 | 6,798.68 |
| Sales and marketing including commission amortization | 14,872.88 | 15,083.18 | 15,065.76 | 14,884.54 | 14,928.85 |
| General and administrative | 2,820.90 | 2,842.62 | 2,864.82 | 2,860.04 | 2,855.45 |
| Recurring restructuring reserve | 223.88 | 225.60 | 227.37 | 226.99 | 226.62 |
| EBITA after recurring compensation | 10,298.51 | 10,377.82 | 10,686.23 | 10,895.38 | 10,877.89 |
| Acquired amortization | 1,588.50 | 1,344.00 | 976.50 | 630.50 | 400.00 |
| EBIT | 8,710.01 | 9,033.82 | 9,709.73 | 10,264.88 | 10,477.89 |
| Interest | 2,189.61 | 2,014.48 | 1,725.27 | 1,602.45 | 1,392.19 |
| Cash-tax proxy | 1,532.30 | 1,649.54 | 1,876.35 | 2,035.67 | 2,135.14 |
| Net income | 4,988.11 | 5,369.79 | 6,108.11 | 6,626.75 | 6,950.56 |
| Diluted EPS USD | 6.05 | 6.52 | 7.41 | 8.04 | 8.44 |


| Balance sheet USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| cash | 12,755.03 | 11,640.76 | 12,806.64 | 18,327.64 | 16,552.21 |
| securities | 3,093.00 | 3,093.00 | 3,093.00 | 3,093.00 | 3,093.00 |
| ar | 6,367.95 | 6,416.98 | 6,467.10 | 6,456.30 | 6,445.94 |
| commissions | 5,495.80 | 5,827.06 | 6,037.29 | 6,152.92 | 6,216.52 |
| prepaid | 2,303.34 | 2,321.08 | 2,339.21 | 2,335.30 | 2,331.55 |
| ppe | 3,105.24 | 3,161.01 | 3,210.91 | 3,249.69 | 3,279.62 |
| rou | 1,787.00 | 1,787.00 | 1,787.00 | 1,787.00 | 1,787.00 |
| investments | 11,324.00 | 11,324.00 | 11,324.00 | 11,324.00 | 11,324.00 |
| goodwill | 59,250.00 | 59,250.00 | 59,250.00 | 59,250.00 | 59,250.00 |
| intangibles | 4,553.50 | 3,209.50 | 2,233.00 | 1,602.50 | 1,202.50 |
| other assets | 3,122.00 | 3,122.00 | 3,122.00 | 3,122.00 | 3,122.00 |
| operating liabilities | 10,155.47 | 10,233.67 | 10,313.59 | 10,296.37 | 10,279.84 |
| operating leases | 2,455.00 | 2,455.00 | 2,455.00 | 2,455.00 | 2,455.00 |
| deferred revenue | 18,929.53 | 19,075.30 | 19,224.26 | 19,192.17 | 19,161.36 |
| debt | 39,701.00 | 33,553.00 | 29,184.00 | 29,087.00 | 21,538.00 |
| equity | 41,915.87 | 45,835.42 | 50,493.29 | 55,669.81 | 61,170.13 |
| total assets | 113,156.87 | 111,152.39 | 111,670.14 | 116,700.35 | 114,604.33 |
| total liabilities | 71,240.99 | 65,316.96 | 61,176.85 | 61,030.54 | 53,434.21 |


| Cash flow USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| begin cash | 8,310.00 | 12,755.03 | 11,640.76 | 12,806.64 | 18,327.64 |
| net income | 4,988.11 | 5,369.79 | 6,108.11 | 6,626.75 | 6,950.56 |
| depreciation | 608.40 | 621.05 | 632.20 | 642.18 | 649.94 |
| acquired amortization | 1,588.50 | 1,344.00 | 976.50 | 630.50 | 400.00 |
| commission amortization | 2,224.80 | 2,473.11 | 2,622.18 | 2,716.78 | 2,768.81 |
| commission additions | 2,776.60 | 2,804.37 | 2,832.41 | 2,832.41 | 2,832.41 |
| change operating nwc | -153.70 | -157.20 | -160.65 | 34.61 | 33.22 |
| sbc addback | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cfo | 6,786.91 | 7,160.78 | 7,667.23 | 7,749.20 | 7,903.68 |
| capex | 671.64 | 676.81 | 682.10 | 680.96 | 679.87 |
| acquisitions | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cfi | -671.64 | -676.81 | -682.10 | -680.96 | -679.87 |
| debt repayment | 220.00 | 6,148.00 | 4,369.00 | 97.00 | 7,549.00 |
| dividends | 1,450.24 | 1,450.24 | 1,450.24 | 1,450.24 | 1,450.24 |
| new borrowing | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cff | -1,670.24 | -7,598.24 | -5,819.24 | -1,547.24 | -8,999.24 |
| cash change | 4,445.03 | -1,114.28 | 1,165.89 | 5,521.00 | -1,775.43 |
| end cash | 12,755.03 | 11,640.76 | 12,806.64 | 18,327.64 | 16,552.21 |
| fcff | 7,790.32 | 8,025.04 | 8,304.96 | 8,294.11 | 8,288.83 |


| Check USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| balance_sheet_error | -0.00000000 | 0.00000000 | -0.00000000 | -0.00000000 | -0.00000000 |
| cash_tie_error | 0.00000000 | 0.00000000 | 0.00000000 | 0.00000000 | -0.00000000 |


### Base case

| Income statement USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| Subscription/support | 46,100.46 | 50,249.50 | 54,269.46 | 58,068.32 | 61,552.42 |
| Services/other | 2,145.00 | 2,145.00 | 2,145.00 | 2,145.00 | 2,145.00 |
| Revenue | 48,245.46 | 52,394.50 | 56,414.46 | 60,213.32 | 63,697.42 |
| Subscription cost before acquired amortization | 8,067.58 | 8,793.66 | 9,497.16 | 10,161.96 | 10,771.67 |
| Services cost | 2,466.75 | 2,466.75 | 2,466.75 | 2,466.75 | 2,466.75 |
| Gross profit before acquired amortization | 37,711.13 | 41,134.09 | 44,450.56 | 47,584.62 | 50,459.00 |
| Research and development | 7,236.82 | 7,859.18 | 8,462.17 | 9,032.00 | 9,554.61 |
| Sales and marketing including commission amortization | 14,408.57 | 15,303.60 | 16,074.08 | 16,996.25 | 18,100.71 |
| General and administrative | 3,039.46 | 3,300.85 | 3,554.11 | 3,793.44 | 4,012.94 |
| Recurring restructuring reserve | 241.23 | 261.97 | 282.07 | 301.07 | 318.49 |
| EBITA after recurring compensation | 12,785.05 | 14,408.49 | 16,078.12 | 17,461.86 | 18,472.25 |
| Acquired amortization | 1,588.50 | 1,344.00 | 976.50 | 630.50 | 400.00 |
| EBIT | 11,196.55 | 13,064.49 | 15,101.62 | 16,831.36 | 18,072.25 |
| Interest | 2,189.61 | 2,014.48 | 1,725.27 | 1,602.45 | 1,392.19 |
| Cash-tax proxy | 2,116.63 | 2,596.75 | 3,143.44 | 3,578.79 | 3,919.82 |
| Net income | 6,890.31 | 8,453.25 | 10,232.91 | 11,650.12 | 12,760.25 |
| Diluted EPS USD | 8.36 | 10.26 | 12.42 | 14.14 | 15.49 |


| Balance sheet USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| cash | 15,966.95 | 19,208.93 | 25,604.88 | 37,265.49 | 42,242.59 |
| securities | 3,093.00 | 3,093.00 | 3,093.00 | 3,093.00 | 3,093.00 |
| ar | 6,861.34 | 7,451.41 | 8,023.12 | 8,563.38 | 9,058.88 |
| commissions | 5,715.73 | 6,409.87 | 7,052.94 | 7,653.56 | 8,210.37 |
| prepaid | 2,481.81 | 2,695.24 | 2,902.03 | 3,097.45 | 3,276.68 |
| ppe | 3,157.28 | 3,311.74 | 3,495.61 | 3,699.69 | 3,915.21 |
| rou | 1,787.00 | 1,787.00 | 1,787.00 | 1,787.00 | 1,787.00 |
| investments | 11,324.00 | 11,324.00 | 11,324.00 | 11,324.00 | 11,324.00 |
| goodwill | 59,250.00 | 59,250.00 | 59,250.00 | 59,250.00 | 59,250.00 |
| intangibles | 4,553.50 | 3,209.50 | 2,233.00 | 1,602.50 | 1,202.50 |
| other assets | 3,122.00 | 3,122.00 | 3,122.00 | 3,122.00 | 3,122.00 |
| operating liabilities | 10,942.33 | 11,883.35 | 12,795.10 | 13,656.70 | 14,446.91 |
| operating leases | 2,455.00 | 2,455.00 | 2,455.00 | 2,455.00 | 2,455.00 |
| deferred revenue | 20,396.22 | 22,150.26 | 23,849.74 | 25,455.74 | 26,928.68 |
| debt | 39,701.00 | 33,553.00 | 29,184.00 | 29,087.00 | 21,538.00 |
| equity | 43,818.07 | 50,821.08 | 59,603.75 | 69,803.63 | 81,113.64 |
| total assets | 117,312.61 | 120,862.69 | 127,887.59 | 140,458.07 | 146,482.23 |
| total liabilities | 73,494.54 | 70,041.61 | 68,283.84 | 70,654.44 | 65,368.59 |


| Cash flow USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| begin cash | 8,310.00 | 15,966.95 | 19,208.93 | 25,604.88 | 37,265.49 |
| net income | 6,890.31 | 8,453.25 | 10,232.91 | 11,650.12 | 12,760.25 |
| depreciation | 608.40 | 631.46 | 662.35 | 699.12 | 739.94 |
| acquired amortization | 1,588.50 | 1,344.00 | 976.50 | 630.50 | 400.00 |
| commission amortization | 2,224.80 | 2,572.08 | 2,884.44 | 3,173.82 | 3,444.10 |
| commission additions | 2,996.53 | 3,266.22 | 3,527.51 | 3,774.44 | 4,000.91 |
| change operating nwc | -1,735.39 | -1,891.57 | -1,832.72 | -1,731.92 | -1,588.42 |
| sbc addback | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cfo | 10,050.87 | 11,626.14 | 13,061.41 | 14,111.05 | 14,931.80 |
| capex | 723.68 | 785.92 | 846.22 | 903.20 | 955.46 |
| acquisitions | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cfi | -723.68 | -785.92 | -846.22 | -903.20 | -955.46 |
| debt repayment | 220.00 | 6,148.00 | 4,369.00 | 97.00 | 7,549.00 |
| dividends | 1,450.24 | 1,450.24 | 1,450.24 | 1,450.24 | 1,450.24 |
| new borrowing | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cff | -1,670.24 | -7,598.24 | -5,819.24 | -1,547.24 | -8,999.24 |
| cash change | 7,656.95 | 3,241.98 | 6,395.95 | 11,660.61 | 4,977.10 |
| end cash | 15,966.95 | 19,208.93 | 25,604.88 | 37,265.49 | 42,242.59 |
| fcff | 11,002.23 | 12,381.31 | 13,535.02 | 14,433.72 | 15,041.37 |


| Check USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| balance_sheet_error | -0.00000000 | 0.00000000 | -0.00000000 | 0.00000000 | 0.00000000 |
| cash_tie_error | -0.00000000 | 0.00000000 | -0.00000000 | 0.00000000 | 0.00000000 |


### High case

| Income statement USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| Subscription/support | 47,792.22 | 54,005.21 | 60,485.83 | 67,139.28 | 73,853.20 |
| Services/other | 2,187.90 | 2,231.66 | 2,276.29 | 2,321.82 | 2,368.25 |
| Revenue | 49,980.12 | 56,236.87 | 62,762.12 | 69,461.09 | 76,221.46 |
| Subscription cost before acquired amortization | 8,363.64 | 9,450.91 | 10,585.02 | 11,749.37 | 12,924.31 |
| Services cost | 2,516.09 | 2,566.41 | 2,617.73 | 2,670.09 | 2,723.49 |
| Gross profit before acquired amortization | 39,100.40 | 44,219.55 | 49,559.37 | 55,041.63 | 60,573.65 |
| Research and development | 7,497.02 | 8,435.53 | 9,414.32 | 10,419.16 | 11,433.22 |
| Sales and marketing including commission amortization | 14,210.30 | 15,370.04 | 16,420.97 | 17,671.56 | 19,566.51 |
| General and administrative | 3,148.75 | 3,542.92 | 3,954.01 | 4,376.05 | 4,801.95 |
| Recurring restructuring reserve | 249.90 | 281.18 | 313.81 | 347.31 | 381.11 |
| EBITA after recurring compensation | 13,994.43 | 16,589.88 | 19,456.26 | 22,227.55 | 24,390.87 |
| Acquired amortization | 1,588.50 | 1,344.00 | 976.50 | 630.50 | 400.00 |
| EBIT | 12,405.93 | 15,245.88 | 18,479.76 | 21,597.05 | 23,990.87 |
| Interest | 2,189.61 | 2,014.48 | 1,725.27 | 1,602.45 | 1,392.19 |
| Cash-tax proxy | 2,400.84 | 3,109.38 | 3,937.31 | 4,698.73 | 5,310.69 |
| Net income | 7,815.49 | 10,122.01 | 12,817.19 | 15,295.87 | 17,287.99 |
| Diluted EPS USD | 9.48 | 12.28 | 15.55 | 18.56 | 20.98 |


| Balance sheet USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| cash | 17,546.98 | 23,171.58 | 32,947.47 | 49,136.48 | 59,607.39 |
| securities | 3,093.00 | 3,093.00 | 3,093.00 | 3,093.00 | 3,093.00 |
| ar | 7,108.04 | 7,997.86 | 8,925.87 | 9,878.58 | 10,840.02 |
| commissions | 5,825.69 | 6,714.47 | 7,624.54 | 8,557.55 | 9,507.11 |
| prepaid | 2,571.04 | 2,892.90 | 3,228.57 | 3,573.17 | 3,920.93 |
| ppe | 3,183.30 | 3,390.19 | 3,653.59 | 3,964.79 | 4,315.15 |
| rou | 1,787.00 | 1,787.00 | 1,787.00 | 1,787.00 | 1,787.00 |
| investments | 11,324.00 | 11,324.00 | 11,324.00 | 11,324.00 | 11,324.00 |
| goodwill | 59,250.00 | 59,250.00 | 59,250.00 | 59,250.00 | 59,250.00 |
| intangibles | 4,553.50 | 3,209.50 | 2,233.00 | 1,602.50 | 1,202.50 |
| other assets | 3,122.00 | 3,122.00 | 3,122.00 | 3,122.00 | 3,122.00 |
| operating liabilities | 11,335.76 | 12,754.82 | 14,234.78 | 15,754.14 | 17,287.43 |
| operating leases | 2,455.00 | 2,455.00 | 2,455.00 | 2,455.00 | 2,455.00 |
| deferred revenue | 21,129.56 | 23,774.66 | 26,533.27 | 29,365.32 | 32,223.33 |
| debt | 39,701.00 | 33,553.00 | 29,184.00 | 29,087.00 | 21,538.00 |
| equity | 44,743.25 | 53,415.03 | 64,781.97 | 78,627.60 | 94,465.35 |
| total assets | 119,364.57 | 125,952.50 | 137,189.02 | 155,289.06 | 167,969.10 |
| total liabilities | 74,621.32 | 72,537.48 | 72,407.05 | 76,661.46 | 73,503.76 |


| Cash flow USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| begin cash | 8,310.00 | 17,546.98 | 23,171.58 | 32,947.47 | 49,136.48 |
| net income | 7,815.49 | 10,122.01 | 12,817.19 | 15,295.87 | 17,287.99 |
| depreciation | 608.40 | 636.66 | 678.04 | 730.72 | 792.96 |
| acquired amortization | 1,588.50 | 1,344.00 | 976.50 | 630.50 | 400.00 |
| commission amortization | 2,224.80 | 2,621.56 | 3,021.51 | 3,431.04 | 3,850.90 |
| commission additions | 3,106.49 | 3,510.34 | 3,931.58 | 4,364.05 | 4,800.46 |
| change operating nwc | -2,526.23 | -2,852.49 | -2,974.90 | -3,054.10 | -3,082.09 |
| sbc addback | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cfo | 11,656.93 | 14,066.39 | 16,536.56 | 18,778.17 | 20,613.47 |
| capex | 749.70 | 843.55 | 941.43 | 1,041.92 | 1,143.32 |
| acquisitions | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cfi | -749.70 | -843.55 | -941.43 | -1,041.92 | -1,143.32 |
| debt repayment | 220.00 | 6,148.00 | 4,369.00 | 97.00 | 7,549.00 |
| dividends | 1,450.24 | 1,450.24 | 1,450.24 | 1,450.24 | 1,450.24 |
| new borrowing | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cff | -1,670.24 | -7,598.24 | -5,819.24 | -1,547.24 | -8,999.24 |
| cash change | 9,236.98 | 5,624.59 | 9,775.89 | 16,189.02 | 10,470.91 |
| end cash | 17,546.98 | 23,171.58 | 32,947.47 | 49,136.48 | 59,607.39 |
| fcff | 12,582.27 | 14,763.91 | 16,914.96 | 18,962.13 | 20,535.18 |


| Check USD M | 2027-07-31 | 2028-07-31 | 2029-07-31 | 2030-07-31 | 2031-07-31 |
|---|---|---|---|---|---|
| balance_sheet_error | 0.00000000 | -0.00000000 | -0.00000000 | -0.00000000 | -0.00000000 |
| cash_tie_error | -0.00000000 | -0.00000000 | 0.00000000 | -0.00000000 | 0.00000000 |


## Validation

22 automated checks passed; 0 failed. Human AI-off lock, peer challenge and recorded cold-run ownership remain separate open requirements.

| Test | Status | Evidence |
|---|---|---|
| Official DCF and all nine sensitivity answers | PASS | {'enterprise_value': 1624.8685199098418, 'per_share': 27.497370398196836, 'grid': [[28.598850582928744, 32.942594335725296, 39.02383558964048], [24.356422648726173, 27.497370398196836, 31.68530073082439], [21.057925415989104, 23.41403273251337, 26.443313568044573]], 'fixture': 'lessons/week-03/teach-dcf-worked-example.md; published official answers'} |
| Official Week2 FCFF and bridge | PASS | {'fcff': 77.5, 'equity': 820, 'price': 8.2, 'fixture': 'lessons/week-02/starter/mini_case.csv'} |
| Source and definition cross-check | PASS | {'cash_plus_securities': 11403, 'debt_fair_value': 36800, 'independent_evidence': 'CRM_RELEASE balance sheet vs CRM_Q p3; CRM_Q note8 notes fair value30800 plus term loan6000; Treasury date/10yr column'} |
| Historical reconciliation and 30 forecast articulations | PASS | {'periods_checked': 30, 'max_balance_error_millions': 2.1827872842550278e-11, 'historical_periods': 'FY26, H1FY26, H1FY27 income/cash statements and Jan26/Jul26 balance sheets'} |
| Directional changed-input test | PASS | {'prediction_file': 'evidence/directional-test-precommit.md', 'authorship': 'AI, not the required human lock', 'old_wacc': 0.08983202277819488, 'new_wacc': 0.09983202277819488, 'old_price': 194.85516595567645, 'new_price': 164.54410363948872, 'expected_direction': 'lower', 'actual_direction': 'lower', 'old_action': 'watch/defer', 'new_action': 'watch/defer', 'decision_effect': 'No initiation: margin-of-safety condition remains unmet; a lower valuation strengthens deferral'} |
| DCF monotonicity | PASS | WACC falls / g rises: value rises in every admissible tested cell, with positive FCFF and fixed bridge |
| g equals WACC | PASS | Rejected: Require WACC > g and WACC > 0 |
| g above WACC | PASS | Rejected: Require WACC > g and WACC > 0 |
| zero WACC | PASS | Rejected: Require WACC > g and WACC > 0 |
| Injected one-million-dollar accounting error | PASS | Rejected: bs_jul26 asset sum: 109621 != 109620 |
| Missing source availability | PASS | Rejected: Missing source field CRM_K: published |
| Future source contamination | PASS | Rejected: Look-ahead source CRM_K |
| Zero shares | PASS | Rejected: Nonpositive diluted shares |
| Duplicate peer | PASS | Rejected: Duplicate peer |
| Negative peer earnings | PASS | Rejected: Nonpositive peer denominator or price |
| Peer policy and multiple definitions | PASS | {'peers': 2, 'leave_one_out': [{'removed': 'ADBE', 'remaining_count': 1, 'pe_implied_price': 646.5592814371258, 'interpretation': 'one-peer reference, no range'}, {'removed': 'NOW', 'remaining_count': 1, 'pe_implied_price': 135.05209580838323, 'interpretation': 'one-peer reference, no range'}], 'definition': 'GAAP annual EPS for all; USD common shares; identical price date; leases operating; no bridge on P/E'} |
| Highest-risk failure: recurring SBC disappears | PASS | {'accepted_price': 194.85516595567645, 'rejected_price': 285.33491990395083, 'overstatement_per_share': 90.47975394827438, 'accepted_action': 'watch/defer', 'rejected_action': 'watch/defer', 'disposition': 'REJECT SBC addback with no compensating dilution/cash cost', 'independent_evidence': 'CRM_Q p4 recurring compensation; p7 CFO adds back noncash expense; shareholders still bear award cost'} |
| Recurring compensation driver propagates | PASS | {'old_rate': 0.08, 'new_rate': 0.09, 'old_price': 194.85516595567645, 'new_price': 187.16948432417672, 'effect': 'Higher recurring compensation propagates into earnings, cash and value; this fixes a disconnected driver found in the audit'} |
| Funding shortfall is actionable | PASS | {'new_funding_year1': 34033.05387054644, 'action': 'do not initiate', 'meaning': 'Hypothetical financing plug is visible, not evidence that credit is available'} |
| Decision-altering downside | PASS | {'base_action': 'watch/defer', 'downside_action': 'do not initiate', 'base_price': 194.85516595567645, 'downside_price': 83.11929631041909, 'first_flags': ['Weak growth and operating margin jointly breach underwriting floors'], 'coverage_first_year': 3.256351716405471, 'liquidity_first_year': 7136.136713707432} |
| Share-overhang and bridge basis robustness | PASS | {'base_shares': 824, 'overhang_stress_shares': 857, 'stressed_per_share': 187.34697831821504, 'no_cash_roll_per_share': 194.1677821762668, 'book_instead_of_market_debt_effect': -3.0194174757281553, 'interpretation': '33M-share stress is a conservative overhang overlay, not a replacement dilution valuation; do not count both routinely'} |
| Reverse DCF round trip | PASS | {'solved_variable': 'parallel additive shift to all five EBITA margins and terminal EBITA margin', 'margin_shift': 0.07441738649427168, 'year1_ebita_margin': 0.33941738649427167, 'terminal_ebita_margin': 0.3544173864942717, 'reproduced_price': 252.04999999999995, 'held_fixed': 'revenue cohorts, WACC, g, tax, ROIC, capex/working-capital policies, share count, cash/debt/investment bridge policy; cash roll reacts to changed profitability'} |


## Source map

See `data/sources.json`, `evidence/data-lineage.md`, `evidence/assumption-challenges.md`, and `docs/validation-and-ai-use.md`. All nonhistorical rates are labeled analyst assumptions. Retrieval occurred2026-10-19; economic evidence availability stops2026-08-27.
