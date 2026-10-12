"""逐项读取二级 UI；只打开窗口/视图，避免业务提交。"""
import json
from .browser import make_driver, ensure_login
from .pages import SystemPage
from .settings import RUNTIME, REPORTS
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def main():
    driver = make_driver(headless=True, profile=RUNTIME / "secondary_audit")
    records = []
    try:
        ensure_login(driver, headless=True)
        page = SystemPage(driver)
        for route,tab,button in [
            ("settlement","co-list","新增课程代码"),
            ("settlement","SIS同步明细","SIS数据导入"),
            ("settlement","SIS同步明细","SIS课时导入"),
            ("course","历史导入记录","新导入历史数据"),
            ("course","开课列表","版本"),
            ("course","跨学年结转","详情"),
        ]:
            page.open(route)
            page.tab(tab)
            try:
                page.click(button)
                dialog = page.dialog()
                record = {"page": route,"tab":tab,"button":button,"dialog":dialog.text,
                    "buttons":[e.text or e.get_attribute("aria-label") for e in page.visible(By.TAG_NAME,"button",dialog)]}
            except TimeoutException:
                record = {"page":route,"tab":tab,"button":button,"status":"入口不可达",
                    "text":page.text[:3000],"buttons":[e.text for e in page.visible(By.TAG_NAME,"button",page.content)]}
            records.append(record)
            print(json.dumps(record,ensure_ascii=False),flush=True)
        for route,tab,label in [("course","计划版","按课程明细"),
                               ("settlement","工作量明细","按教师汇总")]:
            page.open(route)
            page.tab(tab)
            labels = page.visible(By.CSS_SELECTOR,"label",page.content)
            choice = next(e for e in labels if e.text.strip()==label)
            choice.click()
            page.idle()
            record={"page":route,"tab":tab,"choice":label,"text":page.text[:2500]}
            records.append(record)
            print(json.dumps(record,ensure_ascii=False),flush=True)
        page.open("home")
        header=page.visible(By.CSS_SELECTOR,".v-tool-header")[0]
        print(json.dumps({"header":driver.execute_script("return arguments[0].outerHTML",header)},ensure_ascii=False),flush=True)
    finally:
        REPORTS.mkdir(exist_ok=True)
        (REPORTS/"secondary_audit.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
        driver.quit()


if __name__=="__main__":
    main()
