"""Three fixed 16:9 recording charts, drawn from the saved NVIDIA evidence.

Optional authoring dependencies only: ReportLab and PyMuPDF. No model changes.
"""
import hashlib
import json
from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
import pymupdf

ROOT=Path(__file__).resolve().parent
W,H=1280,720
NAVY='#173853';INK='#183044';MUTED='#4c6475';GREEN='#28592e';PALE='#eff5e9';BORDER='#d2dde5';BG='#f5f7fa';ORANGE='#aa5515'


def main():
    r=json.loads((ROOT/'outputs/results.json').read_text(encoding='utf-8'))
    v=json.loads((ROOT/'outputs/validation-results.json').read_text(encoding='utf-8'))
    tests={x['test']:x['result'] for x in v['tests']}
    b=r['cases']['base'];lo=r['cases']['low'];hi=r['cases']['high'];y=b['forecast'][0]
    ch=tests['Prewritten directional changed input'];bad=tests['Highest-risk investment contamination experiment']
    known=tests['Official training DCF and nine cells'];pe=r['comparables']
    source=(ROOT/'model.py').read_text(encoding='utf-8')
    assert "b['ar']=revenue*c['dso']/365" in source
    assert 'fcff=nopat+da-capex-delta_nwc' in source
    dest=ROOT/'Recording-Charts.pdf'
    c=canvas.Canvas(str(dest),pagesize=(W,H),invariant=1,pageCompression=1)
    c.setTitle('NVIDIA - fixed recording charts');c.setAuthor('Course investment research')
    boxes=[]

    def rect(x,top,w,h,fill='white',stroke=BORDER,radius=9):
        c.setFillColor(colors.toColor(fill));c.setStrokeColor(colors.toColor(stroke))
        c.setLineWidth(1)
        c.roundRect(x,H-top-h,w,h,radius,fill=1,stroke=1)

    def text(s,x,top,w,size=15,color=INK,bold=False,maxh=100,leading=None):
        style=ParagraphStyle('chart',fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,
                             leading=leading or size*1.26,textColor=colors.toColor(color),autoLeading='max')
        p=Paragraph(s,style);pw,ph=p.wrap(w,maxh)
        assert ph<=maxh+0.1,(s,ph,maxh)
        assert x>=0 and top>=0 and x+pw<=W+0.1 and top+ph<=H+0.1,(s,x,top,pw,ph)
        p.drawOn(c,x,H-top-ph);boxes.append({'page':c.getPageNumber(),'top':top,'bottom':top+ph,'text':s})
        return ph

    def header(k,title,sub):
        c.setFillColor(colors.HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(colors.HexColor(NAVY));c.rect(0,H-100,W,100,fill=1,stroke=0)
        c.setFillColor(colors.HexColor(GREEN));c.rect(0,H-104,W,4,fill=1,stroke=0)
        text(k,38,16,1200,11,'#c3e79d',True,maxh=16)
        text(title,38,35,1200,29,'white',True,maxh=38)
        text(sub,38,77,1200,12,'#e0ebf2',maxh=18)

    def panel(x,top,w,h,title,body,size=15,fill='white'):
        rect(x,top,w,h,fill)
        text(title,x+16,top+14,w-32,13,NAVY,True,maxh=20)
        text(body,x+16,top+44,w-32,size,maxh=h-52)

    def footer(number,links,note):
        text(note,38,650,1204,11,MUTED,maxh=31)
        x=38
        for label,url in links:
            width=c.stringWidth(label,'Helvetica',10.5)
            c.setFont('Helvetica',10.5);c.setFillColor(colors.HexColor('#07599a'))
            c.drawString(x,21,label);c.linkURL(url,(x,18,x+width,33),relative=0,thickness=0)
            x+=width+27
        c.setFont('Helvetica-Bold',11);c.setFillColor(colors.HexColor(MUTED));c.drawRightString(W-38,21,f'{number} / 3')

    repo='https://github.com/JP161632/FIN43900-Fall2026/blob/main/'
    q='https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm'
    results=repo+'projects/project-1/outputs/results.json'
    validation=repo+'projects/project-1/outputs/validation-results.json'
    lab5=repo+'projects/lab-05-nvda-dcf/nvda-dcf-lab.md'
    lab11=repo+'projects/lab-11-nvda-sensitivity/lab-11-writeup.md'
    baseline=repo+'projects/project-1/evidence/edition-a-existing-nvidia-unchanged.md'

    # PAGE1: a genuine before / evidence / after chain, rather than a decorative price chart.
    header('VIDEO 1 | RESEARCH EVOLUTION','NVIDIA: the estimate changed; the later action held',
           'Historical valuation: Sep 10, 2026 | Earlier annual model vs revised rolling forecast | USD/share unless marked otherwise')
    cw=388;gap=18
    panel(38,118,cw,174,'1  STARTING QUESTION',
          '<b>Research admission, not a buy call</b><br/>Could Data Center growth become durable owner cash flow at a reasonable price?<br/><br/><b>Edition A: Sep 1</b><br/>Demand, margin and valuation were still open.',16)
    panel(38+cw+gap,118,cw,174,'2  EARLIER VALUATION | LAB 5',
          '<font size="30"><b>$62.72</b></font> base<br/><br/><b>$55.59-$72.40</b> WACC / g grid<br/>WACC 15.88% | 24,514M weighted diluted shares<br/>Watch/defer; limited reverse-DCF bracket failed.',15)
    panel(38+2*(cw+gap),118,cw,174,'3  REVISED VALUATION | PROJECT 1',
          f'<font size="30"><b>${b["per_share"]:.2f}</b></font> base<br/><br/><b>${lo["per_share"]:.2f}-${hi["per_share"]:.2f}</b> causal cases<br/>WACC {b["wacc"]:.2%} | 24,242M diluted proxy<br/><b>WATCH / DEFER at $218.36 close</b>',15,PALE)
    text('The old interval is a sensitivity grid; the new interval is causal scenarios. Different definitions, not a measured improvement in accuracy.',
         42,303,1196,13,MUTED,maxh=22)
    panel(38,339,cw,214,'WHAT CHANGED - AND WHY',
          '<b>Operating base:</b> FY26 sales $215.94B -> LTM $302.97B.<br/>'
          '<b>Year 1 FCFF:</b> $130.81B -> $191.48B*.<br/>'
          '<b>Lab11:</b> withheld a new value until classification / terminal issues were fixed.<br/>'
          '<b>Rebuild:</b> signed FCFF, investments outside operating NWC, terminal reinvestment.',15)
    panel(38+cw+gap,339,cw,214,'INDEPENDENT SOURCE CHECK',
          '<b>July 26, 2026 balance sheet, USD millions</b><br/>'
          'Cash 22,443 + debt securities 34,143<br/>'
          '<b>= 56,586 cash / debt securities</b><br/>'
          'Marketable equity <b>42,783 is separate</b>.<br/>'
          'Investment gains are not operating cash.<br/>'
          '<b>AI classification output: CORRECTED</b>',15)
    panel(38+2*(cw+gap),339,cw,214,'WHAT HELD / WHAT WOULD CHANGE',
          '<b>Lab5 -> final: watch/defer held.</b><br/>'
          'Growth, WACC and recoveries remain assumptions to challenge.<br/>'
          'Demand must convert to collections and margins; supply commitments are not orders.<br/>'
          f'<b>Conditional entry: <= ${b["entry_ceiling"]:.2f}</b> with refreshed evidence.',15)
    rect(38,568,1204,66,fill='#e5edf3')
    text('<b>Source of change:</b> course -> FCFF framework; prior labs -> recorded limitations; AI -> rebuild / checks; filings + numerical tests -> accept or qualify outputs. No single correction explains the full valuation change.',
         54,582,1172,14,maxh=46)
    footer(1,[('Edition A text',baseline),('Lab5 earlier estimate',lab5),('Lab11 limitations',lab11),('SEC Q2 filing',q),('Revised results',results)],
           '* Different forecast windows / methods; not a realized cash-flow gain or a controlled price bridge. Original checkpoint receipt remains separate.')
    c.showPage()

    # PAGE2: actual code excerpts and outcomes; a short recorded terminal overlay supplies live execution.
    header('VIDEO 2 | CODE AND VALIDATION','From one driver to FCFF - then challenge the result',
           'Saved code / numerical outcomes shown here | Record the fresh-environment run as a short terminal overlay; no tab scrolling needed')
    chain=[('INPUT','DSO 75 days','Revenue $417,865M'),('BALANCE / CASH',f'AR {y["balance_sheet"]["ar"]:,.2f}M',f'Change NWC {y["cash_flow"]["delta_operating_nwc"]:,.2f}M'),
           ('OPERATING FCFF',f'{y["fcff"]:,.2f}M','After tax + D&A - capex - change NWC'),('OWNERSHIP VALUE',f'${b["per_share"]:.2f} / share','EV -> claims -> equity / diluted shares')]
    for i,(label,value,detail) in enumerate(chain):
        xx=38+i*305
        panel(xx,118,289,106,label,f'<b>{value}</b><br/>{detail}',14)
    rect(38,238,1204,83,fill='#e5edf3')
    text('<b>Source excerpts (model.py) + terminal math</b><br/>'
         '<font name="Courier">b[\'ar\']=revenue*c[\'dso\']/365</font><br/>'
         '<font name="Courier">fcff=nopat+da-capex-delta_nwc</font> | Terminal math: <font name="Courier">NOPAT5*(1+g)*(1-g/ROIC)</font>',
         54,250,1172,14,maxh=62)
    panel(38,337,388,213,'KNOWN ANSWER - NOT JUST "IT RUNS"',
          '<b>Published course training case</b><br/>'
          f'EV expected 1,624.87M<br/>Actual <b>{known["ev"]:,.5f}M</b><br/>'
          f'Price expected $27.50<br/>Actual <b>${known["grid"][1][1]:.5f}</b><br/>'
          'All 9 sensitivity cells checked.<br/>25 forecast-year articulation checks.',15)
    panel(444,337,388,213,'EXPECTED -> ACTUAL -> DECISION',
          '<b>WACC +1 percentage point</b><br/>'
          f'{ch["old_wacc"]:.2%} -> {ch["new_wacc"]:.2%}<br/>'
          f'Value <b>${ch["old_price"]:.2f} -> ${ch["new_price"]:.2f}</b><br/>'
          'Expected lower; actual lower.<br/>'
          '<b>WATCH / DEFER remains:</b> market price still fails the entry threshold.',15,PALE)
    panel(850,337,392,213,'HIGH-RISK FAILURE EVIDENCE',
          '<b>Forced cash deficit is rejected:</b><br/>'
          '"cash below floor; explicit funding needed"<br/>'
          '<b>Wrong investment scaling:</b><br/>'
          f'False discounted investment ${bad["wrong_scaling_explicit_ev_drag"]/1000:,.2f}B (~${bad["minimum_wrong_price_drag"]:.2f}/share).<br/>'
          'Bounded diagnostic, not a full alternate valuation.',15)
    rect(38,565,1204,70,fill='#e5edf3')
    text('<b>Controls:</b> cash from CFO + CFI + CFF; equity from retained income; no balancing plugs; g &lt; WACC; SBC cost retained. <b>Evidence boundary:</b> these are technical test results, not proof of an independently authored human prediction or an unseen student run.',
         54,579,1172,14,maxh=48)
    footer(2,[('Actual code',repo+'projects/project-1/model.py'),('Published training case',repo+'lessons/week-03/teach-dcf-worked-example.md'),('Observed validation',validation),('Cold-run log',repo+'projects/project-1/evidence/cold-run-log.md')],
           'Full year 1 FCFF shown before the elapsed valuation-stub adjustment. A PASS on the forced-error test means the invalid input was caught.')
    c.showPage()

    # PAGE3: formal committee defense can remain on this chart throughout.
    header('VIDEO 3 | COMMITTEE DEFENSE','WATCH / DEFER - require price AND evidence',
           'No existing position | 12-24 month decision horizon | Historical Sep 10, 2026 close: $218.36 | Not a current quote')
    rect(38,117,1204,147)
    text('Causal intrinsic range, not confidence limits or a mechanical average',55,128,1168,14,NAVY,True,maxh=22)
    ax0,ax1=85,1197;ay=H-201
    def px(value):return ax0+(ax1-ax0)*value/250
    c.setStrokeColor(colors.HexColor(BORDER));c.setLineWidth(2);c.line(ax0,ay,ax1,ay)
    c.setStrokeColor(colors.HexColor(GREEN));c.setLineWidth(10);c.line(px(lo['per_share']),ay,px(hi['per_share']),ay)
    for value,label,above,color in [(lo['per_share'],f'Low ${lo["per_share"]:.2f}',False,NAVY),
                                   (b['per_share'],f'Base ${b["per_share"]:.2f}',True,GREEN),
                                   (hi['per_share'],f'High ${hi["per_share"]:.2f}',False,NAVY),
                                   (218.36,'Market $218.36',True,ORANGE)]:
        c.setFillColor(colors.HexColor(color));c.circle(px(value),ay,6,fill=1,stroke=0)
        yy=169 if above else 215
        text(label,px(value)-88,yy,176,15,color,True,maxh=23)
    text(f'Conditional base entry ceiling: <= ${b["entry_ceiling"]:.2f} (20% margin of safety) + supported operating / commitment evidence',
         55,239,1168,12,MUTED,maxh=18)
    panel(38,279,388,247,'WHY THIS DCF NEEDS CAUTION',
          f'WACC <b>{b["wacc"]:.2%}</b> | g <b>3%</b> | terminal ROIC <b>25%</b><br/>'
          f'Terminal value: <b>{b["terminal_share"]:.1%} of EV</b>.<br/>'
          f'WACC +1pp -> <b>${ch["new_price"]:.2f}</b>/share.<br/><br/>'
          f'Market price implies <b>+{r["reverse_dcf"]["constant_increment_to_each_dc_growth"]*100:.2f}pp</b> in EVERY DC growth rate, holding other base inputs fixed.<br/>'
          'One conditional solution, not proof the market is wrong.',15)
    panel(444,279,388,247,'WHY METHODS DISAGREE',
          f'<b>DCF causal:</b> ${lo["per_share"]:.2f}-${hi["per_share"]:.2f}<br/>'
          f'<b>Annual P/E:</b> ${min(pe["pe_implied_prices"]):.2f}-${max(pe["pe_implied_prices"]):.2f}<br/>'
          f'<b>EV / annual sales:</b> ${min(pe["ev_sales_implied_prices"]):.2f}-${max(pe["ev_sales_implied_prices"]):.2f}<br/><br/>'
          'Annual earnings lag rapid growth.<br/>AMD: different margins / product mix.<br/>AVGO: software / acquisition mix.<br/>'
          '<b>Two peers; do not average methods.</b>',15)
    panel(850,279,392,247,'WHAT WOULD REVERSE THE ACTION',
          '<b>Review each quarterly filing.</b><br/>'
          'Two quarters DC growth &lt;20%: challenge durability.<br/>'
          'DSO &gt;95 or GM &lt;70%: challenge conversion / profitability.<br/>'
          'Material capacity / guarantee losses: reassess immediately.<br/><br/>'
          '<b>Initiate only with price cushion AND supported demand, margins, collections and funding.</b>',15,PALE)
    rect(38,540,1204,56,fill='#e5edf3')
    text(f'<b>Downside changes action:</b> DC growth 20% ->3%; GM 70% ->66%; DSO 95; supply / guarantee losses -> <b>DO NOT INITIATE (~${lo["per_share"]:.0f})</b>. This adverse-regime risk gate is a declared decision policy.',
         54,550,1172,14,maxh=40)
    text(f'Ownership bridge: operating EV ${b["enterprise_value"]/1000:,.1f}B + net adjustments ${sum(b["bridge"].values())/1000:,.1f}B = equity ${b["equity_value"]/1000:,.1f}B / 24.242B diluted proxy shares = ${b["per_share"]:.2f}.',
         42,610,1196,13,maxh=32)
    footer(3,[('Decision memo',repo+'projects/project-1/Decision-Memo.pdf'),('Executed cases / bridge',results),('Peer policy',repo+'projects/project-1/evidence/peer-policy.md'),('Driver challenges',repo+'projects/project-1/evidence/assumption-challenges.md')],
           'Assumptions and simplified financing / investment recoveries remain challengeable. Refresh market, cap-table and commitment evidence before any trade.')
    c.save()
    doc=pymupdf.open(dest);assert len(doc)==3
    names=['Video-1-Research-Chart','Video-2-Validation-Chart','Video-3-Committee-Chart']
    paths=[]
    for page,name in zip(doc,names):
        path=ROOT/'outputs'/f'{name}.png';page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(path)
        assert all(b[0]>=0 and b[1]>=0 and b[2]<=W+1 and b[3]<=H+1 for b in page.get_text('blocks'))
        paths.append({'file':path.relative_to(ROOT).as_posix(),'width':1920,'height':1080,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    receipt={'status':'PASS','pages':3,'page_points':[W,H],'render_pixels':[1920,1080],
             'pdf_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'pngs':paths,
             'financial_results_unchanged_sha256':hashlib.sha256((ROOT/'outputs/results.json').read_bytes()).hexdigest(),
             'scope':'Fixed recording charts; underlying original evidence remains linked; technical Video2 still needs a recorded run'}
    write=ROOT/'outputs/recording-charts-audit.json';write.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
