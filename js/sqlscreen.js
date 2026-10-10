// SQL practice list and problem screen (mirrors the Python practice screen).
window.BP = window.BP || {};
BP.sqlscreen = (function () {
  const esc = (s) => BP.vis.esc(s);
  const fmt = (t) => esc(t).replace(/`([^`]+)`/g, '<code class="k">$1</code>');
  const HINT_NAMES = ['Nudge', 'Bigger hint', 'Plain-English plan', 'Pseudocode', 'Full solution'];

  function list(main, C) {
    const d = BP.store.get();
    let h = '<h1>SQL practice</h1><p class="mute">Each problem gives you the tables, a question and the shape of the answer. Write a query, run it, and check it.</p>';
    C.study.filter((l) => l.track === 'SQL Foundations').forEach((L) => {
      const ps = C.sql.filter((p) => p.lesson === L.id);
      const solved = ps.filter((p) => (d.problems[p.id] || {}).solved).length;
      h += '<div class="card"><h2>' + esc(L.title) + ' <span class="mute" style="font-size:14px">' + solved + ' of ' + ps.length + ' solved</span></h2><p><a href="#/study/' + L.id + '">Read the lesson</a></p><div class="grid">' +
        ps.map((p) => { const s = d.problems[p.id] || {}; return '<a class="item ' + (s.solved ? 'done' : '') + '" href="#/sqlproblem/' + p.id + '"><b>' + esc(p.title) + '</b><br><span class="pill ' + p.difficulty + '">' + p.difficulty + '</span> ' + (s.solved ? '<span class="pill done">solved</span>' : '') + '</a>'; }).join('') + '</div></div>';
    });
    main.innerHTML = h;
  }

  function schemaHtml(names, tables) {
    return names.map((n) => '<details open><summary><b>' + esc(n) + '</b></summary><table><tr><th>Column</th><th>Type</th><th>Meaning</th></tr>' +
      tables[n].columns.map((c) => '<tr><td><code class="k">' + esc(c[0]) + '</code></td><td>' + esc(c[1]) + '</td><td>' + esc(c[2]) + '</td></tr>').join('') + '</table></details>').join('');
  }

  // opts.exam: mock exam mode. No saved progress, no Check button, no hints.
  async function view(main, P, C, allowHints, opts) {
    opts = opts || {};
    allowHints = allowHints !== false;
    const st = opts.exam ? {} : BP.store.problem(P.id);
    const lessonTitle = (C.study.find((l) => l.id === P.lesson) || {}).title || '';
    const expected = { columns: P.columns, rows: P.expected };
    main.innerHTML = (opts.exam ? '' : BP.practice.flowBar(P, 'sql')) + '<div class="split"><div class="left"><div class="card">' +
      (opts.exam ? '' : '<div class="mute">' + esc(lessonTitle) + '</div>') + '<h1>' + esc(P.title) + '</h1>' +
      '<span class="pill ' + P.difficulty + '">' + P.difficulty + '</span> ' + (st.solved ? '<span class="pill done">solved</span>' : '') +
      P.statement.map((p) => '<p>' + fmt(p) + '</p>').join('') +
      '<h3>Tables you can use</h3>' + schemaHtml(P.tables, C.sqlTables) +
      '<h3>What the answer looks like</h3><p class="mute">Your result needs these ' + P.columns.length + ' column(s) in this order: ' + P.columns.map((c) => '<code class="k">' + esc(c) + '</code>').join(', ') + '. It should have ' + P.expected.length + ' row' + (P.expected.length === 1 ? '' : 's') + (P.ordered ? ', in the order the question asks for' : '') + '. Here are the first rows:</p>' +
      BP.sql.gridHtml(P.columns, P.expected.slice(0, 3), 3, P.expected.length) +
      '</div></div><div class="right"><div class="card"><div class="row" style="margin-bottom:8px"><b>SQL</b><span class="mute">The database runs in your browser. Nothing is sent anywhere.</span></div>' +
      '<textarea id="code"></textarea><div class="row" style="margin-top:8px"><button id="run">Run query</button><button class="primary" id="check">Check my answer</button><button id="reset">Reset</button></div>' +
      '<div class="results" id="res"></div></div>' +
      (allowHints ? '<div class="card"><h2>Need help</h2><p class="mute">Open one hint at a time. Each one gives away a little more.</p><div id="hints"></div><button id="hintbtn">Show hint 1: Nudge</button></div>' : '') + '</div></div>' + (opts.exam ? '' : BP.practice.flowBar(P, 'sql', true));
    const start = '-- Write your query here\n';
    const cm = CodeMirror.fromTextArea(main.querySelector('#code'), { mode: 'text/x-sqlite', lineNumbers: true, indentUnit: 2, indentWithTabs: false, extraKeys: { Tab: (c) => c.replaceSelection('  ') } });
    cm.setValue((opts.exam ? opts.initial : st.draft) || start);
    if (opts.exam) main.querySelector('#check').style.display = 'none';
    let t; cm.on('change', () => {
      if (opts.exam) { opts.onChange && opts.onChange(cm.getValue()); return; }
      clearTimeout(t); t = setTimeout(() => BP.store.update(() => { BP.store.problem(P.id).draft = cm.getValue(); }), 600);
    });
    const res = main.querySelector('#res');
    main.querySelector('#run').onclick = async () => { res.innerHTML = '<div class="mute">Running.</div>'; res.innerHTML = '<h3>Your result</h3>' + await BP.sql.runToHtml(cm.getValue(), C.sqlTables); };
    main.querySelector('#check').onclick = async () => {
      res.innerHTML = '<div class="mute">Checking.</div>';
      const r = await BP.sql.exec(cm.getValue(), C.sqlTables);
      let ok = false;
      if (!r.ok) res.innerHTML = '<div class="bad"><b>SQL error.</b> ' + esc(BP.sql.explain(r.error)) + '</div>';
      else {
        const c = BP.sql.compare(r, expected, P.ordered);
        ok = c.ok;
        res.innerHTML = ok ? '<div class="good"><b>Correct.</b> Your query returns the expected result. Nicely done.</div>' + (opts.exam ? '' : BP.practice.flowDone(P, 'sql')) + '<h3>Your result</h3>' + BP.sql.gridHtml(r.columns, r.rows)
          : '<div class="bad"><b>Not yet.</b> ' + esc(c.why) + '</div><div class="cmpgrid"><div><h3>Your result</h3>' + BP.sql.gridHtml(r.columns, r.rows) + '</div><div><h3>Expected result</h3>' + BP.sql.gridHtml(P.columns, P.expected) + '</div></div>';
      }
      BP.store.update(() => { const s = BP.store.problem(P.id); s.attempts++; s.lesson = P.lesson; s.difficulty = P.difficulty; s.last = ok ? 1 : 0; s.total = 1; s.best = Math.max(s.best, ok ? 1 : 0); if (ok) s.solved = true; });
      if (BP.adaptive) BP.adaptive.afterProblemRun(P.id, ok);
    };
    main.querySelector('#reset').onclick = () => cm.setValue(start);
    if (allowHints) {
      const hints = P.hints.concat([P.solution]);
      let shown = 0;
      const hb = main.querySelector('#hintbtn'), hd = main.querySelector('#hints');
      hb.onclick = () => {
        hd.insertAdjacentHTML('beforeend', '<div class="hint"><b>' + (shown + 1) + '. ' + HINT_NAMES[shown] + '</b><br>' + (shown === 4 ? '<pre>' + esc(P.solution) + '</pre>Type it in yourself rather than pasting, so it sticks.' : fmt(hints[shown])) + '</div>');
        shown++;
        BP.store.update(() => { const s = BP.store.problem(P.id); s.hints = Math.max(s.hints, shown); });
        if (shown === 5 && !BP.store.problem(P.id).solved && BP.adaptive) BP.adaptive.record(P.id, false);
        if (shown >= 5) hb.style.display = 'none'; else hb.textContent = 'Show hint ' + (shown + 1) + ': ' + HINT_NAMES[shown];
      };
    }
    return { cm };
  }

  BP.routeHandlers = BP.routeHandlers || [];
  BP.routeHandlers.push((r, main, C) => {
    if (r[0] === 'sql') { list(main, C); return true; }
    if (r[0] === 'sqlproblem') { const p = C.sql.find((x) => x.id === r[1]); p ? view(main, p, C) : (main.innerHTML = 'Problem not found.'); return true; }
    return false;
  });
  return { list, view };
})();
