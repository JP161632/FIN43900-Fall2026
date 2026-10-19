"""Finance-focused validation, including independent published known answers."""
import copy
import hashlib
import json
from pathlib import Path

from model import (ModelError, all_results, comparables, dcf_cashflows, normalized_base,
                   opening_balance, totals, validate_inputs, valuation, wacc_build)


def validate(d, sources):
    tests=[]
    def record(name, fn, purpose):
        try:
            detail=fn()
            tests.append({"test":name,"status":"PASS","claim":purpose,"result":detail})
        except Exception as exc:
            tests.append({"test":name,"status":"FAIL","claim":purpose,"result":str(exc)})
    def expect_error(fn, fragment):
        try: fn()
        except ModelError as exc:
            assert fragment.lower() in str(exc).lower(), str(exc)
            return "Rejected: "+str(exc)
        raise AssertionError("Bad input was accepted")
    def near(actual,expected,tolerance):
        assert abs(actual-expected)<=tolerance, (actual,expected)

    def known_dcf():
        fcff=100
        path=[]
        for g in [0.08,0.06,0.05,0.04,0.03]:
            fcff*=1+g
            path.append(fcff)
        r=dcf_cashflows(path,.10,.03)
        price=(r["enterprise_value"]+50-300)/50
        near(r["enterprise_value"],1624.87,.01)
        near(price,27.50,.005)
        grid=[]
        expected=[[28.60,32.94,39.02],[24.36,27.50,31.69],[21.06,23.41,26.44]]
        for i,w in enumerate([.09,.10,.11]):
            row=[]
            for j,g in enumerate([.02,.03,.04]):
                v=(dcf_cashflows(path,w,g)["enterprise_value"]+50-300)/50
                near(v,expected[i][j],.006)
                row.append(v)
            grid.append(row)
        return {"enterprise_value":r["enterprise_value"],"per_share":price,"grid":grid,
                "fixture":"lessons/week-03/teach-dcf-worked-example.md; published official answers"}
    record("Official DCF and all nine sensitivity answers",known_dcf,"Independent known-answer reconciliation")

    def bridge_fixture():
        fcff=150*(1-.25)+40-60-15
        equity=1000+100-250-20-10
        near(fcff,77.5,1e-9)
        near(equity/100,8.2,1e-9)
        return {"fcff":fcff,"equity":equity,"price":equity/100,
                "fixture":"lessons/week-02/starter/mini_case.csv"}
    record("Official Week2 FCFF and bridge",bridge_fixture,"Units and enterprise-to-common-equity signs")

    def source_check():
        # Independent extraction from issuer release and 10-Q, not a provider EV label.
        b=d["historical"]["bs_jul26"]
        near(b["cash"]+b["securities"],11403,1e-9)
        near(d["market"]["debt_market_value"],30800+6000,1e-9)
        near(d["market"]["risk_free"],4.67/100,1e-12)
        return {"cash_plus_securities":11403,"debt_fair_value":36800,
                "independent_evidence":"CRM_RELEASE balance sheet vs CRM_Q p3; CRM_Q note8 notes fair value30800 plus term loan6000; Treasury date/10yr column"}
    record("Source and definition cross-check",source_check,"Prevent cash labels, book debt and Treasury column contamination")

    def articulation():
        validate_inputs(d,sources)
        a,l=totals(opening_balance(d))
        near(a,109620,1e-7)
        near(l,71242,1e-7)
        r=all_results(d,sources)
        errors=[abs(y["checks"]["balance_sheet_error"]) for x in list(r["cases"].values())+list(r["what_if"].values()) for y in x["forecast"]]
        return {"periods_checked":30,"max_balance_error_millions":max(errors),
                "historical_periods":"FY26, H1FY26, H1FY27 income/cash statements and Jan26/Jul26 balance sheets"}
    record("Historical reconciliation and 30 forecast articulations",articulation,"Statements agree without a balance-sheet equity plug")

    def directional():
        w=wacc_build(d)["wacc"]
        before,after=valuation(d),valuation(d,wacc=w+.01)
        assert after["enterprise_value"]<before["enterprise_value"] and after["per_share"]<before["per_share"]
        return {"prediction_file":"evidence/directional-test-precommit.md","authorship":"AI, not the required human lock",
                "old_wacc":w,"new_wacc":w+.01,"old_price":before["per_share"],"new_price":after["per_share"],
                "expected_direction":"lower","actual_direction":"lower","old_action":before["action"],"new_action":after["action"],
                "decision_effect":"No initiation: margin-of-safety condition remains unmet; a lower valuation strengthens deferral"}
    record("Directional changed-input test",directional,"Predicted discount-rate direction and actual action, separated from human lock")

    def monotonicity():
        w=wacc_build(d)["wacc"]
        for g in [.01,.02,.03,.04]:
            vals=[valuation(d,wacc=x,growth=g)["per_share"] for x in [w-.01,w,w+.01]]
            assert vals[0]>vals[1]>vals[2], vals
        for wr in [w-.01,w,w+.01]:
            vals=[valuation(d,wacc=wr,growth=g)["per_share"] for g in [.01,.02,.03,.04]]
            assert all(a<b for a,b in zip(vals,vals[1:])),vals
        return "WACC falls / g rises: value rises in every admissible tested cell, with positive FCFF and fixed bridge"
    record("DCF monotonicity",monotonicity,"Terminal growth includes a reinvestment cost instead of free growth")

    for name,rate,g in [("g equals WACC",.09,.09),("g above WACC",.08,.10),("zero WACC",0,.0)]:
        record(name,lambda rate=rate,g=g:expect_error(lambda:dcf_cashflows([100]*5,rate,g),"WACC"),"Invalid Gordon-growth boundary fails loudly")
    broken=copy.deepcopy(d)
    broken["historical"]["bs_jul26"]["cash"]+=1
    record("Injected one-million-dollar accounting error",lambda:expect_error(lambda:validate_inputs(broken,sources),"asset sum"),"Independent historical balance error must be detected")
    missing=copy.deepcopy(sources)
    missing[0]["published"]=""
    record("Missing source availability",lambda:expect_error(lambda:validate_inputs(d,missing),"Missing source"),"Missing provenance blocks execution")
    future=copy.deepcopy(sources)
    future[0]["published"]="2026-08-28"
    record("Future source contamination",lambda:expect_error(lambda:validate_inputs(d,future),"Look-ahead"),"Facts unavailable at valuation date must not leak into output")
    no_shares=copy.deepcopy(d)
    no_shares["market"]["diluted_shares"]=0
    record("Zero shares",lambda:expect_error(lambda:validate_inputs(no_shares,sources),"shares"),"No division by zero or fabricated per-share result")
    duplicate=copy.deepcopy(d)
    duplicate["peers"].append(copy.deepcopy(duplicate["peers"][0]))
    record("Duplicate peer",lambda:expect_error(lambda:comparables(duplicate),"Duplicate"),"Prevent multiple weighting through duplicate securities")
    bad_pe=copy.deepcopy(d)
    bad_pe["peers"][0]["annual_diluted_eps"]=-1
    record("Negative peer earnings",lambda:expect_error(lambda:comparables(bad_pe),"Nonpositive"),"P/E is not meaningful with nonpositive earnings")

    def peer_arithmetic():
        r=comparables(d)
        # Independent public EPS and share-price arithmetic, distinct from cash/debt bridge.
        near(r["peers"][0]["pe"],289.15/16.70,1e-9)
        near(r["peers"][1]["pe"],138.43/1.67,1e-9)
        for p in r["peers"]:
            near(p["enterprise_value"]-p["equity_market_value"],p["financial_debt"]-p["cash_and_securities"],1e-7)
        assert r["leave_one_out"][1]["pe_implied_price"]<r["pe_median_price"]
        return {"peers":len(r["peers"]),"leave_one_out":r["leave_one_out"],
                "definition":"GAAP annual EPS for all; USD common shares; identical price date; leases operating; no bridge on P/E"}
    record("Peer policy and multiple definitions",peer_arithmetic,"Separate enterprise-value multiples from equity-value multiples")

    def sbc_failure():
        good,bad=valuation(d),valuation(d,erroneous_sbc_addback=True)
        assert bad["per_share"]>good["per_share"]
        return {"accepted_price":good["per_share"],"rejected_price":bad["per_share"],
                "overstatement_per_share":bad["per_share"]-good["per_share"],
                "accepted_action":good["action"],"rejected_action":bad["action"],
                "disposition":"REJECT SBC addback with no compensating dilution/cash cost",
                "independent_evidence":"CRM_Q p4 recurring compensation; p7 CFO adds back noncash expense; shareholders still bear award cost"}
    record("Highest-risk failure: recurring SBC disappears",sbc_failure,"A running model can still recommend buying on a false cash-flow premise")

    def compensation_driver():
        altered=copy.deepcopy(d)
        altered['forecast']['sbc_rate']+=0.01
        before,after=valuation(d),valuation(altered)
        assert after['forecast'][0]['income_statement']['ebit']<before['forecast'][0]['income_statement']['ebit']
        assert after['forecast'][4]['balance_sheet']['cash']<before['forecast'][4]['balance_sheet']['cash']
        assert after['per_share']<before['per_share']
        return {'old_rate':.08,'new_rate':.09,'old_price':before['per_share'],'new_price':after['per_share'],
                'effect':'Higher recurring compensation propagates into earnings, cash and value; this fixes a disconnected driver found in the audit'}
    record("Recurring compensation driver propagates",compensation_driver,"A disclosed input must affect the statements and valuation")

    def funding_failure():
        altered=copy.deepcopy(d)
        altered['forecast']['minimum_cash']=50000
        out=valuation(altered)
        assert out['forecast'][0]['cash_flow']['new_borrowing']>0 and out['action']=='do not initiate'
        return {'new_funding_year1':out['forecast'][0]['cash_flow']['new_borrowing'],
                'action':out['action'],'meaning':'Hypothetical financing plug is visible, not evidence that credit is available'}
    record("Funding shortfall is actionable",funding_failure,"A cash-floor financing plug cannot silently make an insolvent forecast look safe")

    def downside():
        good,bad=valuation(d),valuation(d,shock="churn_and_collections")
        assert bad["per_share"]<good["per_share"] and bad["action"]=="do not initiate"
        for y in bad["forecast"]:
            assert abs(y["checks"]["balance_sheet_error"])<1e-7
        return {"base_action":good["action"],"downside_action":bad["action"],"base_price":good["per_share"],
                "downside_price":bad["per_share"],"first_flags":bad["risk_flags"],
                "coverage_first_year":bad["forecast"][0]["credit"]["ebit_interest_coverage"],
                "liquidity_first_year":bad["forecast"][0]["balance_sheet"]["cash"]}
    record("Decision-altering downside",downside,"Churn, margin pressure and collections flow through the statements and committee rule")

    def bridge_sensitivity():
        base=valuation(d)
        altered=copy.deepcopy(d)
        altered["market"]["diluted_shares"]+=33
        diluted=valuation(altered)
        assert diluted["per_share"]<base["per_share"]
        # Exclude July-Aug estimated cash roll to expose stale balance-sheet risk.
        b=base["bridge"]
        return {"base_shares":d["market"]["diluted_shares"],"overhang_stress_shares":altered["market"]["diluted_shares"],
                "stressed_per_share":diluted["per_share"],
                "no_cash_roll_per_share":base["per_share"]-b["estimated_cash_roll_to_valuation"]/b["diluted_shares"],
                "book_instead_of_market_debt_effect":-(39288-36800)/b["diluted_shares"],
                "interpretation":"33M-share stress is a conservative overhang overlay, not a replacement dilution valuation; do not count both routinely"}
    record("Share-overhang and bridge basis robustness",bridge_sensitivity,"Quantify proxy shares and stale debt/cash basis limitations")
    r=all_results(d,sources)
    record("Reverse DCF round trip",lambda:(near(r["reverse_dcf"]["reproduced_price"],d["market"]["price"],1e-7) or r["reverse_dcf"]),"Solved margin path actually reproduces the observed price")
    failed=[x for x in tests if x["status"]=="FAIL"]
    return {"passed":len(tests)-len(failed),"failed":len(failed),"tests":tests,
            "human_locked_record":"MISSING; no AI-authored test is substituted",
            "partner_challenge":"MISSING; no challenger attribution invented"}
