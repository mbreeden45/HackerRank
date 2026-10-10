// Checks the line explainer names every piece of a line. Usage: node tools/test_explain.js
const assert = require('assert'), fs = require('fs'), path = require('path');
global.window = { BP: {} }; global.BP = window.BP; BP.vis = { esc: (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;') };
eval(fs.readFileSync(path.join(__dirname, '../js/explain.js'), 'utf8'));
const html = (l) => BP.explain.lineHtml(l);
let n = 0; const t = (name, fn) => { fn(); n++; console.log('  PASS  ' + name); };
t('print(sum(nums)) explains print, sum, nums and the brackets', () => {
  const h = html('print(sum(nums))');
  ['print', 'sum', 'nums', 'brackets', 'adds up all the numbers', 'shows sum(nums) on the screen', 'inside out'].forEach((w) => assert.ok(h.includes(w), 'missing: ' + w));
  assert.ok(h.indexOf('sum(nums)') < h.indexOf('print(sum(nums))'), 'sum is explained before print');
});
t('max and min lines', () => {
  assert.ok(html('print(max(nums))').includes('finds the biggest value in nums'));
  assert.ok(html('print(min(nums))').includes('finds the smallest value in nums'));
});
t('the input line explains list, map, int, input and split', () => {
  const h = html('nums = list(map(int, input().split()))');
  ['input', 'split', 'list', 'map', 'int'].forEach((w) => assert.ok(h.includes(w), 'missing: ' + w));
});
t('a plain line with no calls still works', () => { assert.ok(html('x = 5').includes('stores')); });
console.log(n + ' explainer tests passed');
