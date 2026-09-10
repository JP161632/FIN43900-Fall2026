# NVIDIA FCFF DCF Lab

**Company:** NVIDIA Corporation (NASDAQ: NVDA)

**Primary filing:** [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), filed February 25, 2026, for the fiscal year ended January 25, 2026

**Model units:** USD millions except percentages and per-share values

## R — Inputs and sources

| Input | Model value | Unit | As-of date | Status | Exact locator and support |
|---|---:|---|---|---|---|
| Starting FCFF | 96,895.891 | USD millions | FY ended Jan. 25, 2026 | **Estimate from sourced components** | 10-K, Item 8, p. 55, **Consolidated Statements of Cash Flows**: operating cash flow $102,718; purchases related to property/equipment/intangibles $6,042. Item 7, p. 40, income statement: interest expense $259. Item 7, p. 45, **Income Taxes**: 15.1% effective rate. NVIDIA does not separately disclose cash interest, so interest expense is used as a labeled proxy: $102,718 + $259 × (1 − 15.1%) − $6,042 = $96,895.891. |
| Growth, Years 1–5 | 35%, 25%, 18%, 12%, 8% | annual FCFF growth | Forecast made Sept. 10, 2026 | **Forecast / estimate** | 10-K, Item 7, p. 39, **Executive Summary**: FY2026 revenue $215.9B, up 65%; Data Center revenue up 68%, driven by accelerated computing and AI. Item 7, pp. 40–41, **Results of Operations**; p. 4 notes Blackwell Ultra scaled in FY2026 and p. 5 says Rubin production shipments are expected in 2H FY2027. The deliberately fading forecast recognizes maturation, product-transition risk, and the China restriction discussed in Item 1, p. 9. |
| WACC | 15.88% | annual discount rate | Sept. 9, 2026 market inputs; FY2026 debt/tax | **Estimate, independently calculated** | Cost of equity = 4.80% risk-free rate + 2.22 beta × 5.00% course equity-risk premium = 15.90%. Risk-free source: [Federal Reserve H.15, Sept. 9 release](https://www.federalreserve.gov/releases/h15/) (Sept. 8 10-year Treasury constant maturity). Beta and $5.401T equity market value: [Yahoo Finance NVDA](https://finance.yahoo.com/quote/NVDA/) (5-year monthly beta; data through Sept. 9). Debt cost = 2.854%, principal-weighted stated coupon rates from 10-K Note 11, p. 70; after-tax debt cost = 2.423% using the 15.1% effective tax rate. Weights use $5.401T equity market value and $7.5B debt fair value from Note 11, p. 70. Result: 15.881%, rounded to 15.88%. |
| Terminal growth | 3.0% | annual perpetual growth | Sept. 10, 2026 forecast | **Estimate** | [CBO, *The Budget and Economic Outlook: 2026 to 2036*](https://www.cbo.gov/publication/62105), February 2026, Chapter 2, **Figure 2-8**, places 2036 average nominal GDP growth in a 2.7%–5.1% two-thirds probability range. The 3.0% assumption is a deliberately conservative long-run economy rate near the bottom of that range—not NVIDIA’s near-term company growth—and remains below WACC. |
| Cash · debt · diluted shares | 62,556 · 8,468 · 24,514 | USD millions · USD millions · millions of shares | Cash/debt: Jan. 25, 2026; shares: FY ended Jan. 25, 2026 | **Sourced** | **Cash:** 10-K, Item 7, p. 42, **Liquidity and Capital Resources**, cash, cash equivalents, and marketable securities of $62,556, treated as non-operating assets. **Debt:** Note 11, p. 70, **Debt**, net carrying amount $8,468, including $999 short-term and $7,469 long-term; its separately disclosed $7.5B fair value is used only in the WACC weights. **Shares:** Item 8, p. 52, **Consolidated Statements of Income**, “Weighted average shares used in per share computation — Diluted,” 24,514; this is not the cover-page basic count. |

### Market-price target

**$224.35 per share as of September 10, 2026, 1:37:33 p.m. EDT**, from [Yahoo Finance’s NVDA quote](https://sg.finance.yahoo.com/quote/NVDA/). This timestamped observed price is the reverse-DCF target.

## Training-case validation

Before applying NVIDIA’s inputs, the model reproduced the supplied training-case checkpoints:

| WACC \ terminal growth | 2% | 3% | 4% |
|---:|---:|---:|---:|
| 9% | $28.60 | $32.94 | $39.02 |
| 10% | $24.36 | **$27.50** | $31.69 |
| 11% | $21.06 | $23.41 | $26.44 |

The training reverse DCF reproduced a **+1.78 percentage-point uniform shift** to all five explicit growth rates for a $30.00 target, holding starting FCFF, 10% WACC, 3% terminal growth, $50 cash, $300 debt, 50 diluted shares, and the five-year structure fixed.

## I — NVIDIA through the model

Running `python dcf.py` produces the company valuation, sensitivity table, and reverse DCF.

| Output | Result |
|---|---:|
| FCFF Year 1 | $130,809.4529M |
| FCFF Year 2 | $163,511.8161M |
| FCFF Year 3 | $192,943.9430M |
| FCFF Year 4 | $216,097.2161M |
| FCFF Year 5 | $233,384.9934M |
| PV of explicit FCFF | $590,184.5695M |
| Terminal value at Year 5 | $1,866,355.1491M |
| PV of terminal value | $893,206.4625M |
| Enterprise value | $1,483,391.0319M |
| Equity value | $1,537,479.0319M |
| Value per diluted share | **$62.7184** |
| PV of terminal value / enterprise value | 60.21% |

## E — Sensitivity grid and reverse DCF

All non-WACC and non-terminal-growth inputs are held fixed. The base case is centered and bolded.

| WACC \ terminal growth | 2% | 3% | 4% |
|---:|---:|---:|---:|
| 14.88% | $64.60 | $68.17 | **$72.40** |
| 15.88% | $59.77 | **$62.72** | $66.17 |
| 16.88% | **$55.59** | $58.06 | $60.92 |

Direction check passes: value falls moving down as WACC rises and increases moving right as terminal growth rises. The corner-derived valuation range is **$55.59–$72.40 per diluted share**; the center cell is the base case, not the range.

The company reverse DCF solves for a **uniform shift added to all five explicit growth rates**, holding starting FCFF, WACC, terminal growth, cash, debt, diluted shares, and the five-year forecast structure fixed. There is **no solution inside the required −5 to +10 percentage-point bracket** for the $224.35 target; even the +10-point endpoint yields only $87.37 per share. A bound is therefore not reported as an answer. This is an implied-expectations test, not proof that NVIDIA is mispriced.

## V — Reasonableness and conditional call

The base-case value is **$62.72 per share** versus the observed **$224.35 price**, or **0.28× the market price**. It is outside the required 0.5×–2.0× reasonableness band. I did not adjust the model to force a match.

The input I distrust most is the **five-year FCFF growth path**. NVIDIA’s unusually rapid AI-driven expansion and product cadence make a mechanically fading forecast especially uncertain; the reverse DCF’s failed bracket shows that the market embeds expectations beyond this deliberately bounded path (or assumptions elsewhere that differ materially).

**Watch-defer. Initiate if NVDA’s market price falls to $72.40 or below, the top of my supported DCF range; otherwise do not initiate under these assumptions. Monitor quarterly operating margin, because sustained margins above the FY2026 60.4% level would provide measurable evidence that my FCFF growth path may be too conservative.**

## Checkout

- [Markdown analysis](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-05-nvda-dcf/nvda-dcf-lab.md)
- [Python model](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-05-nvda-dcf/dcf.py)

