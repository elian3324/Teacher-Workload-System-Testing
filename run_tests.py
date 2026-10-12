"""直接运行本文件即可启动完整 UI 回归；无需另装依赖。"""
from ui_test_support.bootstrap import use_project_python
use_project_python()
import argparse
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.pycache_prefix = str(ROOT / "ui_test_support" / "runtime" / "pycache")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", choices=["full", "smoke"], default="full")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--collect-only", action="store_true")
    args, extra = parser.parse_known_args(argv)
    import pytest
    report_dir = ROOT / "ui_test_support" / "reports" / "runs" / datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir.mkdir(parents=True, exist_ok=True)
    targets = [arg for arg in extra if not arg.startswith("-") and (arg.endswith(".py") or ".py::" in arg)]
    extra = [arg for arg in extra if arg not in targets]
    options = ["-p", "ui_test_support.pytest_plugin", "--rootdir", str(ROOT),
        "-c", str(ROOT / "ui_test_support" / "pytest.ini"), *(targets or [str(ROOT)]),
        "-o", f"cache_dir={ROOT / 'ui_test_support' / 'runtime' / 'pytest_cache'}",
        "--basetemp", str(ROOT / "ui_test_support" / "runtime" / "pytest_tmp"),
        "--html", str(report_dir / "report.html"), "--self-contained-html",
        "--json-report", f"--json-report-file={report_dir / 'results.json'}",
        f"--junitxml={report_dir / 'junit.xml'}"]
    if args.suite == "smoke":
        options.extend(["-m", "smoke"])
    if args.headless:
        options.append("--headless")
    if args.collect_only:
        options.append("--collect-only")
    code = pytest.main(options + extra)
    print(f"\nHTML 报告：{report_dir / 'report.html'}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
