"""Windows DPAPI 本机加密；凭据仅供本项目登录同一 UAT 站点。"""
import ctypes
from ctypes import wintypes
import json
import os
import sys
from .settings import RUNTIME


class Blob(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte))]


def crypt(data, decrypt=False):
    if os.name != "nt":
        raise RuntimeError("本机加密凭据需要 Windows；其他系统请使用环境变量。")
    buf = ctypes.create_string_buffer(data)
    source = Blob(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_ubyte)))
    dest = Blob()
    lib = ctypes.WinDLL("crypt32", use_last_error=True)
    fn = lib.CryptUnprotectData if decrypt else lib.CryptProtectData
    fn.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.c_void_p,
                   ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
    fn.restype = wintypes.BOOL
    if not fn(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(dest)):
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return ctypes.string_at(dest.pbData, dest.cbData)
    finally:
        kernel = ctypes.WinDLL("kernel32")
        kernel.LocalFree.argtypes = [ctypes.c_void_p]
        kernel.LocalFree(dest.pbData)


def save_credentials(username, password):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    raw = json.dumps({"username": username, "password": password}).encode()
    (RUNTIME / "credentials.dpapi").write_bytes(crypt(raw))


def get_credentials():
    if os.getenv("HSS_USERNAME") and os.getenv("HSS_PASSWORD"):
        return os.environ["HSS_USERNAME"], os.environ["HSS_PASSWORD"]
    path = RUNTIME / "credentials.dpapi"
    if path.exists():
        data = json.loads(crypt(path.read_bytes(), decrypt=True))
        return data["username"], data["password"]
    return None


if __name__ == "__main__":
    data = json.loads(sys.stdin.readline())
    save_credentials(data["username"], data["password"])
    print("登录凭据已使用 Windows DPAPI 加密保存。")
