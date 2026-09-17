# Lab 08 — NVIDIA Deal Evidence and Valuation Triangulation

**Target:** NVIDIA Corporation (NASDAQ: NVDA)  
**Comparison date:** September 10, 2026  
**Valuation object:** one common share, in U.S. dollars

**Decision to make:** initiate, watch-defer, or do not initiate NVIDIA after comparing the saved Week 3 DCF with an independently sourced peer-P/E reference. The peer policy below was fixed before AMD and Broadcom were selected and before their prices or multiples were calculated.

## Reopen and working method

I reran the unchanged Lab 07 Asbury calculator successfully with the repository's virtual-environment Python. A peer's P/E becomes a price for NVIDIA by dividing the peer's same-date share price by its annual GAAP diluted EPS, then multiplying that P/E by NVIDIA's annual GAAP diluted EPS. The multiplication transfers the peer's market price per dollar of earnings to NVIDIA; it does not transfer the peer's share price directly.

## Define and discover

NVIDIA earns money from accelerated-computing platforms. Its Compute & Networking segment includes data-center computing, networking, AI software and automotive offerings; Graphics includes gaming and professional-visualization GPUs. NVIDIA outsources fabrication, assembly, testing and packaging, which lets it concentrate resources on design, software, marketing and support. The [FY2026 10-K, Item 1, “Our Businesses,” “Our Markets,” and “Manufacturing”](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) provides this business description.

Businesses most likely to share the economics are listed fabless semiconductor designers selling high-performance processors, accelerators or data-center connectivity. They should also rely on outside manufacturing and invest heavily in product design and software. NVIDIA's latest annual reported earnings public by the comparison date are positive: FY2026 GAAP diluted EPS was **$4.90** for the year ended January 25, 2026 ([10-K, Item 8, Consolidated Statements of Income and Note 4](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)), filed February 25, 2026.

**Focused research question:** On September 10, 2026, what price does NVIDIA's FY2026 GAAP diluted EPS support when valued at the same-date P/E multiples of two profitable, U.S.-listed semiconductor designers with meaningful AI/data-center exposure, after qualifying differences in product mix and software exposure?

I still needed to research each candidate's operating mix, manufacturing model, annual GAAP diluted EPS available by the comparison date, fiscal year-end and same-day closing price.

## Initial peer policy (set before selection)

Admit a listed operating company only if it designs and sells semiconductors or semiconductor-based systems, uses an outsourced/fabless manufacturing model, has meaningful data-center or accelerated-computing exposure, reports in U.S. dollars, and has positive annual GAAP diluted EPS public by September 10, 2026. Qualify a company when its non-data-center products, custom silicon, infrastructure software, acquisition effects, growth or margins materially differ from NVIDIA. Exclude foundries, equipment makers, memory manufacturers, unprofitable companies, and businesses whose economics are dominated by software or unrelated operations.

Evidence that would make me reject a candidate includes owning fabrication plants as its central model, immaterial computing/data-center exposure, nonpositive annual GAAP EPS, incompatible share/currency bases, or a consolidated business mix so different that its P/E cannot reasonably be interpreted as a semiconductor operating-company reference. I did not revise this policy after seeing prices or multiples.

## Candidate decisions and evidence

| Candidate | Decision | Business evidence and section locator | Important difference and judgment |
|---|---|---|---|
| Advanced Micro Devices (AMD) | **Use** | [FY2025 10-K, Item 1, “Our Business—Data Center Segment” and “Manufacturing Arrangements and Assembly and Test Facilities”](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm): AMD designs CPUs, GPUs, accelerators, networking and related software for data-center and other markets; the manufacturing section identifies TSMC and other third-party foundries. | AMD is the closest of the two because it sells competing CPUs/GPUs and data-center accelerators, but Item 7, “Results of Operations—Segment Results,” reports FY2025 revenue of $16.635 billion Data Center, $14.550 billion Client & Gaming and $3.454 billion Embedded. NVIDIA is more concentrated in accelerated computing and has a different growth and margin profile. The difference is material but does not defeat the operating-model match. |
| Broadcom (AVGO) | **Qualify** | [FY2025 10-K, Item 1, “Business—Products and Markets” and “Manufacturing,” plus Item 7, “Overview”](https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm): Broadcom designs semiconductor solutions used in AI data centers, servers and networking; “Manufacturing” says it outsources most wafer fabrication, assembly and testing. | Item 7, “Net Revenue,” shows Broadcom's VMware-led infrastructure-software segment generated 42% of FY2025 revenue and semiconductor solutions generated 58%. Custom AI accelerators and networking also differ from NVIDIA's merchant GPU/platform concentration. I retain Broadcom as a qualified—not clean—reference because its semiconductor majority and AI networking/custom-compute exposure match part of NVIDIA's economics. |

Neither candidate is admitted merely for sharing a semiconductor label. AMD passes the core product and outsourced-production tests. Broadcom passes those tests but requires an explicit consolidated-earnings-mix qualification.

## Inputs and sources

All prices are unadjusted closing prices in USD on the same trading date. Earnings are the latest full-year **reported GAAP diluted EPS** public by that date; adjusted EPS is not used.

| Company | 9/10/2026 close | Annual GAAP diluted EPS | Fiscal year-end | Publication date | Source and locator |
|---|---:|---:|---|---|---|
| NVIDIA (NVDA), target | $218.36 | $4.90 | Jan. 25, 2026 | Feb. 25, 2026 | Price: [historical daily record](https://www.historicalstockprice.com/?symbol=NVDA), 9/10/2026 row. EPS: [NVIDIA FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm), Item 8, Consolidated Statements of Income and Note 4. |
| AMD | $503.60 | $2.65 | Dec. 27, 2025 | Feb. 3, 2026 | Price: [historical daily record](https://www.historicalstockprice.com/?symbol=AMD), 9/10/2026 row. EPS: [AMD FY2025 earnings release](https://www.sec.gov/Archives/edgar/data/2488/000000248826000014/q42025991.htm), “Full Year 2025 Results”; confirmed in [10-K Note 13, Earnings Per Share](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm). |
| Broadcom (AVGO) | $360.83 | $4.77 | Nov. 2, 2025 | Dec. 11, 2025 | Price: [Yahoo Finance historical data](https://uk.finance.yahoo.com/quote/AVGO/history/), 10 Sept. 2026 row. EPS: [Broadcom FY2025 earnings release](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-fourth-quarter-and-fiscal-year-2025), “Fiscal Year 2025 Financial Highlights”; confirmed in [10-K, Item 8, Consolidated Statements of Operations](https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm). |

The target price differs from the Week 3 DCF's $224.35 intraday observation because this lab requires one consistent price convention for all companies. I therefore use September 10 closing prices throughout the peer comparison. The DCF valuation itself remains the saved Week 3 result and date.

**Period and earnings-basis limitation:** the inputs are point-in-time valid but not coterminous. NVIDIA's EPS covers the year ended January 25, 2026, AMD's covers December 27, 2025, and Broadcom's covers November 2, 2025. Each was the latest full-year GAAP diluted EPS available on September 10, 2026, so no later information is used, but the different year-ends expose the multiples to different portions of the AI cycle. Consolidated GAAP EPS is consistently used; quarterly, trailing-twelve-month and adjusted EPS are excluded. AMD's $2.65 includes $2.254 billion of acquisition-related intangible amortization across cost of sales and operating expenses and $1.6 billion of stock-based compensation in All Other (10-K, Item 7, “Results of Operations”). Broadcom's GAAP earnings similarly reflect its VMware acquisition and software mix. Those real GAAP costs preserve consistency, but they also help explain why transferring these P/Es produces a wide and potentially distorted NVIDIA reference.

## Implementation and result

Command run:

```powershell
.\.venv\Scripts\python.exe projects\lab-08-nvda-pe\nvda_pe_comps.py
```

| Calculation | Result |
|---|---:|
| AMD P/E | $503.60 / $2.65 = **190.037736x** |
| Broadcom P/E | $360.83 / $4.77 = **75.645702x** |
| Two-peer median P/E | (190.037736x + 75.645702x) / 2 = **132.841719x** |
| NVIDIA implied by Broadcom | 75.645702x × $4.90 = **$370.66** |
| NVIDIA implied by two-peer median | 132.841719x × $4.90 = **$650.92** |
| NVIDIA implied by AMD | 190.037736x × $4.90 = **$931.18** |

The peer-implied span is **$370.66–$931.18 per NVIDIA share**, with a two-peer median estimate of **$650.92**. I call it a *span/reference*, not a defendable fair-value range: its $560.52 width is 151% of the low endpoint, and the two endpoints arise from materially different consolidated earnings. The width is evidence of comparability risk rather than valuation precision.

## Validation and changed-peer test

The hand check for Broadcom is $360.83 / $4.77 = **75.645702x**, matching the calculator. Before running the removal test, I predicted that removing AMD would sharply lower the estimate because AMD has the higher P/E; removing Broadcom would raise it.

The calculator confirms the prediction:

- Remove AMD: the only remaining reference is Broadcom at **$370.66**, a **$280.26 decrease** from the full-peer median estimate.
- Remove Broadcom: the only remaining reference is AMD at **$931.18**, a **$280.26 increase**.

Each one-peer result is a reference, not a range. I retain both original decisions because the removal test diagnoses sensitivity; it is not a reason to discard an inconvenient multiple.

## DCF comparison and provisional call

| Method | NVIDIA result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | **$55.59–$72.40** per diluted share; valuation dated Sept. 10, 2026 | Five-year FCFF growth of 35%, 25%, 18%, 12% and 8%; 15.88% WACC; 3.0% terminal growth. The high WACC and bounded growth path are especially consequential. |
| Peer P/E | **$370.66–$931.18**; two-peer median **$650.92**, using Sept. 10, 2026 closes | Only two peers; FY2025/FY2026 GAAP diluted EPS; major differences in revenue mix, growth, margins and acquisition-related expenses make the transferred P/Es unstable. |

**Provisional call: watch-defer.** The methods do not overlap, and I will not average them. The DCF is internally tied to my cash-flow forecasts but appears unusually conservative relative to both the market and peer pricing. The peer result supplies market context but is too wide and too sensitive to business mix to serve as a stand-alone fair-value band. The evidence most likely to change my mind is a source-supported revision to sustainable FCFF growth and WACC, or evidence from later annual filings that the peer companies' GAAP earnings and segment mixes have become more comparable to NVIDIA's without switching to adjusted EPS.

## Skeptical AI review and my judgment

**Criticism received:** The weakest supported assumption is that consolidated GAAP P/E is transferable across these firms. Broadcom combines semiconductor earnings with a large infrastructure-software business and acquisition-related amortization, while AMD has a much broader client, gaming and embedded mix. There is also a date/object distinction: the DCF is an intrinsic value estimate using forecast FCFF, while peer P/E applies September 10 market multiples to annual accounting earnings; the DCF's saved market-price observation was intraday, whereas the peer table uses closes.

**Question:** What evidence shows that NVIDIA's exceptional margin and growth profile will converge enough toward AMD and Broadcom for either consolidated P/E to be a stable anchor rather than merely a market-expectations comparison?

**Decision: accept.** The primary filings support the criticism. AMD's 10-K reports material Data Center, Client & Gaming, and Embedded businesses. Broadcom's FY2025 release reports 58% semiconductor and 42% infrastructure-software revenue. NVIDIA's 10-K shows a distinct accelerated-computing platform and FY2026 revenue growth of 65%. The price-timing mismatch is resolved inside the peer analysis by using closes for all three companies, but the DCF-versus-P/E valuation-object and earnings-definition differences remain real. I therefore treat the peer output as a market expectations bracket, not an interchangeable estimate of intrinsic value.

## Reflection and conditional conclusion

AMD is used because its fabless design model, CPUs/GPUs, AI accelerators and data-center customers closely match important NVIDIA economics. Broadcom is qualified because its AI accelerators and networking are relevant, but its 42% infrastructure-software mix materially affects consolidated GAAP earnings. The comparison adds a same-date market check that the DCF alone cannot provide. The methods differ because the DCF discounts my deliberately fading FCFF forecast at 15.88%, while peer P/E embeds investors' growth, margin and risk expectations in two companies whose consolidated earnings are not identical to NVIDIA's.

**Final call: watch-defer; do not initiate at the September 10 close of $218.36.** I can defend the saved DCF range of **$55.59–$72.40** as the output of my stated intrinsic assumptions. I withhold a peer-based fair-value range: **$370.66–$931.18** is only a broad market-expectations reference because the endpoints are dominated by earnings-mix and period differences. The market price lies above the entire DCF range but below both peer references, so the methods give opposite action signals and the less-comparable method cannot override the sourced DCF.

In answer to the skeptical question, I do **not** have evidence that NVIDIA's growth and margins will converge enough to make either peer a stable anchor. That is why I qualify the peer conclusion instead of averaging it with the DCF. Under the assumptions currently supported, **$72.40 or below** is the price condition that would move me from watch-defer to initiate. Above that price, I would reconsider only if later filings support higher sustainable FCFF growth or margins and a recalculated WACC, causing the DCF range to rise, or if annual GAAP segment evidence supports a tighter peer set. A lower peer multiple by itself would not change the call unless the business evidence also supported admitting that peer.

## Evidence-to-decision audit

| Required link | Where it is established | Status |
|---|---|---|
| Explicit company, date, valuation object and pre-selection policy | Opening lines, focused question and “Initial peer policy” | Complete |
| Two sourced candidate decisions | Candidate table with 10-K business, manufacturing and segment locators | Complete |
| Same-date prices and compatible annual earnings | Input table and period/earnings-basis limitation | Complete, with non-coterminous year-ends explicitly qualified |
| Arithmetic and changed-peer result | Implementation table, hand check, prediction and removal output | Complete |
| DCF comparison without mechanical averaging | Comparison table and final call | Complete |
| Source-checked AI criticism and conditional action | Skeptical review, accept decision and $72.40/action-evidence conditions | Complete |

## Checkout

- [Markdown analysis](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-08-nvda-pe/lab-08-writeup.md)
- [Python calculator](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-08-nvda-pe/nvda_pe_comps.py)
