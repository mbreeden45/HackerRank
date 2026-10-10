// Checks the spaced repetition scheduling. Usage: node tools/test_cards.js
const assert = require('assert');
const K = require('../js/cards.js');
const { MIN, DAY } = K;
let n = 0; const t = (name, fn) => { fn(); n++; console.log('  PASS  ' + name); };
t('Again returns the card in 10 minutes and counts a lapse', () => {
  const s = K.schedule(undefined, 'again', 0);
  assert.strictEqual(s.due, 10 * MIN); assert.strictEqual(s.lapses, 1); assert.strictEqual(s.reps, 0);
});
t('first Good is 1 day, then 3 days, then it multiplies by ease', () => {
  let s = K.schedule(undefined, 'good', 0); assert.strictEqual(s.interval, 1);
  s = K.schedule(s, 'good', s.due); assert.strictEqual(s.interval, 3);
  const before = s; s = K.schedule(s, 'good', s.due); assert.strictEqual(s.interval, Math.round(3 * before.ease));
});
t('Easy jumps further than Good, Hard stays short', () => {
  const g = K.schedule({ reps: 2, interval: 6, ease: 2.5, due: 0, lapses: 0 }, 'good', 0);
  const e = K.schedule({ reps: 2, interval: 6, ease: 2.5, due: 0, lapses: 0 }, 'easy', 0);
  const h = K.schedule({ reps: 2, interval: 6, ease: 2.5, due: 0, lapses: 0 }, 'hard', 0);
  assert.ok(e.interval > g.interval && g.interval > h.interval, [h.interval, g.interval, e.interval].join(' < '));
});
t('ease never drops below 1.3 and never rises above 3', () => {
  let s = undefined; for (let i = 0; i < 20; i++) s = K.schedule(s, 'again', 0);
  assert.strictEqual(s.ease, 1.3);
  let e = undefined; for (let i = 0; i < 20; i++) e = K.schedule(e, 'easy', 0);
  assert.strictEqual(e.ease, 3);
});
t('Again after a long interval resets the card', () => {
  const s = K.schedule({ reps: 5, interval: 40, ease: 2.5, due: 0, lapses: 0 }, 'again', 100);
  assert.strictEqual(s.interval, 0); assert.strictEqual(s.reps, 0); assert.strictEqual(s.due, 100 + 10 * MIN);
});
t('previews show readable labels', () => {
  const p = K.previews(undefined, 0);
  assert.deepStrictEqual(p, { again: '10 min', hard: '1 day', good: '1 day', easy: '4 days' });
});
t('queue: due cards first (oldest first), then at most the new-card limit', () => {
  const cards = []; for (let i = 1; i <= 15; i++) cards.push({ id: 'c' + i, topic: i % 2 ? 'a' : 'b' });
  const states = { c3: { due: 50 }, c1: { due: 10 }, c2: { due: 9999 } };
  const q = K.queue(cards, states, 100, null, 5).map((c) => c.id);
  assert.deepStrictEqual(q.slice(0, 2), ['c1', 'c3']); assert.strictEqual(q.length, 2 + 5);
  assert.ok(q.indexOf('c2') < 0, 'a card due in the future is not offered');
  assert.deepStrictEqual(K.queue(cards, {}, 100, 'a', 3).map((c) => c.id), ['c1', 'c3', 'c5']);
});
console.log(n + ' flashcard scheduling tests passed');
