from ui_test_support.bootstrap import use_project_python
use_project_python()
import re
import pytest
from selenium.webdriver.common.by import By


CONDITIONS = [
    ("工作量计算规则", "上课频率系数", "上课模式(每周/隔周)", "每周", "每周上课系数", 1),
    ("工作量计算规则", "上课频率系数", "上课模式(每周/隔周)", "隔周", "隔周上课系数", 0.5),
    *[("课时计算", "分钟取整规则", "超出整点的分钟数", str(n), rule, value)
      for n,rule,value in [(0,"低于阈值舍去",0),(9,"低于阈值舍去",0),
          (20,"≥30分钟取半",0.5),(49,"≥30分钟取半",0.5),(50,"≥10分钟靠整",1),(59,"≥10分钟靠整",1)]],
    ("SCH计算规则", "评分基础权重", "评分基础(DPF/PU/ADF)", "DPF", "通过/失败评分权重(DPF)", 0.8),
    ("SCH计算规则", "评分基础权重", "评分基础(DPF/PU/ADF)", "ADF", "等级制评分权重(A-D,F)", 1),
    ("SCH计算规则", "评分基础权重", "评分基础(DPF/PU/ADF)", "PU", "及格/不及格权重(P/U)", 1),
    ("SCH计算规则", "课程类型系数", "课程类型(CEC/TRA/SUP)", "CEC", "常规学分课系数", 1),
    ("SCH计算规则", "课程类型系数", "课程类型(CEC/TRA/SUP)", "TRA", "培训旁听课系数", 0.5),
]


@pytest.mark.calculation
@pytest.mark.parametrize("category,group,field,value,matched,coefficient", CONDITIONS,
    ids=[f"{group}-{value}" for _,group,_,value,_,_ in CONDITIONS])
def test_rule_condition_result(page, category, group, field, value, matched, coefficient):
    page.open("rule")
    region = page.expand_rule(category, group)
    page.click("条件测试", scope=region)
    dialog = page.dialog()
    page.fill_label(field, value, scope=dialog)
    page.click("执行测试", scope=dialog)
    page.expect_text("测试完成", scope=dialog)
    text = dialog.text
    assert f'[匹配] {matched}: 条件满足' in text
    assert re.search(r"系数值\s*[:：]\s*" + re.escape(str(coefficient)) + r"(?:\D|$)", text)
    page.close_dialog("取消")


@pytest.mark.calculation
@pytest.mark.parametrize("time,expected", [("Tues:18:00-20:50", 3), ("Mon:10:00-11:20", 1.5)])
def test_engine_trial_result(page, time, expected):
    page.open("rule")
    page.tab("测试计算引擎")
    page.fill("例如：PSY101", "PSY101")
    page.fill("例如：Tues:18:00-20:50", time)
    page.fill("例如：2410（常规学期）或 2450（Summer）", "2410")
    page.fill_label("Enrolled (选课人数)", 30)
    page.click("试算")
    page.expect_text("试算结果汇总", "计算状态", "成功", "Step 5")
    labels = page.visible(By.CSS_SELECTOR, ".el-descriptions__label", page.content)
    final = next(e for e in labels if e.text.strip() == "最终工作量")
    number = final.find_element(By.XPATH, "following-sibling::*[1]").text
    assert float(number) == expected


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
