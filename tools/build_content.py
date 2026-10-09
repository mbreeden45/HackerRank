#!/usr/bin/env python3
"""Builds content/*.json from the tools/c_*.py files. Hidden-test outputs come from running the reference solutions."""
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_py(code, stdin, timeout=10):
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as f:
        f.write(code); path = f.name
    try:
        p = subprocess.run([sys.executable, path], input=stdin, capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    return p.returncode, p.stdout, p.stderr

def main():
    import importlib
    mods = ['c_lessons', 'c_problems1'] + [m for m in ['c_problems2', 'c_quiz2', 'c_cards3'] if os.path.exists(os.path.join(os.path.dirname(__file__), m + '.py'))]
    M = {m: importlib.import_module(m) for m in mods}
    out = os.path.join(ROOT, 'content'); os.makedirs(out, exist_ok=True)
    problems = list(M['c_problems1'].PROBLEMS)
    if 'c_problems2' in M: problems += M['c_problems2'].PROBLEMS
    for p in problems:
        full = p['prefix'] + p['solution'] + p['suffix']
        p['hidden'] = []
        for inp in p.pop('hidden_inputs'):
            rc, so, se = run_py(full, inp)
            if rc != 0: sys.exit('Reference solution crashed for %s on %r: %s' % (p['id'], inp, se))
            p['hidden'].append(dict(input=inp, output=so.rstrip('\n')))
    L = M['c_lessons']
    json.dump(L.LESSONS, open(os.path.join(out, 'lessons.json'), 'w'), indent=1)
    json.dump(dict(questions=L.DIAGNOSTIC), open(os.path.join(out, 'diagnostic.json'), 'w'), indent=1)
    json.dump(L.ERRORS, open(os.path.join(out, 'errors.json'), 'w'), indent=1)
    json.dump(problems, open(os.path.join(out, 'problems.json'), 'w'), indent=1)
    if 'c_quiz2' in M:
        for name, data in M['c_quiz2'].FILES.items():
            json.dump(data, open(os.path.join(out, name), 'w'), indent=1)
    if 'c_cards3' in M:
        json.dump(M['c_cards3'].CARDS, open(os.path.join(out, 'flashcards.json'), 'w'), indent=1)
    print('Built %d lessons, %d problems, %d diagnostic questions, %d error patterns.' % (len(L.LESSONS), len(problems), len(L.DIAGNOSTIC), len(L.ERRORS)))
if __name__ == '__main__':
    main()
