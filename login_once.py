"""直接运行，首次手动登录并保存专用测试浏览器会话。"""
from ui_test_support.bootstrap import use_project_python
use_project_python()
from ui_test_support.browser import make_driver, ensure_login, save_session


def main():
    driver = make_driver()
    try:
        ensure_login(driver)
        save_session(driver)
        print("登录会话已保存，可以直接运行 run_tests.py。", flush=True)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
