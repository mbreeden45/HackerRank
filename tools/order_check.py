#!/usr/bin/env python3
"""Checks that every Python practice problem and every lesson's predict question only needs things taught
in that lesson or an earlier one. 'Taught' means it appears in a lesson's symbols table or a `code span` in its
idea text. Lesson examples are checked too, so an example never shows something it has not explained. The reference solution and the predict code are what get checked, since those are
what the learner has to write or read. Locked lines (the given input-reading code) are not checked."""
import ast, builtins, io, json, keyword, os, re, sys, textwrap, tokenize
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILTINS = set(dir(builtins))
OPS = {'+', '-', '*', '/', '//', '%', '**', '==', '!=', '<', '>', '<=', '>=', '+=', '-=', '*=', '/=', '//=', '%='}

def tokens(text):
    """Python words and operators in a piece of code or a code-like fragment: keywords, builtins, .methods, operators."""
    out = set()
    try:
        prev = None
        for t in tokenize.generate_tokens(io.StringIO(text).readline):
            if t.type == tokenize.NAME:
                if prev == '.': out.add('.' + t.string)
                elif keyword.iskeyword(t.string) or t.string in BUILTINS: out.add(t.string)
            elif t.type == tokenize.OP and t.string in OPS: out.add(t.string)
            elif t.type == tokenize.STRING and t.string.lower().startswith(('f"', "f'")): out.add('f-string')
            prev = t.string
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    return out | shapes(text)

def shapes(text):
    """Things a token list cannot see: indexing, slices, negative positions, comprehensions, tuple unpacking."""
    try: tree = ast.parse(text)
    except SyntaxError: return set()
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Subscript): out.add('[slice]' if isinstance(n.slice, ast.Slice) else '[index]')
        if isinstance(n, ast.Slice) and n.step is not None: out.add('[slice step]')
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub) and isinstance(n.operand, ast.Constant): pass
        if isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)): out.add('comprehension')
        if isinstance(n, ast.Dict): out.add('{dict}')
        if isinstance(n, ast.Set): out.add('{set}')
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Tuple) for t in n.targets): out.add('a, b = unpacking')
        if isinstance(n, ast.For) and isinstance(n.target, ast.Tuple): out.add('a, b = unpacking')
        if isinstance(n, ast.Compare) and any(isinstance(o, (ast.In, ast.NotIn)) for o in n.ops): out.add('x in y (membership test)')
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.UnaryOp) and isinstance(n.slice.op, ast.USub): out.add('[negative index]')
    return out

SQL_WORDS = set('SELECT FROM WHERE AND OR NOT IN BETWEEN LIKE IS NULL ORDER BY ASC DESC LIMIT OFFSET DISTINCT AS JOIN LEFT RIGHT INNER OUTER ON '
    'GROUP HAVING COUNT SUM AVG MIN MAX ROUND CASE WHEN THEN ELSE END UNION COALESCE IFNULL LENGTH UPPER LOWER SUBSTR WITH EXISTS'.split())
def sql_words(text):
    text = re.sub(r"'[^']*'", "''", text)  # ignore words inside quoted text
    words = {w.upper() for w in re.findall(r'[A-Za-z_]+', text)} & SQL_WORDS
    return words | {op for op in ('<>', '!=', '>=', '<=', '%') if op in text}

def taught_by(lesson):
    found = set()
    for row in lesson.get('symbols', []):
        found |= tokens(row[0])
        found |= tokens(re.sub(r'\b(name|x|a|b|n)\b', 'v', row[0]) + '\n')
    for para in lesson.get('idea', []):
        for span in re.findall(r'`([^`]+)`', para): found |= tokens(span)
    return found

def find():
    """Every place something is used before a lesson teaches it, as plain sentences."""
    lessons = json.load(open(os.path.join(ROOT, 'content', 'lessons.json')))
    problems = json.load(open(os.path.join(ROOT, 'content', 'problems.json')))
    pos = {l['id']: i for i, l in enumerate(lessons)}
    first = {}
    for i, l in enumerate(lessons):
        for t in taught_by(l): first.setdefault(t, i)
    bad = []
    def check(where, at, code):
        for t in sorted(tokens(code)):
            if t in ('pass', 'None', 'True', 'False'): continue
            if t not in first: bad.append('%s uses %s, which no lesson teaches' % (where, t))
            elif first[t] > at: bad.append('%s uses %s, first taught later in "%s"' % (where, t, lessons[first[t]]['title']))
    for i, l in enumerate(lessons):
        for k in ('example', 'example2'):
            if l.get(k): check('lesson "%s" %s code' % (l['title'], k), i, l[k]['code'])
        check('lesson "%s" predict question' % l['title'], i, l['predict']['code'])
    for p in problems:
        check('problem %s (lesson "%s")' % (p['id'], lessons[pos[p['lesson']]]['title']), pos[p['lesson']], textwrap.dedent(p['solution']))
    # the placement check asks one question per Basics lesson, so each question may only use what that lesson and earlier ones teach
    for q in json.load(open(os.path.join(ROOT, 'content', 'diagnostic.json')))['questions']:
        check('placement question for "%s"' % lessons[pos[q['lesson']]]['title'], pos[q['lesson']], q['code'])
    # flashcards and the Big O quiz are reviewed across the whole course: their code may only use things some lesson teaches
    end = len(lessons) - 1
    for c in json.load(open(os.path.join(ROOT, 'content', 'flashcards.json'))):
        if c.get('check', {}).get('lang') == 'python': check('flashcard %s' % c['id'], end, c['check']['code'])
    for q in json.load(open(os.path.join(ROOT, 'content', 'quiz_bigo.json'))):
        if q.get('snippet'): check('Big O question %s' % q['id'], end, q['snippet'])
    # SQL track: each problem's solution may only use keywords that its lesson or an earlier SQL lesson shows
    sql_lessons = [l for l in json.load(open(os.path.join(ROOT, 'content', 'lessons_x.json'))) if l['id'].startswith('sql_')]
    spos = {l['id']: i for i, l in enumerate(sql_lessons)}
    sql_first = {}
    for i, l in enumerate(sql_lessons):
        for b in l['blocks']:
            # code blocks and tables count in full; in prose only capitalised SQL words count, so English 'in' or 'on' does not
            code = b.get('text', '') if b.get('t') == 'sql' else ' '.join(re.findall(r'`([^`]+)`', b.get('text', '')))
            code += ' ' + ' '.join(str(c) for r in b.get('rows', []) for c in r)
            prose = ' '.join(w for w in re.findall(r'[A-Z]+', b.get('text', '') + ' ' + b.get('label', '')))
            for w in sql_words(code) | sql_words(prose): sql_first.setdefault(w, i)
    for p in json.load(open(os.path.join(ROOT, 'content', 'sql_problems.json'))):
        at = spos[p['lesson']]
        for w in sorted(sql_words(p['solution'])):
            if w not in sql_first: bad.append('SQL problem %s uses %s, which no SQL lesson teaches' % (p['id'], w))
            elif sql_first[w] > at: bad.append('SQL problem %s uses %s, first taught later in "%s"' % (p['id'], w, sql_lessons[sql_first[w]]['title']))
    return bad

def main():
    bad = find()
    for b in bad: print('  ORDER:', b)
    print('%d things used before they are taught.' % len(bad))
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())
