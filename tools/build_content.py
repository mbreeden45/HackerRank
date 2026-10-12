#!/usr/bin/env python3
"""Builds content/*.json from the tools/c_*.py files. Hidden-test outputs come from running the reference solutions."""
import json, os, subprocess, sys, tempfile
from concepts import detect, program, written_code
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
    here = os.path.dirname(os.path.abspath(__file__))
    def opt(name):
        return importlib.import_module(name) if os.path.exists(os.path.join(here, name + '.py')) else None
    L1 = importlib.import_module('c_lessons')
    P1 = importlib.import_module('c_problems1')
    out = os.path.join(ROOT, 'content'); os.makedirs(out, exist_ok=True)
    problems = list(P1.PROBLEMS)
    lessons = list(L1.LESSONS)
    L2 = opt('c_lessons2')
    if L2: lessons += L2.LESSONS
    for m in ('c_problems2', 'c_problems3'):
        mod = opt(m)
        if mod: problems += mod.PROBLEMS
    ids = [p['id'] for p in problems]
    assert len(ids) == len(set(ids)), 'duplicate problem ids: %s' % sorted({i for i in ids if ids.count(i) > 1})
    for p in problems:
        p.setdefault('mode', 'stdin')
        p['concepts'] = sorted(detect(written_code(p)))
        p['hidden'] = []
        for inp in p.pop('hidden_inputs'):
            code, stdin = program(p, p['solution'], inp)
            rc, so, se = run_py(code, stdin)
            if rc != 0: sys.exit('Reference solution crashed for %s on %r: %s' % (p['id'], inp, se))
            p['hidden'].append(dict(input=inp, output=so.rstrip('\n')))
    json.dump(lessons, open(os.path.join(out, 'lessons.json'), 'w'), indent=1)
    json.dump(dict(questions=L1.DIAGNOSTIC), open(os.path.join(out, 'diagnostic.json'), 'w'), indent=1)
    json.dump(L1.ERRORS, open(os.path.join(out, 'errors.json'), 'w'), indent=1)
    json.dump(problems, open(os.path.join(out, 'problems.json'), 'w'), indent=1)
    extra = []
    study = []
    for m in ('c_prompt', 'c_sql'):
        mod = opt(m)
        if mod and hasattr(mod, 'STUDY'): study += mod.STUDY
    if study:
        json.dump(study, open(os.path.join(out, 'lessons_x.json'), 'w'), indent=1); extra.append('lessons_x.json')
    for m in ('c_quiz2', 'c_prompt', 'c_sql', 'c_mock'):
        mod = opt(m)
        if mod:
            for name, data in mod.FILES.items():
                json.dump(data, open(os.path.join(out, name), 'w'), indent=1); extra.append(name)
    cards = opt('c_cards3')
    if cards:
        json.dump(cards.CARDS, open(os.path.join(out, 'flashcards.json'), 'w'), indent=1); extra.append('flashcards.json')
    print('Built %d lessons, %d problems, %d diagnostic questions, %d error patterns%s.' % (len(lessons), len(problems), len(L1.DIAGNOSTIC), len(L1.ERRORS), (', plus ' + ', '.join(extra)) if extra else ''))
if __name__ == '__main__':
    main()
