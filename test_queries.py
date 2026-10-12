from ui_test_support.bootstrap import use_project_python
use_project_python()
import pytest
from selenium.webdriver.common.by import By
from ui_test_support.catalog import SEARCHES


@pytest.mark.query
@pytest.mark.parametrize("page_id,placeholder", SEARCHES, ids=[p for p,_ in SEARCHES])
def test_search_empty_and_reset(page, page_id, placeholder):
    page.open(page_id)
    original = len(page.rows())
    assert original > 0, "此用例需要至少一条已有记录以验证重置恢复"
    page.fill(placeholder, "__UI_TEST_NO_MATCH_20261012__")
    page.click("搜索")
    page.wait.until(lambda d: not page.rows(), "不存在关键字仍返回了列表记录")
    page.expect_text("暂无数据")
    page.click("重置")
    page.wait.until(lambda d: len(page.rows()) == original, "重置后未恢复原列表")
    assert page.input(placeholder).get_attribute("value") == ""


@pytest.mark.query
@pytest.mark.parametrize("page_id", ["teacher", "special_course", "user", "role", "dict"])
def test_pagination_round_trip(page, page_id):
    page.open(page_id)
    page.wait.until(lambda d: bool(page.rows()))
    first = page.rows()[0].text
    assert not page.button("上一页").is_enabled()
    page.click("下一页")
    page.wait.until(lambda d: bool(page.rows()) and page.rows()[0].text != first)
    assert page.button("上一页").is_enabled()
    page.click("上一页")
    page.wait.until(lambda d: bool(page.rows()) and page.rows()[0].text == first)
    assert not page.button("上一页").is_enabled()


@pytest.mark.query
def test_workload_teacher_detail(page):
    page.open("query")
    page.tab("管理查询")
    page.wait.until(lambda d: bool(page.rows()))
    cells = page.rows()[0].find_elements(By.TAG_NAME, "td")
    teacher, staff_id = cells[0].text.strip(), cells[1].text.strip()
    page.click("详情")
    page.expect_text(f"{teacher} Staff ID: {staff_id} - 课程明细", "课程代码", "总工作量")


@pytest.mark.query
def test_compliance_reduction_detail(page):
    page.open("compliance")
    page.tab("实际版")
    page.click("减免详情")
    page.expect_text("合同原标准", "有效标准", "减免扣减", scope=page.dialog())
    page.close_dialog("关闭")


@pytest.mark.query
def test_settlement_calculation_detail(page):
    page.open("settlement")
    page.tab("计划vs实际对比")
    page.click("查看详情")
    page.expect_text("最终工作量", "授课权重", "计算步骤", "审计追溯", scope=page.dialog())
    page.close_dialog("关闭此对话框")


@pytest.mark.forms
def test_settlement_adjustment_can_cancel(page):
    page.open("settlement")
    page.tab("计划vs实际对比")
    page.click("调整")
    page.expect_text("Days&Time", "最终工作量", "课程数", "调整原因", scope=page.dialog())
    page.close_dialog("取消")


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
