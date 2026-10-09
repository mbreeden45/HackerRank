// Simulates answer histories and checks what the adaptive picker chooses. Usage: node tools/test_adaptive.js
const assert = require('assert');
const A = require('../js/adaptive.js');
const DAY = A.DAY;
let passed = 0;
const t = (name, fn) => { fn(); passed++; console.log('  PASS  ' + name); };

const items = [];
const add = (topic, n) => ['Easy', 'Easy', 'Medium', 'Medium', 'Hard'].slice(0, n).forEach((d, i) => items.push({ id: topic + (i + 1), topic, difficulty: d }));
add('lists', 5); add('dicts', 5); add('prompt', 5);
const base = (extra) => Object.assign({ items, stats: {}, review: {}, now: 1000 * DAY, weights: { lists: 1, dicts: 1, prompt: 3 }, topicOrder: ['lists', 'dicts', 'prompt'] }, extra);
const mastered = (...ids) => { const s = {}; ids.forEach((id) => (s[id] = { tried: true, mastered: true, hints: 0 })); return s; };

t('fresh learner: highest weighted untouched topic, starting at Easy', () => {
  const r = A.pick(base());
  assert.strictEqual(r.topic, 'prompt'); assert.strictEqual(r.item.difficulty, 'Easy'); assert.strictEqual(r.kind, 'new');
});
t('weak topic beats strong topic: failed items in dicts, clean wins in lists', () => {
  const stats = Object.assign(mastered('lists1', 'lists2', 'prompt1', 'prompt2'), { dicts1: { tried: true, mastered: false, hints: 4 }, dicts2: { tried: true, mastered: false, hints: 0 } });
  const r = A.pick(base({ stats }));
  assert.strictEqual(r.topic, 'dicts'); assert.strictEqual(r.kind, 'weak');
});
t('difficulty is one level above the hardest mastered level', () => {
  const others = ['dicts1', 'dicts2', 'prompt1', 'prompt2']; // other topics are clean too, so only lists is in play
  const stats = mastered('lists1', 'lists2', ...others); // Easy mastered only
  const r = A.pick(base({ stats }));
  assert.strictEqual(r.topic, 'lists'); assert.strictEqual(r.item.difficulty, 'Medium');
  const r2 = A.pick(base({ stats: mastered('lists1', 'lists2', 'lists3', ...others) }));
  assert.strictEqual(r2.item.difficulty, 'Hard');
});
t('never goes past Hard, and skips mastered items', () => {
  const r = A.pick(base({ stats: mastered('lists1', 'lists2', 'lists3', 'lists4', 'lists5', 'dicts1', 'dicts2', 'dicts3', 'dicts4', 'dicts5', 'prompt1'), weights: { lists: 1, dicts: 1, prompt: 1 } }));
  assert.strictEqual(r.topic, 'prompt'); assert.notStrictEqual(r.item.id, 'prompt1');
});
t('heavy hint use lowers a topic score', () => {
  const clean = A.topicScore(items.filter((i) => i.topic === 'lists'), mastered('lists1', 'lists2'));
  const hinted = A.topicScore(items.filter((i) => i.topic === 'lists'), { lists1: { tried: true, mastered: true, hints: 4 }, lists2: { tried: true, mastered: true, hints: 4 } });
  assert.ok(hinted < clean, hinted + ' should be below ' + clean);
});
t('everything mastered returns null', () => {
  const all = {}; items.forEach((i) => (all[i.id] = { tried: true, mastered: true, hints: 0 }));
  assert.strictEqual(A.pick(base({ stats: all })), null);
});
t('a missed item is scheduled for 1, then 3, then 7 days, then cleared', () => {
  let now = 0;
  let e = A.applyResult(undefined, false, now);
  assert.deepStrictEqual(e, { stage: 0, due: 1 * DAY });
  assert.strictEqual(A.applyResult(e, true, 0.5 * DAY), e, 'a correct answer before it is due changes nothing');
  now = 1 * DAY; e = A.applyResult(e, true, now);
  assert.deepStrictEqual(e, { stage: 1, due: now + 3 * DAY });
  now = e.due; e = A.applyResult(e, true, now);
  assert.deepStrictEqual(e, { stage: 2, due: now + 7 * DAY });
  now = e.due; e = A.applyResult(e, true, now);
  assert.strictEqual(e, null);
});
t('missing again during review starts the schedule over', () => {
  const e = A.applyResult({ stage: 2, due: 5 * DAY }, false, 6 * DAY);
  assert.deepStrictEqual(e, { stage: 0, due: 7 * DAY });
});
t('a correct answer on an item with no review does not create one', () => {
  assert.strictEqual(A.applyResult(undefined, true, 0), null);
});
t('a due review comes before everything else, oldest first; not-yet-due reviews are ignored', () => {
  const review = { dicts2: { stage: 0, due: 999 * DAY }, lists1: { stage: 1, due: 998 * DAY }, prompt3: { stage: 0, due: 1100 * DAY } };
  const r = A.pick(base({ review }));
  assert.strictEqual(r.kind, 'review'); assert.strictEqual(r.item.id, 'lists1'); assert.strictEqual(r.dueCount, 2);
  const none = A.pick(base({ review: { prompt3: { stage: 0, due: 1100 * DAY } } }));
  assert.notStrictEqual(none.kind, 'review');
});
console.log(passed + ' adaptive tests passed');
