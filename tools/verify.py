#!/usr/bin/env python3
"""Runs every reference solution against its own test cases, and checks the content rules.
Usage: python3 tools/verify.py      (exit code 0 means everything passed)"""
import json, os, re, sqlite3, subprocess, sys, tempfile
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

def check_problems(problems):
    print('\n== Coding problems: %d ==' % len(problems))
    for p in problems:
        pid = p['id']
        full = p['prefix'] + p['solution'] + p['suffix']
        tests = [(s['input'], s['output'], 'sample') for s in p['samples']] + [(h['input'], h['output'], 'hidden') for h in p['hidden']]
        bad = []
        for inp, exp, kind in tests:
            rc, so, se = run_py(full, inp)
            if rc != 0 or norm(so) != norm(exp): bad.append('%s test: input=%r expected=%r got=%r %s' % (kind, inp, exp, so, se.strip()[-120:]))
        ok(not bad, '%s: solution fails: %s' % (pid, bad[:1]))
        ok(len(p['samples']) >= 1 and len(p['hidden']) >= 1, '%s: needs 1+ sample and 1+ hidden test' % pid)
        ok(p['difficulty'] in ('Easy', 'Medium', 'Hard'), '%s: bad difficulty' % pid)
        ok(len(p['hints']) == 4 and all(h.strip() for h in p['hints']), '%s: needs 4 hints' % pid)
        ok(all(s['explanation'].strip() for s in p['samples']), '%s: sample explanation missing' % pid)
        stub = p['prefix'] + p['body'] + p['suffix']
        try: compile(stub, pid, 'exec')
        except SyntaxError as e: ok(False, '%s: starting stub does not compile: %s' % (pid, e))
        ok(len(set(h['output'] for h in p['hidden']) | set(s['output'] for s in p['samples'])) >= 2 or len(p['hidden']) <= 2, '%s: all tests have the same answer, a hard-coded print would pass' % pid)
        # the untouched stub must NOT already pass everything
        passed = 0
        for inp, exp, kind in tests:
            rc, so, se = run_py(stub, inp)
            if rc == 0 and norm(so) == norm(exp): passed += 1
        ok(passed < len(tests), '%s: the starting stub already passes all tests' % pid)
        prose_ok(pid, [p['title'], p['input_fmt'], p['output_fmt']] + p['statement'] + p['hints'] + [s['explanation'] for s in p['samples']])
        print('  %s  %-22s %d tests' % ('PASS' if not bad else 'FAIL', pid, len(tests)))

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
        rc, so, se = run_snippet_output(L['predict']['code'])
        ok(rc == 0, '%s: predict code crashes' % L['id'])
        correct = L['predict']['options'][L['predict']['answer']]
        ok(norm(so) == norm(correct), '%s: predict answer %r does not match real output %r' % (L['id'], correct, so))
        ok(len(L['predict']['options']) == len(set(L['predict']['options'])), '%s: duplicate predict options' % L['id'])
        ok(len(L['idea']) >= 2 and L['symbols'], '%s: needs idea paragraphs and a symbols table' % L['id'])
        prose_ok(L['id'], [L['title']] + L['idea'] + [s[1] for s in L['symbols']] + [L['example']['caption'], L['predict']['why']])
        print('  PASS  %s' % L['id'])
    for i, q in enumerate(diag['questions']):
        rc, so, se = run_snippet_output(q['code'])
        ok(rc == 0 and norm(so) == norm(q['options'][q['answer']]), 'diagnostic %d (%s): answer does not match real output %r' % (i, q['lesson'], so))
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
    for q in items:
        ok(0 <= q['answer'] < len(q['options']), '%s: bad answer index' % q['id'])
        ok(q['difficulty'] in ('Easy', 'Medium', 'Hard'), '%s: bad difficulty' % q['id'])
        prose_ok(q['id'], [q['prompt'], q['why']])

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
        ok(len(p['hints']) == 4, '%s: needs 4 hints' % p['id'])

def check_cards(cards):
    print('\n== Flashcards: %d ==' % len(cards))
    for c in cards:
        ok(c['front'].strip() and c['back'].strip(), 'card %s empty' % c['id'])
        if c.get('check'):
            rc, so, se = run_py(c['check']['code'])
            ok(rc == 0 and norm(so) == norm(c['check']['output']), 'card %s: example output mismatch (got %r)' % (c['id'], so))
        prose_ok('card ' + c['id'], [c['front'], c['back']])

def main():
    problems = load('problems.json', [])
    check_problems(problems)
    check_lessons(load('lessons.json', []), load('diagnostic.json', {'questions': []}))
    check_errors(load('errors.json', []))
    for name in ('quiz_bigo.json', 'quiz_prompt.json'):
        d = load(name)
        if d: print('\n== %s: %d questions ==' % (name, len(d))); check_quiz(name, d)
    sql = load('sql_problems.json')
    if sql: check_sql(sql)
    cards = load('flashcards.json')
    if cards: check_cards(cards)
    mock = load('mock_exam.json')
    if mock:
        print('\n== Mock exam: %d sections ==' % len(mock['sections']))
        pids = {p['id'] for p in problems} | {p['id'] for p in (sql or [])}
        qids = {q['id'] for n in ('quiz_bigo.json', 'quiz_prompt.json') for q in (load(n) or [])}
        for s in mock['sections']:
            for i in s['items']: ok(i in pids or i in qids, 'mock exam references unknown item %s' % i)
    print('\n%d checks run, %d failed.' % (checks, len(fails)))
    for f in fails: print('  FAIL:', f)
    print('RESULT:', 'ALL PASSED' if not fails else 'FAILURES FOUND')
    sys.exit(1 if fails else 0)
main()
