window.BP = window.BP || {};
BP.lesson = (function () {
  const esc = (s) => BP.vis.esc(s);
  const fmt = (t) => esc(t).replace(/`([^`]+)`/g, '<code class="k">$1</code>');

  function staticVisual(v) {
    if (v.type === 'dict') return BP.vis.dictv(v.pairs, { title: v.title });
    if (v.type === 'table') return BP.vis.table(v.head, v.rows, { title: v.title });
    if (v.type === 'grid') return BP.vis.grid(v.rows, { title: v.title, r: v.r, c: v.c });
    return BP.vis.boxes(v.items, { title: v.title, pointers: v.pointers, hl: v.hl, negative: v.negative });
  }

  function tracePlayer(host, ex, lesson) {
    host.innerHTML = '<div class="mute">Loading the step-by-step view. The Python engine can take a few seconds the first time.</div>';
    BP.runner.trace(ex.code, ex.stdin).then((res) => {
      if (!res.ok) { host.innerHTML = '<div class="bad">The step-by-step view could not run: ' + esc(res.timeout ? 'it took too long' : res.error) + '</div>'; return; }
      const tr = res.trace, steps = tr.steps;
      const lines = ex.code.replace(/\n$/, '').split('\n');
      const cols = [];
      steps.forEach((s) => Object.keys(s.vars).forEach((k) => { if (cols.indexOf(k) < 0) cols.push(k); }));
      let cur = 0;
      host.innerHTML = '<div class="trace"><div><div class="lbl">Code</div><div class="codebox" id="cb"></div></div>' +
        '<div><div class="lbl">Picture</div><div id="pic"></div><div class="lbl">Printed so far</div><div class="outbox" id="ob"></div></div></div>' +
        '<div class="note" id="nt"></div>' +
        '<div class="row"><button id="pv">Back</button><button class="primary" id="nx">Next line</button><button id="rs">Start again</button><span class="mute" id="pos"></span></div>' +
        '<div class="lbl" style="margin-top:10px">Trace table (one row per line that ran)</div><div class="tt"><table id="ttb"></table></div>';
      const cb = host.querySelector('#cb');
      cb.innerHTML = lines.map((l, i) => '<div class="ln" data-n="' + (i + 1) + '"><span class="n">' + (i + 1) + '</span><span>' + esc(l) + '</span></div>').join('');
      function render() {
        const s = steps[cur];
        cb.querySelectorAll('.ln').forEach((d) => d.classList.toggle('cur', Number(d.dataset.n) === s.line && s.event === 'line'));
        host.querySelector('#pic').innerHTML = BP.vis.forStep(s.vars, lesson.visual || ex);
        host.querySelector('#ob').textContent = s.out || '(nothing yet)';
        let note;
        if (s.event === 'return') note = s.fn === '<module>' ? 'The program has finished.' : 'The function ' + s.fn + ' is done and hands back ' + BP.vis.show(s.ret) + '.';
        else {
          const nextS = steps[cur + 1];
          note = 'About to run line ' + s.line + ': ' + lines[s.line - 1].trim();
          if (nextS) {
            const changed = Object.keys(nextS.vars).filter((k) => JSON.stringify(nextS.vars[k]) !== JSON.stringify(s.vars[k]));
            if (changed.length) note += '   After it: ' + changed.map((k) => k + ' becomes ' + BP.vis.show(nextS.vars[k])).join(', ') + '.';
          }
        }
        host.querySelector('#nt').textContent = note;
        host.querySelector('#pos').textContent = 'Step ' + (cur + 1) + ' of ' + steps.length;
        let h = '<tr><th>Line</th>' + cols.map((c) => '<th>' + esc(c) + '</th>').join('') + '</tr>';
        for (let i = 0; i <= cur; i++) {
          const st = steps[i];
          h += '<tr class="' + (i === cur ? 'cur' : '') + '"><td>' + st.line + '</td>' + cols.map((c) => '<td>' + (c in st.vars ? esc(BP.vis.show(st.vars[c])) : '') + '</td>').join('') + '</tr>';
        }
        host.querySelector('#ttb').innerHTML = h;
        host.querySelector('#nx').disabled = cur >= steps.length - 1;
        host.querySelector('#pv').disabled = cur <= 0;
      }
      host.querySelector('#nx').onclick = () => { if (cur < steps.length - 1) { cur++; render(); } };
      host.querySelector('#pv').onclick = () => { if (cur > 0) { cur--; render(); } };
      host.querySelector('#rs').onclick = () => { cur = 0; render(); };
      render();
    });
  }

  function view(main, lessons, problems, id) {
    const L = lessons.find((l) => l.id === id);
    if (!L) { main.innerHTML = '<div class="card">Lesson not found.</div>'; return; }
    const idx = lessons.indexOf(L);
    const done = BP.store.get().lessons[id];
    let h = '<div class="card"><div class="mute">Lesson ' + (idx + 1) + ' of ' + lessons.length + '</div><h1>' + esc(L.title) + '</h1>';
    h += L.idea.map((p) => '<p>' + fmt(p) + '</p>').join('');
    if (L.symbols && L.symbols.length) h += '<h3>Symbols in this lesson</h3><table class="sym"><tr><th>Symbol</th><th>What it means</th></tr>' + L.symbols.map((s) => '<tr><td>' + esc(s[0]) + '</td><td>' + fmt(s[1]) + '</td></tr>').join('') + '</table>';
    (L.visuals || []).forEach((v) => (h += staticVisual(v)));
    h += '</div>';
    h += '<div class="card"><h2>Worked example</h2><p>' + fmt(L.example.caption) + '</p><div id="player"></div></div>';
    if (L.example2) h += '<div class="card"><h2>A second worked example</h2><p>' + fmt(L.example2.caption) + '</p><div id="player2"></div></div>';
    h += '<div class="card"><h2>Predict the output</h2><p>Read the code, decide what it prints, then pick an answer.</p><pre>' + esc(L.predict.code) + '</pre><div id="pq">' +
      L.predict.options.map((o, i) => '<button class="opt" data-i="' + i + '">' + esc(o) + '</button>').join('') + '</div><div id="pa"></div></div>';
    const probs = problems.filter((p) => p.lesson === id);
    h += '<div class="card"><h2>Now you try</h2>' + (probs.length ? '<p>These practice problems use only what you have just seen.</p>' : '<p>This lesson has questions instead of coding problems.</p>') + (L.practice_link ? '<p><a class="btn primary" href="' + L.practice_link.href + '">' + esc(L.practice_link.text) + '</a></p>' : '') + '<div class="grid">' +
      probs.map((p) => { const st = BP.store.get().problems[p.id]; return '<a class="item ' + (st && st.solved ? 'done' : '') + '" href="#/problem/' + p.id + '"><b>' + esc(p.title) + '</b><br><span class="pill ' + p.difficulty + '">' + p.difficulty + '</span> ' + (st && st.solved ? '<span class="pill done">solved</span>' : '') + '</a>'; }).join('') + '</div></div>';
    h += '<div class="row"><button class="primary" id="fin">' + (done ? 'Lesson marked complete' : 'Mark lesson complete') + '</button>' +
      (idx + 1 < lessons.length ? '<a class="btn" href="#/lesson/' + lessons[idx + 1].id + '">Next lesson: ' + esc(lessons[idx + 1].title) + '</a>' : '') + '</div>';
    main.innerHTML = h;
    tracePlayer(main.querySelector('#player'), L.example, L);
    if (L.example2) tracePlayer(main.querySelector('#player2'), L.example2, L);
    main.querySelectorAll('#pq .opt').forEach((b) => (b.onclick = () => {
      const i = Number(b.dataset.i), ok = i === L.predict.answer;
      main.querySelectorAll('#pq .opt').forEach((x, j) => { x.disabled = true; if (j === L.predict.answer) x.classList.add('right'); else if (j === i) x.classList.add('wrong'); });
      main.querySelector('#pa').innerHTML = '<div class="' + (ok ? 'good' : 'bad') + '">' + (ok ? 'That is right. ' : 'Not quite. ') + fmt(L.predict.why) + '</div>';
      BP.store.update((d) => { d.quiz['pred-' + id] = ok; });
    }));
    main.querySelector('#fin').onclick = () => { BP.store.update((d) => { d.lessons[id] = { done: true }; }); main.querySelector('#fin').textContent = 'Lesson marked complete'; };
  }
  return { view };
})();
