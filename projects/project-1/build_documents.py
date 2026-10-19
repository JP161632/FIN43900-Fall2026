"""Render the three Markdown sources to required PDFs and verify page/text bounds.

Optional documentation packages only; the valuation engine remains dependency-free.
Run from this project: python build_documents.py
"""
import html
import re
import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                               PageBreak, KeepTogether)

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


def styles():
    s=getSampleStyleSheet()
    for key in ['Normal','BodyText']:
        s[key].fontName='Helvetica'
        s[key].fontSize=9.7
        s[key].leading=13
        s[key].spaceAfter=7
        s[key].textColor=colors.HexColor('#15283c')
    s['Title'].fontName='Helvetica-Bold'; s['Title'].fontSize=20; s['Title'].leading=24
    s['Title'].textColor=colors.black; s['Title'].spaceAfter=13
    s['Heading2'].fontSize=12; s['Heading2'].leading=15; s['Heading2'].spaceBefore=10; s['Heading2'].spaceAfter=6
    s['Heading2'].textColor=colors.HexColor('#15283c')
    s.add(ParagraphStyle(name='Cell',fontName='Helvetica',fontSize=8.6,leading=11,spaceAfter=0,textColor=colors.HexColor('#15283c'),wordWrap='CJK'))
    s.add(ParagraphStyle(name='CellHead',parent=s['Cell'],fontName='Helvetica-Bold',textColor=colors.white))
    return s


def story_from_md(text,s):
    story=[]; lines=text.splitlines(); i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1; continue
        if line=='<!-- pagebreak -->': story.append(PageBreak()); i+=1; continue
        if line.startswith('|'):
            block=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',x or '-') for x in cells): block.append(cells)
                i+=1
            count=len(block[0]); width=504
            ratios=([.20,.40,.40] if count==3 else [.20,.25,.30,.25] if count==4 else [1/count]*count)
            data=[[Paragraph(inline(c),s['CellHead' if ri==0 else 'Cell']) for c in row] for ri,row in enumerate(block)]
            t=Table(data,colWidths=[width*x for x in ratios],repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#173853')),
                                   ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),
                                   ('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
                                   ('BOTTOMPADDING',(0,0),(-1,-1),6),
                                   ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f3f6f9'),colors.white]),
                                   ('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cbd5df'))]))
            story.extend([t,Spacer(1,8)]); continue
        if line.startswith('# '): story.append(Paragraph(inline(line[2:]),s['Title'])); i+=1; continue
        if line.startswith('## '): story.append(Paragraph(inline(line[3:]),s['Heading2'])); i+=1; continue
        para=[line]; i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].strip().startswith(('#','|','<!--')):
            para.append(lines[i].strip()); i+=1
        story.append(Paragraph(inline(' '.join(para)),s['BodyText']))
    return story


def footer(canvas,doc):
    canvas.saveState(); canvas.setFont('Helvetica',8); canvas.setFillColor(colors.HexColor('#526477'))
    canvas.drawString(54,30,'Project 1 NVIDIA | Historical valuation 2026-09-10 | AI use disclosed')
    canvas.drawRightString(558,30,str(doc.page)); canvas.restoreState()


def main():
    s=styles()
    for stem,name in PAIRS:
        source=ROOT/'docs'/f'{stem}.md'; dest=ROOT/f'{name}.pdf'
        doc=SimpleDocTemplate(str(dest),pagesize=letter,rightMargin=54,leftMargin=54,topMargin=44,bottomMargin=48,
                              title=name.replace('-',' '),author='Course equity research analyst')
        doc.build(story_from_md(source.read_text(encoding='utf-8'),s),onFirstPage=footer,onLaterPages=footer)
        shutil.copyfile(dest,ROOT/'docs'/f'{stem}.pdf')
    from pypdf import PdfReader
    for stem,name in PAIRS:
        r=PdfReader(ROOT/f'{name}.pdf')
        assert len(r.pages)>0 and all((p.extract_text() or '').strip() for p in r.pages)
        if stem=='decision-memo': assert len(r.pages)<=2, f'Memo too long: {len(r.pages)} pages'
        assert (ROOT/f'{name}.pdf').read_bytes()==(ROOT/'docs'/f'{stem}.pdf').read_bytes()
        print(f'{name}.pdf: {len(r.pages)} pages; content-equivalent source docs/{stem}.md; identical repository PDF copy')


if __name__=='__main__': main()
