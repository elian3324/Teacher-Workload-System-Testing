"""独立 Edge 配置目录；驱动由 Selenium Manager 安装并缓存。"""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .credentials import get_credentials
from .settings import BASE_URL, PROFILE, RUNTIME, REPORTS, LOGIN_TIMEOUT


def make_driver(headless=False, profile=None):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("SE_CACHE_PATH", str(RUNTIME / "selenium_cache"))
    options = Options()
    options.add_argument(f"--user-data-dir={profile or PROFILE}")
    options.add_argument("--window-size=1600,1000")
    options.add_argument("--no-first-run")
    options.add_experimental_option("prefs", {
        "download.default_directory": str((REPORTS / "downloads").resolve()),
        "download.prompt_for_download": False,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })
    if headless:
        options.add_argument("--headless=new")
    explicit = os.getenv("HSS_EDGE_DRIVER")
    service = Service(executable_path=explicit) if explicit else Service()
    driver = webdriver.Edge(service=service, options=options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(0)
    return driver


def authenticated(driver):
    return (urlsplit(driver.current_url).netloc == urlsplit(BASE_URL).netloc
            and any(e.is_displayed() for e in driver.find_elements(By.CSS_SELECTOR, ".el-menu")))


def open_login_twice(driver):
    driver.get(BASE_URL + "/login")
    first = driver.current_url
    driver.get(BASE_URL + "/login")
    return first, driver.current_url


def auto_login(driver):
    credentials = get_credentials()
    if not credentials:
        return False
    # 只有回到用户指定站点的真正登录界面后才填写凭据。
    if urlsplit(driver.current_url).netloc != urlsplit(BASE_URL).netloc:
        return False
    wait = WebDriverWait(driver, 25)
    username = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="请输入用户名"]')))
    password = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入密码"]')
    username.send_keys(credentials[0])
    password.send_keys(credentials[1])
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space(.)="登录"]')))
    button.click()
    wait.until(authenticated, "自动登录失败，请检查本机凭据或登录页变化。")
    save_session(driver)
    return True


def save_session(driver):
    # 仅保存此专用测试浏览器、此站点的会话，不读取用户日常 Edge 配置。
    if not authenticated(driver):
        raise RuntimeError("登录未完成，无法保存会话")
    storage = driver.execute_script("return Object.assign({}, sessionStorage);")
    (RUNTIME / "session_storage.json").write_text(
        json.dumps({"origin": BASE_URL, "storage": storage}, ensure_ascii=False), encoding="utf-8")


def ensure_login(driver, headless=False):
    driver.get(BASE_URL + "/index")
    if authenticated(driver):
        return
    saved = RUNTIME / "session_storage.json"
    # Cookie / localStorage 由 Edge 自身持久化。补充恢复站点的 sessionStorage。
    if saved.exists():
        driver.get(BASE_URL + "/login")
        if urlsplit(driver.current_url).netloc == urlsplit(BASE_URL).netloc:
            data = json.loads(saved.read_text(encoding="utf-8"))
            if data.get("origin") == BASE_URL:
                driver.execute_script("for (const [k,v] of Object.entries(arguments[0])) sessionStorage.setItem(k,v);", data["storage"])
                driver.get(BASE_URL + "/index")
                if authenticated(driver):
                    return
    open_login_twice(driver)
    if authenticated(driver):
        return
    if auto_login(driver):
        return
    if headless:
        raise RuntimeError("测试会话已过期，请先运行 login_once.py 手动登录，再运行无头测试。")
    print("请在新打开的专用 Edge 窗口手动登录；登录成功后测试自动继续。", flush=True)
    WebDriverWait(driver, LOGIN_TIMEOUT, poll_frequency=1).until(authenticated,
        "等待手动登录超时，请运行 login_once.py 完成登录")
    save_session(driver)

