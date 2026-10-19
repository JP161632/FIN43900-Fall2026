"""Build readable recording evidence directly from saved financial/test artifacts.

No new valuation assumptions or human events are created. Optional PDF packages are
used only to locate headings in the existing deliverables, not by the finance engine.
"""
import hashlib
import html
import json
from pathlib import Path
import re
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]


def write(name,text):
    (ROOT/name).write_text(text.strip()+'\n',encoding='utf-8',newline='\n')


def money(n): return f'${n:,.2f}'


def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+
                     ['| '+' | '.join(str(x).replace('|','/') for x in row)+' |' for row in rows])


def main():
    r=json.loads((ROOT/'outputs/results.json').read_text(encoding='utf-8'))
    v=json.loads((ROOT/'outputs/validation-results.json').read_text(encoding='utf-8'))
    d=json.loads((ROOT/'data/inputs.json').read_text(encoding='utf-8'))
    tests={x['test']:x for x in v['tests']}
    assert v['status']=='PASS'
    b=r['cases']['base']; low=r['cases']['low']; high=r['cases']['high']; y=b['forecast'][0]
    change=tests['Prewritten directional changed input']['result']
    danger=tests['Highest-risk investment contamination experiment']['result']
    known=tests['Official training DCF and nine cells']['result']
    oldfile=REPO/'projects/lab-05-nvda-dcf/nvda-dcf-lab.md'
    old=oldfile.read_text(encoding='utf-8')
    assert '**$62.7184**' in old and '**$55.59–$72.40' in old and '15.88%' in old
    prior=json.loads((ROOT/'evidence/prior-lab-index.json').read_text(encoding='utf-8'))
    oldindex=next(x for x in prior if x['path']==oldfile.relative_to(REPO).as_posix())
    assert hashlib.sha256(oldfile.read_bytes()).hexdigest()==oldindex['sha256']
    assert abs(y['nopat']+y['cash_flow']['depreciation_amortization']-y['cash_flow']['capex']-y['cash_flow']['delta_operating_nwc']-y['fcff'])<1e-6
    page_map={}
    import pymupdf
    for name,terms in {
        'Research-Evolution.pdf':['Initial thesis','A-to-B and prior-lab evidence table','Attribution of research changes','AI output independently corrected'],
        'Decision-Memo.pdf':['Committee ask and valuation range','Disagreement across methods','Conditions, reversal triggers']}.items():
        doc=pymupdf.open(ROOT/name)
        for term in terms:
            found=[i+1 for i,p in enumerate(doc) if term.lower() in p.get_text().lower()]
            assert found,(name,term)
            page_map[name+':'+term]=found[0]
    baseline_page=page_map['Research-Evolution.pdf:Initial thesis']
    values={
        'BASELINE_PAGE':str(baseline_page),'BASE_PRICE':money(b['per_share']),'LOW_PRICE':money(low['per_share']),
        'HIGH_PRICE':money(high['per_share']),'ENTRY_PRICE':money(b['entry_ceiling']),
        'CHANGED_PRICE':money(change['new_price']),'YEAR1_FCFF':f"{y['fcff']:,.2f}",
        'TV_SHARE':f"{b['terminal_share']:.1%}",'REVERSE_SHIFT':f"{r['reverse_dcf']['constant_increment_to_each_dc_growth']*100:.2f}"}
    guide=(ROOT/'docs/recording-guide-template.md').read_text(encoding='utf-8')
    for k,value in values.items():guide=guide.replace('{{'+k+'}}',value)
    assert not re.search(r'\{\{\w+\}\}',guide)
    write('docs/recording-guide.md',guide);write('Student next steps.md',guide)
    comparison=table(['Item','Earlier Lab5','Revised Project1 / why comparison needs care'],[
        ['Decision','Watch-defer, after initial research admission','WATCH / DEFER remains; structural downside -> DO NOT INITIATE'],
        ['Base estimate / USD per share','$62.72',money(b['per_share'])+'; not a controlled single-input change'],
        ['Interval','$55.59-$72.40 WACC/g grid',money(low['per_share'])+'-'+money(high['per_share'])+' causal low/base/high; DIFFERENT definition'],
        ['Operating starting point','FY26 revenue215,938M; startingFCFF96,895.891M','LTM revenue302,970M; five linked statements generate operatingFCFF'],
        ['Year1forecastFCFF / USD millions','130,809.4529 (Lab5 Year1)',f"{y['fcff']:,.4f} full rollingyear before valuationstub; different forecastwindows, not a realized cash-flow gain"],
        ['Discount rate / terminal','15.88% WACC /3%g; FCFF Gordon continuation',f"{b['wacc']:.4%} WACC /3%g /25%ROIC; mature reinvestment explicit"],
        ['Share basis / millions','24,514 annual weighted-average diluted','24,242 proxy =24,147 period-end basic+95 incremental quarter dilution'],
        ['Market comparison','224.35 intraday Sep10,1:37:33pmEDT','218.36 Sep10 US close; neither is an October quote'],
        ['Evidence date versus build date','Annual fiscal2026 endedJan25','LTM endedJul26; publicAug26; valuationSep10; rebuiltOct19']])
    attribution=table(['Cause','Supported contribution','Limit on attribution'],[
        ['Course instruction','Five-year FCFF/enterprise-equity architecture, validation and decision standard','Instruction supplies method, not NVIDIA fair value'],
        ['Existing student-supplied materials','Target/research-admission question and saved earlier lab outputs','Does not establish authorship of each older passage or original checkpoint receipt'],
        ['Prior lab analysis/review','Lab11 withholds a new value until classification/discount/terminal issues are resolved','Student confirms October1 peer challenge; Antigravity log and independent follow-up are in evidence/partner-review-record.md'],
        ['AI assistance Oct19','Source organization, rebuild, assumptions/scenarios, tests and documentation','Not all changes were caused by AI; no claim AI-generated assumptions are reported facts'],
        ['Primary evidence + numerical challenge','Latest filing definitions and test results support accepting/correcting/qualifying outputs','Passing accounting checks cannot establish forecast truth']])
    correction=table(['Primary-source fact / July26,2026','Amount USD millions','Model implication'],[
        ['Cash and equivalents','22,443','Cash balance; retains10,000 operating reserve separately'],
        ['Marketable debt securities','34,143','Cash+debt securities=56,586'],
        ['Marketable equity securities','42,783','Not cash; separate recovery assumption/bridge'],
        ['Financial portfolio excluded from operatingNWC',f"{danger['financial_portfolio_excluded_from_nwc']:,.0f}",'Public47,740 + private/other55,281; counted separately once'],
        ['Carrying debt / fair-value debt','33,366 /31,400','Book debt in statements; fair value in DCF bridge/WACC']])
    fc=y['cash_flow']
    known_table=table(['Check / units','Independent expected answer','Actual engine result'],[
        ['Training EV / USD millions','1,624.87 rounded',f"{known['ev']:,.5f}"],
        ['Training share value / USD','27.50 rounded',f"{known['grid'][1][1]:.5f}"],
        ['All nine sensitivity cells','Published Week3 grid','Each tested within0.006USD/share'],
        ['Company full year1FCFF / USD millions','NOPAT+D&A-capex-deltaoperatingNWC',f"{y['nopat']:,.2f}+{fc['depreciation_amortization']:,.2f}-{fc['capex']:,.2f}-{fc['delta_operating_nwc']:,.2f}={y['fcff']:,.2f}"],
        ['Three-statement articulation','Assets=liabilities+equity; cash ties; no plug',f"25forecastyears; max error {tests['25 forecast statement articulations']['result']['maximum_error_millions']:.3g}M"]])
    changed=table(['Item','Before','After / observed effect'],[
        ['WACC / decimal',f"{change['old_wacc']:.9f}",f"{change['new_wacc']:.9f}; +0.01 =+1percentagepoint"],
        ['Estimated USD/share',money(change['old_price']),money(change['new_price'])],
        ['Prediction / direction','Lower EV/per-share; continued deferral','Lower; WATCH/DEFER remains; price218.36 still above the entry ceiling'],
        ['Chronology','AI prediction committed in7c404d5 before rebuilt model execution','Later humanized draft is retrospective; cannot backdate new wording'],
        ['Human-lock evidence','Separate record currently INCOMPLETE','Use actual completed record or truthful instructor-permitted designation']])
    cases=table(['Causal case','USD/share','Action / economics'],[
        ['Low',money(low['per_share']),'DO NOT INITIATE: demand/financing/margin/collection deterioration, extra losses; declared risk gate'],
        ['Base',money(b['per_share']),'WATCH / DEFER at218.36; no20%marginofsafety'],
        ['High',money(high['per_share']),'Stronger sustained adoption/collections; not a probability-weighted target']])
    peer=r['comparables']; shift=r['reverse_dcf']['constant_increment_to_each_dc_growth']*100
    proof=f'''
# NVIDIA recording evidence - reading aid

Generated from actual saved results, validation output and indexed earlier lab. Historical valuation September10,2026; build/review October19. This aid makes underlying evidence readable; it is not a substitute for original filings, code, test execution or authentic student events. USD millions unless marked USD/share.

## R1 Before and after

{comparison}

Original earlier evidence: [Lab5 valuation and sensitivity](../../lab-05-nvda-dcf/nvda-dcf-lab.md); earlier file SHA256 `{oldindex['sha256']}`. Original baseline text: [unchanged EditionA](../evidence/edition-a-existing-nvidia-unchanged.md); [research evolution](../Research-Evolution.pdf), baseline reading appendix page{baseline_page}. Current numbers: [executed results](results.json). Do not claim a new typeset appendix proves the original Brightspace checkpoint.

## R2 Why it changed / attribution

{attribution}

Lab11 states: “Value-per-share spans are unavailable because valuation remains unresolved.” Read [Main driver over the tested ranges](../../lab-11-nvda-sensitivity/lab-11-writeup.md). It also states that the growth ranking depends on chosen ranges. The recorded limitation existed before the rebuild; internal balance alone did not justify a valuation. The new base is not simply Lab5 plus one correction: data base, forecast method, WACC, terminal economics, bridge and shares all changed. The revised beta1.8 and ERP5% are explicit analyst assumptions, not a newly verified empirical beta; Treasury4.95% is sourced. The lower WACC must be challenged, not presented as automatic model improvement.

## R3 Independent correction and test

{correction}

Primary check: [NVIDIA Q2 Form10-Q, balance sheet and Notes5/6/11](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm); [independent issuer release balance sheet](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027). Find42,783 and read the row label/date; the current source map is our index, not independent proof by itself.

AI output disposition: **CORRECTED** financial-investment/operatingNWC classification; **QUALIFIED** forecast growth, beta, recoveries and guarantees. A deliberately wrong scaling diagnostic creates {danger['wrong_scaling_explicit_ev_drag']/1000:,.2f}bn of false discounted explicit-period investment, equivalent to{money(danger['minimum_wrong_price_drag'])}/share in that calculation. This is a bounded illustrative subtraction exercise, not a full alternate forecast/terminal/stub-consistent valuation or attribution of the historical price change. It supports taking classification seriously; the source definitions justify the correction.

## R4 What changed the judgment

Final base **{money(b['per_share'])}**, causal range **{money(low['per_share'])}-{money(high['per_share'])}**, dated market **218.36**, action **WATCH / DEFER**. Later action held from Lab5 to finalB even though estimated value changed; EditionA was research admission. Base DCgrowth40/30/22/15/10% is a forecast, not filing guidance. It is challenged by customer funding, collections and deployment/power constraints. Next filings showing sustainable demand with collection/margin conversion could justify revising it; supplier commitments are not customer orders. Entry ceiling{money(b['entry_ceiling'])} is conditional on refreshed evidence. [Full driver challenge record](../evidence/assumption-challenges.md).

## V1 Known answer and company arithmetic

{known_table}

Independent expected answers: **course repository** lessons/week-03/teach-dcf-worked-example.md, published training EV1,624.87 and price27.50 (not invented company data). [Actual test results](validation-results.json), “Official training DCF and nine cells”; [test implementation](../tests.py), functionknown. Company year1 endsJuly26,2027; the full-yearFCFF above precedes the elapsed46-day valuation-stub adjustment. [Statement-to-FCFF code](../model.py), forecast; [all company statements](visible-output.md).

## V2 Highest-risk failure evidence

Financial assets excluded from operatingNWC:103,021M. Deliberately scaling them with sales creates false operating reinvestment: the bounded diagnostic's discounted amount is{danger['wrong_scaling_explicit_ev_drag']:,.2f}M /{money(danger['minimum_wrong_price_drag'])}per share. This does not calculate the complete valuation error. Source grouping plus the diagnostic challenges the prior-lab classification rather than only checking whether the statements balance.

Two deliberately bad inputs are also rejected. A1M asset corruption produces **“BS_Jul26 assets:320273 !=320272.”** A forced first-year investment purchase10,000,000M produces **“base year1 cash below floor; explicit funding needed.”** A passing test means the expected rejection happened, not that the corrupted run was financially viable. [Actual failures captured by tests](validation-results.json), “Corrupt source / liquidity failure injection”; [test code](../tests.py), functionbroken.

## V3 Changed input: prediction versus result

{changed}

The current test recomputes discount-dependent bridge claim PVs, holding operating forecasts/terminalgrowth/bridge assumptions fixed. It is not a forecast-change scenario. [Original AI prewritten prediction](../evidence/directional-test-precommit.md); [actual result](validation-results.json), “Prewritten directional changed input.” Correctly anticipating direction supports implementation; it does not validate the selected WACC as true.

## V4 Evidence boundary

[Current student locked record](../evidence/locked-changed-input-record.md) now preserves prediction precommit 5a9de1d and executed terminal growth 3%->2.5%: $118.58->$116.57 (-1.70%), WATCH/DEFER unchanged. The earlier [humanized WACC draft](../docs/changed-input-response-draft.md) is separate historical rehearsal. Attributed peer review is supplied. Original checkpoint and audio/timestamp verification remain open; recorded performances are not inferred from technical tests.

## C1 Dated action and causal range

{cases}

Base operatingEV{money(b['enterprise_value'])}M + netbridge{money(sum(b['bridge'].values()))}M =common equity{money(b['equity_value'])}M; divide24,242M proxy diluted shares ->{money(b['per_share'])}/share. Forecast basic/awards are not exact September fully diluted cap-table facts. [Dashboard](dashboard.html); [memo](../Decision-Memo.pdf).

## C2 Method disagreement

Historical annual GAAP P/E peer references:{money(min(peer['pe_implied_prices']))}-{money(max(peer['pe_implied_prices']))}. EV/annualsales references:{money(min(peer['ev_sales_implied_prices']))}-{money(max(peer['ev_sales_implied_prices']))}. AMD's lower margins and product mix, AVGO's software/acquisition mix, two-peer instability and stale annual denominators limit inference. Each method uses its disclosed consistent numerator/bridge convention; noncash investments are not added twice. Do not average these into the DCF range. [Peer policy](../evidence/peer-policy.md); [full method output](visible-output.md); memo page2.

## C3 Market expectation and terminal dependence

Base terminal-value share:{b['terminal_share']:.1%}. BaseWACC{b['wacc']:.4%},g3%,ROIC25% ->reinvest12%of terminalNOPAT. At fixed other base inputs, the218.36 marketprice requires+{shift:.2f}percentagepoints to **each** DCgrowth assumption: {', '.join(f'{g:.1%}' for g in r['reverse_dcf']['implied_dc_growth_path'])}. Year5sales{r['reverse_dcf']['year5_revenue']/1000:,.1f}bn. This is one conditional solution, not a unique market forecast. It differs from Lab5's limited-bracket failedreverseDCF because the underlying engine/base/shiftedvariable changed. [ReverseDCF output](results.json).

## C4 Committee monitoring

**Ask:** WATCH / DEFER; no current position;12-24month decisionhorizon. Consider initiation only below the refreshed20%-discount entry ceiling (currently{money(b['entry_ceiling'])}) with evidence supporting demand, collections, margins and funded commitments. Price alone is insufficient.

**Review every quarterly filing:** two consecutive quarters of DCgrowth below20% challenge durability; collectiondays above95 or reportedGMbelow70% challenge conversion/profitability; material guarantee/capacity losses require immediate reassessment and a funded cash/NI model update. BaseforecastGM>=72% and collection assumption75days need support before initiation. DSOconvention here is endingreceivables/LTMsales*365, not an unqualified provider label. Current guarantees are valuationbridge expected-loss assumptions, not booked filing debt; the adverse-regime riskgate is a declared policy condition.

Durable faster growth with collection/margin intact could justify an upward revision, rather than a fixed permanent rejection. Refresh price,rates,awards,debt,investmentrealizations,pending-acquisitionfinancing and guarantee terms before any trade. [Memo page2](../Decision-Memo.pdf); [monitoring section](visible-output.md).
'''
    pieces=re.split(r'(`[^`]*`|\]\([^)]*\)|\b[0-9a-fA-F]{7,64}\b)',proof)
    for j in range(0,len(pieces),2):
        s=pieces[j]
        s=re.sub(r'(?<=[a-z])(?=\d)',' ',s)
        s=re.sub(r'(?<=\d)(?=[A-Za-z])',' ',s)
        s=re.sub(r'(?<=%)(?=[A-Za-z])',' ',s)
        s=re.sub(r'\b(WACC|ROIC|DSO|GM|ERP|EV|FCFF|AR)(?=\d)',r'\1 ',s)
        pieces[j]=s
    proof=''.join(pieces)
    write('docs/recording-proof.md',proof)
    css='''body{font:18px/1.5 system-ui;max-width:1180px;margin:28px auto;padding:0 24px;background:#eef3f7;color:#142d40}section,header{background:white;padding:24px;margin:20px 0;border-radius:8px}nav{position:sticky;top:0;background:#173853;padding:12px;display:flex;gap:18px;z-index:2}nav a{color:white}a{color:#07599a}h1{font-size:30px}h2{font-size:24px;scroll-margin-top:75px}td,th{font-size:16px;text-align:left;padding:12px;border-bottom:1px solid #ccd7df;vertical-align:top}th{background:#e5eef5}table{border-collapse:collapse;width:100%}code{font-size:14px;overflow-wrap:anywhere}strong{color:#174c29}section{scroll-margin-top:65px}.note{color:#465e70}p{margin:12px 0}'''
    def inline(s):
        s=html.escape(s)
        s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:'<a href="'+m[2]+'">'+m[1]+'</a>',s)
        s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
        s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
        return s
    body=[];lines=proof.strip().splitlines();i=0;inside=False
    while i<len(lines):
        s=lines[i].strip()
        if not s:i+=1;continue
        if s.startswith('## '):
            if inside:body.append('</section>')
            heading=s[3:];anchor=heading.split()[0].lower();body.append(f'<section id="{anchor}"><h2>{inline(heading)}</h2>');inside=True;i+=1;continue
        if s.startswith('# '):body.append('<header><h1>'+inline(s[2:])+'</h1></header>');i+=1;continue
        if s.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(set(c)<=set('-: ') for c in cells):rows.append(cells)
                i+=1
            body.append('<table>'+''.join('<tr>'+''.join('<'+('th' if j==0 else 'td')+'>'+inline(c)+'</'+('th' if j==0 else 'td')+'>' for c in row)+'</tr>' for j,row in enumerate(rows))+'</table>');continue
        body.append('<p>'+inline(s)+'</p>');i+=1
    if inside:body.append('</section>')
    nav='<nav aria-label="Recording evidence sections"><a href="#r1">Research evolution</a><a href="#r3">Independent correction</a><a href="#v1">Numerical validation</a><a href="#v3">Changed input</a><a href="#c1">Committee evidence</a><a href="#c4">Monitoring</a></nav>'
    page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NVIDIA recording evidence</title><style>'+css+'</style>'+nav+''.join(body)+'</html>'
    write('outputs/recording-proof.html',page)
    class Links(HTMLParser):
        def __init__(self):super().__init__();self.ids=set();self.hrefs=[]
        def handle_starttag(self,tag,attrs):
            attrs=dict(attrs)
            if 'id' in attrs:self.ids.add(attrs['id'])
            if tag=='a' and 'href' in attrs:self.hrefs.append(attrs['href'])
    links=Links();links.feed(page);broken=[]
    for href in links.hrefs:
        if href.startswith('#'):
            if href[1:] not in links.ids:broken.append(href)
        elif not urlsplit(href).scheme:
            if not (ROOT/'outputs'/unquote(urlsplit(href).path)).resolve().is_file():broken.append(href)
    assert not broken,broken
    # Markdown links use output-relative paths so both formats point to the same project artifacts.
    write('docs/recording-proof.md',proof.replace('](results.json)','](../outputs/results.json)').replace('](validation-results.json)','](../outputs/validation-results.json)').replace('](visible-output.md)','](../outputs/visible-output.md)').replace('](dashboard.html)','](../outputs/dashboard.html)'))
    scripts={str(i):len(re.search(f'<!-- SCRIPT{i} -->(.*?)<!-- /SCRIPT{i} -->',guide,re.S)[1].split()) for i in [1,2,3]}
    assert scripts['1']<=355,('Video1 too long',scripts)
    assert all(scripts[str(i)]<=410 for i in [2,3]),scripts
    receipt={'status':'PASS','source_question':'lessons/week-07/student-handout.md: Three evidence surfaces',
        'page_map':page_map,'script_word_counts':scripts,'numbers_checked_against':'outputs/results.json and validation-results.json',
        'old_lab_hash_verified':oldindex['sha256'],'fcff_arithmetic_error_millions':abs(y['nopat']+fc['depreciation_amortization']-fc['capex']-fc['delta_operating_nwc']-y['fcff']),
        'limitations':'Evidence navigation/script audit, not observed video performance or human-history certification',
        'financial_result_sha256':hashlib.sha256((ROOT/'outputs/results.json').read_bytes()).hexdigest(),
        'proof_anchor_and_local_links_checked':len(links.hrefs),'broken_local_or_anchor_links':broken,
        'browser_visual_check':'Not available: no enabled browser surface; PDF pages visually checked; student HTML rehearsal required'}
    write('outputs/recording-script-audit.json',json.dumps(receipt,indent=2))
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
