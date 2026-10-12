"""PyCharm 默认入口：运行完整 Selenium + pytest UI 回归。"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
sys.pycache_prefix = str(Path(__file__).resolve().parent / "ui_test_support" / "runtime" / "pycache")
from run_tests import main

if __name__ == "__main__":
    raise SystemExit(main())
