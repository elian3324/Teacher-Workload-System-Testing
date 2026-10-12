"""安装验证时检查隔离浏览器中的真实登录 DOM，不输出表单值。"""
from .browser import make_driver, open_login_twice
from .settings import RUNTIME
from selenium.webdriver.support.ui import WebDriverWait


if __name__ == "__main__":
    driver = make_driver(headless=True, profile=RUNTIME / "login_probe")
    try:
        print(open_login_twice(driver), flush=True)
        WebDriverWait(driver, 25).until(lambda d: d.execute_script("return document.readyState") == "complete")
        print(driver.execute_script("return {text:document.body.innerText,inputs:Array.from(document.querySelectorAll('input')).map(e=>({type:e.type,placeholder:e.placeholder,name:e.name,id:e.id}))};"), flush=True)
        driver.save_screenshot(str(RUNTIME / "login_probe.png"))
    finally:
        driver.quit()
