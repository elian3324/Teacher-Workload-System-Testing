from ui_test_support.bootstrap import use_project_python
use_project_python()
import pytest
from selenium.webdriver.common.by import By
from ui_test_support.catalog import PAGES


@pytest.mark.smoke
@pytest.mark.parametrize("spec", PAGES, ids=lambda p: p.id)
def test_page_loads(page, spec):
    """所有已发现路由必须显示真实正文，而不是仅显示标题/面包屑。"""
    page.open(spec.id)
    assert len(page.text.strip()) > 30
    assert not page.visible(By.CSS_SELECTOR, ".el-result__title")
    assert "404" not in page.driver.title


@pytest.mark.navigation
@pytest.mark.parametrize("spec", [p for p in PAGES if p.id not in {"dict_data", "notify"}], ids=lambda p: p.id)
def test_sidebar_navigation(page, spec):
    page.open("home")
    page.navigate_menu(spec)


@pytest.mark.navigation
def test_dictionary_data_link(page):
    page.open("dict")
    link = page.wait.until(lambda d: next(iter(page.visible(By.CSS_SELECTOR,
        'a[href="/dict/type/data/hss_course_belongs"]', page.content)), False))
    link.click()
    page.expect_text("字典标签", "字典键值", "课程所属学院")


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
