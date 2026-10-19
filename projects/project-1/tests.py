"""Tests target valuation claims, source definitions and deliberately broken inputs."""
import copy
from model import (ModelError,all_results,comparables,dcf_cashflows,forecast,historical_checks,
                   ltm,near,opening,totals,valuation,wacc_build)


def validate(d):
    tests=[]
    def record(name,purpose,fn):
        try: tests.append({'test':name,'claim':purpose,'status':'PASS','result':fn()})
        except Exception as exc: tests.append({'test':name,'claim':purpose,'status':'FAIL','result':str(exc)})
    def rejects(fn,fragment):
        try: fn()
        except ModelError as exc:
            assert fragment.lower() in str(exc).lower(),str(exc)
            return str(exc)
        raise AssertionError('Corrupted input was accepted')
    def known():
        f=100; flows=[]
        for g in [.08,.06,.05,.04,.03]: f*=1+g; flows.append(f)
        expected=[[28.60,32.94,39.02],[24.36,27.50,31.69],[21.06,23.41,26.44]]
        r=dcf_cashflows(flows,.10,.03); near(r['enterprise_value'],1624.87,'official EV',.01)
        grid=[]
        for i,w in enumerate([.09,.10,.11]):
            row=[]
            for j,g in enumerate([.02,.03,.04]):
                v=(dcf_cashflows(flows,w,g)['enterprise_value']+50-300)/50
                near(v,expected[i][j],'official price',.006); row.append(v)
            grid.append(row)
        return {'ev':r['enterprise_value'],'grid':grid,'benchmark':'lessons/week-03/teach-dcf-worked-example.md'}
    record('Official training DCF and nine cells','Published independent known answers, not self-generated expectations',known)
    def bridge_fixture():
        f=150*(1-.25)+40-60-15; e=1000+100-250-20-10
        near(f,77.5,'FCFF'); near(e/100,8.2,'share value')
        return {'fcff':f,'equity':e,'price':e/100,'benchmark':'lessons/week-02/starter/mini_case.csv'}
    record('Official Week2 FCFF and bridge','Units and senior-claim signs',bridge_fixture)
    record('Historical source reconciliations','Income, balance sheets and cash reconciliation across filings',lambda:historical_checks(d))
    def definition():
        b=d['history']['BS_Jul26']; near(b['cash']+b['debt_securities'],56586,'cash/debt securities')
        near(b['equity_securities'],42783,'equities are not cash')
        near(b['debt_current']+b['debt_long'],33366,'carrying debt')
        near(d['market']['debt_fair_value'],31400,'fair value debt')
        near(d['market']['risk_free'],.0495,'Treasury 10-year column')
        return {'evidence':'Issuer Q2 release BS independently compared with 10-Q BS/Notes5,10,11; Treasury Sep10 10Yr (not real yield)',
                'cash_like':56586,'marketable_equity_excluded':42783,'book_debt':33366,'fair_debt':31400,'risk_free':.0495}
    record('Independent source / definition check','Prevent cash-label, debt-basis and interest-rate-column contamination',definition)
    def statements():
        rows=[y for case in d['cases'] for y in forecast(d,case)]
        for name in ('margin_minus_2pp','dc_growth_minus_5pp'):
            rows+=all_results(d)['what_if'][name]['forecast']
        return {'years':len(rows),'maximum_error_millions':max(abs(v) for y in rows for v in y['checks'].values()),
                'no_plug':'Cash from cash flow; equity from retained earnings; minimum cash enforced'}
    record('25 forecast statement articulations','Every causal case and named what-if',statements)
    def directional():
        w=wacc_build(d)['wacc']; old=valuation(d); new=valuation(d,wacc=w+.01)
        assert new['per_share']<old['per_share'] and new['enterprise_value']<old['enterprise_value']
        return {'prediction':'evidence/directional-test-precommit.md (AI-authored; not human lock)',
                'old_wacc':w,'new_wacc':w+.01,'old_price':old['per_share'],'new_price':new['per_share'],
                'expected_direction':'lower','actual_direction':'lower','old_action':old['action'],'new_action':new['action'],
                'decision_effect':'Deferral persists because price remains above the base entry ceiling; discount-rate risk strengthens caution'}
    record('Prewritten directional changed input','Expected and actual valuation/action effect',directional)
    def monotonic():
        w=wacc_build(d)['wacc']
        for g in [.01,.02,.03,.04]:
            p=[valuation(d,wacc=r,growth=g)['per_share'] for r in [w-.02,w-.01,w,w+.01,w+.02]]
            assert all(a>b for a,b in zip(p,p[1:])),p
        for r in [w-.02,w,w+.02]:
            p=[valuation(d,wacc=r,growth=g)['per_share'] for g in [.01,.02,.03,.04]]
            assert all(a<b for a,b in zip(p,p[1:])),p
        return 'Higher WACC lowers value; higher g raises it even after terminal reinvestment; full bridge recomputed'
    record('WACC / growth monotonicity','Test expected direction over 32 admissible comparisons',monotonic)
    def boundary():
        return [rejects(lambda:dcf_cashflows([100]*5,.10,.10),'g < WACC'),
                rejects(lambda:dcf_cashflows([100]*5,10,.03),'decimal'),
                rejects(lambda:valuation(d,growth=.25),'ROIC')]
    record('Invalid terminal / units rejected','Fail loudly rather than create infinite value',boundary)
    def economic_bridge():
        r=valuation(d); near(r['equity_value'],r['enterprise_value']+sum(r['bridge'].values()),'bridge')
        near(r['per_share']*d['market']['shares'],r['equity_value'],'per share')
        bigger=copy.deepcopy(d); bigger['market']['shares']*=1.02
        assert valuation(bigger)['per_share']<r['per_share']
        return {'equity':r['equity_value'],'dilution_test':'2% more shares lowers value; dividend cash also recomputed'}
    record('EV / equity / share bridge','No duplicate non-operating investments, debt at fair value',economic_bridge)
    def broken():
        bad=copy.deepcopy(d); bad['history']['BS_Jul26']['equity_securities']+=1
        result=rejects(lambda:historical_checks(bad),'assets')
        cash=copy.deepcopy(d); cash['common']['new_investments'][0]=1e7
        return [result,rejects(lambda:forecast(cash),'cash below floor')]
    record('Corrupt source / liquidity failure injection','Highest-risk classification and unsupported financing cannot silently pass',broken)
    def contamination():
        b=opening(d); correct=valuation(d); portfolio=b['public_investments']+b['private_investments']
        rev0=ltm(d)['revenue']; prior=portfolio; extra=[]
        for y in correct['forecast']:
            wrong=portfolio*y['income_statement']['revenue']/rev0
            extra.append(wrong-prior); prior=wrong
        ev_drag=sum(z/(1+correct['wacc'])**t for z,t in zip(extra,correct['discount_times']))
        assert ev_drag>0
        return {'financial_portfolio_excluded_from_nwc':portfolio,'wrong_scaling_explicit_ev_drag':ev_drag,
                'minimum_wrong_price_drag':ev_drag/d['market']['shares'],
                'diagnosis':'Repeats the Lab10/11 investment-classification failure; false operating reinvestment is not economic capex'}
    record('Highest-risk investment contamination experiment','Quantify the prior-lab error rather than trust a balancing model',contamination)
    def signed():
        full=dcf_cashflows([-100,100,100,100,100],.10,.03)
        dropped=dcf_cashflows([0,100,100,100,100],.10,.03)
        near(dropped['enterprise_value']-full['enterprise_value'],100/1.1,'signed negative FCFF preserved')
        return 'Negative year1 FCFF reduces EV by90.9091; no nonpositive-flow filter'
    record('Signed cash-flow regression','Reject the old practice of dropping negative forecast flows',signed)
    def sbc():
        b=valuation(d); addback=ltm(d)['sbc']; require_cost=all('cash replacement' in d['common']['stock_compensation'] for _ in [0])
        assert require_cost
        wrong=sum(addback/(1+b['wacc'])**t for t in b['discount_times'])/d['market']['shares']
        assert wrong>0
        return {'cost_treatment':'SBC expense retained, cash substitute, no addback, fixed shares',
                'minimum_wrong_five_year_value_inflation_per_share':wrong,'warning':'Terminal inflation would make the full error larger'}
    record('SBC free-cash-flow overstatement challenge','Economic cost retained; quantified intentionally wrong addback',sbc)
    def peer():
        p=comparables(d)
        for x in p['peers']:
            near(x['ev_annual_sales']*x['annual_revenue'],x['enterprise_value_proxy'],'EV/sales')
            near(x['pe_annual_gaap']*x['annual_eps'],x['price'],'P/E')
            assert x['price_date']=='2026-09-10' and x['annual_publication']<='2026-09-10' and x['quarter_publication']<='2026-09-10'
        for x,price in zip(p['peers'],p['ev_sales_implied_prices']):
            near(price*d['market']['shares']-p['comparison_cash_less_book_debt_bridge'],x['ev_annual_sales']*d['history']['FY26']['revenue'],'same comparison EV convention backsolve')
        return {'policy':'Retained from Lab8; AMD use / AVGO qualify before new multiple calculations',
                'annual_gaap_only':True,'no_lease_debt':'Operating leases treated as operating in all EV calculations'}
    record('Peer policy and consistent definitions','Dates, fiscal-period limits and EV/equity definitions',peer)
    def risk():
        r=all_results(d); assert r['cases']['low']['per_share']<r['cases']['base']['per_share']<r['cases']['high']['per_share']
        assert r['cases']['low']['action']=='DO NOT INITIATE'
        assert r['cases']['base']['action']=='WATCH / DEFER'
        low=r['cases']['low']; claim=d['cases']['low']['guarantee_claim']; start=d['cases']['low']['claim_year']
        cash_after_call=min(y['cash_flow']['cash_end']-claim for i,y in enumerate(low['forecast'],1) if i>=start)
        assert cash_after_call>=d['common']['minimum_cash']
        return {'base_action':r['cases']['base']['action'],'downside_action':r['cases']['low']['action'],
                'minimum_low_case_cash_after_hypothetical_year3_claim':cash_after_call,
                'cause':'Demand/collection/margin deterioration plus guarantee losses breaches the risk gate',
                'reverse_dc_shift':r['reverse_dcf']['constant_increment_to_each_dc_growth']}
    record('Highest-risk causal downside and reverse DCF','Limitation changes action; market expectation solves within bracket',risk)
    return {'status':'PASS' if all(t['status']=='PASS' for t in tests) else 'FAIL','tests':tests,
            'human_evidence_status':'INCOMPLETE: genuine human AI-off locked prediction and observed recording/transcripts not provided'}
