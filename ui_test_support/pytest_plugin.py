from datetime import datetime
from pathlib import Path
import re
import pytest
from pytest_html import extras
from .browser import make_driver, ensure_login, save_session
from .pages import SystemPage
from .settings import REPORTS
from selenium.common.exceptions import InvalidSessionIdException, NoSuchWindowException


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="使用无头 Edge；需要已保存的会话或本机加密账号")


def close_browser(browser):
    if browser is None:
        return
    try:
        from .browser import authenticated
        if authenticated(browser):
            save_session(browser)
    except (InvalidSessionIdException, NoSuchWindowException):
        # 原始测试已报告浏览器终止；清理不制造重复 teardown 错误。
        pass
    finally:
        browser.quit()


@pytest.fixture(scope="session")
def browser_pool():
    pool = {"browser": None, "count": 0}
    yield pool
    close_browser(pool["browser"])


@pytest.fixture
def driver(request, browser_pool):
    # 每 10 用例重建专用浏览器，防止长期导航的资源累积。
    # 不自动重跑失败用例，不改变失败结论。
    if browser_pool["browser"] is None or browser_pool["count"] >= 10:
        close_browser(browser_pool["browser"])
        browser_pool["browser"] = make_driver(headless=request.config.getoption("--headless"))
        browser_pool["count"] = 0
        ensure_login(browser_pool["browser"], headless=request.config.getoption("--headless"))
    browser_pool["count"] += 1
    yield browser_pool["browser"]


@pytest.fixture
def page(driver):
    return SystemPage(driver)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    browser = item.funcargs.get("driver")
    if browser is None or report.when != "call":
        return
    if report.failed and "invalid session id" in str(report.longrepr).lower():
        report.extras = [extras.text("浏览器会话已断开；原始失败已记录，无法截图。", name="浏览器状态")]
        return
    evidence = REPORTS / "screenshots"
    if report.failed or "test_page_loads" in item.name:
        evidence.mkdir(parents=True, exist_ok=True)
        name = re.sub(r"[^\w.-]", "_", item.nodeid)[:160]
        path = evidence / f"{name}_{datetime.now():%Y%m%d_%H%M%S}.png"
        try:
            browser.save_screenshot(str(path))
            report.extras = list(getattr(report, "extras", [])) + [
                extras.png(browser.get_screenshot_as_base64(), name="页面证据"),
                extras.text(browser.current_url, name="当前页面 URL"),
            ]
        except Exception as exc:
            # 截图失败不能改变原始测试结果；在报告中保留原因。
            report.extras = list(getattr(report, "extras", [])) + [extras.text(str(exc), name="截图失败")]


def pytest_html_report_title(report):
    report.title = "教师工作量系统 — Selenium UI 自动化测试报告"
