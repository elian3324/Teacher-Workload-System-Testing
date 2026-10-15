from pathlib import Path
import json, re
import pypdfium2 as pdf
from PIL import Image, ImageOps, ImageDraw

ROOT=Path(__file__).resolve().parent
render=ROOT/'render'
data=json.loads((ROOT/'业务流程信息梳理.json').read_text(encoding='utf-8'))
d=pdf.PdfDocument(render/'acceptance_qa.pdf')
assert len(d)==len(data['steps'])+2,(len(d),len(data['steps'])+2)
checks=[]
for i,page in enumerate(d):
    text=page.get_textpage().get_text_range()
    if i>=2:
        step=data['steps'][i-2]
        assert re.search(r'步骤\s*'+f'{step["number"]:03d}',text),('wrong page',i+1)
        assert '操作说明' in text and '验收记录' in text and '原图' in text,('missing content',i+1)
    out=render/f'page-{i+1:03d}.png'
    page.render(scale=1.5).to_pil().save(out)
    checks.append({'page':i+1,'step':i-1 if i>=2 else None,'text_chars':len(text)})
for batch,start in enumerate(range(0,len(d),16),1):
    sheet=Image.new('RGB',(1920,2560),'#dfe3e7');draw=ImageDraw.Draw(sheet)
    for k,index in enumerate(range(start,min(start+16,len(d)))):
        im=Image.open(render/f'page-{index+1:03d}.png').convert('RGB')
        im.thumbnail((470,600))
        x=(k%4)*480+(480-im.width)//2;y=(k//4)*640+26
        sheet.paste(im,(x,y));draw.text(((k%4)*480+12,(k//4)*640+5),f'Page {index+1:03d}',fill='black')
    sheet.save(render/f'overview-{batch:02d}.jpg',quality=94)
(ROOT/'分页核查.json').write_text(json.dumps({'pages':len(d),'step_pages':len(data['steps']),'page_text_checks':checks,'source_records_mapped':data['covered_source_records'],'browser_used_for_rewrite':False},ensure_ascii=False,indent=2),encoding='utf-8')
print('pages',len(d),'all step titles, descriptions, results and figures present','overview sheets',(len(d)+15)//16)
