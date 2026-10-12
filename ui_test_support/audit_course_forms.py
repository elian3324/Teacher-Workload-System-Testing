"""只切换查询学期，检查可编辑学期的新增表单及全年版本入口。"""
import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .browser import make_driver, ensure_login
from .pages import SystemPage
from .settings import RUNTIME, REPORTS


if __name__ == "__main__":
    driver=make_driver(headless=True,profile=RUNTIME/"course_form_audit")
    records=[]
    try:
        ensure_login(driver,headless=True)
        page=SystemPage(driver).open("course")
        page.tab("开课列表")
        page.wait.until(lambda d: len(page.visible(By.CSS_SELECTOR,'.el-select',page.content)) >= 2)
        combo=page.visible(By.CSS_SELECTOR,'.el-select',page.content)[1]
        combo.click()
        options=page.wait.until(lambda d: page.visible(By.CSS_SELECTOR,'[role="option"]'))
        names=[e.text for e in options]
        records.append({"entry":"学期选项","options":names})
        print(json.dumps(records[-1],ensure_ascii=False),flush=True)
        term2=next((e for e in options if "Term 2" in e.text),None)
        if term2 is not None:
            term2.click()
            page.idle()
            try:
                page.click("新增课程")
                dialog=page.dialog()
                records.append({"entry":"Term 2 新增课程","dialog":dialog.text,
                    "buttons":[e.text or e.get_attribute('aria-label') for e in page.visible(By.TAG_NAME,'button',dialog)]})
                tabs=page.visible(By.CSS_SELECTOR,'[role="tab"]',dialog)
                for tab in tabs:
                    name=tab.text
                    tab.click()
                    page.wait.until(lambda d: tab.get_attribute('aria-selected')=='true')
                    records.append({"entry":f"新增课程-{name}","dialog":dialog.text})
                    print(json.dumps(records[-1],ensure_ascii=False),flush=True)
                page.close_dialog("取消")
                page.tab("历史导入记录")
                try:
                    page.click("新导入历史数据")
                    history=page.dialog()
                    records.append({"entry":"Term 2 历史导入窗口","dialog":history.text})
                    print(json.dumps(records[-1],ensure_ascii=False),flush=True)
                    page.close_dialog("关闭")
                except TimeoutException:
                    records.append({"entry":"Term 2 历史导入窗口","status":"入口不可达"})
            except TimeoutException:
                records.append({"entry":"Term 2 新增课程","status":"入口不可达","text":page.text[:1800]})
            print(json.dumps(records[-1],ensure_ascii=False),flush=True)
        page.open("course")
        page.tab("开课列表")
        page.wait.until(lambda d: len(page.visible(By.CSS_SELECTOR,'.el-select',page.content)) >= 2)
        page.visible(By.CSS_SELECTOR,'.el-select',page.content)[1].click()
        yearly=page.wait.until(lambda d: next((e for e in page.visible(By.CSS_SELECTOR,'[role="option"]') if e.text.strip()=="全年"),False))
        yearly.click()
        try:
            page.click("版本")
            records.append({"entry":"全年课程版本","dialog":page.dialog().text})
        except TimeoutException:
            records.append({"entry":"全年课程版本","status":"入口不可达","text":page.text[:1800]})
        print(json.dumps(records[-1],ensure_ascii=False),flush=True)
    finally:
        (REPORTS/"course_form_audit.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
        driver.quit()
