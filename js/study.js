// Viewer for reading-style lessons (Prompt Engineering, SQL Foundations). Content lives in content/lessons_x.json.
// Block types: p, h, code, compare (weak vs strong), table, callout, warn, sql (a runnable query), steps.
window.BP = window.BP || {};
BP.study = (function () {
  const esc = (s) => BP.vis.esc(s);
  const fmt = (t) => esc(t).replace(/`([^`]+)`/g, '<code class="k">$1</code>');

  function block(b, idx) {
    switch (b.t) {
      case 'h': return '<h3>' + fmt(b.text) + '</h3>';
      case 'p': return '<p>' + fmt(b.text) + '</p>';
      case 'code': return (b.label ? '<div class="lbl">' + esc(b.label) + '</div>' : '') + '<pre>' + esc(b.text) + '</pre>';
      case 'callout': return '<div class="callout">' + fmt(b.text) + '</div>';
      case 'warn': return '<div class="warnbox">' + fmt(b.text) + '</div>';
      case 'steps': return '<ol>' + b.items.map((x) => '<li>' + fmt(x) + '</li>').join('') + '</ol>';
      case 'table': return BP.vis.table(b.head, b.rows, { title: b.title });
      case 'compare': return '<div class="cmp"><div class="cmp-bad"><div class="lbl">' + esc(b.badLabel || 'Weaker') + '</div><pre class="wrap">' + esc(b.bad) + '</pre><p class="mute">' + fmt(b.badWhy) + '</p></div>' +
        '<div class="cmp-good"><div class="lbl">' + esc(b.goodLabel || 'Stronger') + '</div><pre class="wrap">' + esc(b.good) + '</pre><p class="mute">' + fmt(b.goodWhy) + '</p></div></div>';
      case 'sql': return '<div class="sqlblock" data-i="' + idx + '"><div class="lbl">' + esc(b.label || 'Try this query') + '</div><textarea class="sqled" rows="' + Math.max(2, b.text.split('\n').length) + '">' + esc(b.text) + '</textarea><div class="row"><button class="primary sqlrun">Run query</button><span class="mute">You can edit the query and run it again.</span></div><div class="sqlout"></div></div>';
      default: return '';
    }
  }

  function view(main, lessons, id, C) {
    const L = lessons.find((l) => l.id === id);
    if (!L) { main.innerHTML = '<div class="card">Lesson not found.</div>'; return; }
    const group = lessons.filter((l) => l.track === L.track), gi = group.indexOf(L);
    const done = BP.store.get().lessons[id];
    let h = '<div class="card"><div class="mute">' + esc(L.track) + ': lesson ' + (gi + 1) + ' of ' + group.length + '</div><h1>' + esc(L.title) + '</h1>';
    h += L.blocks.map((b, i) => block(b, i)).join('');
    h += '</div>';
    const sqlProbs = (C.sql || []).filter((p) => p.lesson === id);
    if (sqlProbs.length) h += '<div class="card"><h2>Now you try</h2><p>' + fmt(L.after.text) + ' This lesson has ' + sqlProbs.length + ' problems.</p><a class="btn primary" href="#/sqlproblem/' + sqlProbs[0].id + '">Start practice problem 1 of ' + sqlProbs.length + ' &rarr;</a><div class="grid" style="margin-top:12px">' + sqlProbs.map((p, k) => '<a class="item" href="#/sqlproblem/' + p.id + '"><b>' + (k + 1) + '. ' + esc(p.title) + '</b><br><span class="pill ' + p.difficulty + '">' + p.difficulty + '</span></a>').join('') + '</div></div>';
    else if (L.after) h += '<div class="card"><h2>Now you try</h2><p>' + fmt(L.after.text) + '</p><a class="btn primary" href="' + L.after.href + '">' + esc(L.after.button) + '</a></div>';
    h += '<div class="row"><button class="primary" id="fin">' + (done ? 'Lesson marked complete' : 'Mark lesson complete') + '</button>' +
      (gi + 1 < group.length ? '<a class="btn" href="#/study/' + group[gi + 1].id + '">Next lesson: ' + esc(group[gi + 1].title) + '</a>' : '') + '</div>';
    main.innerHTML = h;
    main.querySelector('#fin').onclick = () => { BP.store.update((d) => { d.lessons[id] = { done: true }; }); main.querySelector('#fin').textContent = 'Lesson marked complete'; };
    main.querySelectorAll('.sqlblock').forEach((el) => {
      const out = el.querySelector('.sqlout');
      el.querySelector('.sqlrun').onclick = async () => {
        out.innerHTML = '<div class="mute">Running.</div>';
        out.innerHTML = await BP.sql.runToHtml(el.querySelector('.sqled').value, C.sqlTables);
      };
    });
  }

  BP.routeHandlers = BP.routeHandlers || [];
  BP.routeHandlers.push((r, main, C) => {
    if (r[0] === 'study') { view(main, C.study, r[1], C); return true; }
    return false;
  });
  return { view };
})();
