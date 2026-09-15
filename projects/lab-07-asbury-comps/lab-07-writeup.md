# Lab 07 — Asbury Comparable-Company Policy and Implied Range

## Represent — peer policy decided before prices

The peer policy is to use publicly traded franchised vehicle retailers that sell new and used
vehicles and have meaningful parts/service operations. This business model matters more than a
broad automotive label. Dealership sales, recurring service and parts work, and finance and
insurance products create operating economics that differ from those of manufacturers, parts
suppliers, rental companies, or online marketplaces.

- **AutoNation — use.** Its vehicle sales, parts/service, and related finance and insurance
  activities fit Asbury's core model. AutoNation Finance is a difference to monitor, but the
  case evidence does not show that it displaces the comparable dealership business.
- **Group 1 Automotive — qualify.** Its dealership and service/parts model fits, but its U.S.
  and U.K. exposure and acquisition of 54 Inchcape dealerships during 2024 can affect its
  earnings mix, growth, integration costs, and risk relative to Asbury.
- **Exclude neither candidate.** Both fit the required core business model and have positive,
  consistently defined annual earnings. These decisions are based on business evidence, not on
  which peer produces a preferred implied price.

## Implement and validate

P/E equals share price divided by annual diluted earnings per share. It states how many dollars
investors pay for one dollar of annual per-share earnings. The frozen case uses December 31,
2024 closing prices and FY2024 total GAAP diluted EPS.

| Check | Calculation | Result |
|---|---:|---:|
| AutoNation P/E | $169.84 / $16.92 | 10.037825x |
| Group 1 P/E | $421.48 / $36.81 | 11.450149x |
| Peer median P/E | (10.037825x + 11.450149x) / 2 | 10.743987x |
| Asbury implied by AutoNation | 10.037825x * $21.50 | $215.81 |
| Asbury implied by peer median | 10.743987x * $21.50 | $231.00 |
| Asbury implied by Group 1 | 11.450149x * $21.50 | $246.18 |

Therefore, the two-peer implied range is **$215.81–$246.18**, with a median-implied price of
**$231.00**. The program retains unrounded multiples internally and rounds only displayed
multiples to six decimals and displayed prices to cents.

Exact command successfully used on this computer (offline; no packages fetched or installed):

```powershell
uv run --offline --no-project python projects/lab-07-asbury-comps/asbury_comps.py
```

## Evolve — remove Group 1

Before reading the result, I predict that removing Group 1 will lower the estimate because
Group 1 has the higher P/E multiple. The remaining AutoNation reference produces **$215.81**,
which is **$15.18 below** the unrounded two-peer median estimate. One peer supplies only one
reference estimate; it cannot establish a range because there are no longer distinct minimum
and maximum peer observations. The removal does not change the original business judgment:
Group 1 remains a qualified peer unless new business evidence supports exclusion.

## Reflect

The peer-implied band does not prove that Asbury is fairly valued. It depends on only two peer
observations, the chosen peer policy, the total-GAAP-EPS convention, and the assumption that
differences in geography, financing, acquisitions, growth, risk, and leverage do not warrant
different multiples. The comparison is a market reference to investigate alongside the DCF,
not an investment recommendation. No cash or debt bridge is applied because P/E already values
shareholders' earnings.

## Audit record

- Frozen price and FY2024 total GAAP diluted EPS inputs match the assigned case.
- The calculator excludes the target, deduplicates peer tickers, and labels invalid inputs.
- It handles zero valid peers, one valid peer, and multiple valid peers explicitly.
- All P/E and implied-price calculations use full precision before display rounding.
- Leave-one-out changes use the unrounded full-peer and remaining-peer estimates.
- The file was executed with the command above; its displayed reference checks match the case.
- Peer decisions and the Group 1 removal are explained using business evidence rather than a
  preferred valuation result.
- No packages, fetched data, adjusted earnings, or cash/debt bridge are used.
