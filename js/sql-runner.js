// SQL engine glue: sql.js (SQLite compiled to WebAssembly, vendored in vendor/sqljs). Every run uses a fresh in-memory database.
window.BP = window.BP || {};
BP.sql = (function () {
  const esc = (s) => BP.vis.esc(s);
  let SQLp = null;
  function init() {
    if (!SQLp) SQLp = initSqlJs({ locateFile: (f) => 'vendor/sqljs/' + f });
    return SQLp;
  }
  async function open(tables) {
    const SQL = await init();
    const db = new SQL.Database();
    Object.keys(tables).forEach((n) => db.run(tables[n].create));
    return db;
  }
  // Returns {ok:true, columns, rows} for the last statement that produced rows, or {ok:false, error}.
  async function exec(query, tables) {
    let db;
    try {
      db = await open(tables);
      const sets = db.exec(query);
      if (!sets.length) return { ok: true, columns: [], rows: [] };
      const last = sets[sets.length - 1];
      return { ok: true, columns: last.columns, rows: last.values };
    } catch (e) {
      return { ok: false, error: String(e.message || e) };
    } finally {
      if (db) db.close();
    }
  }
  const norm = (v) => (typeof v === 'number' ? Math.round(v * 1e6) / 1e6 : v);
  const key = (row) => JSON.stringify(row.map(norm));
  // Same rows (any order unless ordered). Column names are not compared, only the values.
  function compare(actual, expected, ordered) {
    if (actual.columns.length !== expected.columns.length) return { ok: false, why: 'Your result has ' + actual.columns.length + ' column(s) but the expected result has ' + expected.columns.length + '.' };
    if (actual.rows.length !== expected.rows.length) return { ok: false, why: 'Your result has ' + actual.rows.length + ' row(s) but the expected result has ' + expected.rows.length + '.' };
    let a = actual.rows.map(key), e = expected.rows.map(key);
    if (!ordered) { a = a.slice().sort(); e = e.slice().sort(); }
    for (let i = 0; i < a.length; i++) if (a[i] !== e[i]) return { ok: false, why: ordered && actual.rows.map(key).slice().sort().join('|') === expected.rows.map(key).slice().sort().join('|') ? 'You have the right rows, but not in the order that the question asks for.' : 'The rows are not the same as the expected rows.' };
    return { ok: true };
  }
  const FRIENDLY = [
    [/no such table: (\S+)/, (m) => 'There is no table called ' + m[1] + '. Check the spelling against the table list.'],
    [/no such column: (\S+)/, (m) => 'There is no column called ' + m[1] + '. Check the spelling, and if you used a table nickname, make sure it is spelled the same each time.'],
    [/ambiguous column name: (\S+)/, (m) => 'The column ' + m[1] + ' exists in more than one table. Put the table name or nickname and a dot in front of it.'],
    [/near "([^"]*)": syntax error/, (m) => 'SQL could not read the query near "' + m[1] + '". Look for a missing comma, a missing quote mark, or keywords in the wrong order.'],
    [/incomplete input/, () => 'The query stops too early. Check for a missing closing bracket or quote mark.'],
    [/misuse of aggregate/, () => 'An aggregate such as COUNT or SUM cannot be used in WHERE. Use HAVING to filter on a total.'],
  ];
  function explain(msg) {
    for (const [re, f] of FRIENDLY) { const m = re.exec(msg); if (m) return f(m); }
    return 'SQL reported: ' + msg;
  }
  function gridHtml(columns, rows, limit, total) {
    limit = limit || 60;
    total = total === undefined ? rows.length : total;
    if (!columns.length) return '<div class="mute">The query ran, but it returned no table.</div>';
    const shown = rows.slice(0, limit);
    return '<div class="tt"><table class="resgrid"><tr>' + columns.map((c) => '<th>' + esc(c) + '</th>').join('') + '</tr>' +
      (shown.length ? shown.map((r) => '<tr>' + r.map((v) => '<td>' + (v === null ? '<span class="mute">NULL</span>' : esc(String(v))) + '</td>').join('') + '</tr>').join('') : '<tr><td colspan="' + columns.length + '" class="mute">No rows</td></tr>') +
      '</table></div><div class="mute">' + total + ' row' + (total === 1 ? '' : 's') + (total > shown.length ? ', showing the first ' + shown.length : '') + '</div>';
  }
  async function runToHtml(query, tables) {
    const r = await exec(query, tables);
    if (!r.ok) return '<div class="bad"><b>SQL error.</b> ' + esc(explain(r.error)) + '</div>';
    return gridHtml(r.columns, r.rows);
  }
  return { init, open, exec, compare, explain, gridHtml, runToHtml };
})();
