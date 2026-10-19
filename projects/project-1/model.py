"""Offline Salesforce FCFF engine. Python 3.10+, standard library only.

USD millions, shares millions. Forecast periods end July 31; valuation is Aug 27.
Financial judgments and data sources are deliberately separate from this arithmetic.
"""
from __future__ import annotations

import copy
import datetime as dt
import math
import statistics


class ModelError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ModelError(message)


def close(a, b, label, tolerance=1e-7):
    require(math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tolerance,
            f"{label}: {a} != {b}")


ASSET_KEYS = ("cash", "securities", "ar", "commission_current", "prepaid", "ppe",
              "rou", "commission_noncurrent", "investments", "goodwill", "intangibles", "other_assets")
LIABILITY_KEYS = ("ap_other_current", "lease_current", "deferred_revenue", "debt_current",
                  "debt_noncurrent", "lease_noncurrent", "other_noncurrent_liabilities")


def validate_inputs(d, sources):
    ids = {s["id"] for s in sources}
    require(len(ids) == len(sources), "Duplicate source ID")
    for s in sources:
        for key in ("id", "url", "published", "period", "locator", "retrieved"):
            require(bool(s.get(key)), f"Missing source field {s.get('id')}: {key}")
        if s['type'] != 'local course fixture':
            require(s["published"] <= d["valuation_date"], f"Look-ahead source {s['id']}")
    require(d["market"]["diluted_shares"] > 0, "Nonpositive diluted shares")
    require(d["market"]["price"] > 0, "Nonpositive target price")
    require(0 < d["normalization"]["tax_rate"] < 1, "Tax rate must be decimal between 0 and 1")
    for key in ("debt_repayments", "finance_lease_principal", "acquired_amortization"):
        require(len(d["forecast"][key]) == 5, f"{key} must have five annual values")
    for name, case in d["cases"].items():
        require(len(case["expansion"]) == len(case["ebita_margin"]) == 5, f"Five drivers required for {name}")
        require(0 < case["retention"] <= 1, f"Invalid retention for {name}")
    for bsname in ("bs_jan26", "bs_jul26"):
        b = d["historical"][bsname]
        close(sum(b[k] for k in ASSET_KEYS), b["total_assets"], f"{bsname} asset sum")
        close(sum(b[k] for k in LIABILITY_KEYS), b["total_liabilities"], f"{bsname} liability sum")
        close(b["total_assets"], b["total_liabilities"] + b["equity"], f"{bsname} balances")
    for period in ("fy26", "h1fy27", "h1fy26"):
        a = d["historical"][period]
        close(a["subscription"] + a["services"], a["revenue"], f"{period} revenue")
        close(a["revenue"] - a["subscription_cogs"] - a["services_cogs"] - a["rd"]
              - a["sm"] - a["ga"] - a["restructuring"], a["ebit"], f"{period} EBIT")
        nonop = (a["investment_gains"] + a["other_income_net_interest"] if period == "fy26"
                 else a["investment_gains"] + a["other_income"] - a["interest"])
        close(a["ebit"] + nonop - a["tax"], a["net_income"], f"{period} net income")
        close(a["begin_cash"] + a["cfo"] + a["cfi"] + a["cff"] + a["fx"],
              a["end_cash"], f"{period} cash flow")
    for p in d["peers"]:
        require(p["annual_available"] <= d["valuation_date"], f"Future earnings {p['ticker']}")
        require(p["price_date"] == d["valuation_date"], "Peer price date mismatch")
        for key in ("price_source", "annual_source", "balance_source"):
            require(p[key] in ids, f"Missing peer source {p['ticker']} {key}")
    return True


def normalized_base(d):
    h = d["historical"]
    ltm = {k: h["fy26"][k] + h["h1fy27"][k] - h["h1fy26"][k]
           for k in ("subscription", "services", "revenue", "ebit", "restructuring", "net_income",
                     "tax", "investment_gains", "da", "acquired_amortization", "commission_amortization",
                     "sbc", "cfo", "capex")}
    n = d["normalization"]
    sub_add = n["informatica_subscription_runrate"] - n["informatica_subscription_ltm"]
    rev_add = n["informatica_total_runrate"] - n["informatica_total_ltm"]
    revenue = ltm["revenue"] + rev_add
    ebit = (ltm["ebit"] + ltm["restructuring"] - revenue * n["recurring_restructure_rate"]
            + rev_add * n["incremental_ebita_margin"])
    return {"reported_ltm": ltm, "subscription": ltm["subscription"] + sub_add,
            "services": ltm["services"] + rev_add - sub_add, "revenue": revenue,
            "normalized_ebit": ebit, "normalized_ebita": ebit + ltm["acquired_amortization"],
            "informatica_revenue_add": rev_add,
            "restructure_adjustment": ltm["restructuring"] - revenue * n["recurring_restructure_rate"]}


def wacc_build(d):
    m = d["market"]
    eq = m["ordinary_shares"] * m["price"]
    debt = m["debt_market_value"] + m["finance_leases"]
    dw = debt / (debt + eq)
    ke = m["risk_free"] + m["beta"] * m["equity_risk_premium"]
    kd_after = m["cost_of_debt"] * (1 - d["normalization"]["tax_rate"])
    return {"risk_free": m["risk_free"], "beta_assumption": m["beta"],
            "equity_risk_premium_assumption": m["equity_risk_premium"], "cost_equity": ke,
            "pretax_cost_debt_assumption": m["cost_of_debt"], "aftertax_cost_debt": kd_after,
            "equity_market_value": eq, "debt_market_value_including_finance_leases": debt,
            "equity_weight": 1 - dw, "debt_weight": dw,
            "wacc": ke * (1 - dw) + kd_after * dw}


def opening_balance(d):
    b = d["historical"]["bs_jul26"]
    fl = d["market"]["finance_leases"]
    return {"cash": b["cash"], "securities": b["securities"], "ar": b["ar"],
            "commissions": b["commission_current"] + b["commission_noncurrent"],
            "prepaid": b["prepaid"], "ppe": b["ppe"], "rou": b["rou"],
            "investments": b["investments"], "goodwill": b["goodwill"], "intangibles": b["intangibles"],
            "other_assets": b["other_assets"],
            "operating_liabilities": b["ap_other_current"] + b["other_noncurrent_liabilities"] - fl,
            "operating_leases": b["lease_current"] + b["lease_noncurrent"],
            "deferred_revenue": b["deferred_revenue"],
            "debt": b["debt_current"] + b["debt_noncurrent"] + fl, "equity": b["equity"]}


def totals(b):
    assets = sum(b[k] for k in ("cash", "securities", "ar", "commissions", "prepaid", "ppe", "rou",
                                "investments", "goodwill", "intangibles", "other_assets"))
    liabilities = sum(b[k] for k in ("operating_liabilities", "operating_leases", "deferred_revenue", "debt"))
    return assets, liabilities


def forecast(d, case="base", shock=None, margin_shift=0.0):
    n, f, c, m = d["normalization"], d["forecast"], copy.deepcopy(d["cases"][case]), d["market"]
    b0, base = opening_balance(d), normalized_base(d)
    ar_ratio = b0["ar"] / base["revenue"]
    prepaid_ratio = b0["prepaid"] / base["revenue"]
    op_liab_ratio = b0["operating_liabilities"] / base["revenue"]
    def_ratio = b0["deferred_revenue"] / base["revenue"]
    if shock == "churn_and_collections":
        spec=d["what_if_assumptions"][shock]
        c.update({k:spec[k] for k in ("retention","expansion","new_business","ebita_margin")})
        ar_ratio += spec["extra_receivable_days"]/365
        def_ratio -= spec["deferred_ratio_drop"]
    if shock == "ai_hosting_cost":
        c["ebita_margin"] = [x+d["what_if_assumptions"][shock]["ebita_margin_delta"] for x in c["ebita_margin"]]
    if shock == "cash_acquisitions_no_benefit":
        acquisition_spend = d["what_if_assumptions"][shock]["cash_cost"]
    else:
        acquisition_spend = 0
    sub, services, prev = base["subscription"], base["services"], b0
    rows = []
    for i in range(5):
        sub *= c["retention"] + c["expansion"][i] + c["new_business"]
        services *= 1 + c["services_growth"]
        revenue = sub + services
        # Case margins were calibrated at 8% compensation. Changing that driver must
        # affect earnings; merely displaying an SBC rate would be a disconnected input.
        margin = c["ebita_margin"][i] + margin_shift + f["margin_calibration_sbc_rate"] - f["sbc_rate"]
        require(0.02 < margin < 0.70, "EBITA margin outside modeled economic domain")
        ebita = revenue * margin
        subscription_cogs_ex_acquired_amort = sub * f["subscription_cogs_rate_ex_acquired_amort"]
        services_cogs = services * f["services_cogs_rate"]
        rd = revenue * f["rd_rate"]
        ga = revenue * f["ga_rate"]
        restructuring = revenue * n["recurring_restructure_rate"]
        gross_profit_ex_acquired_amort = revenue-subscription_cogs_ex_acquired_amort-services_cogs
        # S&M is the expense budget required by the margin path, not an independent
        # claim about sales productivity. Its implied ratio is exposed for challenge.
        sm = gross_profit_ex_acquired_amort-rd-ga-restructuring-ebita
        require(sm >= 0, "Margin path implies a negative sales and marketing budget")
        amort = min(prev["intangibles"], f["acquired_amortization"][i])
        depreciation = f["depreciation_opening_ppe"] * prev["ppe"]
        ebit = ebita - amort  # EBITA retains PP&E depreciation and recurring compensation.
        repayment = min(prev["debt"], f["debt_repayments"][i]+f["finance_lease_principal"][i])
        interest = (prev["debt"] - 0.5*repayment) * m["cost_of_debt"]
        pretax = ebit - interest
        tax = max(pretax, 0) * n["tax_rate"]  # no immediate monetization of tax losses
        ni = pretax - tax
        ar = revenue * ar_ratio
        prepaid = revenue * prepaid_ratio
        op_liab = revenue * op_liab_ratio
        deferred = revenue * def_ratio
        comm_add = sub * f["commission_add_rate"]
        comm_amort = min(prev["commissions"], prev["commissions"] * f["commission_amort_opening"])
        change_nwc = ((ar-prev["ar"]) + (prepaid-prev["prepaid"])
                      - (op_liab-prev["operating_liabilities"]) - (deferred-prev["deferred_revenue"]))
        capex = revenue * f["capex_rate"]
        # Compensation is economically cash-settled; there is no SBC cash-flow addback.
        cfo = ni + depreciation + amort + comm_amort - comm_add - change_nwc
        dividends = f["dividend_per_share"] * m["diluted_shares"]
        acq = acquisition_spend if i == 0 else 0
        cfi = -capex - acq
        cash_pre_financing = prev["cash"] + cfo + cfi - repayment - dividends
        revolver = max(0, f["minimum_cash"] - cash_pre_financing)
        cff = -repayment - dividends + revolver
        cash = prev["cash"] + cfo + cfi + cff
        b = {**prev, "cash":cash, "ar":ar, "prepaid":prepaid,
             "commissions":prev["commissions"] + comm_add - comm_amort,
             "ppe":prev["ppe"] + capex - depreciation,
             "goodwill":prev["goodwill"] + acq,
             "intangibles":prev["intangibles"] - amort,
             "operating_liabilities":op_liab, "deferred_revenue":deferred,
             "debt":prev["debt"] - repayment + revolver,
             "equity":prev["equity"] + ni - dividends}
        assets, liabilities = totals(b)
        close(assets, liabilities+b["equity"], f"{case}/{shock} year{i+1} balance sheet")
        close(cash-prev["cash"], cfo+cfi+cff, f"{case}/{shock} year{i+1} cash tie")
        nopat = ebit * (1-n["tax_rate"])
        fcff = nopat + depreciation + amort + comm_amort - comm_add - change_nwc - capex - acq
        # Valid in profitable cases with tax shield fully used.
        if pretax > 0:
            close(fcff, cfo + interest*(1-n["tax_rate"]) - capex - acq,
                  f"{case}/{shock} year{i+1} FCFF reconciliation")
        revenue_prior = base["revenue"] if i == 0 else rows[-1]["income_statement"]["revenue"]
        is_ = {"subscription":sub,"services":services,"revenue":revenue,
               "subscription_cogs_ex_acquired_amort":subscription_cogs_ex_acquired_amort,
               "services_cogs":services_cogs,"gross_profit_ex_acquired_amort":gross_profit_ex_acquired_amort,
               "rd":rd,"sm_including_commission_amortization":sm,"ga":ga,"recurring_restructuring":restructuring,
               "revenue_growth":revenue/revenue_prior-1,"ebita":ebita,"ebita_margin":margin,
               "acquired_amortization":amort,"ebit":ebit,"ebit_margin":ebit/revenue,
               "interest":interest,"tax":tax,"net_income":ni,
               "diluted_eps":ni/m["diluted_shares"],
               "economic_cash_compensation_included":revenue*f["sbc_rate"]}
        cf = {"begin_cash":prev["cash"],"net_income":ni,"depreciation":depreciation,
              "acquired_amortization":amort,"commission_amortization":comm_amort,
              "commission_additions":comm_add,"change_operating_nwc":change_nwc,
              "sbc_addback":0,"cfo":cfo,"capex":capex,"acquisitions":acq,"cfi":cfi,
              "debt_repayment":repayment,"dividends":dividends,"new_borrowing":revolver,
              "cff":cff,"cash_change":cash-prev["cash"],"end_cash":cash,"fcff":fcff}
        ebitda = ebit + depreciation + amort
        rows.append({"period_end":f"{2027+i}-07-31", "income_statement":is_,
                     "balance_sheet":{**b,"total_assets":assets,"total_liabilities":liabilities},
                     "cash_flow":cf,
                     "credit":{"constructed_ebitda":ebitda,"ebit_interest_coverage":ebit/interest,
                               "gross_debt_ebitda":b["debt"]/ebitda,
                               "cash_headroom":cash-f["minimum_cash"]},
                     "checks":{"balance_sheet_error":assets-liabilities-b["equity"],
                               "cash_tie_error":cash-prev["cash"]-cfo-cfi-cff}})
        prev = b
    return rows


def dcf_cashflows(cashflows, wacc, growth, terminal_cashflow=None, first_time=1.0):
    require(len(cashflows) > 0, "No explicit cash flows")
    require(math.isfinite(wacc) and math.isfinite(growth), "Nonfinite discount inputs")
    require(wacc > growth and wacc > 0 and growth > -1, "Require WACC > g and WACC > 0")
    require(all(math.isfinite(x) for x in cashflows), "Nonfinite FCFF")
    require(first_time > 0, "First discount period must be positive")
    pvs = [cf/(1+wacc)**(first_time+i) for i,cf in enumerate(cashflows)]
    terminal_cf = cashflows[-1]*(1+growth) if terminal_cashflow is None else terminal_cashflow
    require(terminal_cf > 0, "Nonpositive terminal FCFF")
    terminal = terminal_cf/(wacc-growth)
    pv_terminal = terminal/(1+wacc)**(first_time+len(cashflows)-1)
    ev = sum(pvs)+pv_terminal
    return {"explicit_fcff":cashflows,"pv_explicit_by_year":pvs,"pv_explicit":sum(pvs),
            "terminal_fcff":terminal_cf,"terminal_value_at_end_year5":terminal,
            "pv_terminal":pv_terminal,"enterprise_value":ev,"terminal_share":pv_terminal/ev,
            "wacc":wacc,"g":growth,"first_discount_years":first_time}


def valuation(d, case="base", shock=None, wacc=None, growth=None, margin_shift=0.0,
              erroneous_sbc_addback=False):
    rows = forecast(d,case,shock,margin_shift)
    c, f, n, m = d["cases"][case], d["forecast"], d["normalization"], d["market"]
    rate = wacc if wacc is not None else (c["wacc"] if c["wacc"] is not None else wacc_build(d)["wacc"])
    g = c["g"] if growth is None else growth
    require(g < f["terminal_roic"], "Terminal growth must be below terminal ROIC")
    # Explicit July-to-July years; remove elapsed July31-Aug27 cash flow, then roll cash.
    elapsed = (dt.date.fromisoformat(d["valuation_date"]) - dt.date(2026,7,31)).days/365
    require(0 <= elapsed < 1, "Valuation date outside supported first-year stub")
    cashflows = [r["cash_flow"]["fcff"] for r in rows]
    # A pending acquisition cannot have spent cash before the information cutoff.
    acquisition = rows[0]["cash_flow"]["acquisitions"]
    cash_rollforward = (rows[0]["cash_flow"]["cash_change"]+acquisition)*elapsed
    cashflows[0] *= 1-elapsed
    cashflows[0] -= acquisition*elapsed
    lastrev = rows[-1]["income_statement"]["revenue"]
    terminal_margin = min(f["terminal_ebita_margin"] + margin_shift + f["margin_calibration_sbc_rate"] - f["sbc_rate"],
                          rows[-1]["income_statement"]["ebita_margin"])
    terminal_nopat = lastrev*(1+g)*terminal_margin*(1-n["tax_rate"])
    # Acquired amortization fades out; perpetual reinvestment g/ROIC prevents free growth.
    terminal_fcff = terminal_nopat*(1-g/f["terminal_roic"])
    if erroneous_sbc_addback:
        for i,r in enumerate(rows):
            cashflows[i] += r["income_statement"]["economic_cash_compensation_included"]*(1-elapsed if i==0 else 1)
        terminal_fcff += lastrev*(1+g)*f["sbc_rate"]
    result = dcf_cashflows(cashflows,rate,g,terminal_fcff,1-elapsed)
    b = d["historical"]["bs_jul26"]
    operating_cash = normalized_base(d)["revenue"]*f["operating_cash_rate"]
    excess_cash = b["cash"]+b["securities"]+cash_rollforward-operating_cash
    investments = b["investments"]*c["investment_realization"]
    debt = m["debt_market_value"]+m["finance_leases"]
    equity = result["enterprise_value"]+excess_cash+investments-debt
    price = equity/m["diluted_shares"]
    close(price*m["diluted_shares"],equity,"per-share bridge")
    flags = []
    for r in rows:
        if r["credit"]["ebit_interest_coverage"] < 3: flags.append("EBIT coverage below 3x analyst floor")
        if r["cash_flow"]["new_borrowing"] > 0: flags.append("New borrowing needed to preserve cash floor")
    first = rows[0]["income_statement"]
    if first["revenue_growth"] < 0.03 and first["ebit_margin"] < 0.21:
        flags.append("Weak growth and operating margin jointly breach underwriting floors")
    if flags:
        action = "do not initiate"
    elif m["price"] <= 0.8*price:
        action = "initiate conditionally"
    else:
        action = "watch/defer"
    return {"case":case,"shock":shock,"forecast":rows,**result,
            "terminal_convention":{"ebita_margin":terminal_margin,"roic":f["terminal_roic"],
                                   "reinvestment_fraction":g/f["terminal_roic"],"nopat":terminal_nopat},
            "bridge":{"cash_and_securities_july31":b["cash"]+b["securities"],
                      "estimated_cash_roll_to_valuation":cash_rollforward,
                      "operating_cash_retained":operating_cash,"excess_cash":excess_cash,
                      "strategic_investments_carrying":b["investments"],
                      "investment_realization_fraction":c["investment_realization"],
                      "strategic_investments_value":investments,"financial_debt_market":m["debt_market_value"],
                      "finance_leases":m["finance_leases"],"operating_leases_subtracted":0,
                      "preferred":0,"noncontrolling_interest":0,"other_senior_claims":0,
                      "common_equity_value":equity,"diluted_shares":m["diluted_shares"]},
            "per_share":price,"return_to_value":price/m["price"]-1,"action":action,
            "risk_flags":sorted(set(flags)),"conditional_entry_price":0.8*price}


def comparables(d):
    seen, rows = set(), []
    for p in d["peers"]:
        require(p["ticker"] != "CRM", "Target cannot be its own peer")
        require(p["ticker"] not in seen, "Duplicate peer")
        seen.add(p["ticker"])
        require(p["price"] > 0 and p["annual_diluted_eps"] > 0 and p["annual_revenue"] > 0
                and p["ordinary_shares"] > 0, "Nonpositive peer denominator or price")
        eq = p["price"]*p["ordinary_shares"]
        ev = eq+p["financial_debt"]-p["cash_and_securities"]
        rows.append({**p,"equity_market_value":eq,"enterprise_value":ev,
                     "pe":p["price"]/p["annual_diluted_eps"],"ev_revenue":ev/p["annual_revenue"]})
    require(rows, "No usable peers")
    annual = d["historical"]["fy26"]
    prices_pe = [r["pe"]*annual["diluted_eps"] for r in rows]
    # Gross-cash, financial-debt-only bridge matches peers; no strategic-investment adjustment.
    target_financial_debt = d["market"]["debt_market_value"]+d["market"]["finance_leases"]
    gross_cash = d["historical"]["bs_jul26"]["cash"]+d["historical"]["bs_jul26"]["securities"]
    prices_ev = [(r["ev_revenue"]*annual["revenue"]-target_financial_debt+gross_cash)
                 /d["market"]["diluted_shares"] for r in rows]
    leave = []
    for p in rows:
        remaining = [r for r in rows if r["ticker"] != p["ticker"]]
        leave.append({"removed":p["ticker"],"remaining_count":len(remaining),
                      "pe_implied_price":statistics.median([r["pe"] for r in remaining])*annual["diluted_eps"]
                      if remaining else None,"interpretation":"one-peer reference, no range" if len(remaining)==1 else "no estimate"})
    return {"peers":rows,"pe_implied_prices":prices_pe,"ev_revenue_implied_prices":prices_ev,
            "pe_range":[min(prices_pe),max(prices_pe)],"ev_revenue_range":[min(prices_ev),max(prices_ev)],
            "pe_median_price":statistics.median(prices_pe),"leave_one_out":leave,
            "target_reported_annual_pe":d["market"]["price"]/annual["diluted_eps"]}


def reverse_dcf(d):
    """Solve a parallel shift of all five EBITA margins AND terminal margin, other inputs fixed."""
    target = d["market"]["price"]
    lo, hi = -0.10, 0.20
    require(valuation(d,margin_shift=lo)["per_share"] <= target <= valuation(d,margin_shift=hi)["per_share"],
            "Market price outside reverse-DCF bracket")
    for _ in range(70):
        mid = (lo+hi)/2
        if valuation(d,margin_shift=mid)["per_share"] < target: lo = mid
        else: hi = mid
    shift=(lo+hi)/2
    solved=valuation(d,margin_shift=shift)
    return {"solved_variable":"parallel additive shift to all five EBITA margins and terminal EBITA margin",
            "margin_shift":shift,"year1_ebita_margin":d["cases"]["base"]["ebita_margin"][0]+shift,
            "terminal_ebita_margin":solved["terminal_convention"]["ebita_margin"],
            "reproduced_price":solved["per_share"],
            "held_fixed":"revenue cohorts, WACC, g, tax, ROIC, capex/working-capital policies, share count, cash/debt/investment bridge policy; cash roll reacts to changed profitability"}


def all_results(d, sources):
    validate_inputs(d,sources)
    cases={name:valuation(d,name) for name in d["cases"]}
    w=wacc_build(d)["wacc"]
    grid=[{"wacc":r,"values":[valuation(d,wacc=r,growth=g)["per_share"] for g in (0.02,0.03,0.04)]}
          for r in (w-0.01,w,w+0.01)]
    shocks={name:valuation(d,shock=name) for name in
            ("churn_and_collections","ai_hosting_cost","cash_acquisitions_no_benefit")}
    return {"valuation_date":d["valuation_date"],"information_cutoff":d["information_cutoff"],
            "units":d["units"],"market":d["market"],"normalized_base":normalized_base(d),
            "wacc_build":wacc_build(d),"cases":cases,"sensitivity":{"growth_columns":[0.02,0.03,0.04],"rows":grid},
            "reverse_dcf":reverse_dcf(d),"comparables":comparables(d),"what_if":shocks,
            "decision":{"user":"Buy-side portfolio manager and investment committee; no CRM position",
                        "horizon":"12-24 month decision horizon; five-year explicit operating forecast and going-concern terminal",
                        "action":cases["base"]["action"],
                        "valuation_range":[cases["low"]["per_share"],cases["high"]["per_share"]],
                        "primary_case":cases["base"]["per_share"],
                        "conditions":"20% margin of safety to base, two quarters of >=8% organic subscription growth and >=22% GAAP EBIT margin; validate acquisitions, ASR settlement and cash/share bridge first",
                        "reversal":"Suspend initiation if two quarters organic growth <3% with EBIT margin <21%, EBIT coverage <3x, or cash <USD2000M / new funding need; these are analyst floors, not covenants"}}
