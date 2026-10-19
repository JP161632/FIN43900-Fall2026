"""Offline NVIDIA three-statement / FCFF engine. All dollars and shares in millions."""
import copy
import datetime as dt
import math
import statistics


class ModelError(ValueError):
    pass


def require(test, message):
    if not test:
        raise ModelError(message)


def near(a, b, name, tolerance=1e-6):
    require(abs(a-b) <= tolerance, f'{name}: {a} != {b}')


def ltm(d):
    h=d['history']
    return {k:h['FY26'][k]+h['H1FY27'][k]-h['H1FY26'][k]
            for k in h['FY26'] if k in h['H1FY27'] and k not in ('cash_start','cash_end')}


def elapsed(d):
    a=dt.date.fromisoformat(d['identity']['financial_date'])
    b=dt.date.fromisoformat(d['identity']['valuation_date'])
    days=(b-a).days
    require(0<=days<365, 'Valuation must follow the financial date by less than a year')
    return days/365


def historical_checks(d):
    h=d['history']; errors=[]
    for name in ('FY26','H1FY26','H1FY27'):
        y=h[name]
        for a,b,label in [(y['revenue']-y['cost'],y['gross_profit'],'gross profit'),
                           (y['gross_profit']-y['rd']-y['sga'],y['ebit'],'EBIT'),
                           (y['ebit']+y['nonoperating'],y['pretax'],'pretax'),
                           (y['pretax']-y['tax'],y['net_income'],'net income'),
                           (y['cash_start']+y['cfo']+y['cfi']+y['cff'],y['cash_end'],'cash')]:
            near(a,b,name+' '+label); errors.append(a-b)
    for name in ('BS_Jan26','BS_Jul26'):
        b=h[name]
        assets=sum(b[k] for k in ('cash','debt_securities','equity_securities','ar','inventory','prepaid','ppe','rou','goodwill','intangibles','dta','private_investments','other_assets'))
        liabilities=sum(b[k] for k in ('ap','accrued','debt_current','debt_long','lease_long','other_liabilities'))
        near(assets,b['assets'],name+' assets'); near(liabilities,b['liabilities'],name+' liabilities')
        near(assets,liabilities+b['equity'],name+' balance')
    return {'income_cash_periods':3,'balance_dates':2,'max_income_cash_error':max(map(abs,errors))}


def wacc_build(d):
    m=d['market']; tax=d['common']['tax_rate']
    equity=m['price']*m['shares']; debt=m['debt_fair_value']
    ke=m['risk_free']+m['beta']*m['equity_risk_premium']
    kd=m['risk_free']+m['debt_spread']; dw=debt/(equity+debt)
    return {'risk_free':m['risk_free'],'beta_assumption':m['beta'],'erp_assumption':m['equity_risk_premium'],
            'cost_equity':ke,'pretax_cost_debt':kd,'market_debt_weight':dw,
            'equity_weight':1-dw,'tax_rate':tax,'wacc':ke*(1-dw)+kd*(1-tax)*dw}


def opening(d):
    h=d['history']; b=h['BS_Jul26']; pieces=h['other_assets_investments']
    out={k:b[k] for k in ('cash','debt_securities','ar','inventory','prepaid','ppe','rou','goodwill','intangibles','dta','equity')}
    out.update(public_investments=b['equity_securities']+pieces['locked_public'],
               private_investments=b['private_investments']+pieces['equity_method_rounded']+pieces['derivatives'],
               other_operating_assets=b['other_assets']-sum(pieces.values()),ap=b['ap'],
               operating_accruals=b['accrued']-h['groq_consideration']+b['other_liabilities'],
               purchase_consideration=h['groq_consideration'],debt=b['debt_current']+b['debt_long'],lease_long=b['lease_long'])
    return out


ASSETS=('cash','debt_securities','public_investments','private_investments','ar','inventory','prepaid','ppe','rou','goodwill','intangibles','dta','other_operating_assets')
LIABILITIES=('ap','operating_accruals','purchase_consideration','debt','lease_long')


def totals(b):
    return sum(b[k] for k in ASSETS),sum(b[k] for k in LIABILITIES)


def nwc(b):
    return b['ar']+b['inventory']+b['prepaid']+b['other_operating_assets']-b['ap']-b['operating_accruals']


def forecast(d,case='base',growth_shift=0,margin_shift=0):
    require(case in d['cases'],'Unknown case')
    c=d['cases'][case]; x=d['common']; b=opening(d); result=[]; base=ltm(d)
    require(d['market']['shares']>0,'Diluted shares must be positive')
    for name in ('tax_rate','rd_ratio','sga_gp_ratio','capex_ratio','ppe_depreciation'):
        require(0<=x[name]<1,f'{name} must be a decimal rate between zero and one')
    require(x['capex_ratio']>0 and x['minimum_cash']>=0,'Capex must be positive and cash floor nonnegative')
    require(all(len(c[k])==5 for k in ('data_center_growth','edge_growth','gross_margin','risk_charge')),'Five annual case driver values required')
    require(c['dso']>0 and c['inventory_days']>0 and c['dpo']>0,'Working-capital days must be positive')
    dc=base['data_center']; edge=base['revenue']-dc
    for i in range(5):
        prev=copy.deepcopy(b)
        dc*=1+c['data_center_growth'][i]+growth_shift
        edge*=1+c['edge_growth'][i]
        revenue=dc+edge; gm=c['gross_margin'][i]+margin_shift
        require(revenue>0 and 0<gm<1,'Invalid revenue or margin')
        cost=revenue*(1-gm); gp=revenue-cost
        retention=d['history']['pending_retention_cash_substitute'] if i==0 else 0
        acquisition=d['history']['pending_acquisition_cash'] if i==0 else 0
        rd=revenue*x['rd_ratio']; sga=gp*x['sga_gp_ratio']+retention; charge=c['risk_charge'][i]
        ebit=gp-rd-sga-charge; interest=prev['debt']*(d['market']['risk_free']+d['market']['debt_spread'])
        pretax=ebit-interest; tax=max(pretax,0)*x['tax_rate']; ni=pretax-tax
        dep=prev['ppe']*x['ppe_depreciation']; amort=min(x['amortization'][i],prev['intangibles']); da=dep+amort
        capex=revenue*x['capex_ratio']
        b['ar']=revenue*c['dso']/365; b['inventory']=cost*c['inventory_days']/365
        b['ap']=cost*c['dpo']/365; b['prepaid']=revenue*x['prepaid_ratio']
        b['other_operating_assets']=revenue*x['other_operating_assets_ratio']
        b['operating_accruals']=revenue*x['operating_accrual_ratio']
        b['ppe']=prev['ppe']+capex-dep; b['intangibles']=prev['intangibles']-amort
        delta_nwc=nwc(b)-nwc(prev)
        cfo=ni+da-delta_nwc
        investment=x['new_investments'][i]; b['private_investments']+=investment
        cfi=-capex-investment-acquisition
        b['goodwill']+=acquisition  # Illustrative unallocated acquisition asset; zero incremental operating benefit.
        groq=prev['purchase_consideration'] if i==0 else 0
        b['purchase_consideration']-=groq
        dividends=d['market']['shares']*x['dividend_per_share']; cff=-dividends-x['buybacks']-groq
        delta_cash=cfo+cfi+cff; b['cash']=prev['cash']+delta_cash
        b['equity']=prev['equity']+ni-dividends-x['buybacks']
        a,l=totals(b)
        # Cash follows the CF statement and equity follows retained income: neither is a balancing plug.
        near(a,l+b['equity'],f'{case} year{i+1} balance')
        near(b['cash']-prev['cash'],cfo+cfi+cff,f'{case} year{i+1} cash')
        require(b['cash']>=x['minimum_cash'],f'{case} year{i+1} cash below floor; explicit funding needed')
        nopat=ebit*(1-x['tax_rate']); fcff=nopat+da-capex-delta_nwc
        # With positive taxable income, levered CFO plus after-tax interest must reproduce FCFF.
        near(fcff,cfo+interest*(1-x['tax_rate'])-capex,'FCFF from CFO')
        result.append({'year':2027+i,'period_end':f'{2027+i}-07-26','data_center_revenue':dc,'edge_revenue':edge,
            'income_statement':{'revenue':revenue,'cost_of_revenue':cost,'gross_profit':gp,'rd':rd,'sga':sga,
                'risk_charge':charge,'retention_included_in_sga':retention,'ebit':ebit,'interest_expense':interest,'pretax_income':pretax,'tax':tax,'net_income':ni},
            'balance_sheet':dict(b,total_assets=a,total_liabilities=l),
            'cash_flow':{'net_income':ni,'depreciation_amortization':da,'delta_operating_nwc':delta_nwc,
                'cfo':cfo,'capex':capex,'financial_investment_purchases':investment,'acquisition_cash':acquisition,'cfi':cfi,'dividends':dividends,
                'purchase_consideration_paid':groq,'buybacks':x['buybacks'],'cff':cff,'cash_start':prev['cash'],
                'cash_change':delta_cash,'cash_end':b['cash']},
            'fcff':fcff,'nopat':nopat,'checks':{'balance_error':a-l-b['equity'],
                'cash_error':b['cash']-prev['cash']-cfo-cfi-cff,'equity_error':b['equity']-prev['equity']-ni+dividends+x['buybacks']}})
    return result


def dcf_cashflows(flows,wacc,growth,terminal_cf=None,times=None):
    require(math.isfinite(wacc) and math.isfinite(growth) and 0<=growth<wacc,'Require 0 <= g < WACC')
    require(wacc<1,'WACC must be a decimal below 1')
    require(len(flows)>0 and all(math.isfinite(v) for v in flows),'Invalid cash flows')
    times=times or list(range(1,len(flows)+1))
    require(len(times)==len(flows) and all(t>0 for t in times),'Invalid discount dates')
    terminal_cf=flows[-1]*(1+growth) if terminal_cf is None else terminal_cf
    require(terminal_cf>0,'Nonpositive terminal cash flow')
    pv=[v/(1+wacc)**t for v,t in zip(flows,times)]
    tv=terminal_cf/(wacc-growth); tvpv=tv/(1+wacc)**times[-1]
    ev=sum(pv)+tvpv
    return {'enterprise_value':ev,'pv_explicit':sum(pv),'pv_cashflows':pv,'terminal_value':tv,
            'pv_terminal':tvpv,'terminal_share':tvpv/ev,'terminal_fcff':terminal_cf,'discount_times':times}


def valuation(d,case='base',wacc=None,growth=None,growth_shift=0,margin_shift=0):
    c=d['cases'][case]; rows=forecast(d,case,growth_shift,margin_shift); e=elapsed(d)
    w=wacc_build(d)['wacc']+c['wacc_shift'] if wacc is None else wacc
    g=c['terminal_growth'] if growth is None else growth; roic=c['terminal_roic']
    require(0<=g<roic,'Terminal growth must be below terminal ROIC')
    # Terminal NOPAT grows at g; reinvestment = g/ROIC, rather than free perpetual growth.
    terminal=rows[-1]['nopat']*(1+g)*(1-g/roic)
    flows=[r['fcff'] for r in rows]
    retention=d['history']['pending_retention_cash_substitute']*(1-d['common']['tax_rate'])
    flows[0]=(flows[0]+retention)*(1-e)-retention  # Pending retention not incurred before valuation.
    r=dcf_cashflows(flows,w,g,terminal,[i+1-e for i in range(5)])
    b=opening(d); first=rows[0]['cash_flow']
    rollcash=b['cash']+e*(first['cash_change']+first['acquisition_cash']+retention)
    public=b['public_investments']*c['public_recovery']
    private=(b['private_investments']+e*first['financial_investment_purchases'])*c['private_recovery']
    # Future financial investments are assumed worth cost upon purchase; no operating FCFF or speculative return.
    # Haircut on future purchases is charged once as a separate negative NPV, not operating capex.
    future_loss=sum(v*(1-c['private_recovery'])*(1-e if i==0 else 1)/(1+w)**(i+1-e)
                    for i,v in enumerate(d['common']['new_investments']))
    guarantee=c['guarantee_claim']/(1+w)**(c['claim_year']-e)
    bridge={'rolled_cash':rollcash,'debt_securities':b['debt_securities'],
            'less_operating_cash':-d['market']['operating_cash'],'less_cash_tax_reserve':-d['market']['cash_tax_reserve'],
            'public_investments_net':public,'private_other_investments_net':private,
            'less_debt_fair_value':-d['market']['debt_fair_value'],
            'less_purchase_consideration':-d['history']['groq_consideration']*(1-e),
            'less_future_investment_loss_pv':-future_loss,'less_guarantee_claim_pv':-guarantee,
            'less_pending_acquisition_cash_pv':-d['history']['pending_acquisition_cash']/(1+w)**(1-e)}
    equity=r['enterprise_value']+sum(bridge.values()); price=equity/d['market']['shares']
    require(equity>0,'Equity is nonpositive')
    entry=price*(1-d['market']['entry_discount'])
    action=('DO NOT INITIATE' if c['risk_gate'] else 'INITIATE CONDITIONALLY' if d['market']['price']<=entry else 'WATCH / DEFER')
    r.update(case=case,wacc=w,growth=g,terminal_roic=roic,bridge=bridge,equity_value=equity,
             diluted_shares=d['market']['shares'],per_share=price,entry_ceiling=entry,action=action,
             forecast=rows,stub_fraction=e,stub_note='Uniform within-year CF roll-forward assumption, not a reported September balance sheet')
    near(equity,r['enterprise_value']+sum(bridge.values()),'EV to equity')
    return r


def comparables(d):
    peers=[]
    for p in d['peers']:
        cap=p['price']*p['diluted_shares']; ev=cap+p['debt']-p['cash']-p['debt_securities']
        peers.append(dict(p,market_cap_proxy=cap,enterprise_value_proxy=ev,
                          ev_annual_sales=ev/p['annual_revenue'],pe_annual_gaap=p['price']/p['annual_eps']))
    pe=statistics.median(p['pe_annual_gaap'] for p in peers)
    sales=statistics.median(p['ev_annual_sales'] for p in peers)
    v=valuation(d); eps=d['history']['FY26']['diluted_eps']
    subject_ev=d['market']['price']*d['market']['shares']+d['history']['BS_Jul26']['debt_current']+d['history']['BS_Jul26']['debt_long']-d['history']['BS_Jul26']['cash']-d['history']['BS_Jul26']['debt_securities']
    comparison_bridge=d['history']['BS_Jul26']['cash']+d['history']['BS_Jul26']['debt_securities']-d['history']['BS_Jul26']['debt_current']-d['history']['BS_Jul26']['debt_long']
    return {'policy_record':'evidence/peer-policy.md','peers':peers,'median_pe':pe,'median_ev_sales':sales,
        'subject_pe_annual_gaap':d['market']['price']/eps,'subject_ev_annual_sales':subject_ev/d['history']['FY26']['revenue'],
        'comparison_cash_less_book_debt_bridge':comparison_bridge,
        'pe_implied_prices':[p['pe_annual_gaap']*eps for p in peers],
        'median_pe_implied_price':pe*eps,
        'ev_sales_implied_prices':[(p['ev_annual_sales']*d['history']['FY26']['revenue']+comparison_bridge)/d['market']['shares'] for p in peers],
        'warning':'Same-date unadjusted closes; latest-quarter diluted share proxies and financial bridges; latest ANNUAL GAAP earnings/sales for every name. Fiscal years differ and are stale versus AI growth. Not a TTM, forward or clean pure-play valuation.'}


def all_results(d):
    historical_checks(d); cases={k:valuation(d,k) for k in d['cases']}; w=wacc_build(d)['wacc']
    sensitivity=[{'wacc':wr,'growth':g,'per_share':valuation(d,wacc=wr,growth=g)['per_share']}
                 for wr in [w-.01,w,w+.01] for g in [.02,.03,.04]]
    lo,hi=-.15,.50; target=d['market']['price']
    for _ in range(70):
        mid=(lo+hi)/2
        if valuation(d,growth_shift=mid)['per_share']<target: lo=mid
        else: hi=mid
    shift=(lo+hi)/2
    reverse=valuation(d,growth_shift=shift)
    require(abs(reverse['per_share']-target)<1e-6,'Reverse DCF failed to bracket price')
    return {'identity':d['identity'],'market':d['market'],'historical_checks':historical_checks(d),
        'ltm':ltm(d),'wacc_build':wacc_build(d),'cases':cases,'sensitivity':sensitivity,
        'reverse_dcf':{'constant_increment_to_each_dc_growth':shift,'implied_dc_growth_path':[v+shift for v in d['cases']['base']['data_center_growth']],
                       'year5_revenue':reverse['forecast'][-1]['income_statement']['revenue'],'matched_price':reverse['per_share'],
                       'held_fixed':'All other base operating, terminal, capital structure and bridge assumptions'},
        'what_if':{'demand_financing_downside':cases['low'],
                   'margin_minus_2pp':valuation(d,margin_shift=-.02),
                   'dc_growth_minus_5pp':valuation(d,growth_shift=-.05)},'comparables':comparables(d)}
