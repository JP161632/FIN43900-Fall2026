# Data lineage and contamination catalog

Economic cutoff: 2026-08-27 at the US close. Research/retrieval: 2026-10-19. This is a deliberately frozen historical valuation, not a claim about October's latest price or filings. Sources must have been public by the cutoff. `data/sources.json` supplies permanent primary URLs, availability dates, period dates and locators. `data/inputs.json` contains every material number; `outputs/results.json` contains full-precision calculations. Model runs never fetch revised provider data. Versioned inputs and SHA256 receipts preserve the data actually used.

## Field map

| Input path | Source and locator | Definition and transformation | Classification |
|---|---|---|---|
| historical.fy26 income and cash rows | CRM_K printed pp.58,61,62; issuer PDF pp.59,62,63 | FY ended2026-01-31; USD M. Costs/taxes/capex stored as positive expenses; CFO/CFI/CFF/FX retain signed cash-flow direction. Annual other income already includes net interest. | Filing facts, transcribed |
| historical.h1fy27 and h1fy26 | CRM_Q pp.4,7,8 | Six months ended July31 2026/2025. Interest is separately disclosed in interim format; do not subtract it again from annual net other income. Acquired amortization is the sum of cost-of-revenue and S&M amortization. | Filing facts |
| historical.bs_jan26 | CRM_K p.57 and CRM_Q p.3 comparative | Asset/liability carrying values, not fair values. Commission assets remain separate from capex. | Filing facts with cross-source reconciliation |
| historical.bs_jul26 | CRM_Q p.3; CRM_RELEASE balance sheet | Actual last public balance sheet. Twelve asset components and seven liability components independently sum to published totals. | Filing facts |
| market.price | CRM_PRICE, Aug27 US Close; CRM_PRICE_CHECK |252.05 USD per NYSE common share. Exclude adjusted-close251.61, TSX CAD-hedged CDRs and foreign quotes. No market-cap provider label is used. | Market fact |
| market.ordinary_shares | CRM_Q cover, Aug20 |823M shares outstanding. Period-end/cover count is distinct from annual weighted average956M, H1 diluted845M, and Q2 diluted821M. | Filing fact |
| market.diluted_shares | CRM_Q cover and p.4 EPS rows |823 + (821 diluted -820 basic) =824M current diluted proxy. Includes existing incremental dilution on that basis; future SBC is cash-substituted. A33M extra-share overlay quantifies unvested-award risk. | Analyst transformation, not a fully diluted appraisal |
| market.debt_market_value | CRM_Q note8 p.24 |Senior notes estimated fair value30800 + floating-rate term loan6000 =36800. Carrying value39288 is not interchanged silently. Fair values are July31 observations, not Aug27 fresh bond quotes. | Filing facts plus addition |
| market.finance_leases | CRM_Q note5 p.21 |633M finance-lease present value. Included once in financial claims. Operating-lease liability2455 stays operating. | Filing fact |
| market.risk_free | UST Aug27 10 Yr column |4.67 percent /100 =0.0467. The adjacent 7 Yr figure4.52 is not the ten-year rate. Nominal USD model uses nominal USD government yield. | Government market fact |
| market.beta, ERP, cost_of_debt | Analyst judgment anchored to UST and CRM_Q note8 coupons |1.15,4.5%,5.5%. Beta is an underwriting assumption, not an estimated regression or provider observation. ERP is not misrepresented as a current published market fact. Debt coupons4.5%-6.7% provide context, not a yield estimate. | Assumptions; challenge record governs |
| peers ADBE annual rows | ADBE_K consolidated income/EPS note |FY ended2025-11-28 revenue23769M and GAAP diluted EPS16.70, public by Jan15. The source is the issuer-hosted annual filing. | Filing facts |
| peers ADBE balance/share rows | ADBE_Q p.3 |May29 ordinary shares399M; cash4919+short-term securities707; debt1843+4802. Not annual weighted shares427 or later June11 count397.5. | Filing facts; explicit same-balance-date policy |
| peers NOW annual rows | NOW_ANNUAL GAAP annual table and split footnote |FY ended2025-12-31 revenue13278M, GAAP diluted EPS1.67. All share data reflect Dec17 2025 five-for-one split. | Issuer facts |
| peers NOW balance/share rows | NOW_Q cover/p.1; NOW_Q_RELEASE |Jun30 ordinary1034M; cash2503+current securities2161+long-term securities2043=6707; financial debt2082+5435=7517. | Filing facts plus addition |
| peers prices | ADBE_PRICE and NOW_PRICE |Aug27 US common-share closes289.15 and138.43 in USD; same trading day as CRM. | Provider observations |
| normalized_base output | model.normalized_base |LTM = FY26 + H1FY27 - H1FY26. No summing overlapping full-year and quarter earnings. | Model output |
| normalization Informatica | CRM_K, CRM_Q MD&A, CRM_RELEASE/Q1 archive |LTM contribution1299M total and1256M subscription. Annualize current H1 contributions to1800 and1736. Add501M total,480M subscription and21M services to normalized base. Incremental EBITA25% is assumed. | Facts plus explicitly analyst run-rate normalization |
| forecasts, shocks, terminal and bridge haircuts | data/inputs.json; assumption-challenges.md |These are analyst hypotheses, never historical or company guidance. | Forecast assumptions/model outputs |

## Week 2 contamination catalog

| Contamination | Treatment and decision implication |
|---|---|
| Investment remeasurement gains |LTM reported gains4245M are non-operating; no gain recurs in FCFF. Investments enter the bridge only, with a25/50/75% all-in realization factor covering liquidity, tax and valuation uncertainty. Those factors are not observed market bids. |
| Acquisitions change the reporting base |Informatica had only a partial year in the LTM. Annualization is shown as a501M adjustment, not organic growth. Qualified is already consolidated; separate revenue is immaterial in the filing and not invented. |
| Restructuring recurs |Replace LTM720M with a recurring0.5% normalized-revenue reserve222.195M. The resulting497.805M addback is smaller than removing all charges. Case margins retain that reserve. |
| Stock compensation is an economic expense |Retain all recurring compensation in operating margins. Forecast future awards as equivalent cash pay; no CFO addback and no extra future dilution for the same pay. The8% policy approximates LTM3665/43938=8.34%. Changes in the rate change earnings and cash. |
| Debt-funded repurchases |Do not divide equity by annual956M shares while using the July debt increase. Use a current824M diluted proxy; no forecast discretionary buybacks. Final ASR settlement was not yet observable at cutoff; require bridge refresh before action. |
| Acquired amortization versus capitalized commissions |Acquired amortization is added back once, amortizes down acquired assets and fades; future growth receives no acquisition-amortization perpetuity. Commission additions are cash operating investment; amortization is added back separately. |
| ROU amortization in provider D&A |Reported D&A includes operating ROU amortization and some impairment. Do not add the full reported aggregate to EBIT while leaving rent operating. Forecast PP&E depreciation20% of opening PP&E and acquired amortization separately; operating rent remains in expenses. |
| Finance versus operating leases |Aggregate historical AP/other liabilities, remove633M finance leases, place that amount in debt. Keep operating leases operating, with flat ROU/liability replacement convention. Finance-lease principal repayment is modeled, not forgotten. |
| Tax-law effects and timing |Use23.5% normalized cash-tax proxy, not a low historical cash-tax rate as a permanent benefit. Deferred-tax assets remain fixed; no unmodeled tax-asset windfall is added to equity. No tax benefit is monetized on a pretax loss. |
| Seasonal billings |Annual years end July31 to compare like seasonal endpoints. Receivables/deferred balances are tied to revenue on the same basis; first-period27-day roll uses a uniform-cash-flow estimate, not claimed daily observations. A no-roll check quantifies this approximation. |
| Pending Contentful/Fin |Core valuation excludes both future cash purchase costs and incremental operating benefits. A separate5100M cash-cost/no-benefit downside case runs through CFI, goodwill, cash and value. Full deal PPA/synergies are not fabricated. Base recommendation remains conditional on integration evidence. |
| Fiscal periods and provider multiples |Peer prices share one trading date; annual denominator fiscal ends differ and are displayed. No forward/non-GAAP EPS is mixed into GAAP P/E. Provider EV/EBITDA labels are not copied. |

## Exclusions, revision and licensing policy

Exclude screening scores from valuation evidence, forecasts released after the cutoff, crypto/CDR/foreign securities, transaction synergies not attributable to a standalone shareholder, unidentified pension claims, personal information and credentials. No paid data or credential is required. Keep primary links and a limited factual numerical transcription; do not redistribute complete paid data feeds, article text or copyrighted financial reports. Temporary downloaded source documents are ignored by Git.

If a transcription error is discovered, retain the old Git version, correct the input, record the reason and run all checks. A new economic cutoff requires new prices, rate, share/debt and announcement review together. Do not quietly refresh one convenient input. `outputs/run-receipt.json` records runtime and input hashes. No historical receipt, independent partner review, recording or human attestation is manufactured.
