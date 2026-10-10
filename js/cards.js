// Flashcards with spaced repetition. The scheduling (core) is pure so tools/test_cards.js can test it in Node.
// Each card stores {reps, interval (days), ease, due (ms), lapses} under builderPrep.v1 -> cards.
(function (root, factory) {
  const core = factory();
  if (typeof module === 'object' && module.exports) module.exports = core;
  else { root.BP = root.BP || {}; root.BP.cardsCore = core; if (typeof root.document !== 'undefined') core.attach(root.BP); }
})(typeof window !== 'undefined' ? window : this, function () {
  const MIN = 60000, DAY = 86400000, NEW_PER_SESSION = 10;
  const fresh = () => ({ reps: 0, interval: 0, ease: 2.5, due: 0, lapses: 0 });

  // grade: 'again' | 'hard' | 'good' | 'easy'. Returns the new state.
  function schedule(state, grade, now) {
    const s = Object.assign(fresh(), state || {});
    const out = { reps: s.reps, interval: s.interval, ease: s.ease, lapses: s.lapses, due: 0 };
    if (grade === 'again') {
      out.reps = 0; out.interval = 0; out.lapses = s.lapses + 1; out.ease = Math.max(1.3, s.ease - 0.2); out.due = now + 10 * MIN;
      return out;
    }
    if (grade === 'hard') { out.ease = Math.max(1.3, s.ease - 0.15); out.interval = s.reps === 0 ? 1 : Math.max(1, Math.round(s.interval * 1.2)); }
    else if (grade === 'good') { out.interval = s.reps === 0 ? 1 : s.reps === 1 ? 3 : Math.round(s.interval * s.ease); }
    else { out.ease = Math.min(3, s.ease + 0.15); out.interval = s.reps === 0 ? 4 : Math.round(s.interval * s.ease * 1.3); }
    out.reps = s.reps + 1;
    out.due = now + out.interval * DAY;
    return out;
  }
  function label(ms) {
    if (ms < 60 * MIN) return Math.round(ms / MIN) + ' min';
    const d = Math.round(ms / DAY);
    return d < 30 ? d + (d === 1 ? ' day' : ' days') : Math.round(d / 30) + (Math.round(d / 30) === 1 ? ' month' : ' months');
  }
  function previews(state, now) {
    const o = {}; ['again', 'hard', 'good', 'easy'].forEach((g) => (o[g] = label(schedule(state, g, now).due - now))); return o;
  }
  // Which cards to study: due ones first (oldest due first), then up to `limit` new ones.
  function queue(cards, states, now, topic, limit) {
    const list = topic ? cards.filter((c) => c.topic === topic) : cards;
    const due = list.filter((c) => states[c.id] && states[c.id].due <= now).sort((a, b) => states[a.id].due - states[b.id].due);
    const fresh = list.filter((c) => !states[c.id]).slice(0, limit === undefined ? NEW_PER_SESSION : limit);
    return due.concat(fresh);
  }

  function attach(BP) {
    const esc = (s) => BP.vis.esc(s);
    const fmt = (t) => esc(t).replace(/`([^`]+)`/g, '<code class="k">$1</code>');
    const states = () => { const d = BP.store.get(); return d.cards || (d.cards = {}); };

    function overview(main, C) {
      const st = states(), now = Date.now();
      const topics = []; C.cards.forEach((c) => { if (topics.indexOf(c.topic) < 0) topics.push(c.topic); });
      const dueN = C.cards.filter((c) => st[c.id] && st[c.id].due <= now).length, newN = C.cards.filter((c) => !st[c.id]).length, learned = C.cards.length - newN;
      let h = '<h1>Flashcards</h1><div class="card"><p>Each card starts with <i>I want to...</i> and the back says <i>so I write...</i>. Try to say the answer before you flip the card, then tell the app how it went. Cards you find hard come back sooner.</p>' +
        '<div class="row"><div><b>' + dueN + '</b> due now</div><div><b>' + newN + '</b> new</div><div><b>' + learned + '</b> started</div></div><p style="margin-top:10px"><a class="btn primary" href="#/cards/study">Start a session</a> <span class="mute">due cards first, then up to ' + NEW_PER_SESSION + ' new ones</span></p></div>' +
        '<div class="card"><h2>By topic</h2><div class="grid">' + topics.map((t) => {
          const list = C.cards.filter((c) => c.topic === t), dn = list.filter((c) => st[c.id] && st[c.id].due <= now).length, nn = list.filter((c) => !st[c.id]).length;
          return '<a class="item" href="#/cards/study/' + encodeURIComponent(t) + '"><b>' + esc(t) + '</b><br><span class="mute">' + list.length + ' cards, ' + dn + ' due, ' + nn + ' new</span></a>';
        }).join('') + '</div></div>';
      main.innerHTML = h;
    }

    function study(main, C, topic) {
      const st = states();
      let q = queue(C.cards, st, Date.now(), topic, NEW_PER_SESSION), total = q.length, done = 0, shown = false;
      if (!q.length) { main.innerHTML = '<div class="card"><h1>All caught up</h1><p>No cards are due right now' + (topic ? ' in ' + esc(topic) : '') + '. Come back later, or pick another topic.</p><a class="btn" href="#/cards">Back to flashcards</a></div>'; return; }
      function exampleHtml(c) {
        if (!c.check) return '';
        if (c.check.lang === 'python') return '<div class="lbl">Example</div><pre>' + esc(c.check.code) + '</pre>' + (c.check.stdin ? '<div class="lbl">Typed in</div><pre>' + esc(c.check.stdin) + '</pre>' : '') + '<div class="lbl">Prints</div><pre class="out">' + esc(c.check.output) + '</pre><button id="runex">Run it again here</button><div id="exout"></div>';
        return '<div class="lbl">Example query</div><pre>' + esc(c.check.sql) + '</pre><div id="exout">' + BP.sql.gridHtml(c.check.columns, c.check.rows) + '</div><button id="runex">Run it again here</button>';
      }
      function show() {
        if (!q.length) { return finish(); }
        const c = q[0]; shown = false;
        main.innerHTML = '<div class="card fc"><div class="row"><span class="mute">' + esc(c.topic) + '</span><span class="mute" style="margin-left:auto">' + done + ' done, ' + q.length + ' to go</span></div><div class="bar" style="margin:8px 0"><i style="width:' + (done / (done + q.length) * 100) + '%"></i></div>' +
          '<div class="fcfront">' + fmt(c.front) + '</div><div id="back"></div><div id="act" style="margin-top:14px"><button class="primary" id="flip">Show the answer</button> <span class="mute">or press space</span></div></div>';
        main.querySelector('#flip').onclick = reveal;
      }
      function reveal() {
        if (shown || !q.length) return; shown = true;
        const c = q[0], p = previews(st[c.id], Date.now());
        main.querySelector('#back').innerHTML = '<div class="fcback">' + fmt(c.back) + '</div>' + exampleHtml(c);
        main.querySelector('#act').innerHTML = '<div class="row grades">' + [['again', 'Again', '1'], ['hard', 'Hard', '2'], ['good', 'Good', '3'], ['easy', 'Easy', '4']].map((g) => '<button class="grade ' + g[0] + '" data-g="' + g[0] + '"><b>' + g[1] + '</b><br><span class="mute">' + p[g[0]] + '</span></button>').join('') + '</div><div class="mute" style="margin-top:6px">Keys 1 to 4 also work.</div>';
        main.querySelectorAll('.grade').forEach((b) => (b.onclick = () => grade(b.dataset.g)));
        const rb = main.querySelector('#runex');
        if (rb) rb.onclick = async () => {
          const out = main.querySelector('#exout'); out.innerHTML = '<div class="mute">Running.</div>';
          if (c.check.lang === 'python') { const r = await BP.runner.run(c.check.code, [c.check.stdin || '']); const x = r.ok ? r.results[0] : null; out.innerHTML = x ? '<div class="lbl">Result</div><pre class="out">' + esc(x.error ? x.error : x.stdout) + '</pre>' : '<div class="bad">Could not run.</div>'; }
          else out.innerHTML = await BP.sql.runToHtml(c.check.sql, C.sqlTables);
        };
      }
      function grade(g) {
        if (!shown) return;
        const c = q.shift(), now = Date.now();
        BP.store.update((d) => { d.cards = d.cards || {}; d.cards[c.id] = schedule(d.cards[c.id], g, now); });
        if (g === 'again') q.push(c); else done++;
        show();
      }
      function finish() {
        main.innerHTML = '<div class="card"><h1>Session finished</h1><p>You went through ' + total + ' card' + (total === 1 ? '' : 's') + '. The app has scheduled when each one comes back.</p><a class="btn primary" href="#/cards">Back to flashcards</a> <a class="btn" href="#/">Home</a></div>';
      }
      BP.cards.onKey = (e) => {
        if (!/^#\/cards\/study/.test(location.hash) || /TEXTAREA|INPUT/.test((e.target || {}).tagName || '')) return;
        if (e.key === ' ') { e.preventDefault(); reveal(); }
        else if (shown && '1234'.indexOf(e.key) >= 0 && e.key) grade(['again', 'hard', 'good', 'easy'][Number(e.key) - 1]);
      };
      show();
    }
    BP.cards = { schedule, previews, queue, onKey: null };
    document.addEventListener('keydown', (e) => BP.cards.onKey && BP.cards.onKey(e));
    BP.routeHandlers = BP.routeHandlers || [];
    BP.routeHandlers.push((r, main, C) => {
      if (r[0] !== 'cards') return false;
      if (!C.cards.length) { main.innerHTML = '<div class="card">Flashcards are not part of this version.</div>'; return true; }
      if (r[1] === 'study') study(main, C, r[2] ? decodeURIComponent(r[2]) : null); else overview(main, C);
      return true;
    });
  }
  return { schedule, previews, queue, label, attach, NEW_PER_SESSION, MIN, DAY };
});
