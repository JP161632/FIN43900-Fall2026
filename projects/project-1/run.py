"""Execute the offline project; fail nonzero on any financial validation failure."""
import argparse
import datetime as dt
import html
import json
from pathlib import Path
from model import ASSETS,LIABILITIES,ModelError,all_results,valuation
from tests import validate

ROOT=Path(__file__).resolve().parent


def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')


def table(headers,rows):
    return '\n'.join(['| '+' | '.join(map(str,headers))+' |','|'+'|'.join(['---']*len(headers))+'|']+
                     ['| '+' | '.join(map(str,row))+' |' for row in rows])


def money(v): return f'{v:,.2f}'


def visible(d,r,v):
    cases=r['cases']; b=cases['base']; m=d['market']; h=d['history']; x=d['common']
    out=['# NVIDIA - executed investment decision',
        f"Historical valuation: **{d['identity']['valuation_date']} US close**, prepared {d['identity']['prepared']}. USD millions except shares (millions) and USD/share. Intended user: buy-side committee, no existing position; 12-24 month decision horizon.",
        f"**{b['action']}** at ${m['price']:.2f}. Causal intrinsic range ${cases['low']['per_share']:.0f}-${cases['high']['per_share']:.0f}; base reference ${b['per_share']:.0f}. These are assumptions, not probability-weighted targets. Entry ceiling with 20% margin of safety: ${b['entry_ceiling']:.0f}, subject to evidence gates.",
        'No post-September10 fact is used in the valuation. October19 is the build/review date. Read data/source-map.md and evidence/assumption-challenges.md for definitions and evidence that changes each driver.',
        '## Causal cases',table(['Case','Year1 / Year5 sales','WACC / g','EV','Equity','USD/share','TV share','Action'],
            [[k,f"{money(y['forecast'][0]['income_statement']['revenue'])} / {money(y['forecast'][-1]['income_statement']['revenue'])}",
              f"{y['wacc']:.2%} / {y['growth']:.1%}",money(y['enterprise_value']),money(y['equity_value']),f"{y['per_share']:.2f}",f"{y['terminal_share']:.1%}",y['action']] for k,y in cases.items()]),
        'Low: deployment/financing slowdown, weaker margin, longer collections, excess inventory, $10bn supply charge and $25bn guarantee-call assumption. Base: strong DC growth fading with competition. High: sustained platform adoption, execution and collection improvement. Scenario claims are analyst assumptions, not issuer guidance.',
        '## Historical facts and normalization',table(['Item','FY26','H1FY26','H1FY27','LTM July26'],
            [[k]+[money(h[p][k]) for p in ['FY26','H1FY26','H1FY27']]+[money(r['ltm'][k])] for k in ['revenue','ebit','net_income','cfo','capex','da','sbc','investment_gains']]),
        'LTM = FY26 + H1FY27 - H1FY26. The $4.32bn net H20 charge is an annual normalization only: FY26 reported EBIT130,387 -> normalized134,707 and GM73.07%. It rolls out of the LTM comparator; no second LTM addback. Investment markups/interest are excluded from operating EBIT/FCFF. Latest-quarter platform presentation is recast; annual legacy Gaming labels are not combined with recast Edge categories.',
        f"Share proxy = July26 period-end basic24,147 + Q2 incremental dilution95 = {m['shares']:,}. Annual diluted weighted-average24,514 is used only in historical EPS. Forecast SBC is replaced by equal cash compensation; expense retained, no addback and no forecast dilution benefit. Additional 2% dilution is tested.",
        '## WACC construction',table(['Component','Value'],[[k,f'{z:.6f}'] for k,z in r['wacc_build'].items()]),
        'Risk-free4.95% is Treasury Sep10 nominal10-year. Beta1.8, ERP5%, debt spread1% are explicit assumptions (not current provider estimates). Market equity uses diluted proxy * price, debt uses filing fair value31,400. Operating leases stay operating; rent in cost forecast, no second lease-debt deduction.',
        '## Enterprise to common equity - base',table(['Bridge component','USD millions'],[['Enterprise value',money(b['enterprise_value'])]]+[[k,money(z)] for k,z in b['bridge'].items()]+[['Common equity',money(b['equity_value'])],['Diluted proxy shares',money(m['shares'])],['USD/share',f"{b['per_share']:.2f}"]]),
        f"Financial date July26 precedes valuation by {b['stub_fraction']*365:.0f} days. Uniform within-year cash-flow interpolation rolls cash and purchases to September10; first FCFF is reduced by elapsed fraction. Dates to remaining payments: {', '.join(f'{t:.6f}' for t in b['discount_times'])} years. No interim reported balance sheet is implied. Test residual timing risk before trading.",
        'Public investments:42,783+4,957 locked holdings; base90% recovery. Private/other:51,157+3,300 rounded equity-method+824 derivatives; base50% recovery. These haircuts include tax/illiquidity/realization uncertainty; not precision tax estimates. Future committed equity investments25,000 are financing assets in CFI, not operating NWC/capex; cost/recovery shortfall has a separate negative-PV bridge, once. Debt33,366 carrying versus31,400 fair value. Groq986 consideration is a separate claim. Cash reserve10,000 and foreign-cash tax reserve1,700 are withheld.',
        '## Base five-year income statement',table(['USD millions']+[y['period_end'] for y in b['forecast']],
            [[k]+[money(y['income_statement'][k]) for y in b['forecast']] for k in b['forecast'][0]['income_statement']]),
        '## Base five-year balance sheet',table(['USD millions']+[y['period_end'] for y in b['forecast']],
            [[k]+[money(y['balance_sheet'][k]) for y in b['forecast']] for k in list(ASSETS)+list(LIABILITIES)+['equity','total_assets','total_liabilities']]),
        '## Base five-year cash flow and FCFF',table(['USD millions']+[y['period_end'] for y in b['forecast']],
            [[k]+[money(y['cash_flow'][k]) for y in b['forecast']] for k in b['forecast'][0]['cash_flow']]+[['FCFF']+[money(y['fcff']) for y in b['forecast']]]),
        'FCFF = EBIT*(1-tax) + D&A - operating capex - change in operating NWC. CFO + interest*(1-tax) - capex independently agrees. Dividends, buybacks and financial investments are excluded from FCFF. Cash is calculated from CFO+CFI+CFF; equity from retained earnings. No balancing equity plug. Full signed statements for all cases are in results.json.',
        'Pending Hugging Face: September3 8-K discloses ~11,900 purchase consideration and up to1,000 equity retention, closing expected first half2027. Forecast assumes cash purchase11,900 and cash-equivalent retention1,000 in year1, no incremental revenue/synergies. Purchase cash is CFI; separate discounted bridge claim prevents treating acquisition as free. Retention cost is in SGA/FCFF once. Unallocated acquired assets are shown in goodwill as an illustrative purchase-allocation placeholder, not a GAAP purchase-price allocation. Closing/cancellation/allocation require a model revision. Neither pending payment is interpolated into elapsed pre-valuation cash.',
        '## Terminal convention',f"Year6 normalized FCFF = Year5 NOPAT*(1+g)*(1-g/ROIC) = {money(b['terminal_fcff'])}. Base terminal ROIC25%, g3%; reinvestment12% of NOPAT. D&A equals maintenance capex in steady state; incremental operating investment is g/ROIC. This deliberately replaces year5 growth reinvestment with a mature steady state; TV share {b['terminal_share']:.1%} requires caution.",
        '## WACC-growth sensitivity',table(['WACC','g','USD/share'],[[f"{z['wacc']:.3%}",f"{z['growth']:.1%}",f"{z['per_share']:.2f}"] for z in r['sensitivity']]),
        '## Market-implied expectation',f"Holding all other base assumptions fixed, ${m['price']:.2f} implies adding {r['reverse_dcf']['constant_increment_to_each_dc_growth']*100:.2f} percentage points to EACH of the five DC growth rates: {', '.join(f'{z:.1%}' for z in r['reverse_dcf']['implied_dc_growth_path'])}. Implied year5 total revenue {money(r['reverse_dcf']['year5_revenue'])}. One conditional solution, not a unique market forecast.",
        '## Comparable companies',r['comparables']['warning'],table(['Peer','P/E annual GAAP','EV/annual sales','Balance date','Share basis'],
            [[z['ticker'],f"{z['pe_annual_gaap']:.2f}x",f"{z['ev_annual_sales']:.2f}x",z['balance_date'],f"Q diluted {z['diluted_shares']:,}"] for z in r['comparables']['peers']]),
        f"NVIDIA on the same comparison convention: annual GAAP P/E {r['comparables']['subject_pe_annual_gaap']:.2f}x; EV/annual sales {r['comparables']['subject_ev_annual_sales']:.2f}x. P/E target cross-check ${min(r['comparables']['pe_implied_prices']):.0f}-${max(r['comparables']['pe_implied_prices']):.0f}; EV/sales target cross-check ${min(r['comparables']['ev_sales_implied_prices']):.0f}-${max(r['comparables']['ev_sales_implied_prices']):.0f}. Do not average these with DCF. Annual earnings lag explosive growth, AMD has lower margins, and AVGO includes software. Two peers cannot establish a stable fair multiple; leave-one-out exposes the endpoint spread. See policy and transaction exclusions.",
        'Peer EV/annual-sales backsolve uses the SAME narrow cash/debt-securities-minus-BOOK-debt bridge as each comparison numerator. Noncash equity holdings stay inside the broad comparison EV for all names; they are not added again. This proxy comparison is not the separately adjusted operating EV used in DCF. No DCF-specific investment/claim adjustment is silently applied to a peer proxy.',
        '## Named what-if outcomes',table(['Scenario','USD/share','Action'],[[k,f"{z['per_share']:.2f}",z['action']] for k,z in r['what_if'].items()]),
        '## Monitoring and reversal',
        'Revisit after each filing. Initiation requires price below the base entry ceiling AND evidence that 75-day collection, 125-day inventory, margin>=72%, and cash compensation economics are sustainable; refresh all market facts before trade. Failure conditions: sustained DC growth below20%, DSO>95 days, GM<70%, or material guarantee calls/capacity losses -> DO NOT INITIATE. Faster durable DC growth with collections and margins intact can justify revising toward high case. Supply commitments279bn are not customer backlog. $105bn SB Energy guarantee cap and $56bn additional cloud/third-party lease commitments are exposures, not certain present debt; scenario expected losses require review.',
        '## Validation and submission status',f"Engine validation: **{v['status']}**, {sum(z['status']=='PASS' for z in v['tests'])}/{len(v['tests'])} tests. Read validation-results.json for observed outcomes.",
        'Student-confirmed peer challenge is documented in evidence/partner-review-record.md; three videos/transcripts are supplied. Still unresolved: original EditionA PDF/first Brightspace receipt, completed locked-input exercise, and audio/timestamp checks. Student prediction is preserved before the new terminal-growth run; exact new rate/action are pending. This package does not claim a full score or Brightspace submission.']
    return '\n\n'.join(out)+'\n'


def dashboard(r):
    payload=json.dumps(r).replace('</','<\\/')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NVIDIA Project 1</title>
<style>body{font:17px/1.5 system-ui;margin:32px auto;padding:0 24px;max-width:1150px;background:#f2f6f9;color:#102a40}header,section{background:white;padding:24px;margin:20px 0;border-radius:10px}h1{margin:0}select{font:inherit;padding:8px}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:9px;border-bottom:1px solid #ccd4dc;text-align:right}td:first-child,th:first-child{text-align:left}.cards{display:flex;gap:35px;flex-wrap:wrap}.value{font-size:32px;font-weight:bold;color:#225c30}.note{color:#40566a}a{color:#07599a}</style>
<header><h1>NVIDIA | Investment committee</h1><p>Historical valuation: September 10, 2026 US close · USD · no current position</p><p><a href="visible-output.md">Visible report and statements</a> · <a href="../Decision-Memo.pdf">Memo</a> · <a href="../evidence/assumption-challenges.md">Driver challenges</a> · <a href="validation-results.json">Validation results</a></p></header>
<section><label>Choose causal case <select id="case"><option>base</option><option>low</option><option>high</option></select></label><div class="cards" id="cards"></div><p id="story"></p><p class="note">Low changes growth, margin, collections, inventory, asset recovery, discount rate and commitment losses together. This selector displays executed model results; it does not fetch live prices.</p></section>
<section><h2>Enterprise to common equity</h2><table id="bridge"></table></section>
<section><h2>Five rolling forecast years</h2><label>Statement <select id="statement"><option value="income_statement">Income statement</option><option value="balance_sheet">Balance sheet</option><option value="cash_flow">Cash flow</option></select></label><table id="statements"></table></section>
<section><h2>WACC–growth sensitivity | base</h2><table id="grid"></table><p>Terminal FCFF includes reinvestment at 25% terminal ROIC. Click a sensitivity row to compare with the base reference.</p><p id="picked"></p></section>
<section><h2>Reverse DCF and conditions</h2><p id="reverse"></p><p>WATCH / DEFER at $218.36. Consider initiation only below a 20% discount to the refreshed base estimate, with growth/collection/margin/commitment gates satisfied. Demand-financing downside: DO NOT INITIATE. Read the memo for monitoring triggers.</p><p>AI-assisted model; assumptions are judgments. Videos and attributed peer review are supplied; the human lock, original checkpoint and audio/timestamp evidence still need closure. <a href="../Student%20next%20steps.md">Student next steps and scripts</a></p></section>
<script>const R='''+payload+'''; const fmt=n=>Number(n).toLocaleString('en-US',{maximumFractionDigits:2});
function rows(head,rs){return '<tr>'+head.map(x=>'<th>'+x+'</th>').join('')+'</tr>'+rs.map(r=>'<tr>'+r.map(x=>'<td>'+x+'</td>').join('')+'</tr>').join('')}
function draw(){let name=document.querySelector('#case').value,v=R.cases[name],st=document.querySelector('#statement').value;
document.querySelector('#cards').innerHTML=[['USD/share','$'+fmt(v.per_share)],['Action',v.action],['Terminal share',fmt(v.terminal_share*100)+'%'],['Market','$218.36']].map(([a,b])=>'<div>'+a+'<div class="value">'+b+'</div></div>').join('');
document.querySelector('#story').textContent=name==='low'?'Deployment and financing slowdown; weaker margins; slower collections; excess inventory; supply and guarantee losses.':name==='high'?'Sustained platform adoption, stronger execution, improving collections and inventory.':'Strong Data Center demand fades as competition and infrastructure constraints rise.';
document.querySelector('#bridge').innerHTML=rows(['USD millions','Value'],[['Operating EV',fmt(v.enterprise_value)],...Object.entries(v.bridge).map(([k,z])=>[k,fmt(z)]),['Common equity',fmt(v.equity_value)],['Diluted shares',fmt(v.diluted_shares)]]);
let keys=Object.keys(v.forecast[0][st]);document.querySelector('#statements').innerHTML=rows(['USD millions',...v.forecast.map(y=>y.period_end)],keys.map(k=>[k,...v.forecast.map(y=>fmt(y[st][k]))]));}
document.querySelector('#case').onchange=draw;document.querySelector('#statement').onchange=draw;
document.querySelector('#grid').innerHTML=rows(['WACC','g','USD/share'],R.sensitivity.map(z=>[fmt(z.wacc*100)+'%',fmt(z.growth*100)+'%',fmt(z.per_share)]));
document.querySelectorAll('#grid tr').forEach((row,i)=>{if(i)row.onclick=()=>{let z=R.sensitivity[i-1];document.querySelector('#picked').textContent='Selected value $'+fmt(z.per_share)+' versus base $'+fmt(R.cases.base.per_share)+'. Base operating forecast held fixed; bridge PV claims recomputed.';}});
document.querySelector('#reverse').textContent='Market price implies '+fmt(R.reverse_dcf.constant_increment_to_each_dc_growth*100)+' additional percentage points in every DC growth rate, with other base assumptions fixed. Year5 sales: $'+fmt(R.reverse_dcf.year5_revenue)+' million.';draw();</script></html>'''


def main():
    p=argparse.ArgumentParser();p.add_argument('--all',action='store_true');p.add_argument('--output',type=Path,default=ROOT/'outputs')
    p.add_argument('--case',choices=['low','base','high'],default='base');p.add_argument('--wacc',type=float);p.add_argument('--growth',type=float)
    a=p.parse_args(); d=json.loads((ROOT/'data/inputs.json').read_text(encoding='utf-8'))
    changed=a.wacc is not None or a.growth is not None or a.case!='base'
    if changed:
        if a.output.resolve()==(ROOT/'outputs').resolve(): p.error('Changed runs require --output .build/<name> to protect frozen outputs')
        r=valuation(d,a.case,a.wacc,a.growth)
        write(a.output/'scenario.json',json.dumps(r,indent=2)+'\n')
        print(json.dumps({k:r[k] for k in ['case','wacc','growth','per_share','action']},indent=2)); return
    r=all_results(d); v=validate(d)
    for name,obj in [('results',r),('validation-results',v)]: write(a.output/f'{name}.json',json.dumps(obj,indent=2)+'\n')
    write(a.output/'visible-output.md',visible(d,r,v));write(a.output/'dashboard.html',dashboard(r))
    write(a.output/'run-receipt.json',json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':v['status'],'operator':'actual executor; command recorded separately'},indent=2)+'\n')
    print(f"NVIDIA: {v['status']} {sum(t['status']=='PASS' for t in v['tests'])}/{len(v['tests'])} tests; WATCH/DEFER; base ${r['cases']['base']['per_share']:.2f}; outputs: {a.output.name}")
    if v['status']!='PASS':
        for t in v['tests']:
            if t['status']=='FAIL': print(t['test'],t['result'])
        raise SystemExit(1)


if __name__=='__main__':
    try: main()
    except (ModelError,OSError,ValueError) as exc: raise SystemExit('FAIL: '+str(exc))
