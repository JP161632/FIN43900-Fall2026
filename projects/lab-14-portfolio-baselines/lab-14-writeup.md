# Lab 14 — Portfolio Baselines

**Lab date:** October 20, 2026. This submission covers Tuesday's Meridian portfolio-baseline exercise using the instructor's supplied training inputs.

## D — Decision and mandate

**What does each simple portfolio earn and risk — and does any of them meet the Meridian mandate?**

The decision user is Meridian Foundation's CIO. Lab 13 specifies a seven-year horizon, annual rebalancing, a CPI + 4% net-of-costs objective over rolling five-year periods, and a benchmark of 40% investment-grade bonds and 60% global equity. Today's classroom return threshold is **6.5%**, using **2.5% CPI as a labelled estimate**, plus four percentage points. The four training sleeves below are the universe for today's engine.

The Lab 13 reserve rule requires four $0.75 million quarterly distributions against $100 million: **3.0%** in cash or daily-liquid government securities. Today's eligible sleeves are bills and the 10-year Treasury note. Other stated constraints include long-only, no borrowing/shorts/derivatives, no single non-exempt issuer above 8%, at least 90% redeemable in five business days, and annual turnover no more than 25% without approval. The calendar-year loss limit remains undefined. The checker does not certify future losses or turnover, and today's expected return is not proof of net-of-costs rolling-five-year performance.

**Conclusion:** none of the three baselines meets both today's return threshold and the reserve floor. The benchmark earns 6.80% but has no eligible reserve. Equal weight and inverse volatility have ample reserves but expected returns below 6.50%. No baseline is established as fully mandate compliant.

## R — Inputs and boundaries

These are course-authored annual training values, **not market estimates**. Returns and volatilities enter the code as decimals. Weights are decimal fractions, computed without intermediate rounding. No historical estimation window or missing-price treatment applies to these supplied inputs. No fee input was supplied.

| Sleeve | Expected return | Volatility | Reserve eligible? |
|---|---:|---:|---|
| Treasury bills | 3.5% | 0.5% | Yes |
| Treasury 10-year note | 4.3% | 7.0% | Yes |
| Investment-grade bond fund | 5.0% | 6.0% | No |
| Global equity index fund | 8.0% | 16.0% | No |

| Correlation | Bills | 10-year | IG bonds | Equity |
|---|---:|---:|---:|---:|
| Bills | 1.00 | 0.10 | 0.05 | 0.00 |
| 10-year | 0.10 | 1.00 | 0.80 | -0.10 |
| IG bonds | 0.05 | 0.80 | 1.00 | 0.25 |
| Equity | 0.00 | -0.10 | 0.25 | 1.00 |

## I — Reusable risk engine

[portfolio.py](portfolio.py) uses only Python's standard library. Editable sleeve inputs, correlation matrix, benchmark weights, and objective appear at the top. Functions build covariance, validate inputs and weights, generate equal and inverse-volatility weights, and compute return, variance, volatility, reserve share, and the objective comparison. Importing the file does not run the report.

Run from the repository root with the installed course environment:

```powershell
.\.venv\Scripts\python.exe projects\lab-14-portfolio-baselines\portfolio.py
.\.venv\Scripts\python.exe projects\lab-13-portfolio-mandate\mandate.py
.\.venv\Scripts\python.exe projects\lab-14-portfolio-baselines\verify_portfolio.py
```

Or, with Python on PATH, change into this lab folder and run `python portfolio.py`.

The covariance formula is `covariance[i][j] = correlation[i][j] * volatility[i] * volatility[j]`. Its diagonal contains individual variances. Expected portfolio return is `sum(weight[i] * expected_return[i])`. Portfolio variance is `sum(weight[i] * weight[j] * covariance[i][j])` across **all** i,j pairs, followed by a square root to obtain volatility. Both off-diagonal entries are included, providing the factor of two in a two-asset formula.

The engine rejects correlations outside [-1, 1], asymmetric or incorrectly sized tables, non-unit self-correlations, nonfinite inputs, and nonpositive sleeve volatilities. It also checks that the correlation matrix is positive semidefinite, so individually plausible pairwise numbers cannot imply an impossible joint risk model. Weight labels must match the sleeve order used to construct covariance; weights must be nonnegative and sum to one.

### Partner discussion and swap-and-break

**Partner's question, paraphrased:** Should I spread my money across multiple assets rather than put it all into a single asset?

**My answer:** Diversification can reduce the risk of relying on one asset. Holding multiple assets whose returns do not move perfectly together reduces exposure to a single asset's volatility and large losses. It does not eliminate losses or guarantee lower risk than every individual holding.

**Reported partner-file check:** My partner's file ran and matched the known answers. Setting the correlation to **1.3** was rejected. The reproducible audit below separately checks my submitted engine.

## V — Known-answer reconciliation

All displayed values match the supplied known answer. Weight order is **bills / 10-year / IG / equity**.

| Portfolio | Weights (%) | Return (%) | Volatility (%) | Reserve eligible (%) | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80 | 10.46 | 0.0 | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20 | 5.21 | 50.0 | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77 | 1.05 | 90.3 | No |

The displayed inverse-volatility weights sum to 99.9% because each is rounded to one decimal. Their full-precision sum is 100%; those unrounded weights drive every calculation.

### Required changes and refusal tests

| Executed probe | Observed result |
|---|---|
| Original training inputs | Every known-answer value matches |
| IG–equity correlation changed to 0.50 in both cells | Benchmark volatility 11.00% |
| Restore IG–equity correlation to 0.25 | Benchmark volatility 10.46%; both source cells remain 0.25 |
| Set both IG–equity correlations to 1.3 in a temporary file and run its CLI | Exit code 1; clear message requiring correlation between -1 and 1; no portfolio results |
| Change only one IG–equity correlation to 0.50 in a temporary file | Exit code 1; clear message requiring symmetry |
| Covariance order, symmetry, diagonals, and long-only fully invested weights | Pass |
| Benchmark E through Lab 13 checker | Reserve 0.0% FAIL; all other coded checks pass |

[verify_portfolio.py](verify_portfolio.py) contains the reproducible audit, including a two-asset formula independent of the matrix calculation. Temporary failure-injection files leave the delivered inputs intact. [verification-results.txt](verification-results.txt) records the actual runs.

### Benchmark through the mandate checker

The original Lab 13 checker was rerun before editing: A passes all coded rules, B fails three, C fails one, and D passes all coded rules. Candidate **E** was then added to [Lab 13 mandate.py](../lab-13-portfolio-mandate/mandate.py), with 40% IG bonds, 60% equity, and zero in the other holdings.

| Candidate E rule | Actual result |
|---|---|
| Weights sum to 100% | 100.0 pass |
| Long-only, lowest weight | 0.0 pass |
| Reserve at least 3.0% | **0.0 FAIL** |
| Redeemable within five days at least 90% | 100.0 pass |
| Largest non-exempt single company at most 8% | 0.0 pass |
| Calendar-year loss | Requires CIO clarification |
| Verdict | **Fails one coded rule** |

The client's own performance benchmark breaks the client's reserve mandate. A benchmark is a comparison reference, not automatic permission to hold its exact allocation.

## Diversification — Learn on your own

**What is it?** Diversification combines exposures whose returns do not move perfectly together, reducing reliance on a single risk source.

**How does it work?** Risk depends on how assets move together. With two positive weights, lowering correlation below +1 lowers the covariance contribution and portfolio variance relative to that same mix at +1. It does not guarantee volatility below each asset separately, remove all loss risk, or guarantee returns. Here the benchmark's 10.46% volatility is below equity's 16.00%, but above the bond fund's 6.00%.

**Work the benchmark by hand.** In percentage units:

```text
Expected return = 0.40 × 5 + 0.60 × 8 = 6.80%
Variance = 0.40² × 6² + 0.60² × 16²
         + 2 × 0.40 × 0.60 × 0.25 × 6 × 16
         = 5.76 + 92.16 + 11.52 = 109.44 (% squared)
Volatility = sqrt(109.44) = 10.461357...% = 10.46%
```

At correlation +1, the same weights yield 0.40 × 6% + 0.60 × 16% = 12.00% volatility. At 0.50, variance is 5.76 + 92.16 + 23.04 = 120.96, whose square root is 10.99818...%, displayed as 11.00%. Omitting covariance gives sqrt(97.92) = 9.90%, which is the lab's diagnostic error.

This worked explanation was prepared with AI and independently checked against the matrix calculation by the audit.

## Reflection

**Why inverse volatility piles into bills:** inverse volatilities in decimal units are approximately 200, 14.286, 16.667, and 6.25. Normalizing makes the bills weight about 84.3%. Bills' 0.5% volatility is much smaller than the others, so the reciprocal weighting gives bills most of the allocation. This method uses standalone volatility, not expected return or correlation. Its 3.77% expected return falls short of the 6.50% objective despite its 1.05% portfolio volatility.

**Baseline to show the CIO first:** the benchmark is the clearest starting comparison because it is the CIO's own reference. Its 6.80% expected return exceeds today's threshold, yet its 0.0% reserve fails the mandate. Showing it first exposes the need to reconcile the benchmark with reserve requirements. Equal weight and inverse volatility then illustrate why reducing risk alone does not deliver the return objective.

## Checkout links

- [Lab 14 writeup](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-14-portfolio-baselines/lab-14-writeup.md)
- [portfolio.py](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-14-portfolio-baselines/portfolio.py)
- [mandate.py with candidate E](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-13-portfolio-mandate/mandate.py)
- [Reproducible audit](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-14-portfolio-baselines/verify_portfolio.py)
- [Executed results](https://github.com/JP161632/FIN43900-Fall2026/blob/main/projects/lab-14-portfolio-baselines/verification-results.txt)
