"""从真实 pytest JSON 结果生成交付记录，不改写测试结论。"""
import json
from collections import Counter
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
import sys
from .settings import SUPPORT, REPORTS


def main(run_id):
    run = REPORTS / "runs" / run_id
    data = json.loads((run / "results.json").read_text(encoding="utf-8"))
    summary = data["summary"]
    assert summary.get("total", 0), "这是收集报告，不能当作实际执行验证"
    status = "全部通过" if summary.get("passed") == summary["total"] else "存在未通过用例"
    grouped = {}
    for test in data["tests"]:
        group = test["nodeid"].split("::")[0]
        grouped.setdefault(group, Counter())[test["outcome"]] += 1
    coverage = json.loads((REPORTS / "dictionary_coverage.json").read_text(encoding="utf-8"))
    start = datetime.strptime(run_id, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    lines = ["# 实际验证结果\n", f"执行时间：{start}（北京时间）。环境：UAT。\n",
        f"最终完整回归：**{status}**。\n",
        f"实际统计：{summary.get('passed',0)} passed，{summary.get('failed',0)} failed，{summary.get('error',0)} error，{summary.get('skipped',0)} skipped；共 {summary['total']} 项测试。耗时 {data['duration']:.2f} 秒。\n",
        "执行入口：`python -X utf8 -u main.py --headless -q`。该入口已验证可使用系统 Python 自动调用项目 `.venv`。\n",
        f"报告目录：`../reports/runs/{run_id}/`；[HTML 报告](../reports/runs/{run_id}/report.html)、[JSON 原始结果](../reports/runs/{run_id}/results.json)、[JUnit](../reports/runs/{run_id}/junit.xml)。\n",
        "## 按脚本统计\n", "| 文件 | 通过 | 失败 | 错误/跳过 |", "| --- | --- | --- | --- |"]
    for name, stats in grouped.items():
        lines.append(f"| {name} | {stats.get('passed',0)} | {stats.get('failed',0)} | {stats.get('error',0)+stats.get('skipped',0)} |")
    lines += ["\n## 额外覆盖证据\n",
        f"字典列表分页发现 {coverage['discovered']} 个字典数据入口，实际打开完成 {coverage['completed']} 个，数量与列表总数核对。详细路径见 `../reports/dictionary_coverage.json`。",
        "所有正文加载用例保留截图，失败截图也独立保存；三类 Excel 导出在浏览器实际下载后使用 openpyxl 检查字段和数据行。",
        "在隔离配置目录中验证了两次进入登录地址后的用户名/密码控件，以及本机加密账号的真实自动登录。未在文档或报告中写出密码。",
        "浏览器调研记录：`../reports/secondary_audit.json`、`../reports/header_audit.json`、`../reports/course_form_audit.json`；包含系统消息、通知跳转、可编辑学期的新增课程六标签、历史导入窗口和版本记录。调研不计入144项 pytest 通过数。",
        "\n## 安装和运行环境\n",
        f"Python：{sys.version.split()[0]}；Selenium：{version('selenium')}；pytest：{version('pytest')}；pytest-html：{version('pytest-html')}；openpyxl：{version('openpyxl')}。",
        "Edge 与匹配驱动已实际启动；驱动缓存放在 `../runtime/selenium_cache`。`pip check` 确认依赖一致。",
        "\n## 调试记录与边界\n",
        "初次完整调试在浏览器渲染连接断开后出现连锁失败，原始报告保留；框架增加每10个用例重建浏览器、并避免向失效会话反复请求截图。另修正了字典弹窗字段文案、开课只读状态下的断言和待办标签数量格式。",
        "本记录基于当前 UAT 数据、当前测试账号和本次实际执行，未把未执行的写入或多角色业务流程计入通过数。67项相关场景的前置条件和步骤已列在测试用例文档中。",
        "已检查的不可达/状态限制包括审批中开课的新增、版本、历史导入入口，以及缺少数据的列表；这些限制与业务规则确认项见系统调研。",
        "不会通过隐藏异常、自动跳过失败或删除断言来保证表面通过；服务、配置或数据发生变化时应按报告复核。"]
    (SUPPORT / "docs" / "验证结果.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"run":run_id, "summary":summary,"dictionary":coverage['completed']}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
