from pathlib import Path
import json, zipfile, re

root=Path(__file__).resolve().parent
rows=[r for r in json.loads((root/'执行结果.json').read_text(encoding='utf-8-sig')) if not r['id'].startswith('SYS-')]
(root/'范围内执行结果.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''教师工作量系统业务测试报告 2026年10月14日

先完整解压，再打开“测试报告及截图.html”，可按状态和关键字筛选。
点击截图打开原图并放大，screenshots和evidence目录需保留原位置。
Word版用于提交结论，HTML版提供完整步骤和全部范围内记录。

当前结论：部分流程通过，存在22项合并缺陷，未满足全部流程通过条件。
系统管理六个模块已排除，不计统计。147条范围内记录含复测和清理，不能解释为全功能覆盖率。
早期终审截图可能停留于确认弹窗，最终通过证据使用FLOW-FINAL-RECHECK。
本轮草稿学年删除失败，需协助清理；详情见Word及数据变更台账。
'''
(root/'阅读说明.txt').write_text(readme,encoding='utf-8')
files={root/n for n in ['教师工作量系统业务测试报告_20261014.docx','测试报告及截图.html','范围内执行结果.json','范围内执行明细.csv','缺陷清单.json','截图索引.json','数据变更台账.json','范围调整.md','阅读说明.txt']}
for r in rows:
    files.add(root/r['evidence']);files.add(root/r['screenshot'])
files.add(root/'evidence/CONFIG-YEAR03-console.json')
for p in files:
    if not p.exists():raise RuntimeError('Missing file '+str(p))
# Ensure every relative evidence and screenshot link in the HTML resolves.
h=(root/'测试报告及截图.html').read_text(encoding='utf-8')
links=re.findall(r'(?:href|src)="((?:screenshots|evidence)/[^\"]+)"',h)
assert all((root/x).is_file() for x in links)
out=root/'教师工作量系统测试报告及原始截图_20261014.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(files):z.write(p,p.relative_to(root).as_posix())
with zipfile.ZipFile(out) as z:assert z.testzip() is None
(root/'交付核查.json').write_text(json.dumps({'word_pages':7,'word_visual_review':'7页逐页查看，无裁切、重叠或标题装饰线；截图保留原始文件','renderer':'render_docx.py因缺少LibreOffice未成功，改用已安装Word的原生PDF导出及pypdfium2逐页渲染检查','in_scope_records':len(rows),'excluded_system_management_records':23,'defects':22,'screenshot_links_resolve':True,'zip_integrity':'passed','archive_files':len(files),'archive_bytes':out.stat().st_size},ensure_ascii=False,indent=2),encoding='utf-8')
print('in_scope_records',len(rows),'archive_files',len(files),'zip_bytes',out.stat().st_size)
