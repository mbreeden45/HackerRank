// Runs Python (Pyodide) off the main page so an endless loop cannot freeze the app.
importScripts(new URL('../vendor/pyodide/pyodide.js', self.location.href).href);

const TRACER = `
import sys, io, contextlib
def _conv(v, d=0):
    if v is None or isinstance(v, (bool, int, float)): return (True, v)
    if isinstance(v, str): return (True, v if len(v) <= 60 else v[:57] + '...')
    if d > 2: return (True, {'t': 'obj', 'v': repr(v)[:30]})
    if isinstance(v, (list, tuple)):
        return (True, {'t': type(v).__name__, 'v': [_conv(x, d + 1)[1] for x in list(v)[:30]]})
    if isinstance(v, dict):
        return (True, {'t': 'dict', 'v': [[_conv(k, d + 1)[1], _conv(x, d + 1)[1]] for k, x in list(v.items())[:30]]})
    if isinstance(v, (set, frozenset)):
        return (True, {'t': 'set', 'v': [_conv(x, d + 1)[1] for x in list(v)[:30]]})
    return (False, None)

class _Stop(Exception): pass

def bp_trace(code, maxsteps=300):
    steps = []
    buf = io.StringIO()
    def tracer(frame, event, arg):
        if frame.f_code.co_filename != '<lesson>': return None
        if event in ('line', 'return'):
            if len(steps) >= maxsteps: raise _Stop()
            locs = {}
            for k, v in frame.f_locals.items():
                if k.startswith('__'): continue
                ok, c = _conv(v)
                if ok: locs[k] = c
            ret = None
            if event == 'return': ret = _conv(arg)[1]
            steps.append({'line': frame.f_lineno, 'event': event, 'fn': frame.f_code.co_name,
                          'vars': locs, 'out': buf.getvalue(), 'ret': ret})
        return tracer
    err = None
    try:
        sys.settrace(tracer)
        with contextlib.redirect_stdout(buf):
            exec(compile(code, '<lesson>', 'exec'), {'__name__': '__main__'})
    except _Stop:
        err = 'stopped'
    except BaseException as e:
        err = type(e).__name__ + ': ' + str(e)
    finally:
        sys.settrace(None)
    return {'steps': steps, 'err': err, 'out': buf.getvalue()}
`;

let py = null;
let ready = (async () => {
  py = await loadPyodide({ indexURL: new URL('../vendor/pyodide/', self.location.href).href });
  py.runPython(TRACER);
})();

function setIO(stdinText, outArr, errArr) {
  const lines = String(stdinText || '').split('\n');
  if (lines.length && lines[lines.length - 1] === '') lines.pop();
  let i = 0;
  py.setStdin({ stdin: () => (i < lines.length ? lines[i++] : null) });
  py.setStdout({ batched: (s) => outArr.push(s) });
  py.setStderr({ batched: (s) => errArr.push(s) });
}

function runOne(code, stdinText) {
  const out = [], errs = [];
  setIO(stdinText, out, errs);
  const g = py.globals.get('dict')();
  g.set('__name__', '__main__');
  let error = null;
  try { py.runPython(code, { globals: g }); }
  catch (e) { error = String(e.message || e); }
  finally { g.destroy(); }
  return { stdout: out.join('\n'), error };
}

self.onmessage = async (ev) => {
  const m = ev.data;
  try {
    await ready;
    if (m.type === 'run') {
      self.postMessage({ id: m.id, ok: true, results: m.inputs.map((inp) => runOne(m.code, inp)) });
    } else if (m.type === 'runmany') {
      self.postMessage({ id: m.id, ok: true, results: m.items.map((it) => runOne(it.code, it.stdin)) });
    } else if (m.type === 'trace') {
      setIO(m.stdin, [], []);
      const f = py.globals.get('bp_trace');
      const r = f(m.code);
      const js = r.toJs({ dict_converter: Object.fromEntries });
      r.destroy();
      self.postMessage({ id: m.id, ok: true, trace: js });
    }
  } catch (e) {
    self.postMessage({ id: m.id, ok: false, error: String(e.message || e) });
  }
};
self.postMessage({ type: 'boot' });
ready.then(() => self.postMessage({ type: 'ready' }), (e) => self.postMessage({ type: 'fail', error: String(e) }));
