"""基于实际 Element Plus DOM 的页面对象；所有操作使用显式等待。"""
import re
from urllib.parse import urlsplit
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from .settings import BASE_URL, TIMEOUT
from .catalog import PAGE

CONTENT = (By.CSS_SELECTOR, "section[class*='app-content-padding']")


def compact(text):
    return re.sub(r"\s+", "", text)


class SystemPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT, poll_frequency=0.25,
            ignored_exceptions=(StaleElementReferenceException,))

    def visible(self, by, value, scope=None):
        return [e for e in (scope or self.driver).find_elements(by, value) if e.is_displayed()]

    @property
    def content(self):
        return self.wait.until(lambda d: next(iter(self.visible(*CONTENT)), False), "未找到系统正文区域")

    @property
    def text(self):
        return self.content.text

    def idle(self):
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        self.wait.until(lambda d: not self.visible(By.CSS_SELECTOR, ".el-loading-mask"), "页面加载未完成")

    def expect_text(self, *tokens, scope=None):
        for token in tokens:
            self.wait.until(lambda d: compact(token) in compact((scope.text if scope else self.text)),
                f"页面正文未显示业务内容：{token}")

    def open(self, page_id):
        spec = PAGE[page_id]
        self.driver.get(BASE_URL + spec.path)
        self.wait.until(lambda d: urlsplit(d.current_url).path == spec.path, "页面被重定向，可能会话已失效")
        self.idle()
        self.expect_text(*spec.anchors)
        return self

    def button(self, name, scope=None, index=0):
        def find(d):
            matches = [e for e in self.visible(By.TAG_NAME, "button", scope or self.content)
                       if compact(e.text or e.get_attribute("aria-label") or "") == compact(name)]
            return matches[index] if len(matches) > index else False
        return self.wait.until(find, f"未找到按钮：{name}")

    def click(self, name, scope=None, index=0):
        button = self.button(name, scope, index)
        self.wait.until(lambda d: button.is_enabled() and button.get_attribute("aria-disabled") != "true")
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        button.click()

    def tab(self, name):
        def find(d):
            matches = [e for e in self.visible(By.CSS_SELECTOR, "[role='tab']", self.content)
                       if re.fullmatch(re.escape(compact(name)) + r"\d*", compact(e.text))]
            return matches[0] if matches else False
        target = self.wait.until(find, f"未找到标签：{name}")
        target.click()
        self.wait.until(lambda d: target.get_attribute("aria-selected") == "true")
        self.idle()
        return target

    def dialog(self):
        return self.wait.until(lambda d: next(iter(self.visible(By.CSS_SELECTOR, "[role='dialog']")), False),
            "未打开预期弹窗")

    def close_dialog(self, name):
        dialog = self.dialog()
        self.click(name, scope=dialog)
        self.wait.until(lambda d: not self.visible(By.CSS_SELECTOR, "[role='dialog']"), "弹窗没有关闭")

    def input(self, placeholder, scope=None):
        return self.wait.until(lambda d: next((e for e in self.visible(By.CSS_SELECTOR, "input,textarea", scope or self.content)
            if e.get_attribute("placeholder") == placeholder), False), f"未找到输入框：{placeholder}")

    def fill(self, placeholder, value, scope=None):
        target = self.input(placeholder, scope)
        target.send_keys(Keys.CONTROL, "a")
        target.send_keys(value)

    def fill_label(self, name, value, scope=None):
        def find(d):
            for item in self.visible(By.CSS_SELECTOR, ".el-form-item", scope or self.content):
                labels = item.find_elements(By.CSS_SELECTOR, ".el-form-item__label")
                if labels and compact(labels[0].text).strip("*") == compact(name):
                    inputs = self.visible(By.CSS_SELECTOR, "input,textarea", item)
                    if inputs:
                        return inputs[0]
            return False
        target = self.wait.until(find, f"未找到表单字段：{name}")
        target.send_keys(Keys.CONTROL, "a")
        target.send_keys(str(value))
        target.send_keys(Keys.TAB)

    def rows(self):
        return self.visible(By.CSS_SELECTOR, ".el-table__body-wrapper tbody tr", self.content)

    def navigate_menu(self, spec):
        if spec.group:
            parents = [e for e in self.visible(By.CSS_SELECTOR, ".el-sub-menu")
                       if e.find_element(By.CSS_SELECTOR, ".el-sub-menu__title").text.strip() == spec.group]
            assert len(parents) == 1, f"菜单分组缺失：{spec.group}"
            parent = parents[0]
            if "is-opened" not in parent.get_attribute("class"):
                parent.find_element(By.CSS_SELECTOR, ".el-sub-menu__title").click()
            leaf = self.wait.until(lambda d: next((e for e in self.visible(By.CSS_SELECTOR, ".el-menu-item", parent)
                if e.text.strip() == spec.name), False))
        else:
            leaf = self.wait.until(lambda d: next((e for e in self.visible(By.CSS_SELECTOR, ".el-menu-item")
                if e.text.strip() == spec.name), False))
        leaf.click()
        self.wait.until(lambda d: urlsplit(d.current_url).path == spec.path)
        self.idle()
        self.expect_text(*spec.anchors)

    def expand_rule(self, category, group):
        self.tab("系数规则库")
        self.tab(category)
        button = self.wait.until(lambda d: next((e for e in self.visible(By.TAG_NAME, "button", self.content)
            if e.text.startswith(group)), False))
        if button.get_attribute("aria-expanded") != "true":
            button.click()
        controls = button.get_attribute("aria-controls")
        assert controls, "折叠面板缺少 aria-controls 关联"
        region = self.wait.until(lambda d: next(iter(self.visible(By.ID, controls)), False))
        return region
