// Adaptive practice. The picking logic (core) has no browser dependencies, so tools/test_adaptive.js can test it in Node.
// Rules:
//  1. A missed item comes back after 1, 3 and 7 days (reviews). A due review always comes first.
//  2. Otherwise pick the weakest topic (low success, heavy hint use), weighted by how much that topic counts in the exam.
//  3. Inside that topic pick an unmastered item one level above the hardest level the learner has already mastered.
(function (root, factory) {
  const core = factory();
  if (typeof module === 'object' && module.exports) module.exports = core;
  else { root.BP = root.BP || {}; root.BP.adaptiveCore = core; if (typeof root.document !== 'undefined') core.attach(root.BP); }
})(typeof window !== 'undefined' ? window : this, function () {
  const DAY = 86400000, STEPS = [1, 3, 7], LEVEL = { Easy: 0, Medium: 1, Hard: 2 }, NAMES = ['Easy', 'Medium', 'Hard'];

  // Score for one item the learner has tried: 1 mastered cleanly, 0.6 mastered with some hints, 0.35 with many hints, 0 not mastered.
  function itemScore(s) {
    if (!s || !s.tried) return null;
    if (!s.mastered) return 0;
    if (s.hints >= 3) return 0.35;
    if (s.hints >= 1) return 0.6;
    return 1;
  }
  function topicScore(items, stats) {
    const sc = items.map((i) => itemScore(stats[i.id])).filter((x) => x !== null);
    return sc.length ? sc.reduce((a, b) => a + b, 0) / sc.length : null;
  }

  // Updates one review entry after an answer. entry is {stage, due} or undefined. Returns the new entry, or null when finished.
  function applyResult(entry, correct, now) {
    if (!correct) return { stage: 0, due: now + STEPS[0] * DAY };
    if (!entry) return null;
    if (entry.due > now) return entry;
    const stage = entry.stage + 1;
    if (stage >= STEPS.length) return null;
    return { stage, due: now + STEPS[stage] * DAY };
  }

  // model: {items:[{id, topic, difficulty}], stats:{id:{tried, mastered, hints}}, review:{id:{stage,due}}, now, weights:{topic:w}, topicOrder:[topic]}
  function pick(model) {
    const { items, stats, review, now } = model;
    const weights = model.weights || {}, order = model.topicOrder || [];
    const byId = {}; items.forEach((i) => (byId[i.id] = i));
    const due = Object.keys(review || {}).filter((id) => byId[id] && review[id].due <= now).sort((a, b) => review[a].due - review[b].due);
    if (due.length) {
      const id = due[0], r = review[id], days = Math.max(1, Math.round((now - (r.due - STEPS[r.stage] * DAY)) / DAY));
      return { item: byId[id], kind: 'review', topic: byId[id].topic, reason: 'Review ' + (r.stage + 1) + ' of ' + STEPS.length + ': you missed this ' + days + ' day' + (days === 1 ? '' : 's') + ' ago.', dueCount: due.length };
    }
    const topics = {};
    items.forEach((i) => (topics[i.topic] = topics[i.topic] || []).push(i));
    let best = null;
    Object.keys(topics).forEach((t) => {
      const list = topics[t], remaining = list.filter((i) => !(stats[i.id] && stats[i.id].mastered));
      if (!remaining.length) return;
      const score = topicScore(list, stats);
      const idx = order.indexOf(t) < 0 ? 999 : order.indexOf(t);
      const urgency = (1 - (score === null ? 0.5 : score)) * (weights[t] || 1) - idx * 1e-4;
      if (!best || urgency > best.urgency) best = { topic: t, urgency, score, list, remaining };
    });
    if (!best) return null;
    let level = -1;
    best.list.forEach((i) => { if (stats[i.id] && stats[i.id].mastered) level = Math.max(level, LEVEL[i.difficulty]); });
    const target = level < 0 ? 0 : Math.min(2, level + 1);
    const ranked = best.remaining.map((i, k) => ({ i, k, gap: Math.abs(LEVEL[i.difficulty] - target), tried: stats[i.id] && stats[i.id].tried ? 1 : 0 }))
      .sort((a, b) => a.gap - b.gap || a.tried - b.tried || a.k - b.k);
    const chosen = ranked[0].i;
    const why = best.score === null ? 'You have not started this topic yet.' : best.score < 0.5 ? 'This is your weakest topic so far.' : 'This topic still has room to grow.';
    return { item: chosen, kind: best.score === null ? 'new' : 'weak', topic: best.topic, target: NAMES[target], reason: why + ' Next level to aim for: ' + NAMES[target] + '.' };
  }

  function attach(BP) {
    const store = () => BP.store;
    // Build the model from the loaded content and saved progress.
    function build() {
      const C = BP.app.C, d = store().get();
      const trackOf = {}; C.lessons.forEach((l) => (trackOf[l.id] = l.track || 'Basics')); C.study.forEach((l) => (trackOf[l.id] = l.track));
      const TW = { 'Basics': 1.5, 'Patterns': 2, 'Strings and parsing': 1.5, 'Big O': 1, 'Prompt Engineering': 3, 'SQL Foundations': 2 };
      const items = [], stats = {}, weights = {}, topicOrder = [];
      const addTopic = (t, w) => { if (topicOrder.indexOf(t) < 0) { topicOrder.push(t); weights[t] = w; } };
      C.problems.forEach((p) => { addTopic(p.lesson, TW[trackOf[p.lesson]] || 1); items.push({ id: p.id, topic: p.lesson, difficulty: p.difficulty, href: '#/problem/' + p.id, title: p.title, label: 'Python problem' }); const s = d.problems[p.id]; if (s) stats[p.id] = { tried: s.attempts > 0 || s.hints > 0, mastered: !!s.solved, hints: s.hints || 0 }; });
      C.sql.forEach((p) => { addTopic(p.lesson, TW['SQL Foundations']); items.push({ id: p.id, topic: p.lesson, difficulty: p.difficulty, href: '#/sqlproblem/' + p.id, title: p.title, label: 'SQL problem' }); const s = d.problems[p.id]; if (s) stats[p.id] = { tried: s.attempts > 0 || s.hints > 0, mastered: !!s.solved, hints: s.hints || 0 }; });
      ['prompt', 'bigo'].forEach((name) => (C.quiz[name] || []).forEach((q) => {
        addTopic(name, name === 'prompt' ? TW['Prompt Engineering'] : TW['Big O']);
        items.push({ id: q.id, topic: name, difficulty: q.difficulty, href: '#/quizitem/' + q.id, title: q.prompt.length > 70 ? q.prompt.slice(0, 67) + '...' : q.prompt, label: q.type === 'written' ? 'Written answer' : 'Question' });
        const s = d.quiz[q.id]; if (s && typeof s === 'object') stats[q.id] = { tried: true, mastered: !!s.last, hints: 0 };
      }));
      return { items, stats, review: d.review || {}, now: Date.now(), weights, topicOrder };
    }
    BP.adaptive = {
      build, pick: () => pick(build()),
      // correct: true/false. Updates the review schedule only.
      record(id, correct) { store().update((d) => { d.review = d.review || {}; const next = applyResult(d.review[id], correct, Date.now()); if (next) d.review[id] = next; else delete d.review[id]; }); },
      // Call after "Run all test cases" or "Check my answer". A problem counts as a miss after 3 failed tries, or when solved with 3 or more hints.
      afterProblemRun(id, solvedNow) {
        const s = store().problem(id);
        if (solvedNow) { if (!s.credited) { store().update(() => { s.credited = true; }); BP.adaptive.record(id, (s.hints || 0) < 3); } else BP.adaptive.record(id, true); }
        else if (!s.solved && s.attempts - (s.missMark || 0) >= 3) { store().update(() => { s.missMark = s.attempts; }); BP.adaptive.record(id, false); }
      },
      dueCount() { const d = store().get(), now = Date.now(); return Object.keys(d.review || {}).filter((id) => d.review[id].due <= now).length; },
    };
    BP.routeHandlers = BP.routeHandlers || [];
    BP.routeHandlers.push((r, main, C) => {
      if (r[0] === 'next') { nextPage(main, C); return true; }
      if (r[0] === 'quizitem') { quizItem(main, C, r[1]); return true; }
      return false;
    });
    function nextPage(main, C) {
      const res = BP.adaptive.pick();
      if (!res) { main.innerHTML = '<div class="card"><h1>Nothing left to pick</h1><p>You have mastered every question in this version. Try a mock exam.</p><a class="btn primary" href="#/mock">Mock exam</a></div>'; return; }
      main.innerHTML = '<div class="card"><h1>Next best question</h1><p>' + BP.vis.esc(res.reason) + '</p><div class="item"><span class="mute">' + res.item.label + '</span><br><b>' + BP.vis.esc(res.item.title) + '</b><br><span class="pill ' + res.item.difficulty + '">' + res.item.difficulty + '</span></div><p style="margin-top:12px"><a class="btn primary" href="' + res.item.href + '">Start it</a> <a class="btn" href="#/">Back home</a></p></div>';
    }
    function quizItem(main, C, id) {
      const all = [].concat(C.quiz.prompt || [], C.quiz.bigo || []);
      const q = all.find((x) => x.id === id);
      if (!q) { main.innerHTML = '<div class="card">Question not found.</div>'; return; }
      main.innerHTML = '<div class="card"><div class="mute"><a href="#/quiz/' + q.topic + '">Back to the list</a></div><span class="pill ' + q.difficulty + '">' + q.difficulty + '</span><div id="qh"></div><div id="nb" style="margin-top:10px"></div></div>';
      BP.quiz.renderItem(main.querySelector('#qh'), q, { onRecord: () => { main.querySelector('#nb').innerHTML = '<a class="btn primary" href="#/next">Next best question</a>'; } });
    }
  }
  return { pick, applyResult, itemScore, topicScore, attach, STEPS, DAY };
});
