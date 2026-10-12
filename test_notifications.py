"""侧栏外的顶部系统消息入口。"""
from ui_test_support.bootstrap import use_project_python
use_project_python()
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.navigation
def test_header_message_page(page):
    page.open("home")
    page.visible(By.CSS_SELECTOR, ".v-tool-header .message")[0].click()
    page.click("查看全部", scope=page.driver)
    page.wait.until(lambda d: "/user/notify-message" in d.current_url)
    page.expect_text("消息类型", "消息内容", "接收时间")


@pytest.mark.navigation
def test_course_plan_notification_detail_target(page):
    page.open("notify")
    row = page.wait.until(lambda d: next((e for e in page.rows() if "开课计划" in e.text), False),
        "需要一条已有的开课计划通知来验证详情跳转")
    page.click("详情", scope=row)
    page.wait.until(lambda d: "/hss-task/index" in d.current_url)
    page.expect_text("任务管理", "全部待办", "审批状态")


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
