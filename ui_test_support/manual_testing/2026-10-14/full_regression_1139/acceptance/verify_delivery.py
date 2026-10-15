from pathlib import Path
import json, re, base64, hashlib, zipfile
from html.parser import HTMLParser

OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'业务流程信息梳理.json').read_text(encoding='utf-8'))
manifest=json.loads((OUT/'原始截图清单.json').read_text(encoding='utf-8'))
expected={v['sha256'] for v in manifest.values()}
report=OUT/'教师工作量系统业务流程验收报告_逐步原图版.html'
text=report.read_text(encoding='utf-8')
class Check(HTMLParser):
    def __init__(self):super().__init__();self.articles=0;self.images=[];self.external=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='article':self.articles+=1
        if tag=='img' and 'src' in a:self.images.append(a['src'])
        if tag in ['script','link'] and ('src' in a or 'href' in a):self.external.append(a)
c=Check();c.feed(text)
assert c.articles==len(data['steps'])
assert not c.external
actual={hashlib.sha256(base64.b64decode(u.split(',',1)[1])).hexdigest() for u in c.images}
assert actual==expected, 'HTML截图与原始文件不一致'
docfile=OUT/'教师工作量系统业务流程验收报告_20261014.docx'
with zipfile.ZipFile(docfile) as z:
    media=[n for n in z.namelist() if n.startswith('word/media/')]
    assert all(hashlib.sha256(z.read(n)).hexdigest() in expected for n in media), 'Word图片被压缩或转换'
    xml=z.read('word/document.xml').decode()
    assert xml.count('<wp:inline')==len(data['steps'])
readme='''教师工作量系统业务流程验收报告

1. Word版按业务步骤逐页说明，每一步配图，方便提交及批注。
2. 原图版HTML为独立文件，可直接用Edge打开，不需要登录系统，也不需要其他附件目录。
3. HTML中点击图片可放大，再点“切换原始尺寸”查看清晰原图；可按业务目录跳转。
4. 预览和确认框按操作过程留图，最终状态以回读及后续节点证据共同确认。
5. 上游阻塞处明确标注未执行；报告没有把这些步骤写成通过。
6. 本次只复用已有记录与截图，没有重新操作业务系统。
'''
(OUT/'阅读说明.txt').write_text(readme,encoding='utf-8')
archive=OUT/'教师工作量系统业务流程验收报告_20261014.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in [docfile,report,OUT/'业务流程步骤索引.csv',OUT/'阅读说明.txt']:
        z.write(p,p.name)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
quality=dict(business_steps=len(data['steps']),source_records=data['covered_source_records'],word_pages=112,word_images=len(data['steps']),unique_html_originals=len(actual),html_self_contained=True,all_html_images_match_originals=True,all_word_images_match_originals=True,word_render_method='原生Word导出加pypdfium2逐页渲染；系统无LibreOffice',visual_review='112页版式总览及首页、终审、结算和阻塞示例页检查；无空白溢出页，标题说明结果图注齐全',browser_operated=False,archive_integrity='passed')
(OUT/'交付核查.json').write_text(json.dumps(quality,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(quality,ensure_ascii=False))
