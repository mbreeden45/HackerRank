#!/usr/bin/env python3
"""Runs every reference solution against its own test cases, and checks the content rules.
Usage: python3 tools/verify.py      (exit code 0 means everything passed)"""
import ast, json, os, re, sqlite3, subprocess, sys, tempfile, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from concepts import detect, program, written_code, locked_code
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.path.join(ROOT, 'content')
fails, checks = [], 0

def load(name, default=None):
    p = os.path.join(C, name)
    return json.load(open(p)) if os.path.exists(p) else default

def ok(cond, msg):
    global checks
    checks += 1
    if not cond: fails.append(msg)
    return cond

def run_py(code, stdin='', timeout=10):
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write(code); path = f.name
    try:
        p = subprocess.run([sys.executable, path], input=stdin, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, '', 'timeout'
    finally:
        os.unlink(path)

def norm(s): return '\n'.join(l.rstrip() for l in s.split('\n')).rstrip('\n')
BANG = re.compile(r'!(?!=)')
def prose_ok(label, text):
    if isinstance(text, (list, tuple)):
        for t in text: prose_ok(label, t)
        return
    if isinstance(text, str):
        # remove code spans in backticks before checking
        t = re.sub(r'`[^`]*`', '', text)
        ok(not BANG.search(t), '%s: contains an exclamation mark: %r' % (label, text[:60]))

def syntax_ok(label, code):
    """Every piece of Python shown to the learner must be valid Python 3. Catches Python 2 style print statements."""
    try:
        ast.parse(code)
        return ok(True, '')
    except SyntaxError as e:
        return ok(False, '%s: not valid Python 3 (line %s: %s): %r' % (label, e.lineno, e.msg, (e.text or '').strip()[:60]))

MC_COUNT = {}
def check_mc(file, label, options, answer, code=None):
    """Rules for every multiple-choice item. If code is given, the marked answer must equal what the code really prints."""
    MC_COUNT[file] = MC_COUNT.get(file, 0) + 1
    ok(len(options) >= 3, '%s: fewer than 3 options' % label)
    ok(len(options) == len(set(options)), '%s: two options have identical text: %r' % (label, options))
    ok(isinstance(answer, int) and 0 <= answer < len(options), '%s: answer index %r is not one of the options' % (label, answer))
    if code is not None:
        rc, so, se = run_py(code)
        ok(rc == 0, '%s: snippet crashes: %s' % (label, se.strip()[-100:]))
        matches = [i for i, o in enumerate(options) if norm(o) == norm(so)]
        ok(len(matches) == 1, '%s: %d options match the real output %r (need exactly 1)' % (label, len(matches), so))
        ok(matches == [answer], '%s: marked answer %r but code really prints %r' % (label, options[answer] if isinstance(answer, int) and 0 <= answer < len(options) else answer, so))

def stub_program(p):
    """What the editor shows at the start, made runnable: a def needs one line under it, so a pass is added for the check only."""
    needs_pass = p['prefix'].rstrip().endswith(':')
    return p['body'] + ('    pass\n' if needs_pass else '')

def check_problems(problems):
    print('\n== Coding problems: %d (%d preset, %d with starter code) ==' % (len(problems), sum(1 for p in problems if p.get('mode') == 'preset'), sum(1 for p in problems if p.get('mode') != 'preset')))
    for p in problems:
        pid = p['id']
        preset = p.get('mode') == 'preset'
        ok(p.get('mode') in ('preset', 'stdin'), '%s: mode must be preset or stdin' % pid)
        tests = [(s['input'], s['output'], 'sample') for s in p['samples']] + [(h['input'], h['output'], 'hidden') for h in p['hidden']]
        bad = []
        for inp, exp, kind in tests:
            code, stdin = program(p, p['solution'], inp)
            rc, so, se = run_py(code, stdin)
            if rc != 0 or norm(so) != norm(exp): bad.append('%s test: input=%r expected=%r got=%r %s' % (kind, inp, exp, so, se.strip()[-120:]))
        ok(not bad, '%s: solution fails: %s' % (pid, bad[:1]))
        # every test must bring its own input. The only exception is a problem with no input at all (for example print Hello),
        # which can only have one possible answer.
        inputs = [t[0] for t in tests]
        if all(i == '' for i in inputs):
            ok(len(tests) == 2, '%s: has no input at all, so it should have one sample and one hidden test, not %d' % (pid, len(tests)))
        else:
            ok(len(set(inputs)) > 1, '%s: all %d test cases have the same input' % (pid, len(tests)))
        if preset and len(set(inputs)) > 1:
            # each hidden test runs with ITS OWN starting data in place of the grey lines (this is what the browser does)
            hid_bad = []
            for h in p['hidden']:
                code, stdin = program(p, p['solution'], h['input'])
                rc, so, se = run_py(code, stdin)
                if rc != 0 or norm(so) != norm(h['output']): hid_bad.append(h['input'])
            ok(not hid_bad, '%s: reference solution fails hidden tests when their own starting data replaces the grey lines: %r' % (pid, hid_bad[:1]))
            # and the tests must really depend on that swap: keeping the sample's grey lines for every test must fail at least one
            stuck = [run_py(p['prefix'] + p['solution'] + p['suffix'], '') for _ in [0]][0]
            ok(any(norm(stuck[1]) != norm(h['output']) for h in p['hidden']), '%s: hidden tests would pass even without swapping in their data, so they test nothing new' % pid)
        ok(len(p['samples']) >= 1 and len(p['hidden']) >= 1, '%s: needs 1+ sample and 1+ hidden test' % pid)
        ok(p['difficulty'] in ('Easy', 'Medium', 'Hard'), '%s: bad difficulty' % pid)
        ok(len(p['hints']) == 4 and all(h.strip() for h in p['hints']), '%s: needs 4 hints' % pid)
        ok(all(s['explanation'].strip() for s in p['samples']), '%s: sample explanation missing' % pid)
        if preset:
            ok(p['suffix'] == '', '%s: a preset problem has no locked bottom part' % pid)
            ok(p['prefix'] == p['samples'][0]['input'], '%s: the locked starting data must equal sample 0' % pid)
            lens = {t[0].count('\n') for t in tests}
            ok(len(lens) == 1, '%s: every test needs the same number of starting-data lines (so error line numbers match)' % pid)
            for t in tests:
                try: ast.parse(t[0])
                except SyntaxError as e: ok(False, '%s: starting data is not valid Python: %r' % (pid, t[0]))
                ok('input(' not in t[0] and 'def ' not in t[0], '%s: preset starting data must not use input or def' % pid)
            ok('input(' not in p['solution'] and 'def ' not in p['solution'] and 'return' not in p['solution'], '%s: preset solution must be plain print lines, no input, def or return' % pid)
        # the open section must hold only the Write-your-code-here comment
        body_lines = [l.strip() for l in p['body'].split('\n') if l.strip()]
        ok('# Write your code here' in body_lines, '%s: the open section needs a "# Write your code here" line' % pid)
        ok(all(l.startswith('#') for l in body_lines), '%s: the open section must hold only the comment, but has code: %r' % (pid, body_lines))
        stub_full = p['prefix'] + p['body'] + p['suffix']
        syntax_ok(pid + ' starting stub', p['prefix'] + stub_program(p) + p['suffix'])
        syntax_ok(pid + ' solution', program(p, p['solution'], p['samples'][0]['input'])[0])
        locked = {l.strip() for l in (p['prefix'] + p['suffix']).split('\n') if l.strip()}
        leaked = [l.strip() for l in p['solution'].split('\n') if l.strip() and l.strip() in locked and l.strip() not in ('else:', 'pass')]
        ok(not leaked, '%s: a solution line is already in the locked part: %r' % (pid, leaked[:2]))
        # with the open section empty, the program must not already pass every test
        empty_pass = 0
        for inp, exp, kind in tests:
            code, stdin = program(p, stub_program(p), inp)
            r = run_py(code, stdin)
            if r[0] == 0 and norm(r[1]) == norm(exp): empty_pass += 1
        ok(empty_pass < len(tests), '%s: with the open section empty, the program already passes every test' % pid)
        ok(len(set(h['output'] for h in p['hidden']) | set(s['output'] for s in p['samples'])) >= 2 or len(p['hidden']) <= 2, '%s: all tests have the same answer, a hard-coded print would pass' % pid)
        # the hints must not use Python 2 style print (print x) and must read as Python 3
        names = {n.id for n in ast.walk(ast.parse(textwrap.dedent(written_code(p)))) if isinstance(n, ast.Name)}
        for hint in p['hints']:
            plain = re.sub(r'`[^`]*`', '', hint)
            for m in re.finditer(r'\bprint\s+(\S+)', plain):
                tok = m.group(1).strip('.,;:')
                ok(not (tok in names or tok[:1] in '"\'' or tok[:1].isdigit()), '%s: hint looks like Python 2 print: %r' % (pid, hint[:70]))
        prose_ok(pid, [p['title'], p['input_fmt'], p['output_fmt']] + p['statement'] + p['hints'] + [s['explanation'] for s in p['samples']])
        print('  %s  %-22s %-6s %d tests' % ('PASS' if not bad else 'FAIL', pid, 'preset' if preset else 'stdin', len(tests)))

def check_concepts(problems, lessons, diag):
    """A problem may only use ideas that its own lesson or an earlier lesson teaches."""
    print('\n== Concepts: nothing is used before it is taught ==')
    taught, acc, first = {}, set(), {}
    for i, L in enumerate(lessons):
        ok(isinstance(L.get('concepts'), list), '%s: lesson has no concepts list' % L['id'])
        for c in L.get('concepts', []): first.setdefault(c, L['id'])
        acc = acc | set(L.get('concepts', []))
        taught[L['id']] = set(acc)
    starter = set(next((L.get('starter_concepts', []) for L in lessons if L['id'] == 'functions'), []))
    def explain(c, lesson):
        return '%s (%s)' % (c, ('first taught in lesson "%s", which comes later' % first[c]) if c in first else 'no lesson teaches it')
    per_lesson = {}
    for L in lessons:
        for key in ('example', 'example2', 'predict'):
            if key in L:
                bad = detect(L[key]['code']) - taught[L['id']]
                ok(not bad, 'lesson %s %s uses ideas not yet taught: %s' % (L['id'], key, ', '.join(explain(c, L['id']) for c in sorted(bad))))
        if 'starter' in L:
            for i, blk in enumerate(L['starter']['blocks']):
                if blk.get('static'): continue
                bad = detect(blk['code']) - taught[L['id']] - starter
                ok(not bad, 'lesson %s starter block %d uses ideas not yet taught: %s' % (L['id'], i, sorted(bad)))
                rc, so, se = run_py(blk['code'], blk.get('stdin', ''))
                ok(rc == 0 and norm(so) == norm(blk['output']), 'lesson %s starter block %d prints %r, says %r' % (L['id'], i, so, blk['output']))
            for blk in L['starter']['blocks']:
                for line, meaning in blk['rows']: prose_ok(L['id'], meaning)
    for i, q in enumerate(diag['questions']):
        bad = detect(q['code']) - taught.get(q['lesson'], set())
        ok(not bad, 'diagnostic Q%d (%s) uses ideas not yet taught: %s' % (i + 1, q['lesson'], ', '.join(explain(c, q['lesson']) for c in sorted(bad))))
    for p in problems:
        lid = p['lesson']
        ok(lid in taught, '%s: unknown lesson %s' % (p['id'], lid))
        if lid not in taught: continue
        decl = p.get('concepts')
        ok(isinstance(decl, list) and decl, '%s: problem has no concepts list' % p['id'])
        det = detect(written_code(p))
        ok(det == set(decl or []), '%s: concepts list is out of date (rebuild content). code uses %s, list says %s' % (p['id'], sorted(det), sorted(decl or [])))
        bad = det - taught[lid]
        ok(not bad, '%s (lesson %s) uses ideas not yet taught: %s' % (p['id'], lid, ', '.join(explain(c, lid) for c in sorted(bad))))
        if p.get('mode') != 'preset':
            lbad = detect(locked_code(p)) - taught[lid] - starter
            ok(not lbad, '%s: locked starter code uses ideas not explained in "Reading the starter code": %s' % (p['id'], sorted(lbad)))
        per_lesson.setdefault(lid, [0, set()])
        per_lesson[lid][0] += 1; per_lesson[lid][1] |= det
    for L in lessons:
        n, used = per_lesson.get(L['id'], [0, set()])
        print('  PASS  %-14s teaches %-48s %2d problems' % (L['id'], ' '.join(L.get('concepts', [])) or '(nothing new)', n))

def run_snippet_output(code, stdin=''):
    rc, so, se = run_py(code, stdin)
    return rc, so.rstrip('\n'), se

def check_lessons(lessons, diag):
    print('\n== Lessons: %d, diagnostic questions: %d ==' % (len(lessons), len(diag['questions'])))
    ids = set()
    for L in lessons:
        ids.add(L['id'])
        rc, so, se = run_snippet_output(L['example']['code'], L['example'].get('stdin', ''))
        ok(rc == 0, '%s: worked example crashes: %s' % (L['id'], se[-100:]))
        if 'example2' in L:
            rc, so, se = run_snippet_output(L['example2']['code'], L['example2'].get('stdin', ''))
            ok(rc == 0, '%s: second example crashes' % L['id'])
        for key in ('example', 'example2', 'predict'):
            if key in L: syntax_ok('lesson %s %s' % (L['id'], key), L[key]['code'])
        rc, so, se = run_snippet_output(L['predict']['code'])
        ok(rc == 0, '%s: predict code crashes' % L['id'])
        check_mc('lessons.json (predict)', 'lesson ' + L['id'], L['predict']['options'], L['predict']['answer'], L['predict']['code'])
        ok(len(L['idea']) >= 2 and L['symbols'], '%s: needs idea paragraphs and a symbols table' % L['id'])
        prose_ok(L['id'], [L['title']] + L['idea'] + [s[1] for s in L['symbols']] + [L['example']['caption'], L['predict']['why']])
        print('  PASS  %s' % L['id'])
    for i, q in enumerate(diag['questions']):
        syntax_ok('diagnostic Q%d' % (i + 1), q['code'])
        check_mc('diagnostic.json', 'diagnostic Q%d (%s)' % (i + 1, q['lesson']), q['options'], q['answer'], q['code'])
        ok(q['lesson'] in ids, 'diagnostic %d: unknown lesson %s' % (i, q['lesson']))
        prose_ok('diagnostic %d' % i, [q['prompt'], q['why']])

ERROR_SNIPPETS = [
 ("nums = [1, 2]\nprint(nums[5])", "That position does not exist"),
 ("print(total)", "Python does not know that name"),
 ("print('a' + 1)", "You tried to add text and a number"),
 ("x = int('abc')", "That text is not a whole number"),
 ("print(5 / 0)", "Dividing by zero"),
 ("input()", "The program asked for input that was not there"),
 ("n = 3\nn.append(1)", "That kind of value has no such tool"),
 ("def f(a):\n    return a\nf(1, 2)", "Wrong number of inputs to the function"),
 ("d = {}\nprint(d['k'])", "That key is not in the dictionary"),
 ("nums = [1]\nprint(nums['a'])", "A position must be a whole number"),
 ("print(len(5))", "len needs something with items inside"),
 ("if True:\nprint(1)", "The lines under this line need to be indented"),
 ("x = 5\nprint(x[0])", "You used square brackets on something that has no positions"),
]
LITERALS = [  # messages from newer Pythons (the browser runs 3.12) that older ones cannot produce
 ("SyntaxError: expected ':'", "A colon is missing"),
 ("SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?", "You used = where you meant =="),
 ("IndentationError: expected an indented block after 'if' statement on line 1", "The lines under this line need to be indented"),
 ("SyntaxError: '(' was never closed", "A bracket or quote mark was opened but not closed"),
]
def check_errors(errors):
    print('\n== Error explainer: %d patterns ==' % len(errors))
    for e in errors:
        try: re.compile(e['match'])
        except re.error as ex: ok(False, 'error pattern does not compile: %s' % e['match'])
        prose_ok(e['title'], [e['title'], e['plain'], e.get('fix', '')])
    for code, title in ERROR_SNIPPETS:
        rc, so, se = run_py(code, '')
        lines = [l for l in se.strip().split('\n') if l.strip()]
        last = lines[-1] if lines else ''
        hit = next((e for e in errors if re.search(e['match'], last)), None)
        ok(hit is not None and hit['title'] == title, 'error explainer: %r should give %r but gave %r for %r' % (code, title, hit and hit['title'], last))
    for msg, title in LITERALS:
        hit = next((e for e in errors if re.search(e['match'], msg)), None)
        ok(hit is not None and hit['title'] == title, 'error explainer: %r should give %r' % (msg, title))
    print('  PASS  %d real error messages translate correctly' % len(ERROR_SNIPPETS))

def check_quiz(name, items):
    ids = [q['id'] for q in items]
    ok(len(ids) == len(set(ids)), '%s: duplicate item ids' % name)
    written = 0
    for q in items:
        ok(q['difficulty'] in ('Easy', 'Medium', 'Hard'), '%s: bad difficulty' % q['id'])
        if q.get('snippet'): syntax_ok(q['id'] + ' snippet', q['snippet'])
        if q.get('code'): syntax_ok(q['id'] + ' code', q['code'])
        if q.get('type') == 'written':
            written += 1
            ok(q['model'].strip(), '%s: written item has no model answer' % q['id'])
            ok(4 <= len(q['rubric']) <= 6, '%s: rubric needs 4 to 6 points, has %d' % (q['id'], len(q['rubric'])))
            for r in q['rubric']:
                ok(r['point'].strip() and len(r['keywords']) >= 1 and all(k.strip() for k in r['keywords']), '%s: rubric point needs text and keywords: %r' % (q['id'], r))
            prose_ok(q['id'], [q['prompt'], q['model']] + [r['point'] for r in q['rubric']])
        else:
            check_mc(name, q['id'], q['options'], q['answer'], q.get('code'))
            for o in q['options']:
                ok(not re.search(r'\b(above|all of these|none of these|both of these)\b', o, re.I), '%s: option refers to other options, but options are shuffled: %r' % (q['id'], o[:40]))
            prose_ok(q['id'], [q['prompt'], q['why']])
    return written

def check_study(lessons, sqltables):
    print('\n== Reading lessons: %d ==' % len(lessons))
    kinds = {'p', 'h', 'code', 'callout', 'warn', 'steps', 'table', 'compare', 'sql'}
    seen = set()
    for L in lessons:
        ok(L['id'] not in seen, 'duplicate study lesson id %s' % L['id']); seen.add(L['id'])
        ok(L.get('track'), '%s: missing track' % L['id'])
        for b in L['blocks']:
            ok(b['t'] in kinds, '%s: unknown block type %s' % (L['id'], b['t']))
            if b['t'] in ('p', 'h', 'callout', 'warn'): prose_ok(L['id'], b['text'])
            if b['t'] == 'code' and str(b.get('label', '')).startswith('Python'): syntax_ok(L['id'] + ' code block', b['text'])
            if b['t'] == 'steps': prose_ok(L['id'], b['items'])
            if b['t'] == 'table':
                ok(all(len(r) == len(b['head']) for r in b['rows']), '%s: table row length does not match header' % L['id'])
                prose_ok(L['id'], [c for r in b['rows'] for c in r if isinstance(c, str)])
            if b['t'] == 'compare':
                ok(b['bad'] != b['good'] and b['badWhy'].strip() and b['goodWhy'].strip(), '%s: compare block incomplete' % L['id'])
                prose_ok(L['id'], [b['badWhy'], b['goodWhy']])
            if b['t'] == 'sql':
                con = sqlite3.connect(':memory:')
                for t in sqltables.values(): con.executescript(t['create'])
                try: con.execute(b['text']).fetchall()
                except Exception as ex: ok(False, '%s: SQL block fails: %s' % (L['id'], ex))
        print('  PASS  %s' % L['id'])

def check_sql(items):
    print('\n== SQL problems: %d ==' % len(items))
    tables = load('sql_tables.json', {})
    for p in items:
        con = sqlite3.connect(':memory:')
        for t in tables.values(): con.executescript(t['create'])
        try:
            cur = con.execute(p['solution']); rows = [list(r) for r in cur.fetchall()]
            exp = [list(r) for r in p['expected']]
            same = sorted(map(repr, rows)) == sorted(map(repr, exp)) if not p.get('ordered') else rows == exp
            ok(same, '%s: SQL solution gives %r, expected %r' % (p['id'], rows[:3], exp[:3]))
            print('  %s  %s' % ('PASS' if same else 'FAIL', p['id']))
        except Exception as ex:
            ok(False, '%s: SQL error %s' % (p['id'], ex))
        prose_ok(p['id'], [p['title']] + p['statement'] + p['hints'])
        ok(len(p['hints']) == 4 and all(h.strip() for h in p['hints']), '%s: needs 4 hints' % p['id'])
        ok(len(p['expected']) == p['expect_count'], '%s: has %d rows but the hand-counted number is %d' % (p['id'], len(p['expected']), p['expect_count']))
        ok(not p['ordered'] or 'ORDER BY' in p['solution'].upper(), '%s: marked ordered but the solution has no ORDER BY' % p['id'])
        ok(all(t in tables and t in p['solution'] for t in p['tables']), '%s: tables list does not match the solution' % p['id'])
        ok(p['difficulty'] in ('Easy', 'Medium', 'Hard'), '%s: bad difficulty' % p['id'])

def check_cards(cards):
    print('\n== Flashcards: %d ==' % len(cards))
    ids = [c['id'] for c in cards]
    ok(len(ids) == len(set(ids)), 'flashcard ids must be unique')
    tables = load('sql_tables.json', {})
    by_topic = {}
    for c in cards:
        by_topic[c['topic']] = by_topic.get(c['topic'], 0) + 1
        ok(c['front'].startswith('I want to ') and c['front'].endswith('.'), 'card %s: front must read "I want to ... ." : %r' % (c['id'], c['front'][:50]))
        ok(c['back'].startswith('so I write ') and c['back'].strip() != 'so I write', 'card %s: back must start with "so I write"' % c['id'])
        ok('`' not in c['back'] or c.get('check'), 'card %s shows code but has no executed check' % c['id'])
        chk = c.get('check')
        if chk and chk['lang'] == 'python':
            syntax_ok('card %s example' % c['id'], chk['code'])
            rc, so, se = run_py(chk['code'], chk.get('stdin', ''))
            ok(rc == 0 and norm(so) == norm(chk['output']), 'card %s: example prints %r, card says %r %s' % (c['id'], so, chk['output'], se.strip()[-80:]))
        elif chk and chk['lang'] == 'sql':
            con = sqlite3.connect(':memory:')
            for t in tables.values(): con.executescript(t['create'])
            try:
                rows = [list(r) for r in con.execute(chk['sql']).fetchall()]
                ok(rows == chk['rows'] and len(rows) >= 1, 'card %s: query rows differ from the card or are empty' % c['id'])
            except Exception as ex:
                ok(False, 'card %s: SQL error %s' % (c['id'], ex))
        elif chk: ok(False, 'card %s: unknown check type' % c['id'])
        prose_ok('card ' + c['id'], [c['front'], c['back']])
    print('  PASS  ' + ', '.join('%s %d' % (k, v) for k, v in sorted(by_topic.items())))

def main():
    problems = load('problems.json', [])
    check_problems(problems)
    lessons = load('lessons.json', []); diag = load('diagnostic.json', {'questions': []})
    check_lessons(lessons, diag)
    check_concepts(problems, lessons, diag)
    check_errors(load('errors.json', []))
    for name in ('quiz_bigo.json', 'quiz_prompt.json'):
        d = load(name)
        if d:
            w = check_quiz(name, d)
            print('\n== %s: %d questions (%d written) ==' % (name, len(d), w))
    study = load('lessons_x.json')
    if study: check_study(study, load('sql_tables.json', {}))
    sql = load('sql_problems.json')
    if sql:
        check_sql(sql)
        every = [p['id'] for p in problems] + [p['id'] for p in sql] + [q['id'] for n in ('quiz_bigo.json', 'quiz_prompt.json') for q in (load(n) or [])]
        ok(len(every) == len(set(every)), 'item ids must be unique across Python problems, SQL problems and quiz items')
        lessons_x = {l['id'] for l in (load('lessons_x.json') or [])}
        for p in sql: ok(p['lesson'] in lessons_x, '%s: unknown lesson %s' % (p['id'], p['lesson']))
    cards = load('flashcards.json')
    if cards: check_cards(cards)
    mock = load('mock_exam.json')
    if mock:
        print('\n== Mock exam: %d sections, %d minutes ==' % (len(mock['sections']), mock['minutes']))
        pids = {p['id'] for p in problems}; sids = {p['id'] for p in (sql or [])}
        qids = {q['id'] for n in ('quiz_bigo.json', 'quiz_prompt.json') for q in (load(n) or [])}
        ok(sum(s['weight'] for s in mock['sections']) == 100, 'mock exam weights must add up to 100')
        ok(mock['pass_percent'] == 60, 'mock exam pass line must be 60')
        seen_items = []
        for s in mock['sections']:
            for i in s['items']:
                ok(i in pids or i in sids or i in qids, 'mock exam references unknown item %s' % i)
                seen_items.append(i)
                if s['kind'] == 'python': ok(i in pids, 'mock exam: %s is not a Python problem' % i)
                if s['kind'] == 'sql': ok(i in sids, 'mock exam: %s is not a SQL problem' % i)
        ok(len(seen_items) == len(set(seen_items)), 'mock exam lists an item twice')
        print('  PASS  %d items across %d sections' % (len(seen_items), len(mock['sections'])))
    print('\n== Multiple-choice items checked, by file ==')
    for k in sorted(MC_COUNT): print('  %-26s %d items' % (k, MC_COUNT[k]))
    print('  %-26s %d items' % ('TOTAL', sum(MC_COUNT.values())))
    print('\n%d checks run, %d failed.' % (checks, len(fails)))
    for f in fails: print('  FAIL:', f)
    print('RESULT:', 'ALL PASSED' if not fails else 'FAILURES FOUND')
    sys.exit(1 if fails else 0)
main()
