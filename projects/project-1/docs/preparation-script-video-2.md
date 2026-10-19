# Video 2 preparation script

AI-assisted technical rehearsal, not an actual transcript. Navigate the code and execute the demonstration yourself. Planned length 4:30; maximum 5:00.

This repository runs offline with Python 3.10 or newer and no model packages. Frozen facts and hypotheses are in data/inputs.json; source dates and definitions are in data/sources.json. model.py contains the financial engine, tests.py contains validation, and run.py writes the report, dashboard, full JSON and run receipt. The output is already visible to a grader without running code.

In normalized_base, LTM equals annual FY26 plus current first half minus the prior first half. It annualizes Informatica's partial contribution and retains a recurring restructuring reserve. It does not capitalize investment gains as operating profit. In forecast, subscription revenue follows retention, expansion and new-business assumptions. Those are underwriting hypotheses, not disclosed churn data. EBITA margins control the operating budget; implied sales-and-marketing spending remains visible for challenge.

The statement links matter more than syntax. Net income changes equity. PP&E changes by capex minus depreciation. Commission assets change by cash additions minus amortization. Receivables, deferred revenue and operating liabilities affect CFO. Interest and principal affect financing and liquidity. Cash comes from CFO plus CFI plus CFF. Balance sheets are checked; equity is not plugged to force a balance. If new funding is necessary, the model flags it and blocks initiation.

In valuation, FCFF excludes interest and financing distributions. Future compensation remains a cash-equivalent economic cost. The terminal uses next year's operating profit after tax and reinvestment equal to growth divided by return on incremental capital. It enforces WACC above growth. The bridge adds surplus cash and discounted strategic investments, subtracts financial debt and finance leases, then divides by a current diluted proxy. Operating rent is retained, so operating lease debt is not subtracted again.

I will now follow the README in a fresh environment and run run.py --all. The 22 checks include the official course EV and price answers, nine sensitivity cells, actual statement reconciliation,30 forecast articulations, monotonicity and rejection of invalid data. I will point to the deliberate one-million-dollar balance-sheet error and the rejected SBC addback. The wrong SBC treatment can run and balance while overstating value, which is why accounting checks alone are insufficient.

The WACC directional plan was AI-authored before execution; it is not my required human locked record. I will identify the separate authentic record only if it exists. One remaining limitation is the share proxy and July debt date. They must be refreshed before a trade, and the model's terminal reliance means I cannot defend a purchase only by pointing to five forecast years.
