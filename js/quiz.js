// Multiple-choice and written-answer quiz screens (Big O, Prompt Engineering). Also exports renderItem for the mock exam.
window.BP = window.BP || {};
BP.quiz = (function () {
  const esc = (s) => BP.vis.esc(s);
  const fmt = (t) => esc(t).replace(/`([^`]+)`/g, '<code class="k">$1</code>');
  const TITLES = { bigo: 'Big O questions', prompt: 'Prompt Engineering questions' };

  function shuffled(n) {
    const a = []; for (let i = 0; i < n; i++) a.push(i);
    for (let i = n - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); const t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  // which rubric points have a keyword in the learner's text (a hint only, never the grade)
  function keywordHits(item, text) {
    const low = String(text || '').toLowerCase();
    return item.rubric.map((r) => (r.keywords || []).some((k) => low.indexOf(String(k).toLowerCase()) >= 0));
  }
  function record(id, correct, score) {
    BP.store.update((d) => {
      const s = d.quiz[id] && typeof d.quiz[id] === 'object' ? d.quiz[id] : (d.quiz[id] = { n: 0, right: 0 });
      s.n++; if (correct) s.right++; s.last = correct; s.score = score; s.ts = Date.now();
    });
    if (BP.adaptive && BP.adaptive.record) BP.adaptive.record(id, correct);
  }

  // Draws one item into host. opts: exam (no feedback), onAnswer(info), onRecord(correct, score)
  function renderItem(host, q, opts) {
    opts = opts || {};
    let h = '<div class="qprompt"><p>' + fmt(q.prompt).replace(/\n/g, '<br>') + '</p>' + (q.snippet ? '<pre>' + esc(q.snippet) + '</pre>' : '') + '</div>';
    if (q.type === 'written') {
      h += '<textarea class="custom wtext" id="wt" placeholder="Write your answer here in your own words."></textarea><div id="wfb"></div>' +
        (opts.exam ? '' : '<button class="primary" id="wcheck" style="margin-top:6px">Show the model answer and checklist</button>');
      host.innerHTML = h;
      const ta = host.querySelector('#wt');
      if (opts.prefill) ta.value = opts.prefill;
      ta.oninput = () => opts.onAnswer && opts.onAnswer({ text: ta.value });
      if (!opts.exam) host.querySelector('#wcheck').onclick = () => {
        host.querySelector('#wcheck').style.display = 'none'; ta.readOnly = true;
        showRubric(host.querySelector('#wfb'), q, ta.value, (score) => { record(q.id, score >= 0.6, score); opts.onRecord && opts.onRecord(score >= 0.6, score); });
      };
      return;
    }
    const order = shuffled(q.options.length);
    const plain = q.display === 'prose' ? ' plain' : '';
    h += '<div class="opts">' + order.map((oi, k) => '<button class="opt' + plain + '" data-o="' + oi + '">' + esc(q.options[oi]) + '</button>').join('') + '</div><div id="fb"></div>';
    host.innerHTML = h;
    const btns = host.querySelectorAll('.opt');
    btns.forEach((b) => (b.onclick = () => {
      const o = Number(b.dataset.o);
      if (opts.exam) {
        btns.forEach((x) => x.classList.toggle('sel', x === b));
        opts.onAnswer && opts.onAnswer({ choice: o });
        return;
      }
      const ok = o === q.answer;
      btns.forEach((x) => { x.disabled = true; const xo = Number(x.dataset.o); if (xo === q.answer) x.classList.add('right'); else if (xo === o) x.classList.add('wrong'); });
      host.querySelector('#fb').innerHTML = '<div class="' + (ok ? 'good' : 'bad') + '">' + (ok ? 'That is right. ' : 'Not quite. ') + fmt(q.why) + '</div>';
      record(q.id, ok, ok ? 1 : 0);
      opts.onRecord && opts.onRecord(ok, ok ? 1 : 0);
    }));
  }

  // The model answer plus the tick list. onScore(fraction) fires when the learner presses Save.
  function showRubric(box, q, text, onScore) {
    const hits = keywordHits(q, text);
    box.innerHTML = '<div class="card inner"><h3>Model answer</h3><div class="model">' + fmt(q.model).replace(/\n/g, '<br>') + '</div>' +
      '<h3>Checklist</h3><p class="mute">Tick each point that your answer covers, even if you worded it differently. The marker next to a point only means one of its usual words appears in your text. It is a hint, not a grade.</p>' +
      q.rubric.map((r, i) => '<label class="rub"><input type="checkbox" data-i="' + i + '"> ' + fmt(r.point) + (hits[i] ? ' <span class="pill done">words found</span>' : '') + '</label>').join('') +
      '<div class="row" style="margin-top:8px"><button class="primary" id="rsave">Save my result</button><span id="rscore" class="mute">0 of ' + q.rubric.length + ' ticked</span></div><div id="rdone"></div></div>';
    const boxes = box.querySelectorAll('input[type=checkbox]');
    const count = () => Array.prototype.filter.call(boxes, (b) => b.checked).length;
    boxes.forEach((b) => (b.onchange = () => (box.querySelector('#rscore').textContent = count() + ' of ' + q.rubric.length + ' ticked')));
    box.querySelector('#rsave').onclick = () => {
      const score = count() / q.rubric.length;
      box.querySelector('#rsave').disabled = true; boxes.forEach((b) => (b.disabled = true));
      box.querySelector('#rdone').innerHTML = '<div class="' + (score >= 0.6 ? 'good' : 'warnbox') + '">You covered ' + count() + ' of ' + q.rubric.length + ' points. ' + (score >= 0.6 ? 'That would earn good credit.' : 'Read the model answer again and note the points you missed.') + '</div>';
      onScore(score);
    };
  }

  function start(main, name, items, mode) {
    let list = items.slice();
    const d = BP.store.get();
    if (mode === 'missed') list = list.filter((q) => { const s = d.quiz[q.id]; return s && typeof s === 'object' && !s.last; });
    if (mode === 'new') list = list.filter((q) => !(d.quiz[q.id] && typeof d.quiz[q.id] === 'object'));
    if (!list.length) { main.innerHTML = '<div class="card"><p>No questions match that choice yet.</p><a class="btn" href="#/quiz/' + name + '">Back</a></div>'; return; }
    let i = 0, right = 0;
    function show() {
      const q = list[i];
      main.innerHTML = '<div class="card"><div class="row"><span class="mute">' + esc(TITLES[name]) + ': question ' + (i + 1) + ' of ' + list.length + '</span><span class="pill ' + q.difficulty + '">' + q.difficulty + '</span>' + (q.type === 'written' ? '<span class="pill">written</span>' : '') + '</div><div class="bar" style="margin:8px 0"><i style="width:' + (i / list.length * 100) + '%"></i></div><div id="qhost"></div><div id="nxbox" style="margin-top:10px"></div></div>';
      let answered = false;
      renderItem(main.querySelector('#qhost'), q, { onRecord: (ok) => {
        if (answered) return; answered = true; if (ok) right++;
        main.querySelector('#nxbox').innerHTML = '<button class="primary" id="nx">' + (i + 1 < list.length ? 'Next question' : 'See my result') + '</button>';
        main.querySelector('#nx').onclick = () => { i++; if (i < list.length) show(); else finish(); };
      } });
    }
    function finish() {
      const pct = Math.round(right / list.length * 100);
      main.innerHTML = '<div class="card"><h1>Done</h1><p>You got ' + right + ' of ' + list.length + ' right (' + pct + ' percent). The pass line for the real assessment is ' + BP.app.PASS + ' percent.</p>' +
        '<div class="row"><a class="btn primary" href="#/quiz/' + name + '/missed">Retry the ones I missed</a><a class="btn" href="#/quiz/' + name + '">Back to the list</a></div></div>';
    }
    show();
  }

  function view(main, name, C, mode) {
    const items = C.quiz[name];
    if (!items) { main.innerHTML = '<div class="card">That quiz is not part of this version.</div>'; return; }
    if (mode === 'all' || mode === 'missed' || mode === 'new') return start(main, name, items, mode);
    const d = BP.store.get();
    const stat = (q) => (d.quiz[q.id] && typeof d.quiz[q.id] === 'object' ? d.quiz[q.id] : null);
    const answered = items.filter(stat).length, good = items.filter((q) => stat(q) && stat(q).last).length;
    main.innerHTML = '<h1>' + esc(TITLES[name]) + '</h1><div class="card"><p>' + items.length + ' questions. You have tried ' + answered + ' and your latest answer was right on ' + good + '.</p>' +
      '<div class="row"><a class="btn primary" href="#/quiz/' + name + '/all">Start from the beginning</a><a class="btn" href="#/quiz/' + name + '/new">Only questions I have not tried</a><a class="btn" href="#/quiz/' + name + '/missed">Only ones I missed</a></div></div>' +
      '<div class="card"><h2>All questions</h2><div class="grid">' + items.map((q, i) => { const s = stat(q); return '<div class="item ' + (s && s.last ? 'done' : '') + '"><b>' + (i + 1) + '.</b> ' + esc(q.prompt.length > 70 ? q.prompt.slice(0, 67) + '...' : q.prompt) + '<br><span class="pill ' + q.difficulty + '">' + q.difficulty + '</span> ' + (q.type === 'written' ? '<span class="pill">written</span> ' : '') + (s ? (s.last ? '<span class="pill done">right</span>' : '<span class="pill">missed</span>') : '') + '</div>'; }).join('') + '</div></div>';
  }

  function index(main, C) {
    const d = BP.store.get();
    const tile = (name, text) => {
      const items = C.quiz[name]; if (!items) return '';
      const good = items.filter((q) => d.quiz[q.id] && typeof d.quiz[q.id] === 'object' && d.quiz[q.id].last).length;
      return '<a class="item" href="#/quiz/' + name + '"><b>' + esc(TITLES[name]) + '</b><br><span class="mute">' + text + '</span><br><span class="pill">' + good + ' of ' + items.length + ' right</span></a>';
    };
    main.innerHTML = '<h1>Quizzes</h1><div class="grid">' + tile('prompt', 'Choose the better prompt, and write short answers that you check against a model answer.') + tile('bigo', 'Spot how fast code grows as the input grows.') + '</div>';
  }

  BP.routeHandlers = BP.routeHandlers || [];
  BP.routeHandlers.push((r, main, C) => {
    if (r[0] === 'quizzes') { index(main, C); return true; }
    if (r[0] === 'quiz') { view(main, r[1], C, r[2]); return true; }
    return false;
  });
  return { renderItem, view, index, showRubric, keywordHits, record };
})();
