#!/usr/bin/env python3
import frida, sys, os, time
from pathlib import Path

OUT = Path("~/Downloads/il2cpp_work").expanduser()
OUT.mkdir(parents=True, exist_ok=True)
OUTFILE = OUT / "global-metadata-ram.dat"

def on_message(msg, data):
    if msg['type'] == 'send':
        payload = msg['payload']
        t = payload.get('type')
        if t == 'meta_found':
            addr = payload.get('addr')
            size = payload.get('size')
            print(f"[+] metadata found at {addr}, size {size}, writing to {OUTFILE}")
            with open(OUTFILE, "wb") as f:
                f.write(data or b'')
            print(f"[+] wrote {OUTFILE} ({os.path.getsize(OUTFILE)} bytes)")
        elif t == 'chunk':
            print(f"[+] received chunk offset={payload.get('offset')}, size={payload.get('size')}")
        elif t == 'not_found':
            print("[!] metadata not found")
        elif t == 'fatal':
            print("[!] fatal error:", payload.get('message'))
        else:
            print("[*] message:", payload)
    elif msg['type'] == 'error':
        print("[!] script error:", msg['stack'])
    else:
        print("[?] message:", msg)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pid>")
        sys.exit(1)

    pid = int(sys.argv[1])
    device = frida.get_usb_device(timeout=5)
    print("[*] attaching to pid", pid)
    session = device.attach(pid)

    with open("dump_meta_scan.js", "r") as f:
        src = f.read()

    script = session.create_script(src)
    script.on("message", on_message)
    script.load()
    print("[*] script loaded. calling dumpmeta() ...")

    try:
        r = script.exports.dumpmeta()
        print("[*] dumpmeta returned:", r)
    except Exception as e:
        print("[!] exception calling dumpmeta():", e)

    print("[*] waiting 10s for data...")
    time.sleep(10)
    print("[*] done.")

if __name__ == "__main__":
    main()