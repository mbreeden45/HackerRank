// Main-thread side of the Python runner. Kills and restarts the worker on timeout.
window.BP = window.BP || {};
BP.runner = (function () {
  let worker = null, nextId = 1, pending = {}, isReady = false, readyWaiters = [];
  function start() {
    isReady = false;
    worker = new Worker('js/worker.js');
    worker.onmessage = (ev) => {
      const m = ev.data;
      if (m.type === 'ready') { isReady = true; readyWaiters.splice(0).forEach((f) => f()); BP.ui && BP.ui.setEngine('ready'); return; }
      if (m.type === 'fail') { BP.ui && BP.ui.setEngine('fail: ' + m.error); return; }
      if (m.id && pending[m.id]) { const p = pending[m.id]; delete pending[m.id]; clearTimeout(p.timer); p.resolve(m); }
    };
    BP.ui && BP.ui.setEngine('loading');
  }
  function whenReady() { return isReady ? Promise.resolve() : new Promise((r) => readyWaiters.push(r)); }
  function call(msg, timeoutMs) {
    return whenReady().then(() => new Promise((resolve) => {
      const id = nextId++;
      msg.id = id;
      const timer = setTimeout(() => {
        delete pending[id];
        worker.terminate(); start();
        resolve({ ok: false, timeout: true });
      }, timeoutMs);
      pending[id] = { resolve, timer };
      worker.postMessage(msg);
    }));
  }
  start();
  return {
    // inputs: array of stdin strings. Returns {ok, results:[{stdout,error}]} or {timeout:true}
    run(code, inputs) { return call({ type: 'run', code, inputs }, 4000 + 2500 * inputs.length); },
    // items: array of {code, stdin}, one program per test. Returns {ok, results:[{stdout,error}]} or {timeout:true}
    runMany(items) { return call({ type: 'runmany', items }, 4000 + 2500 * items.length); },
    trace(code, stdin) { return call({ type: 'trace', code, stdin: stdin || '' }, 8000); },
    isReady() { return isReady; },
    whenReady,
  };
})();
