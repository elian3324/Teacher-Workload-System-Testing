"""运行入口自动选用项目现有虚拟环境，不要求修改 PATH。"""
from pathlib import Path
import sys
import subprocess


def use_project_python():
    root = Path(__file__).resolve().parent.parent
    python = root / ".venv" / "Scripts" / "python.exe"
    if python.exists() and Path(sys.executable).resolve() != python.resolve():
        raise SystemExit(subprocess.call([str(python), *sys.argv]))
