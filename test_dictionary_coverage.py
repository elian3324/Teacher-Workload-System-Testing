"""由真实 UI 分页发现并检查全部字典数据实例，避免遗漏二级数据页。"""
from ui_test_support.bootstrap import use_project_python
use_project_python()
import json
from datetime import datetime
from urllib.parse import urlsplit
import pytest
from selenium.webdriver.common.by import By
from ui_test_support.settings import REPORTS


@pytest.mark.query
def test_all_dictionary_data_pages(page):
    page.open("dict")
    links = {}
    while True:
        page.wait.until(lambda d: bool(page.rows()))
        for row in page.rows():
            for link in row.find_elements(By.CSS_SELECTOR, 'a[href^="/dict/type/data/"]'):
                cells = row.find_elements(By.TAG_NAME, "td")
                links[link.get_attribute("href")] = cells[2].text
        next_button = page.button("下一页")
        if not next_button.is_enabled():
            break
        first = page.rows()[0].text
        page.click("下一页")
        page.wait.until(lambda d: page.rows() and page.rows()[0].text != first)
    total_text = page.visible(By.CSS_SELECTOR, ".el-pagination__total", page.content)[0].text
    import re
    expected = int(re.search(r"\d+", total_text).group())
    assert len(links) == expected, "字典列表分页发现数量不完整"
    covered = []
    try:
        for url, name in links.items():
            page.driver.get(url)
            page.idle()
            page.expect_text("字典标签", "字典键值", "字典编码")
            assert urlsplit(page.driver.current_url).path == urlsplit(url).path
            covered.append({"name": name, "path": urlsplit(url).path, "status": "passed"})
    finally:
        REPORTS.mkdir(parents=True, exist_ok=True)
        (REPORTS / "dictionary_coverage.json").write_text(json.dumps({
            "checked_at": datetime.now().isoformat(), "discovered": len(links),
            "completed": len(covered), "pages": covered}, ensure_ascii=False, indent=2), encoding="utf-8")
    assert len(covered) == expected


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
