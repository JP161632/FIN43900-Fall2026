# Lab 13 — Portfolio Mandate Defense

## Sort the CIO statements

| Statement | Type | Reason | IPS component |
|---|---|---|---|
| S1 — seven-year horizon; annual rebalancing | Objective | The horizon sets the time over which success is assessed and the rebalancing cadence implements it. | Investment horizon and governance/rebalancing process |
| S2 — CPI + 4% net of costs over rolling five-year periods | Objective | This is the stated return goal and measurement period. | Return objective |
| S3 — quarterly distributions and one year held in cash or daily-liquid government securities | Hard constraint | It specifies a required cash-flow amount and an explicit reserve floor. | Liquidity and spending constraint |
| S4 — 60% global equities / 40% U.S. investment-grade bonds benchmark | Preference | It is a performance comparison reference, but it does not state a required allocation or tracking-error rule. | Benchmark and performance evaluation |
| S5 — long-only; no borrowing, shorts, or derivatives | Hard constraint | These are explicit prohibited investment practices. | Permitted investments and leverage restrictions |
| S6 — no single issuer above 8% | Hard constraint | This is a numerical concentration limit. | Diversification/concentration constraint |
| S7 — annual turnover at most 25% without committee approval | Hard constraint | Turnover above the limit needs stated governance approval. | Trading and governance constraint |
| S8 — at least 90% redeemable within five business days | Hard constraint | This is a measurable liquidity threshold and window. | Liquidity constraint |
| S9 — no calendar-year loss greater than 10% | Unverifiable promise | The CIO did not define the loss measure or what counts as a breach, so it cannot be coded or enforced yet. | Risk tolerance, still incomplete |
| S10 — no sector, ESG, tax, or home-bias preference; no pilot optimization target | Missing | The optimization criterion and risk trade-off have not been chosen. | Portfolio construction and decision rule, still incomplete |

## Known-answer verification and probe

With the supplied A–C inputs, the checker reports the 3.0% reserve minimum and these outcomes:

| Rule | A | B | C |
|---|---:|---:|---:|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only (lowest weight) | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve >= 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable in 5 days >= 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company <= 8.0% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) |

For the required long-only probe, I temporarily changed candidate A's Cash weight from 2 to -2 and its Global equity index fund weight from 60 to 64, then ran the checker. It reports a lowest weight of -2.0 FAIL; the reserve remains 10.0 pass, and no other rule fails. I restored the supplied A weights afterward.

## Attack portfolio D

Candidate D in `mandate.py` is 3% Cash and 97% Treasury bills. It passes every coded rule: its reserve-eligible share is 100.0%, its five-day liquidity is 100.0%, and the issuer rule exempts cash and the U.S. Treasury.

The objection holds. A nearly all-cash-and-bills portfolio could reasonably be rejected because it is unlikely to pursue CPI + 4% net of costs over rolling five-year periods; S2 decides that objection. In the skeptical-colleague review, I would cite S2 against this D because its allocation does not supply a credible growth engine for the stated return objective.

## Question for the CIO

Which single risk/return metric should govern optimization of the rolling five-year CPI + 4% objective?

The answer changes the portfolio: choosing probability of meeting CPI + 4% would support more growth assets, while choosing expected shortfall or benchmark tracking error could justify more bonds, cash reserves, or a closer 60/40 allocation.

## Investment policy statement

An investment policy statement (IPS) is the client-approved document that connects the purpose of assets to a repeatable investment and governance process. It states what success means, what risks and constraints apply, how the portfolio is managed, and how results are evaluated. Its objectives specify the desired return and time horizon; its constraints cover liquidity, legal or regulatory limits, taxes, unique circumstances, and risk limits. It also identifies the benchmark, permitted investments, rebalancing process, and decision authority.

Meridian's statements map to an IPS as shown in the first table: S1 and S2 establish the investment horizon and return objective; S3 and S8 establish spending and liquidity constraints; S5–S7 set implementation, concentration, and trading constraints; S4 gives a benchmark; S9 is an incomplete risk-tolerance provision; and S10 leaves the construction criterion unresolved.

## Reflection

A portfolio can pass every checkable rule while still being wrong for this client because constraints are only boundaries, not a complete investment decision. Candidate D demonstrates this: it is liquid, diversified under the stated issuer rule, and funded for distributions, yet it may have little chance of earning the client's CPI + 4% objective. The missing definition of success and risk trade-off can therefore make a mechanically compliant portfolio unsuitable.

The statement type I was least sure of was S4. I classified it as a preference because the benchmark tells the CIO how performance can be compared, but it does not require the portfolio to hold 60/40 or establish an allowed tracking-error range. If the CIO intends either of those, it must be written as a hard constraint or optimization target.
