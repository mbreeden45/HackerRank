// Loads the real js/worker.js in Node with a tiny shim, and runs a few jobs through the same Pyodide files the app ships.
const path = require('path'), fs = require('fs');
const root = path.join(__dirname, '..');
const msgs = [];
global.self = { location: { href: 'file://' + root + '/js/worker.js' }, postMessage: (m) => msgs.push(m) };
const py = require(path.join(root, 'vendor/pyodide/pyodide.js'));
global.loadPyodide = (o) => py.loadPyodide({ indexURL: path.join(root, 'vendor/pyodide/') });
global.importScripts = () => {};
global.URL = URL;
eval(fs.readFileSync(path.join(root, 'js/worker.js'), 'utf8').replace(/^importScripts.*$/m, ''));
const send = (m) => new Promise((res) => { const n = msgs.length; self.onmessage({ data: m }).then(() => res(msgs.slice(n).find((x) => x.id === m.id))); });
(async () => {
  const problems = JSON.parse(fs.readFileSync(path.join(root, 'content/problems.json')));
  let bad = 0, n = 0;
  const probs = process.argv[2] === 'all' ? problems : problems.filter((p, i) => i % 6 === 0);
  for (const p of probs) {
    const tests = p.samples.map((s) => [s.input, s.output]).concat(p.hidden.map((h) => [h.input, h.output]));
    const r = await send({ id: ++n, type: 'run', code: p.prefix + p.solution + p.suffix, inputs: tests.map((t) => t[0]) });
    r.results.forEach((x, i) => { const ok = !x.error && x.stdout.trim() === tests[i][1].trim(); if (!ok) { bad++; console.log('FAIL', p.id, JSON.stringify(tests[i][0]), JSON.stringify(x)); } });
    console.log('ran', p.id, r.results.length, 'tests');
  }
  const err = await send({ id: ++n, type: 'run', code: 'nums=[1]\nprint(nums[3])', inputs: [''] });
  console.log('error sample:', JSON.stringify(err.results[0].error.split('\n').slice(-2)));
  const loop = require('fs').readFileSync(path.join(root, 'content/lessons.json'));
  const L = JSON.parse(loop).find((l) => l.id === 'input');
  const t = await send({ id: ++n, type: 'trace', code: L.example.code, stdin: L.example.stdin });
  console.log('trace steps:', t.trace.steps.length, 'last out:', JSON.stringify(t.trace.out), 'sample vars:', JSON.stringify(t.trace.steps[t.trace.steps.length - 1].vars));
  console.log(bad ? 'BROWSER ENGINE FAILURES: ' + bad : 'Pyodide agrees on all tests run');
  process.exit(bad ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
