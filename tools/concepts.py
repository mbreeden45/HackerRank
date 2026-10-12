"""Shared helpers: which Python ideas ("concepts") a piece of code uses, and how a problem becomes a runnable program.

Concept names
  built-in functions   print()  input()  int()  len()  range()  list()  map()  sum()  sorted() ...
  methods              .append()  .split()  .join()  .get() ...
  plain words          assign augassign arith mod floordiv compare in is and or not if for while break continue
                       def return main_guard index slice list dict tuple listcomp lambda del starred
Anything the detector does not know shows up as a name that no lesson teaches, so verify.py fails it.
"""
import ast, textwrap

def detect(code):
    """Return the set of concepts used by `code` (Python source). Calls to functions defined inside `code` are ignored."""
    tree = ast.parse(textwrap.dedent(code))
    defined = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    out = set()

    def is_guard(n):
        t = n.test
        return (isinstance(t, ast.Compare) and isinstance(t.left, ast.Name) and t.left.id == '__name__')

    class V(ast.NodeVisitor):
        def visit_If(self, n):
            if is_guard(n):
                out.add('main_guard')
                for s in n.body: self.visit(s)
                return
            out.add('if'); self.generic_visit(n)
        def visit_FunctionDef(self, n): out.add('def'); self.generic_visit(n)
        def visit_Return(self, n): out.add('return'); self.generic_visit(n)
        def visit_For(self, n): out.add('for'); self.generic_visit(n)
        def visit_While(self, n): out.add('while'); self.generic_visit(n)
        def visit_Break(self, n): out.add('break')
        def visit_Continue(self, n): out.add('continue')
        def visit_Assign(self, n): out.add('assign'); self.generic_visit(n)
        def visit_AnnAssign(self, n): out.add('assign'); self.generic_visit(n)
        def visit_AugAssign(self, n): out.add('augassign'); self.generic_visit(n)
        def visit_Delete(self, n): out.add('del'); self.generic_visit(n)
        def visit_Lambda(self, n): out.add('lambda'); self.generic_visit(n)
        def visit_ListComp(self, n): out.add('listcomp'); self.generic_visit(n)
        def visit_DictComp(self, n): out.add('dictcomp'); self.generic_visit(n)
        def visit_SetComp(self, n): out.add('setcomp'); self.generic_visit(n)
        def visit_GeneratorExp(self, n): out.add('genexp'); self.generic_visit(n)
        def visit_List(self, n): out.add('list'); self.generic_visit(n)
        def visit_Dict(self, n): out.add('dict'); self.generic_visit(n)
        def visit_Set(self, n): out.add('set'); self.generic_visit(n)
        def visit_Tuple(self, n): out.add('tuple'); self.generic_visit(n)
        def visit_Starred(self, n): out.add('starred'); self.generic_visit(n)
        def visit_JoinedStr(self, n): out.add('fstring'); self.generic_visit(n)
        def visit_IfExp(self, n): out.add('ifexp'); self.generic_visit(n)
        def visit_Try(self, n): out.add('try'); self.generic_visit(n)
        def visit_With(self, n): out.add('with'); self.generic_visit(n)
        def visit_Import(self, n): out.add('import')
        def visit_ImportFrom(self, n): out.add('import')
        def visit_Raise(self, n): out.add('raise'); self.generic_visit(n)
        def visit_Assert(self, n): out.add('assert'); self.generic_visit(n)
        def visit_NamedExpr(self, n): out.add('walrus'); self.generic_visit(n)
        def visit_BoolOp(self, n): out.add('and' if isinstance(n.op, ast.And) else 'or'); self.generic_visit(n)
        def visit_UnaryOp(self, n):
            if isinstance(n.op, ast.Not): out.add('not')
            self.generic_visit(n)
        def visit_BinOp(self, n):
            op = type(n.op)
            out.add({ast.Add: 'arith', ast.Sub: 'arith', ast.Mult: 'arith', ast.Mod: 'mod', ast.FloorDiv: 'floordiv',
                     ast.Div: 'div', ast.Pow: 'pow'}.get(op, 'op:' + op.__name__))
            self.generic_visit(n)
        def visit_Compare(self, n):
            for op in n.ops:
                if isinstance(op, (ast.In, ast.NotIn)): out.add('in')
                elif isinstance(op, (ast.Is, ast.IsNot)): out.add('is')
                else: out.add('compare')
            self.generic_visit(n)
        def visit_Subscript(self, n):
            sl = n.slice
            if isinstance(sl, ast.Slice) or (hasattr(ast, 'ExtSlice') and isinstance(sl, getattr(ast, 'ExtSlice'))):
                out.add('slice')
            else:
                out.add('index')
            self.generic_visit(n)
        def visit_Call(self, n):
            f = n.func
            if isinstance(f, ast.Name):
                if f.id not in defined: out.add(f.id + '()')
            elif isinstance(f, ast.Attribute):
                out.add('.' + f.attr + '()')
            self.generic_visit(n)
    V().visit(tree)
    return out

def program(p, body, test_input):
    """Build the runnable program for one test. Returns (code, stdin).
    preset problems: the test input IS the starting-data lines, so it replaces the locked prefix and nothing is typed.
    stdin problems: the locked prefix and suffix stay and the test input is typed in."""
    if p.get('mode') == 'preset':
        return test_input + body + p['suffix'], ''
    return p['prefix'] + body + p['suffix'], test_input

def written_code(p):
    """The code the learner writes or reads as data: starting-data lines (preset) plus the reference solution."""
    if p.get('mode') == 'preset':
        return p['prefix'] + p['solution']
    return textwrap.dedent(p['solution'])

def locked_code(p):
    """Locked starter code for stdin problems (def line and the reading lines at the bottom). Empty for preset."""
    if p.get('mode') == 'preset':
        return ''
    return p['prefix'] + '    pass\n' + p['suffix']
