from pathlib import Path
from docx import Document
from docx.shared import Pt

f=Path(__file__).resolve().parent/'教师工作量系统业务流程验收报告_分级排版版.docx'
d=Document(f)
ps=d.paragraphs
count=0
for i,p in enumerate(ps[:-1]):
    if not p.text and p._p.xpath('.//w:fldChar[@w:fldCharType="end"]') and ps[i+1].style.name=='Heading 1':
        p.paragraph_format.space_before=Pt(0)
        p.paragraph_format.space_after=Pt(0)
        p.paragraph_format.line_spacing=Pt(1)
        p.paragraph_format.keep_with_next=False
        for r in p.runs:r.font.size=Pt(1)
        for marker in p._p.xpath('.//w:lastRenderedPageBreak'):marker.getparent().remove(marker)
        count+=1
d.save(f)
print('TOC tail normalized',count)
