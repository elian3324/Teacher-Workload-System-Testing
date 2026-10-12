from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
SUPPORT = ROOT / "ui_test_support"
RUNTIME = SUPPORT / "runtime"
REPORTS = SUPPORT / "reports"
load_dotenv(SUPPORT / ".env")
BASE_URL = os.getenv("HSS_BASE_URL", "https://hssload-uat.cuhk.edu.cn").rstrip("/")
TIMEOUT = int(os.getenv("HSS_TIMEOUT", "25"))
LOGIN_TIMEOUT = int(os.getenv("HSS_LOGIN_TIMEOUT", "900"))
PROFILE = Path(os.getenv("HSS_EDGE_PROFILE", str(RUNTIME / "edge_profile"))).resolve()

