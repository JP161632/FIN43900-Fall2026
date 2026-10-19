"""Render every final PDF page and record bounding/text checks. Requires PyMuPDF."""
import hashlib
import json
from pathlib import Path
import pymupdf as fitz

ROOT=Path(__file__).resolve().parent


def main():
    target=ROOT/'.build'/'pdf-qa'; target.mkdir(parents=True,exist_ok=True)
    allpages=[]; records=[]
    for name in ('Research-Evolution','Decision-Memo','Validation-and-AI-Use'):
        path=ROOT/f'{name}.pdf'; doc=fitz.open(path)
        pages=[]
        for i,page in enumerate(doc):
            png=target/f'{name}-{i+1}.png'
            page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(png)
            allpages.append(png)
            blocks=page.get_text('blocks')
            bad=[b[:4] for b in blocks if b[0]<0 or b[1]<0 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1]
            assert not bad,(name,i,bad)
            text=page.get_text()
            assert len(text.strip())>80,(name,i,'Unexpected empty page')
            pages.append({'page':i+1,'text_characters':len(text),'out_of_page_blocks':bad})
        records.append({'file':f'{name}.pdf','pages':len(doc),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                        'page_checks':pages})
    # A contact sheet permits visual review of every page, in addition to full-page PNGs.
    from PIL import Image,ImageOps,ImageDraw
    width=612; height=810
    canvas=Image.new('RGB',(width*3,height*((len(allpages)+2)//3)),(225,230,236))
    draw=ImageDraw.Draw(canvas)
    for j,path in enumerate(allpages):
        im=Image.open(path).convert('RGB'); im.thumbnail((width-12,height-30))
        x=(j%3)*width+6; y=(j//3)*height+24
        canvas.paste(im,(x,y)); draw.text((x,y-19),path.stem,fill=(15,30,45))
    canvas.save(target/'all-pages.png')
    (ROOT/'outputs'/'pdf-qa.json').write_text(json.dumps({'status':'rendered; visual review recorded in rubric audit',
        'total_pages':len(allpages),'files':records},indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'Rendered {len(allpages)} pages; page bounds and nonempty text PASS; contact sheet .build/pdf-qa/all-pages.png')


if __name__=='__main__': main()
