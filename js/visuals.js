window.BP = window.BP || {};
BP.vis = (function () {
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function show(v) {
    if (v === null) return 'None';
    if (v === true) return 'True';
    if (v === false) return 'False';
    if (typeof v === 'string') return "'" + v + "'";
    if (typeof v === 'object') {
      if (v.t === 'dict') return '{' + v.v.map((p) => show(p[0]) + ': ' + show(p[1])).join(', ') + '}';
      if (v.t === 'tuple') return '(' + v.v.map(show).join(', ') + (v.v.length === 1 ? ',' : '') + ')';
      if (v.t === 'set') return '{' + v.v.map(show).join(', ') + '}';
      if (v.t === 'obj') return v.v;
      return '[' + v.v.map(show).join(', ') + ']';
    }
    return String(v);
  }
  // items: array of display values; pointers: {name: index}; hl: [from, to] (to exclusive); negative: show -1 style
  function boxes(items, opts) {
    opts = opts || {};
    const ptr = opts.pointers || {};
    const hl = opts.hl || null;
    let h = '<div class="vis">' + (opts.title ? '<div class="t">' + esc(opts.title) + '</div>' : '') + '<div class="boxes">';
    items.forEach((it, i) => {
      const names = Object.keys(ptr).filter((k) => ptr[k] === i);
      const inHl = hl && i >= hl[0] && i < hl[1];
      h += '<div class="bx' + (inHl ? ' hl' : '') + (names.length ? ' cur' : '') + '">' +
        '<div class="ix">' + i + '</div>' +
        (opts.negative ? '<div class="neg">' + (i - items.length) + '</div>' : '') +
        '<div class="v">' + esc(typeof it === 'string' ? it : show(it)) + '</div>' +
        '<div class="arrow">' + (names.length ? '<span class="a">&#9650;</span>' + esc(names.join(', ')) : '') + '</div></div>';
    });
    h += '</div>';
    const off = Object.keys(ptr).filter((k) => ptr[k] < 0 || ptr[k] >= items.length);
    if (opts.showOff && off.length) h += '<div class="warnbox">' + off.map((k) => esc(k) + ' is ' + ptr[k] + ', which is not a position in this row.').join(' ') + '</div>';
    return h + '</div>';
  }
  function grid(rows, opts) {
    opts = opts || {};
    const r0 = opts.r, c0 = opts.c;
    let h = '<div class="vis">' + (opts.title ? '<div class="t">' + esc(opts.title) + '</div>' : '') + '<table class="gridv"><tr><th></th>';
    (rows[0] || []).forEach((_, c) => (h += '<th>col ' + c + '</th>'));
    h += '</tr>';
    rows.forEach((row, r) => {
      h += '<tr><th>row ' + r + '</th>';
      row.forEach((cell, c) => (h += '<td' + (r === r0 && c === c0 ? ' class="hl"' : '') + '>' + esc(show(cell)) + '</td>'));
      h += '</tr>';
    });
    return h + '</table></div>';
  }
  function dictv(pairs, opts) {
    opts = opts || {};
    let h = '<div class="vis">' + (opts.title ? '<div class="t">' + esc(opts.title) + '</div>' : '') + '<table class="dictv"><tr><th>key</th><th>value</th></tr>';
    pairs.forEach((p) => (h += '<tr><td>' + esc(show(p[0])) + '</td><td>' + esc(show(p[1])) + '</td></tr>'));
    if (!pairs.length) h += '<tr><td colspan="2" class="mute">empty</td></tr>';
    return h + '</table></div>';
  }
  function table(head, rows, opts) {
    opts = opts || {};
    return '<div class="vis">' + (opts.title ? '<div class="t">' + esc(opts.title) + '</div>' : '') + '<table><tr>' + head.map((x) => '<th>' + esc(x) + '</th>').join('') + '</tr>' +
      rows.map((r) => '<tr>' + r.map((x) => '<td>' + esc(x) + '</td>').join('') + '</tr>').join('') + '</table></div>';
  }
  const PTR_NAMES = ['i', 'j', 'k', 'idx', 'index', 'pos', 'left', 'right', 'lo', 'hi', 'start', 'end', 'first', 'last'];
  // Draw the picture for one trace step: every list / string as boxes, every grid as a grid
  function forStep(vars, lesson) {
    const ptrNames = (lesson && lesson.pointers) || PTR_NAMES;
    const ptrs = {};
    ptrNames.forEach((n) => { if (typeof vars[n] === 'number' && Number.isInteger(vars[n])) ptrs[n] = vars[n]; });
    const wanted = lesson && lesson.show;
    let h = '';
    Object.keys(vars).forEach((name) => {
      const v = vars[name];
      if (wanted && wanted.indexOf(name) < 0) return;
      if (v && typeof v === 'object' && (v.t === 'list' || v.t === 'tuple')) {
        if (v.v.length && v.v.every((x) => x && typeof x === 'object' && x.t === 'list')) {
          h += grid(v.v.map((x) => x.v), { title: name, r: vars.r !== undefined ? vars.r : vars.row, c: vars.c !== undefined ? vars.c : vars.col });
        } else {
          let hl = null;
          if (lesson && lesson.window && typeof vars[lesson.window[0]] === 'number' && typeof vars[lesson.window[1]] === 'number') hl = [vars[lesson.window[0]], vars[lesson.window[1]] + 1];
          h += boxes(v.v, { title: name, pointers: ptrs, hl: hl, negative: lesson && lesson.negative, showOff: true });
        }
      } else if (v && typeof v === 'object' && v.t === 'dict') {
        h += dictv(v.v, { title: name });
      } else if (typeof v === 'string' && wanted && wanted.indexOf(name) >= 0) {
        h += boxes(v.split(''), { title: name, pointers: ptrs, negative: lesson && lesson.negative, showOff: true });
      }
    });
    return h || '<div class="mute">No list to draw yet.</div>';
  }
  // Option order for a multiple-choice question: a random order, so the right answer is not always the first one.
  function order(n) { const a = []; for (let i = 0; i < n; i++) a.push(i); for (let i = n - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); const t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  return { boxes, grid, dictv, table, forStep, show, esc, order };
})();
