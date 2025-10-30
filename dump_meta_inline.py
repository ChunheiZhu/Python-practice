#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import frida, sys, time, os
from pathlib import Path

OUT = Path.home() / "Downloads" / "il2cpp_work" / "global-metadata-dumped.dat"
CHUNK_SIZE = 0x20000  # 128KB，避免大块读导致闪退；稳定后可改大

JS_CODE = r"""
'use strict';
rpc.exports = {
  dumpmeta: function(chunkArg) {
    return new Promise(function(resolve, reject) {
      try {
        var CHUNK_SIZE = 0x100000;
        if (chunkArg) {
          try { CHUNK_SIZE = parseInt(chunkArg); } catch (_) {}
        }
        var MAGIC = '\x94\x43\x72\x12';
        var foundAny = false;

        function sendChunks(basePtr, totalSize) {
          return new Promise(function(res, rej){
            var idx = 0, sent = 0;
            while (idx < totalSize) {
              var thisSize = Math.min(CHUNK_SIZE, totalSize - idx);
              try {
                var addr = basePtr.add(idx);
                var buf = Memory.readByteArray(addr, thisSize);
                send({ type: 'chunk', offset: idx, size: thisSize }, buf);
                sent++;
              } catch (e) {
                send({ type: 'read_error', offset: idx, message: e.toString() });
              }
              idx += thisSize;
            }
            send({ type: 'done', chunks: sent, base: basePtr.toString(), size: totalSize });
            res({ totalChunks: sent });
          });
        }

        (async function(){
          let ranges = [];
          ranges = ranges.concat(Process.enumerateRangesSync({ protection: 'r--', coalesce: true }));
          ranges = ranges.concat(Process.enumerateRangesSync({ protection: 'rw-', coalesce: true }));

          const pat = '94 43 72 12';
          for (let r of ranges) {
            if (r.size < 4) continue;
            await new Promise(function(ok, _){
              Memory.scan(r.base, r.size, pat, {
                onMatch: function(address, size) {
                  try {
                    foundAny = true;
                    send({ type: 'module_found', base: address.toString(), rangeBase: r.base.toString(), rangeSize: r.size });
                    const MAX = 0x3000000; // 48MB
                    const end = r.base.add(r.size);
                    const left = end.sub(address);
                    const toRead = (left.toInt32 ? left.toInt32() : left.toNumber());
                    const total = Math.min(MAX, toRead);
                    sendChunks(address, total).catch(e => {
                      send({ type: 'fatal', message: 'sendChunks failed: ' + e.toString() });
                    });
                  } catch (e) {
                    send({ type: 'scan_onmatch_error', message: e.toString() });
                  }
                },
                onError: function(reason) {
                  send({ type: 'scan_error', rangeBase: r.base.toString(), message: reason.toString() });
                  ok();
                },
                onComplete: function() { ok(); }
              });
            });
          }

          if (!foundAny) {
            send({ type: 'probe', found: false, message: 'magic not found' });
            resolve({ found: false });
          } else {
            send({ type: 'probe', found: true, message: 'finished scanning' });
            resolve({ found: true });
          }
        })();

      } catch (err) {
        send({ type: 'fatal', message: err.toString() });
        reject(err);
      }
    });
  }
};
"""

def on_message(message, data):
    if message["type"] == "send":
        payload = message["payload"]
        t = payload.get("type")
        if t == "chunk":
            offset = int(payload["offset"])
            # 追加写入
            with open(OUT, "ab") as f:
                f.write(bytes(data))
        elif t in ("done", "probe", "module_found", "scan_error", "read_error", "fatal", "range_error"):
            print("[*]", t, payload)
    elif message["type"] == "error":
        print("[!] script error:", message)

def main():
    if len(sys.argv) != 2:
        print("Usage: python dump_meta_inline.py <PID>")
        sys.exit(1)
    pid = int(sys.argv[1])
    if OUT.exists():
        OUT.unlink()
    device = frida.get_usb_device(timeout=5)
    print("[*] attaching to pid", pid)
    session = device.attach(pid)
    script = session.create_script(JS_CODE)
    script.on("message", on_message)
    script.load()
    print("[*] calling dumpmeta ...")
    # 用同步导出，避免“not a function”时不好排查
    script.exports_sync.dumpmeta(str(CHUNK_SIZE))
    print("[*] waiting a few seconds for remaining chunks ...")
    time.sleep(5)
    print("[*] saved:", OUT)

if __name__ == "__main__":
    main()