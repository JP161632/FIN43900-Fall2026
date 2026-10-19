"""Reproduce all valuation output without fetching data or installing dependencies."""
import argparse
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import sys

from model import ModelError, all_results, valuation, validate_inputs
from tests import validate

ROOT=Path(__file__).resolve().parent


def money(x): return f"${x:,.2f}"
def pct(x): return f"{x*100:.2f}%"


def table(headers,rows):
    return "| "+" | ".join(headers)+" |\n|"+"|".join(["---"]*len(headers))+"|\n"+"\n".join("| "+" | ".join(str(x) for x in row)+" |" for row in rows)+"\n"


def report(r,v):
    b=r["cases"]["base"]
    out=["# Project 1 Salesforce executed valuation",f"Valuation: {r['valuation_date']} US close. USD millions; shares millions; prices USD per diluted share. Historical analysis, not a current October quote.",
         f"**Committee action: {r['decision']['action']}. Causal DCF range {money(r['decision']['valuation_range'][0])} to {money(r['decision']['valuation_range'][1])}.** Base diagnostic {money(b['per_share'])}; observed US common-share close {money(r['market']['price'])}. Do not average methods.",
         "Required human ownership evidence remains incomplete. See `STUDENT-ACTIONS.md` and `docs/rubric-audit.md`. This package does not claim a Salesforce AI-off baseline or a completed human locked prediction.",
         "## Material facts and normalized base",table(["Metric","Value","Basis"],[
             ["LTM revenue",f"{r['normalized_base']['reported_ltm']['revenue']:,.0f}","FY26 + H1FY27 - H1FY26"],
             ["Normalized revenue",f"{r['normalized_base']['revenue']:,.0f}","Informatica current run-rate annualization; analyst normalization"],
             ["Reported LTM EBIT",f"{r['normalized_base']['reported_ltm']['ebit']:,.0f}","filing arithmetic"],
             ["Normalized EBIT",f"{r['normalized_base']['normalized_ebit']:,.2f}","recurring restructuring reserve retained; SBC retained"],
             ["Cash + debt securities",f"{b['bridge']['cash_and_securities_july31']:,.0f}","July31 10-Q; gross, before operating cash"],
             ["Financial debt fair value",f"{b['bridge']['financial_debt_market']:,.0f}","senior notes30800 + term loan6000"],
             ["Finance leases",633,"separate senior claim; operating leases remain operating"],
             ["Diluted share proxy",824,"823 outstanding Aug20 + Q2 incremental1"],
             ["WACC",pct(b['wacc']),"market weights; Treasury4.67%, beta1.15 and ERP4.5% analyst assumptions"],
             ["Terminal g / ROIC",f"{pct(b['g'])} / 20%","perpetual reinvestment g/ROIC; no free-growth terminal"]]),
         "## Causal cases",table(["Case","Price","EV USD M","TV share","WACC / g","Action"],[[k,money(x['per_share']),f"{x['enterprise_value']:,.0f}",pct(x['terminal_share']),f"{pct(x['wacc'])} / {pct(x['g'])}",x['action']] for k,x in r['cases'].items()]),
         "Cases change subscription retention/expansion, operating margins, investment realization and discount/terminal assumptions together. They are causal states, not confidence intervals.",
         "## Base enterprise to equity bridge",table(["Bridge component","USD M"],[["Operating enterprise value",f"{b['enterprise_value']:,.2f}"],["Excess cash after operating-cash reserve",f"{b['bridge']['excess_cash']:,.2f}"],["Strategic investments after all-in realization haircut",f"{b['bridge']['strategic_investments_value']:,.2f}"],["Less debt market value + finance leases",f"{-b['bridge']['financial_debt_market']-633:,.2f}"],["Common equity",f"{b['bridge']['common_equity_value']:,.2f}"],["Shares million",824],["Value USD/share",money(b['per_share'])]]),
         "Cash is estimated forward 27 days using the pro-forma. Operating cash stays in the business. No operating-lease deduction is taken because lease costs stay in operating earnings. Preferred, minority interest and other separately identified senior claims are zero on the disclosed basis; no pension deduction is inferred without evidence.",
         "## WACC and growth sensitivity",table(["WACC / terminal g","2%","3%","4%"],[[pct(x['wacc'])]+[money(vv) for vv in x['values']] for x in r['sensitivity']['rows']]),
         "## Market-implied expectations",f"At {money(r['market']['price'])}, a parallel margin shift of {r['reverse_dcf']['margin_shift']*100:.2f} percentage points is needed under the base revenue/WACC/g path: year1 EBITA margin {pct(r['reverse_dcf']['year1_ebita_margin'])}, terminal EBITA margin {pct(r['reverse_dcf']['terminal_ebita_margin'])}. {r['reverse_dcf']['held_fixed']}. This is a conditional implication, not a unique market forecast.",
         "## Comparable companies",table(["Peer","Close","Annual GAAP P/E","EV / annual revenue","Annual end","Balance date"],[[p['ticker'],money(p['price']),f"{p['pe']:.4f}x",f"{p['ev_revenue']:.4f}x",p['annual_end'],p['balance_date']] for p in r['comparables']['peers']]),
         f"P/E implied range: {money(r['comparables']['pe_range'][0])} to {money(r['comparables']['pe_range'][1])}. EV/revenue implied range: {money(r['comparables']['ev_revenue_range'][0])} to {money(r['comparables']['ev_revenue_range'][1])}. These are qualified cross-checks; two heterogeneous peers do not establish fair value. Salesforce annual reported P/E is {r['comparables']['target_reported_annual_pe']:.2f}x.",
         table(["Peer removed","Remaining reference","Meaning"],[[x['removed'],money(x['pe_implied_price']) if x['pe_implied_price'] else 'none',x['interpretation']] for x in r['comparables']['leave_one_out']]),
         "P/E combines reported earnings with strategic-investment gains and a historical weighted share basis that predates substantial buybacks. Adobe has more creative/prosumer exposure; ServiceNow has much faster growth and a more depressed GAAP earnings denominator. EV/revenue ignores margins and stock compensation. Their very wide ranges explain why the DCF and explicit underwriting conditions carry the decision; no weighted average is used.",
         "## Named what-if scenarios",table(["Scenario","Price","Action","Year1 EBIT / interest","Year1 end cash"],[[k,money(x['per_share']),x['action'],f"{x['forecast'][0]['credit']['ebit_interest_coverage']:.2f}x",f"{x['forecast'][0]['balance_sheet']['cash']:,.0f}"] for k,x in r['what_if'].items()]),
         "Churn/collections: retention90%, expansion6%, new business2%, EBITA margins20/20/21/22/23%, 15 extra receivable days and deferred-revenue balance 5 points of revenue lower. Hosting: EBITA margin lower3 points; other operating drivers unchanged. Acquisition cash: $5100M paid with zero incremental benefits, added to goodwill, no inferred impairment; this is a deliberately adverse execution case, not an acquisition valuation. Flags are analyst diagnostics, not covenant or default findings.",
         "## Five-year statements and checks",
         "These are economically normalized statements with future stock compensation paid in cash at its assumed expense equivalent. Existing dilution is addressed in the bridge proxy and share stress. ROU assets and operating-lease liabilities remain flat under replacement leases; other deferred-tax/assets remain fixed; taxes use a normalized cash-tax proxy. No future discretionary buyback or unidentified M&A is assumed. July fiscal endpoints are analyst rolling years, not Salesforce's January fiscal year."]
    for case,x in r['cases'].items():
        rows=x['forecast']
        out.append(f"### {case.title()} case")
        out.append(table(["Income statement USD M"]+[z['period_end'] for z in rows],[[label]+[f"{z['income_statement'][key]:,.2f}" for z in rows] for key,label in [("subscription","Subscription/support"),("services","Services/other"),("revenue","Revenue"),("subscription_cogs_ex_acquired_amort","Subscription cost before acquired amortization"),("services_cogs","Services cost"),("gross_profit_ex_acquired_amort","Gross profit before acquired amortization"),("rd","Research and development"),("sm_including_commission_amortization","Sales and marketing including commission amortization"),("ga","General and administrative"),("recurring_restructuring","Recurring restructuring reserve"),("ebita","EBITA after recurring compensation"),("acquired_amortization","Acquired amortization"),("ebit","EBIT"),("interest","Interest"),("tax","Cash-tax proxy"),("net_income","Net income"),("diluted_eps","Diluted EPS USD")]]))
        bskeys=list(rows[0]['balance_sheet'])
        out.append(table(["Balance sheet USD M"]+[z['period_end'] for z in rows],[[key.replace('_',' ')]+[f"{z['balance_sheet'][key]:,.2f}" for z in rows] for key in bskeys]))
        out.append(table(["Cash flow USD M"]+[z['period_end'] for z in rows],[[key.replace('_',' ')]+[f"{z['cash_flow'][key]:,.2f}" for z in rows] for key in rows[0]['cash_flow']]))
        out.append(table(["Check USD M"]+[z['period_end'] for z in rows],[[key]+[f"{z['checks'][key]:.8f}" for z in rows] for key in rows[0]['checks']]))
    out += ["## Validation",f"{v['passed']} automated checks passed; {v['failed']} failed. Human AI-off lock, peer challenge and recorded cold-run ownership remain separate open requirements.",
            table(["Test","Status","Evidence"],[[t['test'],t['status'],str(t['result'])] for t in v['tests']]),
            "## Source map", "See `data/sources.json`, `evidence/data-lineage.md`, `evidence/assumption-challenges.md`, and `docs/validation-and-ai-use.md`. All nonhistorical rates are labeled analyst assumptions. Retrieval occurred2026-10-19; economic evidence availability stops2026-08-27."]
    return "\n\n".join(out)+"\n"


def make_html(r,v,md):
    # Static HTML is an offline output viewer, not an external hosted service.
    data=json.dumps(r).replace('</','<\\/')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Project 1 Salesforce valuation</title>
<style>body{font:17px/1.5 system-ui,sans-serif;background:#f4f6fa;color:#172b45;margin:0}main{max-width:1120px;margin:auto;padding:32px}h1{font-size:32px}section{background:white;border:1px solid #ccd6e2;border-radius:10px;padding:22px;margin:20px 0}button,select{font:inherit;padding:8px}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:right;padding:7px;border-bottom:1px solid #dce3ec}th:first-child,td:first-child{text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.5 ui-monospace,monospace}.large{font-size:30px;font-weight:bold}.warning{background:#fff3da}a{color:#0759a0}.scroll{overflow-x:auto}</style>
<main><h1>Project 1 Salesforce valuation</h1><p>NYSE CRM | USD | Valuation August 27, 2026 | Committee with no position</p><section class="warning"><b>Human submission steps remain open.</b> The AI-off baseline, locked prediction, partner challenge, three recordings and corrected transcripts require authentic student evidence. See <a href="../STUDENT-ACTIONS.md">student actions</a>. This is a historical valuation, not a current October quote.</section>
<section><label for="case">Explore a causal case or what-if </label><select id="case"><option>base</option><option>low</option><option>high</option><option>churn_and_collections</option><option>ai_hosting_cost</option><option>cash_acquisitions_no_benefit</option></select><div id="decision"></div><div id="summary"></div></section>
<section><h2>Linked forecast</h2><div class="scroll" id="statements"></div></section><section><h2>WACC and terminal growth</h2><div id="grid"></div><p>Positive operating cash flows; terminal reinvestment equals g / 20% ROIC.</p></section>
<section><h2>Evidence and reproducibility</h2><p><a href="visible-output.md">Full executed report and all statements</a> · <a href="results.json">Machine-readable results</a> · <a href="validation-results.json">Executed validation</a> · <a href="../docs/decision-memo.pdf">Committee memo PDF</a> · <a href="../docs/rubric-audit.md">Rubric audit</a></p><p id="validation"></p><details><summary>Full report text</summary><pre>'''+html.escape(md)+'''</pre></details></section></main>
<script>const R='''+data+''';const fmt=(x)=>Number(x).toLocaleString('en-US',{maximumFractionDigits:2});const cash=(x)=>'$'+fmt(x);function tab(headers,rows){return '<table><thead><tr>'+headers.map(h=>'<th>'+h+'</th>').join('')+'</tr></thead><tbody>'+rows.map(row=>'<tr>'+row.map(c=>'<td>'+c+'</td>').join('')+'</tr>').join('')+'</tbody></table>'}function show(){const key=document.getElementById('case').value;const x=R.cases[key]||R.what_if[key];document.getElementById('decision').innerHTML='<p class="large">'+x.action+' · '+cash(x.per_share)+'</p><p>Causal DCF range '+R.decision.valuation_range.map(cash).join(' to ')+'; observed close '+cash(R.market.price)+'. Each case uses its own underwriting state.</p>';document.getElementById('summary').innerHTML=tab(['WACC','Terminal g','PV terminal / EV','EV USD M','Equity USD M'],[[fmt(x.wacc*100)+'%',fmt(x.g*100)+'%',fmt(x.terminal_share*100)+'%',fmt(x.enterprise_value),fmt(x.bridge.common_equity_value)]]);const rows=x.forecast;const metrics=[['income_statement','revenue','Revenue'],['income_statement','ebit','EBIT'],['income_statement','net_income','Net income'],['balance_sheet','total_assets','Assets'],['balance_sheet','total_liabilities','Liabilities'],['balance_sheet','equity','Equity'],['cash_flow','cfo','CFO'],['cash_flow','cfi','CFI'],['cash_flow','cff','CFF'],['balance_sheet','cash','Ending cash'],['cash_flow','fcff','FCFF'],['credit','ebit_interest_coverage','EBIT / interest'],['checks','balance_sheet_error','Balance error'],['checks','cash_tie_error','Cash tie error']];document.getElementById('statements').innerHTML=tab(['USD M except coverage',...rows.map(z=>z.period_end)],metrics.map(([a,b,label])=>[label,...rows.map(z=>fmt(z[a][b]))]));}document.getElementById('case').addEventListener('change',show);show();document.getElementById('grid').innerHTML=tab(['WACC / g','2%','3%','4%'],R.sensitivity.rows.map(row=>[fmt(row.wacc*100)+'%',...row.values.map(cash)]));document.getElementById('validation').textContent='''+json.dumps(f"{v['passed']} automated checks passed; {v['failed']} failed. Missing human evidence remains open.")+''';</script></html>'''


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=ROOT/'data/inputs.json')
    p.add_argument('--output',type=Path,default=ROOT/'outputs')
    p.add_argument('--case',choices=['low','base','high'])
    p.add_argument('--wacc',type=float,help='Decimal override; .10 means10%')
    p.add_argument('--shock',choices=['churn_and_collections','ai_hosting_cost','cash_acquisitions_no_benefit'])
    p.add_argument('--all',action='store_true',help='Generate all results and run validation (default)')
    args=p.parse_args()
    d=json.loads(args.input.read_text(encoding='utf-8'))
    sources=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))
    args.output.mkdir(parents=True,exist_ok=True)
    validate_inputs(d,sources)
    if args.case or args.wacc is not None or args.shock:
        result=valuation(d,args.case or 'base',args.shock,args.wacc)
        (args.output/'changed-result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
        print(json.dumps({k:result[k] for k in ['case','shock','per_share','wacc','action']},indent=2))
        return
    v=validate(d,sources)
    r=all_results(d,sources)
    text=report(r,v)
    for name,obj in [('results.json',r),('validation-results.json',v)]:
        (args.output/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
    (args.output/'visible-output.md').write_text(text,encoding='utf-8',newline='\n')
    (args.output/'dashboard.html').write_text(make_html(r,v,text),encoding='utf-8',newline='\n')
    receipt={'run_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'python':sys.version,'platform':sys.platform,
             'input_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest(),
             'source_sha256':hashlib.sha256((ROOT/'data/sources.json').read_bytes()).hexdigest(),
             'validation_passed':v['passed'],'validation_failed':v['failed']}
    (args.output/'run-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f"CRM {d['valuation_date']}: {r['decision']['action']}; causal range "+' to '.join(money(x) for x in r['decision']['valuation_range']))
    print(f"Base {money(r['cases']['base']['per_share'])}; {v['passed']} checks passed; {v['failed']} failed.")
    if v['failed']:
        print(json.dumps([t for t in v['tests'] if t['status']=='FAIL'],indent=2))
        raise SystemExit(1)


if __name__=='__main__':
    try: main()
    except (ModelError,KeyError,ValueError) as exc:
        print('MODEL ERROR: '+str(exc),file=sys.stderr)
        raise SystemExit(2)
