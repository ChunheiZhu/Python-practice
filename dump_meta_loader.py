import frida, sys, time
from pathlib import Path

OUT_DIR = Path.home() / "programing" / "meta_chunks"
OUT_DIR.mkdir(parents=True, exist_ok=True)

if len(sys.argv) != 2:
    print("Usage: python dump_meta_loader.py <pid>")
    sys.exit(1)

PID = int(sys.argv[1])

def on_message(message, data):
    t = message.get("type")
    if t == "send":
        payload = message.get("payload", {})
        print("[*] message:", payload)
        if payload.get("type") == "meta_chunk" and data:
            out_path = OUT_DIR / "global-metadata.runtime.dat"
            with open(out_path, "ab") as f:
                f.write(data)
            print(f"[+] wrote chunk -> {out_path} (size={payload.get('size')})")
        elif payload.get("type") == "meta_done":
            print("[*] meta_done size:", payload.get("size"))
    elif t == "error":
        print("[!] script error:", message)
    else:
        print("[*] other message:", message)

def main():
    device = frida.get_usb_device(timeout=5)
    print("[*] attaching to pid", PID)
    session = device.attach(PID)

    js_path = Path(__file__).parent / "dump_metadata.js"
    if not js_path.exists():
        print("[!] missing JS file:", js_path)
        sys.exit(1)
    src = js_path.read_text()

    print("[*] creating script with runtime='v8' ...")
    script = session.create_script(src, runtime='v8')
    script.on('message', on_message)
    script.load()
    print("[*] script loaded. calling dumpmeta via exports_sync ...")

    try:
        r = script.exports_sync.dumpmeta()
        print("[*] dumpmeta returned:", r)
    except Exception as e:
        print("[!] exception calling dumpmeta():", e)

    print("[*] waiting 10s for messages...")
    time.sleep(10)
    print("[*] finished. chunks in", OUT_DIR)

if __name__ == '__main__':
    main()
