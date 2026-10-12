from ui_test_support.bootstrap import use_project_python
use_project_python()
import pytest
from selenium.webdriver.common.by import By
from ui_test_support.catalog import TABS, RULE_GROUPS


@pytest.mark.tabs
@pytest.mark.parametrize("page_id,name,anchor", TABS, ids=[f"{p}-{n}" for p,n,_ in TABS])
def test_business_tab(page, page_id, name, anchor):
    page.open(page_id)
    target = page.tab(name)
    page.expect_text(anchor)
    assert target.get_attribute("aria-selected") == "true"


@pytest.mark.tabs
@pytest.mark.parametrize("category,group,anchor", RULE_GROUPS, ids=[g for _,g,_ in RULE_GROUPS])
def test_rule_group(page, category, group, anchor):
    page.open("rule")
    region = page.expand_rule(category, group)
    page.expect_text(anchor, scope=region)
    assert page.visible(By.CSS_SELECTOR, "table", region)
    assert page.button("条件测试", region).is_enabled()


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
