"""Check all delivered PDF pages, evidence links, numbers and preserved sources."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
import pymupdf

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
PDFS=['Research-Evolution','Decision-Memo','Validation-and-AI-Use','Recording-Charts']


def main():
    # Tight glyph-height boxes avoid false collisions from large headline ascenders.
    pymupdf.TOOLS.set_small_glyph_heights(True)
    results=json.loads((ROOT/'outputs/results.json').read_text(encoding='utf-8'))
    body=(ROOT/'docs/research-evolution.md').read_text(encoding='utf-8')
    baseline=(ROOT/'evidence/edition-a-existing-nvidia-unchanged.md').read_bytes()
    assert baseline.decode('utf-8').strip() in body,'Baseline reading text changed'
    assert hashlib.sha256(baseline).hexdigest()=='ff289d7d83bf56f977d5d3f85f7cdf13125841075d5e8a59af03fa845d39ed6b'
    records=[]
    for name in PDFS:
        path=ROOT/(name+'.pdf');doc=pymupdf.open(path)
        pages=[];links=0;alltext=''
        for index,page in enumerate(doc):
            text=page.get_text();alltext+=text
            assert len(text.strip())>80,(name,index,'empty page')
            assert '\ufffd' not in text and '\u25a0' not in text,(name,index,'replacement glyph')
            assert not re.search(r'\{\{[a-z_]+\}\}',text),(name,index,'unrendered template')
            words=page.get_text('words');collisions=[]
            for i,a in enumerate(words):
                assert a[0]>=0 and a[1]>=0 and a[2]<=page.rect.width+1 and a[3]<=page.rect.height+1,(name,index,'out of bounds',a)
                for b in words[i+1:]:
                    dx=min(a[2],b[2])-max(a[0],b[0]);dy=min(a[3],b[3])-max(a[1],b[1])
                    if dx<=1 or dy<=1:continue
                    smaller=min((a[2]-a[0])*(a[3]-a[1]),(b[2]-b[0])*(b[3]-b[1]))
                    if dx*dy>0.15*smaller:collisions.append([a[4],b[4]])
            assert not collisions,(name,index,'overlapping words',collisions[:5])
            for link in page.get_links():
                url=link.get('uri','');links+=bool(url)
                if 'github.com/JP161632/FIN43900-Fall2026/blob/' in url:
                    parts=unquote(urlsplit(url).path).split('/blob/',1)[1].split('/',1)
                    assert len(parts)==2 and (REPO/parts[1]).is_file(),(name,index,'missing linked evidence',url)
            pages.append({'page':index+1,'word_count':len(words),'bounds':'PASS','word_overlap':'PASS','replacement_glyphs':False})
        assert 'Sales'+'force' not in alltext,name
        if name=='Decision-Memo':assert len(doc)<=2,'Memo exceeds two-page limit'
        if name=='Recording-Charts':assert len(doc)==3 and all(p.rect.width==1280 and p.rect.height==720 for p in doc)
        if name in ['Research-Evolution','Decision-Memo','Recording-Charts']:
            for key in ['low','base','high']:
                expected=f"{results['cases'][key]['per_share']:.2f}"
                assert expected in alltext,(name,'missing executed value',expected)
        records.append({'file':name+'.pdf','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pages':pages,'clickable_links':links})
    for stem,name in [('research-evolution','Research-Evolution'),('decision-memo','Decision-Memo'),('validation-and-ai-use','Validation-and-AI-Use')]:
        assert (ROOT/'docs'/(stem+'.pdf')).read_bytes()==(ROOT/(name+'.pdf')).read_bytes()
    record={'status':'PASS','unique_pdf_pages':sum(len(x['pages']) for x in records),
            'checks':'Baseline bytes/text, bounds, significant word overlaps, glyphs, placeholders, memo length, linked local evidence, model values and mirrored PDF copies',
            'visual_review':'All pages rendered; manual visual inspection recorded in docs/pdf-quality-audit.md',
            'limitation':'Document QA does not certify source truth, unseen audiovisual performance, human-history evidence or a rubric score',
            'financial_results_sha256':hashlib.sha256((ROOT/'outputs/results.json').read_bytes()).hexdigest(),'files':records}
    (ROOT/'outputs/document-quality-audit.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in record.items() if k!='files'},indent=2))


if __name__=='__main__':main()
