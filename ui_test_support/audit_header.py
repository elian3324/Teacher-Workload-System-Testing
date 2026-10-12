"""读取顶部消息和用户菜单，记录是否存在额外页面。"""
import json
from .browser import make_driver, ensure_login
from .pages import SystemPage
from .settings import RUNTIME, REPORTS
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


if __name__=="__main__":
    driver=make_driver(headless=True,profile=RUNTIME/"header_audit")
    records=[]
    try:
        ensure_login(driver,headless=True)
        page=SystemPage(driver).open("home")
        message=page.visible(By.CSS_SELECTOR,".v-tool-header .message")[0]
        message.click()
        page.wait.until(lambda d: "消息" in d.find_element(By.TAG_NAME,"body").text)
        record={"entry":"消息","text":driver.find_element(By.TAG_NAME,"body").text[-7000:],
            "dialogs":[e.text for e in page.visible(By.CSS_SELECTOR,'[role="dialog"]')]}
        records.append(record)
        print(json.dumps(record,ensure_ascii=False),flush=True)
        driver.save_screenshot(str(REPORTS/"header_message.png"))
        matches=page.visible(By.XPATH,'//*[normalize-space(.)="查看全部"]')
        print(json.dumps({"all_matches":[{"tag":e.tag_name,"class":e.get_attribute("class")} for e in matches]},ensure_ascii=False),flush=True)
        all_link=matches[-1]
        handles=driver.window_handles
        all_link.click()
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(driver,5).until(lambda d: d.window_handles!=handles or '/index' not in d.current_url or bool(page.visible(By.CSS_SELECTOR,'[role="dialog"],.el-dialog,.el-drawer')))
        except TimeoutException:
            print("查看全部点击后没有路由、新标签或弹窗变化，记录为不可达入口。",flush=True)
        if driver.window_handles!=handles:
            driver.switch_to.window(next(h for h in driver.window_handles if h not in handles))
        record={"entry":"查看全部消息","url":driver.current_url,"text":driver.find_element(By.TAG_NAME,"body").text[-6500:]}
        records.append(record)
        print(json.dumps(record,ensure_ascii=False),flush=True)
        driver.save_screenshot(str(REPORTS/"header_all_messages.png"))
        page.open("notify")
        page.wait.until(lambda d: bool(page.rows()))
        page.click("详情")
        page.wait.until(lambda d: '/notify-message' not in d.current_url or bool(page.visible(By.CSS_SELECTOR,'[role="dialog"]')))
        record={"entry":"消息详情点击后界面","url":driver.current_url,
                "text":driver.find_element(By.TAG_NAME,"body").text[-4000:]}
        records.append(record)
        print(json.dumps(record,ensure_ascii=False),flush=True)
        for text in ["你好，欢迎", "通知公告"]:
            page.open("notify")
            row=page.wait.until(lambda d: next((e for e in page.rows() if text in e.text),False))
            page.click("详情",scope=row)
            # 通用通知可能导航或展开详情，记录真实 UI 结果而不预设隐藏地址。
            page.idle()
            record={"entry":f"通知详情-{text}","url":driver.current_url,
                "text":driver.find_element(By.TAG_NAME,"body").text[-4000:],
                "dialogs":[e.text for e in page.visible(By.CSS_SELECTOR,'[role="dialog"]')]}
            records.append(record)
            print(json.dumps(record,ensure_ascii=False),flush=True)
        page.open("home")
        trigger=page.visible(By.CSS_SELECTOR,'.v-tool-header .v-user-info [role="button"]')[0]
        trigger.click()
        page.wait.until(lambda d: bool(page.visible(By.CSS_SELECTOR,'.el-dropdown-menu')))
        record={"entry":"用户菜单","menus":[e.text for e in page.visible(By.CSS_SELECTOR,'.el-dropdown-menu')]}
        records.append(record)
        print(json.dumps(record,ensure_ascii=False),flush=True)
        trigger.send_keys(Keys.ESCAPE)
    finally:
        (REPORTS/"header_audit.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
        driver.quit()
