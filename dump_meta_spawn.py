#!/usr/bin/env python3
import frida, sys, time, os
from pathlib import Path

OUT_DIR = Path.home() / "programing" / "meta_chunks"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def on_message(message, data):
    t = message.get("type")
    if t == "send":
        payload = message.get("payload", {})
        typ = payload.get("type")
        # 常规日志/步骤消息
        if typ in ("log", "step"):
            print("[*] message:", payload)
        elif typ == "error":
            print("[!] js error:", payload)
        elif typ == "meta_chunk" and data:
            out = OUT_DIR / "global-metadata.runtime.dat"
            with open(out, "ab") as f:
                f.write(data)
            print(f"[+] wrote chunk -> {out} (size={payload.get('size')})")
        elif typ == "meta_done":
            print("[*] meta_done size:", payload.get("size"))
        else:
            print("[*] message:", payload)
    elif t == "error":
        print("[!] script error:", message)
    else:
        print("[*] other:", message)

def main():
    if len(sys.argv) != 2:
        print("Usage: python dump_meta_spawn.py <package.name>")
        sys.exit(1)
    pkg = sys.argv[1]

    # 获取设备（USB）并 spawn
    device = frida.get_usb_device(timeout=5)
    print("[*] spawn package:", pkg)
    try:
        pid = device.spawn([pkg])
    except Exception as e:
        print("[!] spawn failed:", e)
        sys.exit(1)
    print("[*] spawned pid:", pid)

    # 加载 JS 文件（确保 path 正确）
    js_path = os.path.expanduser("~/programing/dump_metadata.js")
    if not os.path.exists(js_path):
        print("[!] dump_metadata.js not found at", js_path)
        sys.exit(1)
    with open(js_path, "r", encoding="utf-8") as f:
        src = f.read()

    # attach 并注入脚本
    session = device.attach(pid)
    # 注意：runtime 参数可以去掉或改成 'v8'，取决于 frida 版本与 js 脚本
    # 如果脚本在默认 runtime 报 "'xxxSync' is not a function" 的错误，尝试不传 runtime 或改为 'v8'
    try:
        script = session.create_script(src)  # 默认 runtime
    except Exception as e:
        print("[!] create_script with default runtime failed:", e)
        print("[*] trying runtime='v8' ...")
        script = session.create_script(src, runtime='v8')

    script.on('message', on_message)
    script.load()
    print("[*] script loaded, calling dumpmeta() ...")

    # 调用 dumpsetup（如果脚本导出 sync 函数就使用 exports_sync）
    try:
        # 有的 dump js 需要传 chunk size 参数，例如: script.exports_sync.dumpmeta("65536")
        # 先尝试无参数调用，再用 exports_sync 备用
        if hasattr(script, "exports_sync"):
            ret = script.exports_sync.dumpmeta()
        else:
            ret = script.exports.dumpmeta()
        print("[*] dumpmeta returned:", ret)
    except Exception as e:
        print("[!] exception calling dumpmeta():", e)

    # 恢复进程并等待
    print("[*] resuming process ...")
    try:
        device.resume(pid)
    except Exception as e:
        print("[!] resume failed:", e)
    wait_s = 60
    print(f"[*] waiting {wait_s}s for hooks to hit ...")
    time.sleep(wait_s)
    print("[*] done. check:", OUT_DIR)

if __name__ == '__main__':
    main()