# 教师工作量系统 UI 自动化

在项目根目录直接运行 `main.py` 或 `run_tests.py`，即可执行 Selenium + pytest 完整回归。当前项目 `.venv` 已安装全部依赖，Edge 驱动已下载到本项目缓存。入口会自动调用项目虚拟环境，使用系统 Python 或 PyCharm 运行均可。

```powershell
python main.py
python run_tests.py --headless
python run_tests.py --suite smoke
python run_tests.py test_calculations.py --headless
python run_tests.py -k pagination --headless
python run_tests.py --collect-only
```

直接运行某个 `test_*.py` 文件也会通过统一入口执行该文件。PyCharm 解释器使用现有 `.venv/Scripts/python.exe`。若使用 PyCharm 的 pytest 运行器，可在参数中加 `-p ui_test_support.pytest_plugin --rootdir . -c ui_test_support/pytest.ini`。

## 登录

默认复用专用 Edge 测试配置目录 `runtime/edge_profile`，不占用日常 Edge 配置。进入登录地址两次以处理重定向；有效会话会直接复用，过期时使用本机 Windows DPAPI 加密账号自动登录。仅在目标站点的真实登录表单填写凭据，不向重定向的其他域名填写账号。

`login_once.py` 可以重新建立会话。`runtime/credentials.dpapi` 只能由当前 Windows 用户解密；迁移机器时需重新配置账号。提供系统环境变量 `HSS_USERNAME`、`HSS_PASSWORD` 可以覆盖本机账号。不要把 `runtime`、`.env`、测试报告或下载数据提交到仓库。

## 文件布局

根目录所有新增文件均为 Python 运行/测试脚本。支持文件集中在 `ui_test_support`：

| 文件或目录 | 用途 |
| --- | --- |
| `catalog.py` | 已实际检查的页面、标签、规则组、表单清单 |
| `pages.py` | Element Plus 页面对象与显式等待 |
| `browser.py` / `credentials.py` | Edge、登录、会话复用、本机账号加密 |
| `pytest_plugin.py` / `pytest.ini` | fixture、标记、截图、报告配置 |
| `docs/测试用例.md` | 中文前置条件、步骤和预期结果 |
| `docs/系统调研.md` | 页面地图、业务说明和调研限制 |
| `docs/验证结果.md` | 实际运行结果 |
| `runtime/` | 专用浏览器配置、驱动缓存和临时文件 |
| `reports/runs/` | 每次执行独立的 HTML、JSON、JUnit 报告 |
| `reports/screenshots/` | 页面覆盖证据与失败截图 |
| `reports/downloads/` | 实际导出的 Excel 文件 |

## 测试范围

完整回归涵盖登录、所有已发现菜单页面、全部字典数据实例、侧栏导航、顶部系统消息及通知详情跳转、全部业务标签和九组系数、表单打开取消、查询重置、分页往返、工作量详情、减免详情、计算详情、数值试算、列显示恢复、导出下载与文件内容。数值用例以 2026-10-12 当前 UAT 规则配置为基线，修改规则后应评审预期数值。

默认脚本不新增业务记录，不执行审批通过、驳回、清空、归档、全量同步、结算重算或权限保存。对应写入场景已编写人工/后续自动化用例，须在指定可清理的数据集与角色账号下执行。跨学年结转页按页面说明，全年模式读取时可能触发系统自身的账本计算；测试只打开页面，不点击刷新或保存。

测试真实服务，不通过屏蔽异常、无条件通过或跳过失败来制造成功结果。网络、会话、权限、数据或产品变更造成的失败会保留在报告中。页面或数据不存在时会报告所缺少的前置条件。

为降低长时间运行的浏览器资源累积，测试间每10个用例重建一次专用 Edge，会话仍自动复用；失败用例不自动重跑。首次调试报告与最终回归报告分别保留。

技术参考：[Selenium Edge](https://www.selenium.dev/documentation/webdriver/browsers/edge/)、[Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/)、[pytest 运行方式](https://docs.pytest.org/en/stable/how-to/usage.html)。
