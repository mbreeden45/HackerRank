window.BP = window.BP || {};
BP.explain = (function () {
  const esc = (s) => BP.vis.esc(s);
  let ERRORS = [];
  function setErrors(e) { ERRORS = e; }

  // ---------- error explainer ----------
  function lastErrorLine(tb) {
    const lines = String(tb).trim().split('\n').filter((l) => l.trim());
    for (let i = lines.length - 1; i >= 0; i--) if (/^[A-Za-z_.]*(Error|Exception|Exit|Interrupt)\b/.test(lines[i])) return lines[i];
    return lines[lines.length - 1] || '';
  }
  function errorLineNumber(tb) {
    const all = [...String(tb).matchAll(/File "<exec>", line (\d+)/g)];
    return all.length ? Number(all[all.length - 1][1]) : null;
  }
  function explainError(tb) {
    const last = lastErrorLine(tb);
    const ln = errorLineNumber(tb);
    for (const e of ERRORS) {
      const m = last.match(new RegExp(e.match));
      if (m) {
        let txt = e.plain.replace(/\{(\d)\}/g, (_, n) => m[Number(n)] || '');
        return { title: e.title, plain: txt, fix: e.fix || '', line: ln, raw: last };
      }
    }
    return { title: 'Python stopped with an error', plain: 'Python hit something it could not do. Read the last line of the message: it names the kind of error, then gives details.', fix: 'Find the line number in the message and look at that line first.', line: ln, raw: last };
  }
  function errorHtml(tb) {
    const x = explainError(tb);
    return '<div class="bad"><b>' + esc(x.title) + '</b>' + (x.line ? ' (near line ' + x.line + ')' : '') +
      '<p>' + esc(x.plain) + '</p>' + (x.fix ? '<p><b>What to try:</b> ' + esc(x.fix) + '</p>' : '') +
      '<p class="mute">Python said: <code class="k">' + esc(x.raw) + '</code></p></div>';
  }

  // ---------- line explainer ----------
  const GLOSS = [
    [/\bprint\(/, 'print( )', 'shows something on the screen'],
    [/\binput\(/, 'input( )', 'reads one line the user typed, as text'],
    [/\blen\(/, 'len( )', 'counts how many items are inside'],
    [/\brange\(/, 'range( )', 'makes a run of whole numbers'],
    [/\bint\(/, 'int( )', 'turns text into a whole number'],
    [/\bstr\(/, 'str( )', 'turns a value into text'],
    [/\.split\(/, '.split( )', 'cuts text into pieces at the spaces'],
    [/\.append\(/, '.append( )', 'adds one item to the end of a list'],
    [/\bsum\(/, 'sum( )', 'adds up all the numbers in a list'],
    [/\bmax\(/, 'max( )', 'finds the biggest value'],
    [/\bmin\(/, 'min( )', 'finds the smallest value'],
    [/\bsorted\(/, 'sorted( )', 'gives a new list in order, smallest first'],
    [/==/, '==', 'asks the question: are these two things equal. The answer is True or False'],
    [/!=/, '!=', 'asks: are these two things different'],
    [/(^|[^=!<>+\-*\/%])=([^=]|$)/, '=', 'stores the value on the right into the name on the left'],
    [/\+=/, '+=', 'adds the right side to the name, and stores the result back in the name'],
    [/-=/, '-=', 'subtracts the right side from the name, and stores the result back'],
    [/%/, '%', 'the remainder after dividing. 7 % 3 is 1 because 3 goes into 7 twice with 1 left over'],
    [/\/\//, '//', 'divides and drops anything after the decimal point. 7 // 2 is 3'],
    [/<=/, '<=', 'less than or equal to'],
    [/>=/, '>=', 'greater than or equal to'],
    [/[^<]<[^=<]/, '<', 'less than'],
    [/[^>]>[^=>]/, '>', 'greater than'],
    [/\[[^\]]*:[^\]]*\]/, '[a:b]', 'a slice: copies the items from position a up to, but not including, position b'],
    [/\w\[[^:\]]+\]/, '[ ]', 'picks the item at that position. Positions start at 0'],
    [/\bnot\b/, 'not', 'flips True to False and False to True'],
    [/\band\b/, 'and', 'True only when both sides are True'],
    [/\bor\b/, 'or', 'True when at least one side is True'],
    [/\bin\b/, 'in', 'inside a for line: go through the items one at a time. Elsewhere: is this item found inside'],
    [/:\s*$/, ':', 'ends the line and says the indented lines below belong to it'],
  ];
  function strip(s) { return s.replace(/#.*$/, '').trim(); }
  const RULES = [
    [/^for\s+(\w+)\s+in\s+range\(\s*len\((\w+)\)\s*\)\s*:$/, (m) => `Repeat the lines below once for every position in ${m[2]}. The name ${m[1]} holds the position (0, then 1, then 2 and so on), not the item itself. To get the item, write ${m[2]}[${m[1]}].`],
    [/^for\s+(\w+)\s+in\s+range\(\s*([^,()]+)\s*\)\s*:$/, (m) => `Repeat the lines below. The name ${m[1]} counts 0, 1, 2 and so on, stopping just before ${m[2]}. So it runs ${m[2]} times.`],
    [/^for\s+(\w+)\s+in\s+range\(\s*([^,()]+),\s*([^,()]+)\)\s*:$/, (m) => `Repeat the lines below. The name ${m[1]} starts at ${m[2]} and counts up by 1, stopping just before ${m[3]}. The ${m[3]} itself is never used.`],
    [/^for\s+(\w+)\s+in\s+range\(\s*([^,()]+),\s*([^,()]+),\s*([^,()]+)\)\s*:$/, (m) => `Repeat the lines below. The name ${m[1]} starts at ${m[2]} and moves by ${m[4]} each time, stopping before it reaches ${m[3]}.`],
    [/^for\s+(\w+)\s*,\s*(\w+)\s+in\s+enumerate\((\w+)\)\s*:$/, (m) => `Go through ${m[3]} one item at a time. ${m[1]} is the position and ${m[2]} is the item at that position.`],
    [/^for\s+(\w+)\s+in\s+(\w+)\s*:$/, (m) => `Go through ${m[2]} one item at a time. Each time around, the name ${m[1]} holds the next item (the value itself, not its position).`],
    [/^while\s+(.+):$/, (m) => `Keep repeating the lines below for as long as this is True: ${m[1]}. Python checks it again before each repeat.`],
    [/^if\s+(.+):$/, (m) => `Check this: ${m[1]}. If it is True, run the indented lines below. If not, skip them.`],
    [/^elif\s+(.+):$/, (m) => `Only reached if the earlier checks were all False. Then check this: ${m[1]}. If True, run the indented lines below.`],
    [/^else\s*:$/, () => 'Reached only when none of the checks above were True. Runs the indented lines below.'],
    [/^def\s+(\w+)\((.*)\)\s*:$/, (m) => `Creates a function called ${m[1]}. ${m[2].trim() ? 'It receives ' + m[2] + ' when someone uses it.' : 'It receives nothing.'} Nothing inside runs yet. It runs each time someone writes ${m[1]}(...).`],
    [/^return\s*$/, () => 'Stops the function and hands back nothing (None).'],
    [/^return\s+(.+)$/, (m) => `Stops the function right here and hands back ${m[1]} to whoever called it.`],
    [/^print\((.*)\)$/, (m) => `Shows ${m[1] ? m[1] : 'an empty line'} on the screen, then moves to a new line.`],
    [/^(\w+)\s*=\s*input\(\)\s*$/, (m) => `Waits for one line of typing and stores it, as text, in the name ${m[1]}.`],
    [/^(\w+)\s*=\s*int\(input\(\)\)\s*$/, (m) => `Reads one line, turns it into a whole number, and stores it in ${m[1]}.`],
    [/^(\w+)\s*=\s*list\(map\(int,\s*input\(\)\.split\(\)\)\)\s*$/, (m) => `Reads one line like "3 1 4", cuts it at the spaces into pieces, turns each piece into a whole number, and stores the list in ${m[1]}.`],
    [/^(\w+)\.append\((.*)\)$/, (m) => `Adds ${m[2]} to the end of the list ${m[1]}.`],
    [/^(\w+)\s*\+=\s*(.+)$/, (m) => `Adds ${m[2]} to ${m[1]} and stores the new total back in ${m[1]}.`],
    [/^(\w+)\s*-=\s*(.+)$/, (m) => `Subtracts ${m[2]} from ${m[1]} and stores the result back in ${m[1]}.`],
    [/^(\w+)\s*=\s*(\w+)\[([^\]:]+)\]$/, (m) => `Looks inside ${m[2]} at position ${m[3]} (counting from 0) and stores that item in ${m[1]}.`],
    [/^(\w+)\s*=\s*(\w+)\[([^\]]*):([^\]]*)\]$/, (m) => `Copies a piece of ${m[2]}: from position ${m[3] || '0'} up to, but not including, position ${m[4] || 'the end'}. The piece is stored in ${m[1]}.`],
    [/^(\w+)\s*=\s*(.+)$/, (m) => `Works out ${m[2]} first, then stores the answer in the name ${m[1]}. The single = means "store", not "is equal to".`],
    [/^(break)$/, () => 'Leaves the loop right now.'],
    [/^(continue)$/, () => 'Skips the rest of this round and jumps to the next round of the loop.'],
  ];
  // ---------- piece-by-piece breakdown of function calls, read from the inside out ----------
  const FUNCS = {
    print: (a) => `shows ${a || 'an empty line'} on the screen, then moves to a new line`,
    sum: (a) => `adds up all the numbers inside ${a}`,
    max: (a) => `finds the biggest value in ${a}`,
    min: (a) => `finds the smallest value in ${a}`,
    len: (a) => `counts how many items are in ${a}`,
    sorted: (a) => `makes a new list from ${a} in order, smallest first`,
    int: (a) => `turns ${a} into a whole number`,
    str: (a) => `turns ${a} into text`,
    list: (a) => `makes a list out of ${a}`,
    map: (a) => `applies the first tool to each item of the second thing (${a})`,
    range: (a) => `makes the run of whole numbers described by ${a}`,
    input: () => 'waits for one line of typing and gives it back as text',
    abs: (a) => `drops the minus sign of ${a}, so it is never negative`,
    round: (a) => `rounds ${a} to the nearest whole number`,
    split: (a) => `cuts the text at the spaces into a list of pieces${a ? ' (it cuts at ' + a + ' instead of spaces)' : ''}`,
    append: (a) => `adds ${a} to the end of the list`,
  };
  const KEYWORDS = new Set(['for', 'in', 'if', 'else', 'elif', 'while', 'and', 'or', 'not', 'return', 'def', 'True', 'False', 'None', 'range', 'print']);
  function breakdown(line) {
    let work = line, k = 0;
    const steps = [], placeholders = {};
    const re = /([A-Za-z_][\w.]*)\(([^()]*)\)/;
    let m;
    while ((m = re.exec(work)) && k < 12) {
      const name = m[1].split('.').pop(), arg = m[2].trim().replace(/@(\d+)/g, (_, n) => placeholders[n].shown);
      const f = FUNCS[name];
      const id = k++;
      const shown = m[0].replace(/@(\d+)/g, (_, n) => placeholders[n].shown);
      placeholders[id] = { shown };
      steps.push({ code: shown, text: f ? `${name} ${f(arg)}.` : `${name} is a tool (a function). The brackets hold what it is given: ${arg || 'nothing'}.`, name });
      work = work.slice(0, m.index) + '@' + id + work.slice(m.index + m[0].length);
    }
    const names = [];
    line.replace(/"[^"]*"|'[^']*'/g, ' ').replace(/[A-Za-z_]\w*(?!\w*\()/g, (w, off, str) => {
      if (str[off + w.length] === '(' || str[off - 1] === '.' || KEYWORDS.has(w) || FUNCS[w] || names.indexOf(w) >= 0) return;
      names.push(w);
    });
    return { steps, names };
  }

  function explainLine(raw) {
    const line = strip(raw);
    if (!line) return { text: 'This line is empty or only a comment. Python ignores it.', gloss: [] };
    let text = null;
    for (const [re, f] of RULES) { const m = line.match(re); if (m) { text = f(m); break; } }
    if (!text) text = 'This line asks Python to work something out. Read the symbols listed below to see what each part does.';
    const gloss = [];
    GLOSS.forEach(([re, sym, mean]) => { if (re.test(line)) gloss.push([sym, mean]); });
    const calls = breakdown(line);
    if (calls.steps.length) {
      gloss.push(['( )', 'brackets after a tool name hold what you hand to that tool. The tool works on what is inside them']);
    }
    return { text, gloss, steps: calls.steps, names: calls.names };
  }
  function lineHtml(raw) {
    const x = explainLine(raw);
    const parts = (x.steps && x.steps.length ? '<p><b>Piece by piece, from the inside out:</b></p><ol>' + x.steps.map((st) => '<li><code class="k">' + esc(st.code) + '</code> ' + esc(st.text) + '</li>').join('') + '</ol>' : '') +
      (x.names && x.names.length ? '<p><b>Names in this line:</b> ' + x.names.map((n) => '<code class="k">' + esc(n) + '</code>').join(', ') + '. A name is a label for a value stored earlier in the program, so the line uses that value.</p>' : '');
    return '<div class="callout"><b>In plain English:</b> ' + esc(x.text) + '</div>' + parts +
      (x.gloss.length ? '<table class="sym"><tr><th>Symbol</th><th>What it does</th></tr>' + x.gloss.map((g) => '<tr><td>' + esc(g[0]) + '</td><td>' + esc(g[1]) + '</td></tr>').join('') + '</table>' : '');
  }
  return { setErrors, explainError, errorHtml, explainLine, lineHtml };
})();
