#!/usr/bin/env python3
"""Compares the hardest reference solutions with slow, obviously-correct versions on random inputs.
This guards against a wrong solution silently producing wrong hidden-test answers.
Usage: python3 tools/brute_check.py"""
import json, os, random, itertools
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = {p['id']: p for p in json.load(open(os.path.join(ROOT, 'content/problems.json')))}
def fn(pid):
    ns = {'__name__': 'x'}
    exec(P[pid]['prefix'] + P[pid]['solution'], ns)
    return ns['solve']
random.seed(7)
rl = lambda n, lo, hi: [random.randint(lo, hi) for _ in range(n)]
def subs(nums): return [(i, j) for i in range(len(nums)) for j in range(i, len(nums))]
def b_subarray(nums, k): return sum(1 for i, j in subs(nums) if sum(nums[i:j + 1]) == k)
def b_three(nums): return len({tuple(sorted(t)) for t in itertools.combinations(nums, 3) if sum(t) == 0})
def b_container(h): return max(min(h[i], h[j]) * (j - i) for i in range(len(h)) for j in range(i + 1, len(h)))
def b_intervals(lines):
    sp = sorted([list(map(int, l.split())) for l in lines]); g = []
    for a, b in sp:
        if g and a <= g[-1][1]: g[-1][1] = max(g[-1][1], b)
        else: g.append([a, b])
    return len(g)
def b_minlen(nums, t):
    best = 0
    for i, j in subs(nums):
        if sum(nums[i:j + 1]) >= t and (best == 0 or j - i + 1 < best): best = j - i + 1
    return best
def b_unique(s): return max(j - i + 1 for i, j in subs(s) if len(set(s[i:j + 1])) == j - i + 1)
def b_flip(nums, k): return max([j - i + 1 for i, j in subs(nums) if nums[i:j + 1].count(0) <= k] or [0])
def b_distinct(nums, k): return max(len(set(nums[i:i + k])) for i in range(len(nums) - k + 1))
def b_atmost(s, k): return max([j - i + 1 for i, j in subs(s) if len(set(s[i:j + 1])) <= k] or [0])
def b_islands(g):
    R, C = len(g), len(g[0]); seen = set(); n = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] and (r, c) not in seen:
                n += 1; todo = [(r, c)]
                while todo:
                    a, b = todo.pop()
                    if (a, b) in seen or not (0 <= a < R and 0 <= b < C) or not g[a][b]: continue
                    seen.add((a, b)); todo += [(a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)]
    return n
def b_neigh(g):
    R, C = len(g), len(g[0]); n = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] and any(0 <= r + a < R and 0 <= c + b < C and g[r + a][c + b] for a, b in [(1, 0), (-1, 0), (0, 1), (0, -1)]): n += 1
    return n
def b_pal(s):
    t = [ch.lower() for ch in s if ch.isalnum()]; return t == t[::-1]
def b_comp(s): return ''.join(k + str(len(list(g))) for k, g in itertools.groupby(s))
def b_caesar(t, k): return ''.join(ch if ch == ' ' else chr((ord(ch) - 97 + k) % 26 + 97) for ch in t)
def b_dups(nums): return sorted(set(nums))
def b_merge(a, b): return sorted(a + b)
def b_anagram(a, b): return sorted(a) == sorted(b)
def gen_grid(): R, C = random.randint(1, 5), random.randint(1, 5); return [[random.randint(0, 1) for _ in range(C)] for _ in range(R)]
T = 400; bad = 0
def chk(pid, gen, brute):
    global bad
    f = fn(pid)
    for _ in range(T):
        a = gen()
        got = f(*[x[:] if isinstance(x, list) else x for x in a])
        want = brute(*a)
        if got != want:
            bad += 1; print('MISMATCH', pid, a, 'solution', got, 'brute', want); return
    print('ok  ', pid)
chk('hm_subarray_sum', lambda: (rl(random.randint(1, 8), -3, 3), random.randint(-3, 3)), b_subarray)
chk('tp_three_sum', lambda: (rl(random.randint(3, 9), -4, 4),), b_three)
chk('tp_container', lambda: (rl(random.randint(2, 8), 1, 9),), b_container)
chk('sort_intervals', lambda: ([f'{a} {a + random.randint(0, 5)}' for a in rl(random.randint(1, 6), 0, 12)],), b_intervals)
chk('sw_min_len_sum', lambda: (rl(random.randint(1, 8), 1, 5), random.randint(1, 20)), b_minlen)
chk('sw_longest_unique', lambda: (''.join(random.choice('abcd') for _ in range(random.randint(1, 10))),), b_unique)
chk('sw_ones_flip', lambda: (rl(random.randint(1, 10), 0, 1), random.randint(0, 3)), b_flip)
def gd():
    n = random.randint(1, 8); return rl(n, 1, 4), random.randint(1, n)
chk('sw_distinct_in_window', gd, b_distinct)
chk('sw_at_most_k_distinct', lambda: (''.join(random.choice('abcd') for _ in range(random.randint(1, 10))), random.randint(1, 4)), b_atmost)
chk('gr_islands', lambda: (gen_grid(),), b_islands)
chk('gr_neighbors', lambda: (gen_grid(),), b_neigh)
chk('tp_palindrome_clean', lambda: (''.join(random.choice('aAb, 1') for _ in range(random.randint(1, 8))),), b_pal)
chk('ch_compress', lambda: (''.join(random.choice('ab') for _ in range(random.randint(1, 10))),), b_comp)
chk('ch_caesar', lambda: (''.join(random.choice('abxyz ') for _ in range(random.randint(1, 8))), random.randint(0, 25)), b_caesar)
chk('tp_remove_dups', lambda: (sorted(rl(random.randint(1, 8), 0, 4)),), b_dups)
chk('tp_merge_sorted', lambda: (sorted(rl(random.randint(0, 5), 0, 9)), sorted(rl(random.randint(0, 5), 0, 9))), b_merge)
chk('hm_anagram', lambda: (''.join(random.choice('ab') for _ in range(random.randint(1, 4))), ''.join(random.choice('ab') for _ in range(random.randint(1, 4)))), b_anagram)
print('RESULT:', 'ALL AGREE' if not bad else '%d MISMATCHES' % bad)
raise SystemExit(1 if bad else 0)
