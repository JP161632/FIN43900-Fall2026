# Weeks 5 and 6 Salesforce credit transfer

Cutoff August 27, 2026. This is an equity-underwriting credit/liquidity diagnostic, not a lending recommendation or default forecast. Source definitions: CRM_Q July31 balance sheet and notes5/8, CRM_K FY26 statements. All amounts USD millions. Full linked results: outputs/results.json, base and what_if.churn_and_collections. The directional-test plan is AI-authored; no human AI-off freeze is claimed.

## Week 5 definitions and baseline

Historical book financial borrowings are39,288; adding finance leases633 gives39,921. Historical reported LTM EBIT is8,735. The issuer does not supply the course case's exact reported-EBITDA measure; a clearly **constructed** EBIT+D&A proxy is8,735+3,922=12,657. This aggregate D&A includes ROU amortization, so it is not the cash-economic EBITDA used in the pro-forma. Do not label it reported EBITDA. Historical gross-debt/constructed-EBITDA is about3.15x including finance leases. Provider enterprise-value/EBITDA labels are not substituted.

Interest rose during the six months because debt was issued after January. A simple annualized H1 interest number would understate a full-year post-issuance burden. The pro-forma therefore uses5.5% on opening financial debt less half scheduled principal, explicitly an analyst financing assumption. It does not invent an annual historical gross-interest expense out of annual net other income.

In the base first forecast year, EBIT coverage is about5.11x; constructed EBITDA is13,393; ending debt/constructed EBITDA about2.96x; ending cash about15,967. The relevant cash-flow/coverage numbers reconcile to the economic statements. Finance-lease principal220/148/119/97/49 is an analyst allocation of633 present-value principal across disclosed payment maturities; precise amortized-cost detail would refine it. Contractual debt maturities use the filing's principal schedule and dates, not an assumed perpetual refinance.

Analyst diagnostic floors: EBIT/interest3x; cash2000; joint weak organic growth<3% and EBIT margin<21%. These thresholds are not Salesforce's legal covenants. The filing says covenant compliance at July31; it does not justify inventing a new covenant threshold. Unused facility capacity is not assumed available in the downside. A new funding requirement is exposed as a hypothetical plug and blocks initiation.

## Week 6 causal downside and transmission

Named shock: churn_and_collections. Retention90%, expansion6%, new business2% imply subscription contraction2%; EBITA margin20% initially; receivable days+15; deferred-revenue funding balance5 revenue points lower. This is a causal renewal/usage-demand shock accompanied by a weaker billing/collections cycle. Other tax, capex, debt, dividend and share policies stay fixed. It is an AI-assisted scenario, not a reconstructed human before-run prediction.

First-year EBIT coverage falls to roughly3.26x and constructed EBITDA to9,327; gross debt/constructed EBITDA rises to about4.26x. Cash falls to approximately7,136; the model still pays interest and respects the cash floor in that year. The first failure is the joint weak-growth/weak-margin underwriting condition. No payment default, covenant breach or realized investor loss is inferred from that flag. Lower FCFF and the operating path reduce DCF value to roughly83/share, and the committee action changes from watch/defer to **do not initiate**.

The stress remains fully articulated for all five years. Ending cash is calculated from cash flow, not inserted independently. Full numeric outputs and flags are retained; the summary's approximations do not replace those values. A separate extreme cash-floor test creates a visible new-funding need and confirms that the action rule rejects initiation rather than silently treating hypothetical borrowing as certain.

## Conditions for reconsideration

Require two reported quarters supporting organic subscription growth>=8% and GAAP EBIT margin>=22%, coverage>=3x, cash>=2000 and no unverified financing dependence. Reconcile ASR settlement/current awards, debt fair value and pending deal cash before any initiation. A liquidity model flag is a research escalation; legal covenant analysis needs the actual credit agreement and defined metric, and loss/default judgments require additional evidence.
