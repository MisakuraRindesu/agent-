"""CLI-8 环境诊断：确认本地 Ollama 请求是否被 Windows 系统代理劫持。

用法：
    python E:\\DSH\\proxy-probe.py            # 真实环境（会被代理劫持）
    $env:NO_PROXY="localhost,127.0.0.1,::1"; python E:\\DSH\\proxy-probe.py   # 修复后
"""
import os
import urllib.request

TARGET = "http://localhost:11434/api/show"
PAYLOAD = {"model": "qwen2.5:3b"}

print("NO_PROXY  =", repr(os.environ.get("NO_PROXY")))
print("no_proxy  =", repr(os.environ.get("no_proxy")))
print("HTTP_PROXY=", repr(os.environ.get("HTTP_PROXY")))
print("getproxies() =", urllib.request.getproxies())
print("-" * 60)

try:
    import httpx

    r = httpx.post(TARGET, json=PAYLOAD, timeout=20)
    print(f"httpx    -> {r.status_code} ({len(r.text)} bytes)")
except Exception as exc:  # noqa: BLE001
    print(f"httpx    -> ERR {type(exc).__name__}: {exc}")

try:
    import requests

    r = requests.post(TARGET, json=PAYLOAD, timeout=20)
    print(f"requests -> {r.status_code} ({len(r.text)} bytes)")
except Exception as exc:  # noqa: BLE001
    print(f"requests -> ERR {type(exc).__name__}: {exc}")

try:
    import ollama

    info = ollama.show("qwen2.5:3b")
    print("ollama   -> OK, family =", info.get("details", {}).get("family"))
except Exception as exc:  # noqa: BLE001
    print(f"ollama   -> ERR {type(exc).__name__}: {exc}")
