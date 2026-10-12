"""二级导入弹窗、结转详情及表格切换。"""
from ui_test_support.bootstrap import use_project_python
use_project_python()
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.forms
@pytest.mark.parametrize("tab,button,anchor", [
    ("co-list", "新增课程代码", "添加课程代码"),
    ("SIS同步明细", "SIS数据导入", "CUSZ_CRSE_SUMMARY_PG"),
    ("SIS同步明细", "SIS课时导入", "TIME_INSTRUCTOR"),
])
def test_settlement_secondary_dialog_can_cancel(page, tab, button, anchor):
    page.open("settlement")
    page.tab(tab)
    page.click(button)
    page.expect_text(anchor, scope=page.dialog())
    page.close_dialog("取消")


@pytest.mark.query
def test_carryover_detail(page):
    page.open("course")
    page.tab("跨学年结转")
    page.click("详情")
    page.expect_text("结转时数详情", "有效标准", "本学年课时减免", "结算明细来源", scope=page.dialog())
    page.close_dialog("关闭")


@pytest.mark.tabs
@pytest.mark.parametrize("pid,tab,choice,anchors", [
    ("course", "计划版", "按课程明细", ["LEC h/w", "TUT h/w", "授课权重"]),
    ("settlement", "工作量明细", "按教师汇总", ["课程数", "工作量 (hrs)"]),
])
def test_detail_and_teacher_views(page, pid, tab, choice, anchors):
    page.open(pid)
    page.tab(tab)
    label = page.wait.until(lambda d: next((e for e in page.visible(By.TAG_NAME, "label", page.content)
        if e.text.strip() == choice), False))
    label.click()
    page.wait.until(lambda d: label.find_element(By.CSS_SELECTOR, 'input[type="radio"]').is_selected())
    page.expect_text(*anchors)


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
