'use strict';

// 轻量日志
function step(msg, extra) { send(Object.assign({ type: 'step', msg }, extra || {})); }

function jserr(where, e) { send({ type: 'error', where, message: e ? (e.stack || e.toString()) : 'unknown' }); }

// ===== 工具：用 ApiResolver 列出导出 =====
function findExports(patterns) {
    const r = new ApiResolver('module');
    const found = [];
    for (const pat of patterns) {
        try {
            r.enumerateMatches('exports:*!' + pat, {
                onMatch(m) { found.push({ name: m.name, address: m.address }); },
                onComplete() {}
            });
        } catch (e) {}
    }
    return found;
}

// ===== il2cpp 相关挂钩 =====
let il2cppHooked = false;

function tryHookIl2Cpp() {
    if (il2cppHooked) return true;

    const names = [
        'il2cpp_init*',
        'il2cpp_init_utf16*',
        'MetadataCache_Register*',
        'InitializeRuntimeMetadata*',
        'LoadMetadataFile*',
        'ELF_HOOK_*LoadMetadataFile*',
        'ELF_HOOK_*InitializeRuntimeMetadata*'
    ];
    const funcs = findExports(names);
    step('candidates_by_exports', { count: funcs.length });

    const seen = {};
    let attached = 0;

    funcs.forEach(f => {
        const key = String(f.address);
        if (seen[key]) return;
        seen[key] = true;

        try {
            Interceptor.attach(f.address, {
                onEnter(args) {
                    try {
                        // (buf, size, ...) 的常见签名尝试
                        let sz = 0;
                        if (args[1] && typeof args[1].toInt32 === 'function') {
                            sz = args[1].toInt32();
                        }
                        if (sz > 1024 && sz < 0x08000000) {
                            step('hit hook', { fn: f.name, size: sz });
                            const ba = Memory.readByteArray(args[0], sz);
                            send({ type: 'meta_chunk', size: sz }, ba);
                            send({ type: 'meta_done', size: sz });
                        } else {
                            step('hook_enter', { fn: f.name, size: sz });
                        }
                    } catch (e) { jserr('il2cpp.onEnter', e); }
                }
            });
            attached++;
            step('attached', { fn: f.name, addr: String(f.address) });
        } catch (e) { jserr('il2cpp.attach', e); }
    });

    if (attached > 0) il2cppHooked = true;
    return il2cppHooked;
}

// ===== 文件 IO 挂钩（open/read/close/AAssetManager_open）=====
let ioHooked = false;

function tryHookFileIO() {
    if (ioHooked) return true;

    const r = new ApiResolver('module');
    const wantName = 'global-metadata.dat';
    const fds = {}; // fd -> { size, path? }

    function getExportOne(sym) {
        const arr = [];
        r.enumerateMatches('exports:*!' + sym, {
            onMatch(m) { arr.push(m); },
            onComplete() {}
        });
        return arr.length ? arr[0].address : null;
    }

    const openat = getExportOne('openat');
    const read = getExportOne('read');
    const pread64 = getExportOne('pread64');
    const close = getExportOne('close');

    const assetOpen = (function() {
        const arr = [];
        r.enumerateMatches('exports:libandroid.so!AAssetManager_open', {
            onMatch(m) { arr.push(m); },
            onComplete() {}
        });
        return arr.length ? arr[0].address : null;
    })();

    let attached = 0;

    if (openat) {
        Interceptor.attach(openat, {
            onEnter(args) { this._path = ''; try { this._path = Memory.readCString(args[1]); } catch (e) {} },
            onLeave(ret) {
                try {
                    const fd = ret.toInt32();
                    if (fd >= 0 && this._path && this._path.indexOf(wantName) !== -1) {
                        fds[fd] = { size: 0, path: this._path };
                        step('openat hit', { fd, path: this._path });
                    }
                } catch (e) { jserr('openat.onLeave', e); }
            }
        });
        step('attached', { fn: 'openat' });
        attached++;
    }

    if (read) {
        Interceptor.attach(read, {
            onEnter(args) { this.fd = args[0].toInt32();
                this.buf = args[1];
                this.c = args[2].toInt32(); },
            onLeave(ret) {
                try {
                    const n = ret.toInt32();
                    if (n > 0 && fds[this.fd]) {
                        const ba = Memory.readByteArray(this.buf, n);
                        send({ type: 'meta_chunk', size: n }, ba);
                        fds[this.fd].size += n;
                    }
                } catch (e) { jserr('read.onLeave', e); }
            }
        });
        step('attached', { fn: 'read' });
        attached++;
    }

    if (pread64) {
        Interceptor.attach(pread64, {
            onEnter(args) { this.fd = args[0].toInt32();
                this.buf = args[1];
                this.c = args[2].toInt32();
                this.off = args[3].toInt32(); },
            onLeave(ret) {
                try {
                    const n = ret.toInt32();
                    if (n > 0 && fds[this.fd]) {
                        const ba = Memory.readByteArray(this.buf, n);
                        send({ type: 'meta_chunk', size: n }, ba);
                        fds[this.fd].size += n;
                    }
                } catch (e) { jserr('pread64.onLeave', e); }
            }
        });
        step('attached', { fn: 'pread64' });
        attached++;
    }

    if (close) {
        Interceptor.attach(close, {
            onEnter(args) { this.fd = args[0].toInt32(); },
            onLeave(_ret) {
                try {
                    if (fds[this.fd]) {
                        step('close hit', { fd: this.fd, size: fds[this.fd].size, path: fds[this.fd].path });
                        send({ type: 'meta_done', size: fds[this.fd].size });
                        delete fds[this.fd];
                    }
                } catch (e) { jserr('close.onLeave', e); }
            }
        });
        step('attached', { fn: 'close' });
        attached++;
    }

    if (assetOpen) {
        Interceptor.attach(assetOpen, {
            onEnter(args) {
                try {
                    const n = Memory.readCString(args[1]);
                    if (n && n.indexOf(wantName) !== -1) {
                        step('AAssetManager_open hit', { name: n });
                    }
                } catch (e) { jserr('AAssetManager_open.onEnter', e); }
            }
        });
        step('attached', { fn: 'AAssetManager_open' });
        attached++;
    }

    if (attached > 0) ioHooked = true;
    return ioHooked;
}

// ===== 等库加载后自动重试 =====
let listenersSet = false;

function ensureRetryOnModuleLoad() {
    if (listenersSet) return;
    listenersSet = true;

    const mm = new ModuleMap(); // V8 运行时可用
    mm.events.listen('moduleLoaded', (m) => {
        try {
            const name = (m && m.name) ? m.name : '';
            if (!name) return;
            if (name.indexOf('libil2cpp.so') !== -1 || name.indexOf('libandroid.so') !== -1 || name.indexOf('libc.so') !== -1) {
                step('moduleLoaded', { name });
                tryHookIl2Cpp();
                tryHookFileIO();
            }
        } catch (e) { jserr('moduleLoaded', e); }
    });
    step('moduleLoad listener attached');
}

rpc.exports = {
    dumpmeta: function() {
        return new Promise(function(resolve, reject) {
            try {
                step('start script');

                // 先试一次（万一库已经加载了）
                const a = tryHookIl2Cpp();
                const b = tryHookFileIO();

                // 如果还没挂上，监听后续模块加载再重试
                if (!(a && b)) ensureRetryOnModuleLoad();

                // 另外加一个延迟重试（有的 ROM 不触发 moduleLoaded）
                setTimeout(function() {
                    tryHookIl2Cpp();
                    tryHookFileIO();
                }, 3000);

                resolve({ ok: true, note: 'hooks ready' });
            } catch (e) { jserr('rpc.dumpmeta', e);
                reject(e); }
        });
    }
};