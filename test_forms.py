from ui_test_support.bootstrap import use_project_python
use_project_python()
import pytest
from selenium.webdriver.common.by import By
from ui_test_support.catalog import FORMS


@pytest.mark.forms
@pytest.mark.parametrize("page_id,button,anchor,cancel", FORMS, ids=[p for p,_,_,_ in FORMS])
def test_create_form_can_cancel(page, page_id, button, anchor, cancel):
    page.open(page_id)
    page.click(button)
    dialog = page.dialog()
    page.expect_text(anchor, scope=dialog)
    assert page.visible(By.CSS_SELECTOR, "input,textarea", dialog)
    page.close_dialog(cancel)


@pytest.mark.forms
@pytest.mark.parametrize("page_id,button,anchor,cancel", [
    ("teacher", "批量导入", "导入", "取消"),
    ("special_course", "批量导入", ".xlsx", "取消"),
    ("user", "导入", "上传", "取 消"),
], ids=["teacher-import", "course-import", "user-import"])
def test_import_dialog_can_cancel(page, page_id, button, anchor, cancel):
    page.open(page_id)
    page.click(button)
    page.expect_text(anchor, scope=page.dialog())
    page.close_dialog(cancel)


@pytest.mark.forms
@pytest.mark.parametrize("button,anchor", [("菜单权限", "菜单权限"), ("数据权限", "权限范围")])
def test_role_permission_dialog_can_cancel(page, button, anchor):
    page.open("role")
    page.click(button)
    page.expect_text(anchor, scope=page.dialog())
    page.close_dialog("取 消")


@pytest.mark.query
def test_role_user_assignment_page(page):
    page.open("role")
    page.click("分配用户")
    page.expect_text("角色用户", "添加用户", "返回角色列表")
    page.click("添加用户")
    page.expect_text("用户账号", scope=page.dialog())
    page.close_dialog("取消")
    page.click("返回角色列表")
    page.expect_text("角色名称", "角色标识")


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    from run_tests import main
    raise SystemExit(main([__file__, *sys.argv[1:]]))
