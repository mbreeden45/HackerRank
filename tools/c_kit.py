# Shared helper for authoring function-style problems. Each parameter has a type that decides
# how it is written as input text and how the locked "main" block reads it.
STUB = "    # Write your code here\n    pass\n"

def _enc(t, v):
    if t == 'int': return '%d\n' % v
    if t == 'str': return v + '\n'
    if t == 'ints': return '%d\n%s\n' % (len(v), ' '.join(str(x) for x in v))
    if t == 'words': return ' '.join(v) + '\n'
    if t == 'lines': return '%d\n%s' % (len(v), ''.join(x + '\n' for x in v))
    if t == 'grid': return '%d %d\n%s' % (len(v), len(v[0]), ''.join(' '.join(str(x) for x in row) + '\n' for row in v))
    raise ValueError(t)

def _read(name, t):
    if t == 'int': return '    %s = int(input())\n' % name
    if t == 'str': return '    %s = input()\n' % name
    if t == 'ints': return '    count = int(input())\n    %s = list(map(int, input().split()))\n' % name
    if t == 'words': return '    %s = input().split()\n' % name
    if t == 'lines': return '    count = int(input())\n    %s = [input() for _ in range(count)]\n' % name
    if t == 'grid': return '    rows, cols = map(int, input().split())\n    %s = [list(map(int, input().split())) for _ in range(rows)]\n' % name
    raise ValueError(t)

def _fmt(name, t):
    if t == 'int': return 'A line holding the whole number `%s`.' % name
    if t == 'str': return 'A line holding the text `%s`.' % name
    if t == 'ints': return 'A line with how many numbers there are, then a line with the whole numbers for `%s`, separated by spaces.' % name
    if t == 'words': return 'A line of words separated by spaces, which become the list `%s`.' % name
    if t == 'lines': return 'A line with how many lines follow, then that many lines of text, which become the list `%s`.' % name
    if t == 'grid': return 'A line with the number of rows and columns, then one line per row with the numbers separated by spaces, which become the grid `%s`.' % name
    raise ValueError(t)

SUFFIX_TAIL = (
 '    result = solve(%s)\n'
 '    if isinstance(result, list):\n'
 '        if result and isinstance(result[0], list):\n'
 '            for row in result:\n'
 '                print(*row)\n'
 '        else:\n'
 '            print(*result)\n'
 '    else:\n'
 '        print(result)\n')

class Kit:
    def __init__(self):
        self.PROBLEMS = []

    def fp(self, lesson, id, title, diff, statement, params, outfmt, samples, hidden, solution, hints, constraints=None):
        """params: list of (name, type). samples: list of (args, output, explanation). hidden: list of args."""
        assert len(hints) == 4, id
        names = [n for n, _ in params]
        prefix = 'def solve(%s):\n' % ', '.join(names)
        suffix = '\nif __name__ == "__main__":\n' + ''.join(_read(n, t) for n, t in params) + SUFFIX_TAIL % ', '.join(names)
        infmt = ' '.join(_fmt(n, t) for n, t in params)
        enc = lambda args: ''.join(_enc(t, v) for (n, t), v in zip(params, args))
        self.PROBLEMS.append(dict(id=id, lesson=lesson, title=title, difficulty=diff, statement=statement, input_fmt=infmt,
            output_fmt=outfmt, constraints=constraints,
            samples=[dict(input=enc(a), output=o, explanation=e) for a, o, e in samples],
            hidden_inputs=[enc(a) for a in hidden], prefix=prefix, body=STUB, suffix=suffix, solution=solution, hints=hints))
