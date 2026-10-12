// Timed mock exam: mixed sections weighted by priority, no hints, then a score report with a line at 60 percent.
// Routes: #/mock (start page) and #/mock/start[/minutes]. The optional minutes value is a debug override, for example #/mock/start/0.2.
window.BP = window.BP || {};
BP.mock = (function () {
  const esc = (s) => BP.vis.esc(s);
  const fmt = (t) => esc(t).replace(/`([^`]+)`/g, '<code class="k">$1</code>');
  let timerId = null;
  function stopTimer() { if (timerId) { clearInterval(timerId); timerId = null; } }
  const mmss = (ms) => { const s = Math.max(0, Math.ceil(ms / 1000)); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };

  function kindOf(C, id) {
    let it = C.problems.find((p) => p.id === id); if (it) return { kind: 'py', item: it };
    it = C.sql.find((p) => p.id === id); if (it) return { kind: 'sql', item: it };
    const all = [].concat(C.quiz.prompt || [], C.quiz.bigo || []);
    it = all.find((q) => q.id === id); if (it) return { kind: it.type === 'written' ? 'written' : 'mc', item: it };
    return null;
  }
  function flat(C) {
    const out = [];
    C.mock.sections.forEach((sec) => sec.items.forEach((id) => out.push(Object.assign({ sec, id }, kindOf(C, id)))));
    return out;
  }

  function intro(main, C) {
    stopTimer();
    if (!C.mock) { main.innerHTML = '<div class="card">The mock exam is not part of this version.</div>'; return; }
    const d = BP.store.get(), M = C.mock, run = d.examRun;
    let h = '<h1>Mock exam</h1><div class="card"><p>This is a practice run of the real thing. Here is what to expect.</p><ul>' +
      '<li>' + M.minutes + ' minutes on one clock. The clock keeps running if you leave this page.</li>' +
      '<li>' + flat(C).length + ' questions in four sections: ' + M.sections.map((s) => esc(s.name) + ' (' + s.weight + ' points)').join(', ') + '.</li>' +
      '<li>No hints and no step-by-step help. You can run your code on the sample cases and on your own input.</li>' +
      '<li>When you submit, every coding question is run against all of its test cases, and you get a report by topic. The line to pass is ' + M.pass_percent + ' percent.</li>' +
      '<li>Written answers are marked by you, against a model answer, after you submit.</li></ul>';
    if (run) {
      const left = run.start + run.minutes * 60000 - Date.now();
      h += '<div class="callout">You have an exam in progress. ' + (left > 0 ? mmss(left) + ' left on the clock.' : 'Its time ran out, so it will be submitted now.') + '</div><div class="row"><a class="btn primary" href="#/mock/resume">' + (left > 0 ? 'Resume the exam' : 'Submit it and see the report') + '</a><button id="discard">Discard it</button></div>';
    } else h += '<a class="btn primary" href="#/mock/start">Start the exam</a> <span class="mute" style="font-size:13px">To try a short clock, use #/mock/start/0.5 for half a minute.</span>';
    h += '</div>';
    if (d.exams.length) h += '<div class="card"><h2>Your earlier attempts</h2><table><tr><th>Date</th><th>Score</th><th>Result</th></tr>' + d.exams.slice(-8).reverse().map((e) => '<tr><td>' + esc(new Date(e.date).toLocaleString()) + '</td><td>' + e.percent + ' percent</td><td>' + (e.percent >= M.pass_percent ? 'above the ' + M.pass_percent + ' percent line' : 'below the ' + M.pass_percent + ' percent line') + (e.timedOut ? ' (time ran out)' : '') + '</td></tr>').join('') + '</table></div>';
    main.innerHTML = h;
    const dc = main.querySelector('#discard'); if (dc) dc.onclick = () => { if (confirm('Discard the exam in progress?')) { BP.store.update((x) => { x.examRun = null; }); intro(main, C); } };
  }

  function begin(main, C, minutes) {
    BP.store.update((d) => { d.examRun = { start: Date.now(), minutes: minutes, answers: {} }; });
    runExam(main, C);
  }

  function runExam(main, C) {
    const run = BP.store.get().examRun;
    if (!run) { intro(main, C); return; }
    const items = flat(C);
    let idx = 0, saveT = null;
    const persist = () => { clearTimeout(saveT); saveT = setTimeout(() => BP.store.update(() => {}), 400); };
    const answered = (id) => { const a = run.answers[id]; return a !== undefined && a !== '' && a !== null; };
    main.innerHTML = '<div class="examtop"><b>Mock exam</b><span id="clock" class="clock"></span><span class="mute" id="prog"></span><button class="primary" id="submit">Submit exam</button></div>' +
      '<div class="examgrid"><div class="examnav card" id="nav"></div><div class="card" id="qbox"></div></div>';
    function nav() {
      let h = '', last = null;
      items.forEach((it, i) => {
        if (it.sec !== last) { h += '<div class="lbl" style="margin-top:8px">' + esc(it.sec.name) + '</div>'; last = it.sec; }
        h += '<button class="qn' + (i === idx ? ' cur' : '') + (answered(it.id) ? ' ans' : '') + '" data-i="' + i + '">' + (i + 1) + '</button>';
      });
      main.querySelector('#nav').innerHTML = h + '<p class="mute" style="font-size:13px;margin-top:10px">Filled in: ' + items.filter((it) => answered(it.id)).length + ' of ' + items.length + '</p>';
      main.querySelectorAll('.qn').forEach((b) => (b.onclick = () => { idx = Number(b.dataset.i); show(); }));
    }
    function save(id, val) { run.answers[id] = val; persist(); nav(); }
    function show() {
      const it = items[idx];
      nav();
      main.querySelector('#qbox').innerHTML = '<div class="row"><span class="mute">' + esc(it.sec.name) + ': question ' + (idx + 1) + ' of ' + items.length + '</span><span class="pill ' + it.item.difficulty + '">' + it.item.difficulty + '</span></div>' +
        '<div id="host" style="margin:10px 0"></div><div class="row"><button id="prev"' + (idx === 0 ? ' disabled' : '') + '>Previous</button><button id="next"' + (idx === items.length - 1 ? ' disabled' : '') + '>Next</button></div>';
      const host = main.querySelector('#host');
      if (it.kind === 'mc') {
        BP.quiz.renderItem(host, it.item, { exam: true, onAnswer: (a) => save(it.id, a.choice) });
        if (run.answers[it.id] !== undefined) { const b = host.querySelector('.opt[data-o="' + run.answers[it.id] + '"]'); if (b) b.classList.add('sel'); }
      } else if (it.kind === 'written') {
        BP.quiz.renderItem(host, it.item, { exam: true, prefill: run.answers[it.id], onAnswer: (a) => save(it.id, a.text) });
      } else if (it.kind === 'py') {
        BP.practice.view(host, it.item, C.lessons, false, { exam: true, initial: run.answers[it.id], onChange: (code) => save(it.id, code) });
      } else {
        BP.sqlscreen.view(host, it.item, C, false, { exam: true, initial: run.answers[it.id], onChange: (q) => save(it.id, q) });
      }
      main.querySelector('#prev').onclick = () => { idx--; show(); };
      main.querySelector('#next').onclick = () => { idx++; show(); };
    }
    const tick = () => {
      const left = run.start + run.minutes * 60000 - Date.now();
      const c = main.querySelector('#clock'); if (!c) { stopTimer(); return; }
      c.textContent = mmss(left); c.classList.toggle('low', left < 5 * 60000);
      if (left <= 0) { stopTimer(); finish(main, C, run, items, true); }
    };
    stopTimer(); timerId = setInterval(tick, 1000); tick();
    main.querySelector('#submit').onclick = () => { if (confirm('Submit the exam now? You cannot change your answers afterwards.')) { stopTimer(); finish(main, C, run, items, false); } };
    show();
  }

  async function score(C, items, run) {
    const res = [];
    for (const it of items) {
      const a = run.answers[it.id];
      let s = 0, note = '';
      if (it.kind === 'mc') { s = a === it.item.answer ? 1 : 0; note = a === undefined ? 'not answered' : s ? 'right' : 'wrong'; }
      else if (it.kind === 'written') { s = null; }
      else if (it.kind === 'py') {
        const P = it.item, code = a || (P.prefix + P.body + P.suffix);
        const tests = P.samples.map((x) => ({ input: x.input, output: x.output })).concat(P.hidden);
        const r = await BP.runner.runMany(tests.map((t) => BP.programs.forTest(P, code, t.input)));
        if (!r.ok) { s = 0; note = r.timeout ? 'ran out of time' : 'could not run'; }
        else { const pass = r.results.filter((x, i) => !x.error && BP.practice.norm(x.stdout) === BP.practice.norm(tests[i].output)).length; s = pass / tests.length; note = pass + ' of ' + tests.length + ' test cases passed'; }
      } else {
        const r = await BP.sql.exec(a || '', C.sqlTables);
        if (!r.ok) { s = 0; note = 'the query had an error'; }
        else { const c = BP.sql.compare(r, { columns: it.item.columns, rows: it.item.expected }, it.item.ordered); s = c.ok ? 1 : 0; note = c.ok ? 'matches the expected result' : c.why; }
      }
      res.push({ it, s, note });
    }
    return res;
  }

  async function finish(main, C, run, items, timedOut) {
    stopTimer();
    main.innerHTML = '<div class="card"><h1>' + (timedOut ? 'Time is up' : 'Submitted') + '</h1><p>Running every test case and checking your answers. This can take a little while.</p></div>';
    const res = await score(C, items, run);
    const written = res.filter((r) => r.s === null);
    if (!written.length) return report(main, C, run, res, timedOut);
    main.innerHTML = '<div class="card"><h1>' + (timedOut ? 'Time is up' : 'Submitted') + '. Mark your written answers</h1><p>For each written question, compare your answer with the model answer and tick every point you covered, even if you worded it differently. Be honest: this is for you.</p></div>' +
      written.map((r, i) => '<div class="card" data-k="' + i + '"><div class="mute">' + esc(r.it.sec.name) + '</div><p>' + fmt(r.it.item.prompt) + '</p><div class="lbl">Your answer</div><pre class="wrap">' + esc(run.answers[r.it.id] || '(no answer)') + '</pre><div class="rubhost"></div></div>').join('') +
      '<button class="primary" id="done">See my report</button>';
    const state = written.map(() => 0);
    written.forEach((r, i) => {
      const host = main.querySelectorAll('.rubhost')[i], q = r.it.item;
      host.innerHTML = '<div class="model">' + fmt(q.model).replace(/\n/g, '<br>') + '</div>' + q.rubric.map((p, k) => '<label class="rub"><input type="checkbox" data-i="' + i + '"> ' + fmt(p.point) + '</label>').join('');
      host.querySelectorAll('input').forEach((b) => (b.onchange = () => { state[i] = host.querySelectorAll('input:checked').length / q.rubric.length; }));
    });
    main.querySelector('#done').onclick = () => { written.forEach((r, i) => { r.s = state[i]; r.note = Math.round(state[i] * r.it.item.rubric.length) + ' of ' + r.it.item.rubric.length + ' points ticked'; }); report(main, C, run, res, timedOut); };
  }

  function report(main, C, run, res, timedOut) {
    const M = C.mock, PASS = M.pass_percent;
    const secs = M.sections.map((sec) => {
      const rs = res.filter((r) => r.it.sec === sec), mean = rs.reduce((a, r) => a + r.s, 0) / rs.length;
      return { sec, rs, earned: mean * sec.weight, pct: Math.round(mean * 100) };
    });
    const total = Math.round(secs.reduce((a, s) => a + s.earned, 0));
    const lost = secs.slice().sort((a, b) => (b.sec.weight - b.earned) - (a.sec.weight - a.earned))[0];
    const bar = (pct, label) => '<div class="mrow"><div class="mlabel">' + label + '</div><div class="mbar"><i class="' + (pct >= PASS ? '' : 'low') + '" style="width:' + pct + '%"></i><span class="line60" style="left:' + PASS + '%"></span></div><div class="mpct">' + pct + '%</div></div>';
    const used = Math.min(run.minutes, Math.round((Date.now() - run.start) / 600) / 100);
    let h = '<h1>Your mock exam report</h1><div class="card"><h2>' + total + ' percent</h2><p>' + (total >= PASS ? 'This is <b>above</b> the ' + PASS + ' percent line. That is a pass on this practice exam.' : 'This is <b>below</b> the ' + PASS + ' percent line. That is not a pass yet, and it tells you exactly where to practise.') + (timedOut ? ' The time ran out before you submitted.' : '') + '</p>' +
      '<div class="mkey"><span class="line60 inline"></span> the ' + PASS + ' percent line</div>' + bar(total, '<b>Overall</b>') + secs.map((s) => bar(s.pct, esc(s.sec.name))).join('') + '</div>';
    h += '<div class="card"><h2>By topic</h2><table><tr><th>Topic</th><th>Points</th><th>Score</th><th>Against the line</th></tr>' + secs.map((s) => '<tr><td>' + esc(s.sec.name) + '</td><td>' + s.earned.toFixed(1) + ' of ' + s.sec.weight + '</td><td>' + s.pct + '%</td><td>' + (s.pct >= PASS ? 'above' : 'below') + '</td></tr>').join('') + '</table></div>';
    h += '<div class="card"><h2>Recommended next focus</h2>' + (lost.sec.weight - lost.earned < 0.5 ? '<p>Nothing stands out. Try the mock exam again in a few days.</p>' : '<p>Start with <b>' + esc(lost.sec.name) + '</b>. You gave up ' + (lost.sec.weight - lost.earned).toFixed(1) + ' of its ' + lost.sec.weight + ' points, the most of any topic.</p><a class="btn primary" href="' + lost.sec.focus + '">Go to ' + esc(lost.sec.name) + '</a>') + '</div>';
    h += '<div class="card"><h2>Question by question</h2><table><tr><th>#</th><th>Topic</th><th>Result</th><th></th></tr>' + res.map((r, i) => {
      const href = r.it.kind === 'py' ? '#/problem/' + r.it.id : r.it.kind === 'sql' ? '#/sqlproblem/' + r.it.id : '#/quizitem/' + r.it.id;
      return '<tr><td>' + (i + 1) + '</td><td>' + esc(r.it.sec.name) + '</td><td>' + (r.s >= 0.999 ? '&#10003; full marks' : r.s <= 0 ? '&#10007; no marks' : 'partly (' + Math.round(r.s * 100) + '%)') + ' <span class="mute">' + esc(r.note) + '</span></td><td>' + (r.s < 0.999 ? '<a href="' + href + '">Practise this</a>' : '') + '</td></tr>';
    }).join('') + '</table></div><div class="row"><a class="btn primary" href="#/mock">Back to the mock exam page</a><a class="btn" href="#/">Home</a></div>';
    main.innerHTML = h;
    BP.store.update((d) => {
      d.exams.push({ date: new Date().toISOString(), percent: total, timedOut: !!timedOut, minutesUsed: used, sections: secs.map((s) => ({ id: s.sec.id, name: s.sec.name, pct: s.pct, earned: Math.round(s.earned * 10) / 10, weight: s.sec.weight })) });
      d.examRun = null;
    });
    res.forEach((r) => { if (r.s < 0.6 && BP.adaptive) BP.adaptive.record(r.it.id, false); });
  }

  BP.routeHandlers = BP.routeHandlers || [];
  BP.routeHandlers.push((r, main, C) => {
    if (r[0] !== 'mock') return false;
    if (r[1] === 'start') { if (BP.store.get().examRun) { runExam(main, C); } else begin(main, C, Number(r[2]) > 0 ? Number(r[2]) : C.mock.minutes); return true; }
    if (r[1] === 'resume') {
      const run = BP.store.get().examRun;
      if (run && run.start + run.minutes * 60000 <= Date.now()) { finish(main, C, run, flat(C), true); return true; }
      runExam(main, C); return true;
    }
    intro(main, C); return true;
  });
  return { stopTimer, intro };
})();
