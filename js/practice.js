window.BP = window.BP || {};
BP.practice = (function () {
  const esc = (s) => BP.vis.esc(s);
  const fmt = (t) => esc(t).replace(/`([^`]+)`/g, '<code class="k">$1</code>');
  const norm = (s) => String(s).split('\n').map((l) => l.replace(/\s+$/, '')).join('\n').replace(/\n+$/, '');
  const HINT_NAMES = ['Nudge', 'Bigger hint', 'Plain-English plan', 'Pseudocode', 'Full solution'];

  // opts.exam: mock exam mode. No saved progress, no breadcrumb, no Run all test cases (the exam scores the code when you submit).
  // Navigation between the practice problems of one lesson, and back to the lesson. kind: 'py' or 'sql'.
  function flow(P, kind) {
    const C = BP.app.C, sql = kind === 'sql';
    const sibs = (sql ? C.sql : C.problems).filter((p) => p.lesson === P.lesson), i = sibs.findIndex((p) => p.id === P.id);
    const url = (p) => (sql ? '#/sqlproblem/' : '#/problem/') + p.id;
    const lessons = sql ? C.study.filter((l) => l.track === 'SQL Foundations') : C.lessons;
    const li = lessons.findIndex((l) => l.id === P.lesson), L = lessons[li] || {};
    const lessonHref = (sql ? '#/study/' : '#/lesson/') + P.lesson, nl = lessons[li + 1];
    return { sibs, i, url, L, lessonHref, nextLesson: nl ? { href: (sql ? '#/study/' : '#/lesson/') + nl.id, title: nl.title } : null, list: sql ? '#/sql' : '#/practice' };
  }
  // Strip across the top (and again at the bottom): lesson on the left, position in the middle, previous and next on the right.
  function flowBar(P, kind, foot) {
    const f = flow(P, kind), prev = f.sibs[f.i - 1], next = f.sibs[f.i + 1];
    return '<div class="flowbar' + (foot ? ' foot' : '') + '"><div class="fl"><a class="btn" href="' + f.lessonHref + '">&larr; Lesson</a><a class="flowall" href="' + f.list + '">All practice</a></div>' +
      '<div class="fc"><span class="flowpos">Problem ' + (f.i + 1) + ' of ' + f.sibs.length + '</span></div>' +
      '<div class="fr">' + (prev ? '<a class="btn" href="' + f.url(prev) + '">&larr; Previous</a>' : '') + (next ? '<a class="btn primary" href="' + f.url(next) + '">Next &rarr;</a>' : (f.nextLesson ? '<a class="btn primary" href="' + f.nextLesson.href + '">Next lesson &rarr;</a>' : '')) + '</div></div>';
  }
  function flowDone(P, kind) {
    const f = flow(P, kind), next = f.sibs[f.i + 1];
    return '<div class="row flowdone">' + (next ? '<a class="btn primary" href="' + f.url(next) + '">Next problem: ' + esc(next.title) + ' &rarr;</a>' :
      '<span><b>That was the last problem for this lesson.</b></span>' + (f.nextLesson ? '<a class="btn primary" href="' + f.nextLesson.href + '">Next lesson: ' + esc(f.nextLesson.title) + ' &rarr;</a>' : '')) +
      '<a class="btn" href="' + f.lessonHref + '">Back to the lesson</a><a class="btn" href="' + f.list + '">All practice</a></div>';
  }

  function view(main, P, lessons, allowHints, opts) {
    opts = opts || {};
    allowHints = allowHints !== false;
    const lessonTitle = (lessons.find((l) => l.id === P.lesson) || {}).title || '';
    const st = opts.exam ? {} : BP.store.problem(P.id);
    const preset = P.mode === 'preset';
    const inLabel = preset ? 'Starting data (the grey lines for this test)' : 'Input';
    let h = (opts.exam ? '' : flowBar(P, 'py')) + '<div class="split"><div class="left"><div class="card">' +
      (opts.exam ? '' : '<div class="mute">' + esc(lessonTitle) + '</div>') + '<h1>' + esc(P.title) + '</h1>' +
      '<span class="pill ' + P.difficulty + '">' + P.difficulty + '</span> ' + (st.solved ? '<span class="pill done">solved</span>' : '') +
      P.statement.map((p) => '<p>' + fmt(p) + '</p>').join('') +
      '<h3>Input format</h3><p>' + fmt(P.input_fmt) + '</p><h3>Output format</h3><p>' + fmt(P.output_fmt) + '</p>' +
      (P.constraints ? '<h3>Constraints</h3><p>' + fmt(P.constraints) + '</p>' : '') +
      P.samples.map((s, i) => '<h3>Sample ' + i + '</h3><div class="lbl">' + inLabel + '</div><pre>' + esc(s.input) + '</pre><div class="lbl">Output</div><pre>' + esc(s.output) + '</pre><p><b>Explanation.</b> ' + fmt(s.explanation) + '</p>').join('') +
      '</div></div><div class="right"><div class="card"><div class="row" style="margin-bottom:8px"><b>Python 3</b><span class="mute">Grey lines are locked. Write inside the open part.</span></div>' +
      '<textarea id="code"></textarea>' +
      '<div class="row" style="margin-top:8px"><button id="run">Run Code</button><button class="primary" id="all">Run all test cases</button><button id="cust">Custom Input</button><button id="expl">What does this line mean</button><button id="reset">Reset code</button></div>' +
      '<div id="custbox" style="display:none;margin-top:8px"><div class="lbl">' + (preset ? 'Your own starting data (it replaces the grey lines for this run)' : 'Custom input (what you would type)') + '</div><textarea class="custom" id="custin">' + (preset ? esc(P.prefix) : '') + '</textarea><button id="custrun" style="margin-top:6px">Run with this input</button></div>' +
      '<div id="lineinfo"></div><div class="results" id="res"></div></div>' +
      (allowHints ? '<div class="card"><h2>Need help</h2><p class="mute">Open one hint at a time. Each one gives away a little more.</p><div id="hints"></div><button id="hintbtn">Show hint 1: Nudge</button></div>' : '') +
      '</div></div>';
    if (!opts.exam) h += flowBar(P, 'py', true);
    main.innerHTML = h;

    const np = P.prefix ? P.prefix.replace(/\n$/, '').split('\n').length : 0;
    const full = P.prefix + P.body + P.suffix;
    const cm = CodeMirror.fromTextArea(main.querySelector('#code'), { mode: 'python', lineNumbers: true, indentUnit: 4, matchBrackets: true, indentWithTabs: false, extraKeys: { Tab: (c) => c.replaceSelection('    ') } });
    const saved = opts.exam ? opts.initial : (BP.store.get().problems[P.id] || {}).draft;
    if (opts.exam) main.querySelector('#all').style.display = 'none';
    cm.setValue(saved && saved.startsWith(P.prefix) && saved.endsWith(P.suffix) ? saved : full);
    function lock() {
      const total = cm.lineCount();
      if (P.prefix) cm.markText({ line: 0, ch: 0 }, { line: np, ch: 0 }, { readOnly: true, inclusiveLeft: true, inclusiveRight: false, className: 'locked' });
      if (P.suffix) {
        const ns = P.suffix.replace(/\n$/, '').split('\n').length;
        cm.markText({ line: total - ns, ch: 0 }, { line: total, ch: cm.getLine(total - 1).length }, { readOnly: true, inclusiveLeft: false, inclusiveRight: true, className: 'locked' });
      }
    }
    lock();
    let saveT;
    cm.on('change', () => {
      if (opts.exam) { opts.onChange && opts.onChange(cm.getValue()); return; }
      clearTimeout(saveT); saveT = setTimeout(() => BP.store.update(() => { BP.store.problem(P.id).draft = cm.getValue(); }), 600);
    });
    const res = main.querySelector('#res');

    function showResults(rs, tests, label) {
      const errs = rs.filter((r) => r.error);
      let out = '';
      if (errs.length === rs.length && /SyntaxError|IndentationError|TabError/.test(errs[0].error)) out += '<div class="bad"><b>Compilation error.</b> Python could not read your code.</div>' + BP.explain.errorHtml(errs[0].error);
      else out += '<div class="good"><b>Compiled successfully.</b></div>';
      let pass = 0;
      tests.forEach((t, i) => {
        const r = rs[i], ok = !r.error && norm(r.stdout) === norm(t.output);
        if (ok) pass++;
        const hidden = t.hidden;
        out += '<div class="tc ' + (ok ? 'pass' : 'fail') + '" data-i="' + i + '"><span class="dot">' + (ok ? '&#10003;' : '&#10007;') + '</span><b>' + (hidden ? 'Hidden test case ' + (i) : 'Test case ' + i) + '</b><span class="mute">' + (ok ? 'Passed' : 'Failed') + '</span></div>';
        if (!hidden) {
          out += '<div class="tcd" id="d' + i + '" style="display:' + (ok ? 'none' : 'block') + '"><div class="lbl">' + inLabel + '</div><pre>' + esc(t.input) + '</pre><div class="lbl">Your output</div><pre>' + esc(r.error ? '(no output: your code stopped with an error)' : r.stdout) + '</pre><div class="lbl">Expected output</div><pre>' + esc(t.output) + '</pre>' + (r.error ? BP.explain.errorHtml(r.error) : '') + '</div>';
        } else if (r.error) {
          out += '<div class="tcd">' + BP.explain.errorHtml(r.error) + '</div>';
        } else if (!ok) {
          out += '<div class="tcd mute">The details of hidden tests are not shown, as on HackerRank. Try your own inputs with Custom Input to find the case you missed.</div>';
        }
      });
      out = '<h3>' + label + ': ' + pass + ' of ' + tests.length + ' passed</h3>' + out;
      if (pass === tests.length) out += '<div class="good"><b>All test cases passed.</b> Nicely done.</div>' + (opts.exam ? '' : flowDone(P, 'py'));
      res.innerHTML = out;
      res.querySelectorAll('.tc').forEach((el) => (el.onclick = () => { const d = res.querySelector('#d' + el.dataset.i); if (d) d.style.display = d.style.display === 'none' ? 'block' : 'none'; }));
      return pass;
    }
    async function runTests(tests, label, record) {
      res.innerHTML = '<div class="mute">Running. The first run can take a few seconds while Python wakes up.</div>';
      const r = await BP.runner.runMany(tests.map((t) => BP.programs.forTest(P, cm.getValue(), t.input)));
      if (!r.ok) { res.innerHTML = '<div class="bad">' + (r.timeout ? '<b>Time limit exceeded.</b> Your code ran for too long. This usually means a loop that never ends. Check that the loop variable changes each round.' : esc(r.error)) + '</div>'; if (record) record(0, tests.length); return; }
      const pass = showResults(r.results, tests, label);
      if (record) record(pass, tests.length);
    }
    const samples = P.samples.map((s) => ({ input: s.input, output: s.output }));
    const everything = samples.concat(P.hidden.map((t) => ({ input: t.input, output: t.output, hidden: true })));
    main.querySelector('#run').onclick = () => runTests(samples, 'Sample test cases');
    main.querySelector('#all').onclick = () => runTests(everything, 'All test cases', (pass, total) => {
      BP.store.update(() => {
        const s = BP.store.problem(P.id);
        s.attempts++; s.best = Math.max(s.best, pass); s.last = pass; s.total = total;
        if (pass === total) s.solved = true;
        s.lesson = P.lesson; s.difficulty = P.difficulty;
      });
      if (BP.adaptive) BP.adaptive.afterProblemRun(P.id, pass === total);
    });
    main.querySelector('#cust').onclick = () => { const b = main.querySelector('#custbox'); b.style.display = b.style.display === 'none' ? 'block' : 'none'; };
    main.querySelector('#custrun').onclick = async () => {
      res.innerHTML = '<div class="mute">Running.</div>';
      const r = await BP.runner.runMany([BP.programs.forTest(P, cm.getValue(), main.querySelector('#custin').value)]);
      if (!r.ok) { res.innerHTML = '<div class="bad">' + (r.timeout ? '<b>Time limit exceeded.</b>' : esc(r.error)) + '</div>'; return; }
      const x = r.results[0];
      res.innerHTML = '<h3>Custom input result</h3><div class="lbl">Your output</div><pre>' + esc(x.stdout || '(nothing printed)') + '</pre>' + (x.error ? BP.explain.errorHtml(x.error) : '');
    };
    main.querySelector('#expl').onclick = () => {
      const line = cm.getLine(cm.getCursor().line);
      main.querySelector('#lineinfo').innerHTML = '<h3>Line ' + (cm.getCursor().line + 1) + '</h3><pre>' + esc(line) + '</pre>' + BP.explain.lineHtml(line);
    };
    main.querySelector('#reset').onclick = () => { cm.setValue(full); cm.getAllMarks().forEach((m) => m.clear()); lock(); };

    if (allowHints) {
      const hints = P.hints.concat(['Here is one full solution. Type it in yourself rather than pasting, so it sticks.\n\n' + P.solution]);
      let shown = 0;
      const hb = main.querySelector('#hintbtn'), hd = main.querySelector('#hints');
      hb.onclick = () => {
        const text = hints[shown];
        hd.insertAdjacentHTML('beforeend', '<div class="hint"><b>' + (shown + 1) + '. ' + HINT_NAMES[shown] + '</b><br>' + (shown === 4 ? '<pre>' + esc(P.prefix + P.solution + P.suffix) + '</pre>' + fmt(hints[4].split('\n\n')[0]) : fmt(text).replace(/\n/g, '<br>')) + '</div>');
        shown++;
        BP.store.update(() => { const s = BP.store.problem(P.id); s.hints = Math.max(s.hints, shown); });
        if (shown === 5 && !BP.store.problem(P.id).solved && BP.adaptive) BP.adaptive.record(P.id, false);
        if (shown >= 5) hb.style.display = 'none'; else hb.textContent = 'Show hint ' + (shown + 1) + ': ' + HINT_NAMES[shown];
      };
    }
    return { cm, getCode: () => cm.getValue() };
  }

  function list(main, lessons, problems) {
    const d = BP.store.get();
    let h = '<h1>Practice problems</h1><p class="mute">Each problem opens like a HackerRank question. Work through them in order within a topic.</p>';
    lessons.forEach((L) => {
      const ps = problems.filter((p) => p.lesson === L.id);
      if (!ps.length) return;
      const solved = ps.filter((p) => (d.problems[p.id] || {}).solved).length;
      h += '<div class="card"><h2>' + esc(L.title) + ' <span class="mute" style="font-size:14px">' + solved + ' of ' + ps.length + ' solved</span></h2><div class="grid">' +
        ps.map((p) => { const s = d.problems[p.id] || {}; return '<a class="item ' + (s.solved ? 'done' : '') + '" href="#/problem/' + p.id + '"><b>' + esc(p.title) + '</b><br><span class="pill ' + p.difficulty + '">' + p.difficulty + '</span> ' + (s.solved ? '<span class="pill done">solved</span>' : '') + '</a>'; }).join('') + '</div></div>';
    });
    main.innerHTML = h;
  }
  return { view, list, norm, flowBar, flowDone };
})();
