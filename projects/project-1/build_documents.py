"""Render the three Markdown sources to required PDFs and verify page/text bounds.

Optional documentation packages only; the valuation engine remains dependency-free.
Run from this project: python build_documents.py
"""
import html
import re
import shutil
from pathlib import Path
from functools import partial

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                               PageBreak, KeepTogether, ListFlowable, ListItem)

ROOT=Path(__file__).resolve().parent
PAIRS=[('research-evolution','Research-Evolution'),('decision-memo','Decision-Memo'),
       ('validation-and-ai-use','Validation-and-AI-Use')]


def ascii_text(text):
    replacements={'\u2014':' - ','\u2013':'-','\u2011':'-','\u2212':'-','\u2019':"'",'\u2018':"'",
                  '\u201c':'"','\u201d':'"','\u2265':'>=','\u2264':'<=','\u0394':'change ',
                  '\u00d7':'x','\u2192':'to','\u00b7':' / ','\u00a0':' '}
    for a,b in replacements.items(): text=text.replace(a,b)
    return text


def inline(text):
    text=html.escape(ascii_text(text))
    text=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:'<link href="'+m.group(2)+'" color="#0759a0">'+m.group(1)+'</link>',text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'`([^`]+)`',r'<font name="Courier" size="8">\1</font>',text)
    return text


def styles(compact=False):
    s=getSampleStyleSheet()
    for key in ['Normal','BodyText']:
        s[key].fontName='Helvetica'
        s[key].fontSize=9.8 if compact else 10.0
        s[key].leading=13.1 if compact else 13.5
        s[key].spaceAfter=7
        s[key].textColor=colors.HexColor('#15283c')
    s['Title'].fontName='Helvetica-Bold'; s['Title'].fontSize=24; s['Title'].leading=28
    s['Title'].alignment=TA_LEFT; s['Title'].textColor=colors.HexColor('#173853'); s['Title'].spaceAfter=12
    s['Heading2'].fontName='Helvetica-Bold';s['Heading2'].fontSize=12; s['Heading2'].leading=15; s['Heading2'].spaceBefore=11; s['Heading2'].spaceAfter=6
    s['Heading2'].textColor=colors.HexColor('#28592e')
    s.add(ParagraphStyle(name='Cell',fontName='Helvetica',fontSize=8.8,leading=11.5,spaceAfter=0,textColor=colors.HexColor('#15283c'),splitLongWords=True))
    s.add(ParagraphStyle(name='CellHead',parent=s['Cell'],fontName='Helvetica-Bold',textColor=colors.white))
    s.add(ParagraphStyle(name='Metric',fontName='Helvetica-Bold',fontSize=13.3,leading=17,textColor=colors.HexColor('#28592e')))
    s.add(ParagraphStyle(name='Small',parent=s['BodyText'],fontSize=8.4,leading=11,textColor=colors.HexColor('#526477')))
    s.add(ParagraphStyle(name='BulletText',parent=s['BodyText'],leftIndent=10,firstLineIndent=-10,spaceAfter=5))
    return s


def story_from_md(text,s):
    story=[]; lines=text.splitlines(); i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line=='<!-- pagebreak -->': story.append(PageBreak()); i+=1; continue
        if line.startswith('<!--'): i+=1; continue
        if line.startswith('|'):
            block=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',x or '-') for x in cells): block.append(cells)
                i+=1
            count=len(block[0]); width=512
            metric=block[0][0] in ['Causal range','Earlier Lab 5 base']
            ratios=([.27,.10,.63] if count==3 and block[0][1]=='Result' else
                    [.25,.42,.33] if count==3 and block[0][0]=='AI use' else
                    [.25,.37,.38] if count==3 else [.25]*4 if count==4 else [.30,.70] if count==2 else [1/count]*count)
            data=[[Paragraph(inline(c),s['CellHead' if ri==0 else 'Metric' if metric else 'Cell']) for c in row] for ri,row in enumerate(block)]
            t=Table(data,colWidths=[width*x for x in ratios],repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#173853')),
                                   ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),
                                   ('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
                                   ('BOTTOMPADDING',(0,0),(-1,-1),6),
                                   ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f3f6f9'),colors.white]),
                                   ('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cbd5df'))]))
            if metric:t.setStyle(TableStyle([('BACKGROUND',(0,1),(-1,-1),colors.HexColor('#eff5e9')),('TOPPADDING',(0,1),(-1,-1),10),('BOTTOMPADDING',(0,1),(-1,-1),10)]))
            story.extend([t,Spacer(1,8)]); continue
        if line.startswith('# '): story.append(Paragraph(inline(line[2:]),s['Title'])); i+=1; continue
        if line.startswith('## '): story.append(Paragraph(inline(line[3:]),s['Heading2'])); i+=1; continue
        if line.startswith('- '):
            story.append(Paragraph('&#8226; '+inline(line[2:]),s['BulletText']));i+=1;continue
        if re.match(r'^\d+\. ',line):
            story.append(Paragraph(inline(line),s['BulletText']));i+=1;continue
        if line.startswith('> '):
            story.append(Paragraph(inline(line[2:]),s['BodyText']));i+=1;continue
        para=[line]; i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].strip().startswith(('#','|','<!--')):
            para.append(lines[i].strip()); i+=1
        content=' '.join(para)
        style=s['Small'] if content.startswith(('Sources:','Evidence locations:')) else s['BodyText']
        story.append(Paragraph(inline(content),style))
    return story


def footer(canvas,doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#173853'));canvas.rect(0,778,612,14,fill=1,stroke=0)
    canvas.setFont('Helvetica-Bold',8);canvas.setFillColor(colors.HexColor('#173853'))
    canvas.drawString(50,757,'NVDA  /  CORPORATE FINANCE APPLICATION')
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#526477'))
    canvas.drawRightString(562,757,'PROJECT 1  |  OCTOBER 19, 2026')
    canvas.setStrokeColor(colors.HexColor('#b6cb9d'));canvas.setLineWidth(1);canvas.line(50,746,562,746)
    canvas.setStrokeColor(colors.HexColor('#d2dde5'));canvas.line(50,42,562,42)
    canvas.setFont('Helvetica',7.5);canvas.drawString(50,28,'Historical valuation: September 10, 2026  |  USD  |  AI assistance disclosed')
    canvas.drawRightString(562,28,f'{doc.page}'); canvas.restoreState()


def main():
    for stem,name in PAIRS:
        s=styles(compact=stem=='decision-memo')
        source=ROOT/'docs'/f'{stem}.md'; dest=ROOT/f'{name}.pdf'
        doc=SimpleDocTemplate(str(dest),pagesize=letter,rightMargin=50,leftMargin=50,topMargin=60,bottomMargin=55,
                              title=name.replace('-',' '),author='Course equity research analyst')
        doc.build(story_from_md(source.read_text(encoding='utf-8'),s),onFirstPage=footer,onLaterPages=footer,
                  canvasmaker=partial(canvas.Canvas,invariant=1))
        shutil.copyfile(dest,ROOT/'docs'/f'{stem}.pdf')
    from pypdf import PdfReader
    for stem,name in PAIRS:
        r=PdfReader(ROOT/f'{name}.pdf')
        assert len(r.pages)>0 and all((p.extract_text() or '').strip() for p in r.pages)
        if stem=='decision-memo': assert len(r.pages)<=2, f'Memo too long: {len(r.pages)} pages'
        assert (ROOT/f'{name}.pdf').read_bytes()==(ROOT/'docs'/f'{stem}.pdf').read_bytes()
        print(f'{name}.pdf: {len(r.pages)} pages; content-equivalent source docs/{stem}.md; identical repository PDF copy')


if __name__=='__main__': main()
