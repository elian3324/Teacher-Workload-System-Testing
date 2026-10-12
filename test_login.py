from ui_test_support.bootstrap import use_project_python
use_project_python()
from urllib.parse import urlsplit
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from ui_test_support.browser import make_driver, open_login_twice, auto_login, authenticated
from ui_test_support.settings import BASE_URL


@pytest.fixture
def fresh_login_driver(tmp_path):
    browser = make_driver(headless=True, profile=tmp_path / "edge_login")
    try:
        open_login_twice(browser)
        WebDriverWait(browser, 25).until(lambda d: bool(d.find_elements(By.CSS_SELECTOR,
            'input[placeholder="请输入用户名"]')))
        yield browser
    finally:
        browser.quit()


@pytest.mark.login
def test_login_page_after_second_navigation(fresh_login_driver):
    driver = fresh_login_driver
    assert urlsplit(driver.current_url).netloc == urlsplit(BASE_URL).netloc
    assert urlsplit(driver.current_url).path == "/login"
    assert driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入用户名"]').is_displayed()
    password = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入密码"]')
    assert password.is_displayed() and password.get_attribute("type") == "password"


@pytest.mark.login
def test_encrypted_account_can_login(fresh_login_driver):
    assert auto_login(fresh_login_driver), "本机加密凭据缺失，请先配置测试账号"
    assert authenticated(fresh_login_driver)


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
