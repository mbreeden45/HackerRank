window.BP = window.BP || {};
(function () {
  const PASS = 60;
  const esc = (s) => BP.vis.esc(s);
  let C = {};
  const main = document.getElementById('main');
  BP.ui = { setEngine(s) { const e = document.getElementById('engine'); e.textContent = 'Python: ' + (s === 'ready' ? 'ready (offline)' : s); e.classList.toggle('ready', s === 'ready'); } };

  async function load() {
    const get = (f) => fetch('content/' + f).then((r) => r.json());
    const opt = (f) => fetch('content/' + f).then((r) => (r.ok ? r.json() : null)).catch(() => null);
    const [lessons, problems, diag, errors, bigo, prompt, studyX, sqlP, sqlT, cards, mock] = await Promise.all([get('lessons.json'), get('problems.json'), get('diagnostic.json'), get('errors.json'),
      opt('quiz_bigo.json'), opt('quiz_prompt.json'), opt('lessons_x.json'), opt('sql_problems.json'), opt('sql_tables.json'), opt('flashcards.json'), opt('mock_exam.json')]);
    C = { lessons, problems, diag, errors, quiz: { bigo, prompt }, study: studyX || [], sql: sqlP || [], sqlTables: sqlT || {}, cards: cards || [], mock };
    BP.explain.setErrors(errors);
  }

  function home() {
    const d = BP.store.get();
    if (!d.diagnostic) {
      main.innerHTML = '<div class="card"><h1>Welcome</h1><p>This app helps you get ready for the HackerRank Builder assessment. You need ' + PASS + ' percent to pass, and you can retake it.</p><p>We start with a short placement check so we do not waste your time on things you already know.</p><a class="btn primary" href="#/diagnostic">Start the placement check</a> <a class="btn" href="#/lessons">Skip it and see all lessons</a></div>';
      return;
    }
    const doneN = C.lessons.filter((l) => d.lessons[l.id] && d.lessons[l.id].done).length;
    const next = C.lessons.find((l) => !(d.lessons[l.id] && d.lessons[l.id].done));
    const solved = C.problems.filter((p) => (d.problems[p.id] || {}).solved).length;
    let h = '<h1>Your path</h1><div class="card"><div class="row"><div><b>' + doneN + ' of ' + C.lessons.length + '</b> lessons done</div><div><b>' + solved + ' of ' + C.problems.length + '</b> problems solved</div></div><div class="bar" style="margin-top:8px"><i style="width:' + (doneN / C.lessons.length * 100) + '%"></i></div>' +
      (next ? '<p>Next up: <a class="btn primary" href="#/lesson/' + next.id + '">' + esc(next.title) + '</a></p>' : '<p>You have finished every lesson in this version. Keep practicing.</p>') + '</div>';
    const due = BP.adaptive ? BP.adaptive.dueCount() : 0;
    h += '<div class="card"><h2>Not sure what to do next</h2><p>The app picks one question for you: a missed one that is due for another look, or the weakest topic at a level just above what you have already done.</p><a class="btn primary" href="#/next">Next best question</a> ' + (due ? '<span class="pill">' + due + ' review' + (due === 1 ? '' : 's') + ' due now</span>' : '') + '</div>';
    const weak = weakTopics();
    if (weak.length) h += '<div class="card"><h2>Worth another look</h2>' + weak.map((w) => '<p><a href="#/lesson/' + w.id + '">' + esc(w.title) + '</a> <span class="mute">' + w.why + '</span></p>').join('') + '</div>';
    h += '<p class="mute"><a href="#/diagnostic">Retake the placement check</a></p>';
    main.innerHTML = h;
  }
  function weakTopics() {
    const d = BP.store.get(), out = [];
    C.lessons.forEach((l) => {
      const ps = C.problems.filter((p) => p.lesson === l.id).map((p) => d.problems[p.id]).filter(Boolean);
      const attempts = ps.reduce((a, p) => a + p.attempts, 0), hints = ps.reduce((a, p) => a + (p.hints || 0), 0);
      const unsolved = ps.filter((p) => p.attempts > 0 && !p.solved).length;
      if (unsolved > 0) out.push({ id: l.id, title: l.title, score: unsolved * 3, why: unsolved + ' problem(s) not solved yet' });
      else if (attempts && hints / Math.max(1, ps.length) > 2.5) out.push({ id: l.id, title: l.title, score: 1, why: 'you used a lot of hints here' });
      if (d.diagnostic && d.diagnostic.missed.indexOf(l.id) >= 0 && !(d.lessons[l.id] || {}).done) out.push({ id: l.id, title: l.title, score: 2, why: 'missed in the placement check' });
    });
    return out.sort((a, b) => b.score - a.score).slice(0, 4);
  }
  function lessonsList() {
    const d = BP.store.get();
    const order = ['Basics', 'Patterns', 'Strings and parsing', 'Big O', 'Prompt Engineering', 'SQL Foundations'];
    const all = C.lessons.map((l, i) => ({ l, n: i + 1, href: '#/lesson/' + l.id, track: l.track || 'Basics' }))
      .concat(C.study.map((l) => ({ l, n: 0, href: '#/study/' + l.id, track: l.track })));
    let h = '<h1>Lessons</h1><p class="mute">Follow each group in order. Each lesson has an idea, a worked example and practice.</p>';
    order.forEach((t) => {
      const group = all.filter((x) => x.track === t);
      if (!group.length) return;
      h += '<h2 style="margin-top:18px">' + esc(t) + '</h2><div class="grid">' + group.map((x, k) => {
        const dn = d.lessons[x.l.id];
        return '<a class="item ' + (dn && dn.done ? 'done' : '') + '" href="' + x.href + '"><span class="mute">' + (x.n ? 'Lesson ' + x.n : 'Lesson ' + (k + 1) + ' of ' + group.length) + '</span><br><b>' + esc(x.l.title) + '</b>' + (dn && dn.done ? '<br><span class="pill done">' + (dn.auto ? 'known from placement' : 'done') + '</span>' : '') + '</a>';
      }).join('') + '</div>';
    });
    main.innerHTML = h;
  }
  function explainPage() {
    main.innerHTML = '<h1>Explain a line</h1><p>Paste one line of Python to see it in plain English, or paste an error message to see what it means.</p><div class="card"><div class="lbl">A line of code</div><textarea class="custom" id="ln" placeholder="for i in range(len(nums)):"></textarea><button class="primary" id="b1" style="margin:6px 0">What does this line mean</button><div id="o1"></div></div>' +
      '<div class="card"><div class="lbl">An error message</div><textarea class="custom" id="er" placeholder="IndexError: list index out of range"></textarea><button class="primary" id="b2" style="margin:6px 0">Explain this error</button><div id="o2"></div></div>';
    main.querySelector('#b1').onclick = () => (main.querySelector('#o1').innerHTML = BP.explain.lineHtml(main.querySelector('#ln').value));
    main.querySelector('#b2').onclick = () => (main.querySelector('#o2').innerHTML = BP.explain.errorHtml(main.querySelector('#er').value));
  }
  function progress() {
    const d = BP.store.get();
    let h = '<h1>My progress</h1>';
    if (d.diagnostic) h += '<div class="card"><h2>Placement check</h2><p>' + d.diagnostic.score + ' of ' + d.diagnostic.total + ' correct.</p></div>';
    h += '<div class="card"><h2>By topic</h2><table><tr><th>Topic</th><th>Solved</th><th>Attempts</th><th>Hints used</th></tr>' + C.lessons.map((l) => {
      const ps = C.problems.filter((p) => p.lesson === l.id); if (!ps.length) return '';
      const st = ps.map((p) => d.problems[p.id] || {});
      return '<tr><td>' + esc(l.title) + '</td><td>' + st.filter((s) => s.solved).length + ' of ' + ps.length + '</td><td>' + st.reduce((a, s) => a + (s.attempts || 0), 0) + '</td><td>' + st.reduce((a, s) => a + (s.hints || 0), 0) + '</td></tr>';
    }).join('') + '</table></div><button id="rst">Erase all my progress</button>';
    main.innerHTML = h;
    main.querySelector('#rst').onclick = () => { if (confirm('Erase all progress on this computer?')) { BP.store.reset(); progress(); } };
  }

  // Other modules add handlers to BP.routeHandlers: fn(r, main, C) returns true when it drew the page.
  BP.extraRoute = (r, main, C) => (BP.routeHandlers || []).some((f) => f(r, main, C));

  function route() {
    const r = location.hash.replace(/^#\/?/, '').split('/');
    document.querySelectorAll('#nav a').forEach((a) => a.classList.toggle('on', a.dataset.r === (r[0] || 'home') || (a.dataset.r === 'practice' && r[0] === 'problem') || (a.dataset.r === 'lessons' && (r[0] === 'lesson' || r[0] === 'study')) || (a.dataset.r === 'sql' && r[0] === 'sqlproblem') || (a.dataset.r === 'quizzes' && r[0] === 'quiz')));
    window.scrollTo(0, 0);
    if (!r[0]) home();
    else if (r[0] === 'diagnostic') BP.diagnostic.view(main, C.diag, C.lessons);
    else if (r[0] === 'lessons') lessonsList();
    else if (r[0] === 'lesson') BP.lesson.view(main, C.lessons, C.problems, r[1]);
    else if (r[0] === 'practice') BP.practice.list(main, C.lessons, C.problems);
    else if (r[0] === 'problem') { const p = C.problems.find((x) => x.id === r[1]); p ? BP.practice.view(main, p, C.lessons) : (main.innerHTML = 'Problem not found.'); }
    else if (r[0] === 'explain') explainPage();
    else if (r[0] === 'progress') progress();
    else if (BP.extraRoute(r, main, C)) { /* handled */ }
    else home();
  }
  BP.app = { PASS, get C() { return C; }, route, weakTopics };
  BP.store.get();
  load().then(() => { window.addEventListener('hashchange', route); route(); }).catch((e) => { main.innerHTML = '<div class="bad">Could not load the lesson files. Make sure you started the app with start.command, not by opening index.html directly. (' + esc(e.message) + ')</div>'; });
})();
