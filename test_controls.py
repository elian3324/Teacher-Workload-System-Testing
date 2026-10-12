from ui_test_support.bootstrap import use_project_python
use_project_python()
import re
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.query
def test_column_visibility_round_trip(page):
    page.open("teacher")
    def has_email():
        return any(e.text.strip() == "邮箱" for e in page.visible(By.CSS_SELECTOR, "th", page.content))
    assert has_email()
    page.click("列筛选")
    popover = page.wait.until(lambda d: next((e for e in page.visible(By.CSS_SELECTOR, '[role="tooltip"]')
        if "勾选显示的列" in e.text), False))
    label = next(e for e in page.visible(By.CSS_SELECTOR, "label.el-checkbox", popover) if e.text.strip() == "邮箱")
    try:
        label.click()
        page.wait.until(lambda d: not has_email())
    finally:
        if not has_email():
            label.click()
            page.wait.until(lambda d: has_email())
        page.click("列筛选")


@pytest.mark.consistency
def test_compliance_summary_counts_balance(page):
    page.open("compliance")
    page.tab("实际版")
    # 每种合同类型：达标 + 不达标必须等于教师数。
    page.wait.until(lambda d: bool(page.rows()))
    summaries = []
    for row in page.rows():
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 8 and cells[0].text.strip():
            summaries.append(cells)
    assert summaries, "没有合同类型汇总数据"
    for cells in summaries:
        total, passed, failed = [int(c.text.strip()) for c in cells[1:4]]
        assert total == passed + failed, f"合同类型 {cells[0].text} 的汇总数量不一致"


@pytest.mark.query
@pytest.mark.parametrize("button,target", [
    ("查看更多待办", "/hss-task/index"),
    ("查看同步详情", "/hss-settlement/index"),
])
def test_home_shortcut_target(page, button, target):
    page.open("home")
    page.click(button)
    page.wait.until(lambda d: target in d.current_url)
    page.idle()


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
