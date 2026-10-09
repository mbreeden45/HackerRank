window.BP = window.BP || {};
BP.diagnostic = (function () {
  const esc = (s) => BP.vis.esc(s);
  const fmt = (t) => esc(t).replace(/`([^`]+)`/g, '<code class="k">$1</code>');
  function view(main, D, lessons) {
    let i = 0; const missed = []; let score = 0;
    function ask() {
      const q = D.questions[i];
      main.innerHTML = '<div class="card"><div class="mute">Question ' + (i + 1) + ' of ' + D.questions.length + '</div><div class="bar"><i style="width:' + (i / D.questions.length * 100) + '%"></i></div><h2>' + fmt(q.prompt) + '</h2><pre>' + esc(q.code) + '</pre>' +
        q.options.map((o, k) => '<button class="opt" data-k="' + k + '">' + esc(o) + '</button>').join('') +
        '<button class="opt plain" data-k="-1" style="color:#5d6b7c">I am not sure</button><div id="fb"></div></div>';
      main.querySelectorAll('.opt').forEach((b) => (b.onclick = () => {
        const k = Number(b.dataset.k), ok = k === q.answer;
        main.querySelectorAll('.opt').forEach((x) => (x.disabled = true));
        if (k >= 0) main.querySelector('[data-k="' + k + '"]').classList.add(ok ? 'right' : 'wrong');
        main.querySelector('[data-k="' + q.answer + '"]').classList.add('right');
        if (ok) score++; else missed.push(q.lesson);
        main.querySelector('#fb').innerHTML = '<div class="' + (ok ? 'good' : 'warnbox') + '">' + (k < 0 ? 'No problem. Not sure is a useful answer. ' : ok ? 'Right. ' : 'Not quite. ') + fmt(q.why) + '</div><button class="primary" id="nx">' + (i + 1 < D.questions.length ? 'Next question' : 'See my learning path') + '</button>';
        main.querySelector('#nx').onclick = () => { i++; if (i < D.questions.length) ask(); else finish(); };
      }));
    }
    function finish() {
      const order = lessons.map((l) => l.id);
      const firstMiss = order.findIndex((id) => missed.indexOf(id) >= 0);
      const start = firstMiss < 0 ? order.length : firstMiss;
      BP.store.update((d) => {
        d.diagnostic = { done: true, score, total: D.questions.length, missed: missed.slice(), start, date: new Date().toISOString() };
        order.slice(0, start).forEach((id) => { if (!d.lessons[id]) d.lessons[id] = { done: true, auto: true }; });
      });
      main.innerHTML = '<div class="card"><h1>Your starting point</h1><p>You answered ' + score + ' of ' + D.questions.length + ' correctly. That is a starting point, not a grade.</p>' +
        (start >= order.length ? '<div class="good">You are solid on the fundamentals. Go straight to practice problems.</div>' :
          '<div class="callout">Your path begins at <b>Lesson ' + (start + 1) + ': ' + esc(lessons[start].title) + '</b>. ' + (start > 0 ? 'The ' + start + ' lesson' + (start > 1 ? 's' : '') + ' before it are marked as known, and you can still open them any time.' : 'Starting at the very first lesson is the best choice. It builds everything else.') + '</div>') +
        '<p>Topics to watch: ' + (missed.length ? [...new Set(missed)].map((id) => esc((lessons.find((l) => l.id === id) || {}).title)).join(', ') : 'none') + '.</p>' +
        '<a class="btn primary" href="#/">Go to my path</a></div>';
    }
    main.innerHTML = '<div class="card"><h1>Quick placement check</h1><p>' + D.questions.length + ' short questions. Each shows a few lines of Python and asks what it prints. There is no pass or fail. Choose "I am not sure" whenever you are unsure, since that helps the app place you well.</p><button class="primary" id="go">Start</button></div>';
    main.querySelector('#go').onclick = ask;
  }
  return { view };
})();
