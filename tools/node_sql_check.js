// Runs every SQL solution and every runnable lesson query through the vendored sql.js (the same engine the app uses in the browser),
// and compares the rows with the content built by Python's sqlite3.
const path = require('path'), fs = require('fs');
const root = path.join(__dirname, '..');
const initSqlJs = require(path.join(root, 'vendor/sqljs/sql-wasm.js'));
const C = (f) => JSON.parse(fs.readFileSync(path.join(root, 'content', f)));
const norm = (v) => (typeof v === 'number' ? Math.round(v * 1e6) / 1e6 : v);
(async () => {
  const SQL = await initSqlJs({ locateFile: (f) => path.join(root, 'vendor/sqljs', f) });
  const tables = C('sql_tables.json'), probs = C('sql_problems.json'), study = C('lessons_x.json');
  const open = () => { const db = new SQL.Database(); Object.values(tables).forEach((t) => db.run(t.create)); return db; };
  let bad = 0, n = 0;
  for (const p of probs) {
    const db = open();
    const sets = db.exec(p.solution);
    const rows = sets.length ? sets[0].values : [];
    const a = rows.map((r) => JSON.stringify(r.map(norm))), e = p.expected.map((r) => JSON.stringify(r.map(norm)));
    const same = p.ordered ? a.join('|') === e.join('|') : a.slice().sort().join('|') === e.slice().sort().join('|');
    if (!same) { bad++; console.log('FAIL', p.id, 'sql.js gives', JSON.stringify(rows.slice(0, 3)), 'expected', JSON.stringify(p.expected.slice(0, 3))); }
    n++; db.close();
  }
  let q = 0;
  for (const L of study) for (const b of L.blocks) if (b.t === 'sql') {
    const db = open();
    try { db.exec(b.text); q++; } catch (err) { bad++; console.log('FAIL lesson query', L.id, err.message); }
    db.close();
  }
  console.log('sql.js agrees with sqlite3 on ' + (n - bad) + ' of ' + n + ' problems, and ran ' + q + ' lesson queries.');
  process.exit(bad ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
