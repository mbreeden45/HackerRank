# Flashcards worded "I want to ... so I write ...". Cards with code carry a `check` that verify.py really executes:
# Python cards: code (+ optional stdin) and the exact printed output. SQL cards: a query and its rows, produced by sqlite3.
import sqlite3
from c_sql import TABLES
CARDS = []
_n = {}
def _id(topic):
    k = topic.lower().replace(' ', '-'); _n[k] = _n.get(k, 0) + 1
    return '%s-%02d' % (k, _n[k])
def py(topic, want, so, code, out, stdin=''):
    chk = dict(lang='python', code=code, output=out)
    if stdin: chk['stdin'] = stdin
    CARDS.append(dict(id=_id(topic), topic=topic, front='I want to ' + want + '.', back='so I write ' + so, check=chk))
def tx(topic, want, so):
    CARDS.append(dict(id=_id(topic), topic=topic, front='I want to ' + want + '.', back='so I write ' + so))
_con = sqlite3.connect(':memory:')
for _t in TABLES.values(): _con.executescript(_t['create'])
def sq(want, so, query):
    cur = _con.execute(query)
    cols = [d[0] for d in cur.description]
    rows = [list(r) for r in cur.fetchall()]
    CARDS.append(dict(id=_id('SQL'), topic='SQL', front='I want to ' + want + '.', back='so I write ' + so, check=dict(lang='sql', sql=query, columns=cols, rows=rows)))

B = 'Python basics'
py(B, 'show a value on the screen', '`print(value)`. Several things can go in one print, separated by commas, and print puts a space between them.', 'print("Total:", 5)', 'Total: 5')
py(B, 'read one line that the user typed', '`line = input()`. The answer is always text, even when it looks like a number.', 'line = input()\nprint(line.upper())', 'HI', 'hi\n')
py(B, 'turn typed text into a whole number', '`n = int(input())`. Now n can be used in sums and comparisons.', 'n = int(input())\nprint(n + 1)', '42', '41\n')
py(B, 'cut a line of text into pieces at the spaces', '`parts = line.split()`. The result is a list of text pieces.', 'print("3 4 5".split())', "['3', '4', '5']")
py(B, 'read several whole numbers from one line into a list', '`nums = list(map(int, input().split()))`. Split cuts the line, map int converts each piece, and list collects them.', 'nums = list(map(int, input().split()))\nprint(nums)', '[4, 8, 1]', '4 8 1\n')
py(B, 'test whether a number is even', '`n % 2 == 0`. The % sign gives the remainder after dividing, and an even number leaves remainder 0.', 'print(10 % 2 == 0, 7 % 2 == 0)', 'True False')
py(B, 'do one thing when a test is true and another when it is not', '`if test:` then an indented block, then `else:` and another indented block.', 'n = 5\nif n > 3:\n    print("big")\nelse:\n    print("small")', 'big')
py(B, 'get the last item of a list', '`nums[-1]`, or `nums[len(nums) - 1]`. The last position is one less than the length.', 'nums = [4, 9, 7]\nprint(nums[-1], nums[len(nums) - 1])', '7 7')
py(B, 'get the first three items of a list', '`nums[:3]`. A slice starts at the first position and stops before position 3.', 'nums = [1, 2, 3, 4, 5]\nprint(nums[:3])', '[1, 2, 3]')
py(B, 'visit every position of a list', '`for i in range(len(nums)):` and then use `nums[i]` inside the loop.', 'nums = [5, 6]\nfor i in range(len(nums)):\n    print(i, nums[i])', '0 5\n1 6')
py(B, 'visit every value in a list when I do not need positions', '`for x in nums:`. Here x takes each value in turn.', 'for x in [5, 6]:\n    print(x)', '5\n6')
py(B, 'add up all the numbers in a list', '`total = 0` before the loop, and `total += x` inside it.', 'nums = [1, 2, 3, 4]\ntotal = 0\nfor x in nums:\n    total += x\nprint(total)', '10')
py(B, 'find the biggest number by hand', '`best = nums[0]` first, then inside a loop `if x > best: best = x`.', 'nums = [3, 9, 4]\nbest = nums[0]\nfor x in nums:\n    if x > best:\n        best = x\nprint(best)', '9')
py(B, 'reuse a calculation', '`def name(inputs):` with an indented body that ends in `return result`.', 'def double(n):\n    return n * 2\nprint(double(4))', '8')
py(B, 'add an item to the end of a list', '`items.append(x)`. It changes the list itself.', 'items = [1]\nitems.append(2)\nprint(items)', '[1, 2]')
py(B, 'count how many items a list or text holds', '`len(x)`.', 'print(len([4, 5, 6]), len("hello"))', '3 5')
py(B, 'reverse a piece of text', '`s[::-1]`. A slice with step -1 walks backwards.', 'print("abc"[::-1])', 'cba')
py(B, 'check whether a value is in a list', '`x in nums`. It gives True or False.', 'print(3 in [1, 2, 3], 9 in [1, 2, 3])', 'True False')

D = 'Dictionaries'
py(D, 'count how often each item appears', '`counts[x] = counts.get(x, 0) + 1` inside a loop, with `counts = {}` before it.', 'counts = {}\nfor ch in "aab":\n    counts[ch] = counts.get(ch, 0) + 1\nprint(counts)', "{'a': 2, 'b': 1}")
py(D, 'read a value from a dictionary without crashing when the key is missing', '`d.get(key, fallback)`. The fallback is used when the key is not there.', 'd = {"a": 1}\nprint(d.get("z", 0))', '0')
py(D, 'ask whether a key exists in a dictionary', '`key in d`. It gives True or False.', 'd = {"a": 1}\nprint("a" in d, "z" in d)', 'True False')
py(D, 'spot the first value that appears twice', '`seen = {}`, then for each x: `if x in seen:` answer x, otherwise `seen[x] = True`.', 'seen = {}\nfor x in [3, 1, 3]:\n    if x in seen:\n        print("repeat", x)\n    seen[x] = True', 'repeat 3')
py(D, 'go through a dictionary in a stable order', '`for key in sorted(d):` and then `d[key]` for the value.', 'd = {"b": 2, "a": 1}\nfor key in sorted(d):\n    print(key, d[key])', 'a 1\nb 2')
py(D, 'find the partner that completes a target total', '`need = target - nums[i]` and `if need in seen:`, then store `seen[nums[i]] = i`.', 'nums = [2, 7, 11]\ntarget = 9\nseen = {}\nfor i in range(len(nums)):\n    need = target - nums[i]\n    if need in seen:\n        print(seen[need], i)\n    seen[nums[i]] = i', '0 1')
py(D, 'count the blocks of neighbours that add up to k', '`counts = {0: 1}`, then for each x: `running += x`, `answer += counts.get(running - k, 0)`, `counts[running] = counts.get(running, 0) + 1`.', 'counts = {0: 1}\nrunning = 0\nanswer = 0\nfor x in [1, 1, 1]:\n    running += x\n    answer += counts.get(running - 2, 0)\n    counts[running] = counts.get(running, 0) + 1\nprint(answer)', '2')
py(D, 'check whether two words use the same letters', '`sorted(a) == sorted(b)`, or compare two dictionaries of letter counts.', 'print(sorted("listen") == sorted("silent"))', 'True')

S = 'Sorting'
py(S, 'get the numbers in order without changing the original list', '`sorted(nums)`. The original list is left alone.', 'nums = [3, 1, 2]\nprint(sorted(nums), nums)', '[1, 2, 3] [3, 1, 2]')
py(S, 'get the biggest numbers first', '`sorted(nums, reverse=True)`.', 'print(sorted([3, 1, 2], reverse=True))', '[3, 2, 1]')
py(S, 'sort words by their length', '`sorted(words, key=len)`. The key says what to compare.', 'print(sorted(["ccc", "a", "bb"], key=len))', "['a', 'bb', 'ccc']")
py(S, 'sort by length and break ties alphabetically', '`sorted(words, key=lambda w: (len(w), w))`. The pair is compared left to right.', 'print(sorted(["bb", "a", "aa"], key=lambda w: (len(w), w)))', "['a', 'aa', 'bb']")
py(S, 'get the three biggest values', '`sorted(nums, reverse=True)[:3]`.', 'print(sorted([4, 9, 1, 7], reverse=True)[:3])', '[9, 7, 4]')
py(S, 'find the smallest gap between any two numbers', '`nums = sorted(nums)` and then compare each item with the one before it, `nums[i] - nums[i - 1]`.', 'nums = sorted([8, 3, 15, 5])\nbest = nums[1] - nums[0]\nfor i in range(1, len(nums)):\n    best = min(best, nums[i] - nums[i - 1])\nprint(best)', '2')

T = 'Two pointers'
py(T, 'walk in from both ends of a list', '`left = 0`, `right = len(nums) - 1`, then `while left < right:` and move at least one pointer each round.', 'nums = [1, 2, 3, 4]\nleft = 0\nright = len(nums) - 1\nwhile left < right:\n    print(left, right)\n    left += 1\n    right -= 1', '0 3\n1 2')
py(T, 'find a pair with a target total in a sorted list', 'a total that is too small means `left += 1`, a total that is too big means `right -= 1`.', 'nums = [1, 3, 4, 6, 9]\nleft = 0\nright = 4\nwhile left < right:\n    total = nums[left] + nums[right]\n    if total == 13:\n        print("found", left, right)\n        break\n    elif total < 13:\n        left += 1\n    else:\n        right -= 1', 'found 2 4')
py(T, 'swap two items in a list', '`nums[i], nums[j] = nums[j], nums[i]`.', 'nums = [1, 2, 3]\nnums[0], nums[2] = nums[2], nums[0]\nprint(nums)', '[3, 2, 1]')
py(T, 'remove repeats from a sorted list in one pass', 'a slow pointer for where the next new value goes: when `nums[fast] != nums[slow]`, do `slow += 1` and copy the value there.', 'nums = [1, 1, 2, 2, 3]\nslow = 0\nfor fast in range(1, len(nums)):\n    if nums[fast] != nums[slow]:\n        slow += 1\n        nums[slow] = nums[fast]\nprint(nums[:slow + 1])', '[1, 2, 3]')

W = 'Sliding window'
py(W, 'know how many items are in a window', '`right - left + 1`, because both ends are included.', 'left = 2\nright = 4\nprint(right - left + 1)', '3')
py(W, 'slide a fixed window one step', '`window = window + nums[right] - nums[right - k]`: add the new item, take away the old one.', 'nums = [2, 1, 5, 1]\nk = 2\nwindow = nums[0] + nums[1]\nfor right in range(k, len(nums)):\n    window = window + nums[right] - nums[right - k]\n    print(window)', '6\n6')
py(W, 'shrink a window while it is still big enough', '`while total >= target:` record the size, then `total -= nums[left]` and `left += 1`.', 'nums = [2, 3, 1, 2, 4, 3]\ntarget = 7\nleft = 0\ntotal = 0\nbest = 99\nfor right in range(len(nums)):\n    total += nums[right]\n    while total >= target:\n        best = min(best, right - left + 1)\n        total -= nums[left]\n        left += 1\nprint(best)', '2')
py(W, 'keep a window free of repeated letters', 'a dictionary `last[ch] = right`, and when a letter was last seen inside the window, `left = last[ch] + 1`.', 's = "abca"\nlast = {}\nleft = 0\nfor right in range(len(s)):\n    if s[right] in last and last[s[right]] >= left:\n        left = last[s[right]] + 1\n    last[s[right]] = right\nprint(left)', '1')

G = 'Grids'
py(G, 'read one cell of a grid', '`grid[r][c]`: first the row, then the column, both counting from 0.', 'grid = [[1, 2, 3], [4, 5, 6]]\nprint(grid[1][2])', '6')
py(G, 'get the number of rows and columns', '`len(grid)` for rows and `len(grid[0])` for columns.', 'grid = [[1, 2, 3], [4, 5, 6]]\nprint(len(grid), len(grid[0]))', '2 3')
py(G, 'visit every cell of a grid', '`for r in range(len(grid)):` and inside it `for c in range(len(grid[0])):`.', 'grid = [[1, 2], [3, 4]]\nfor r in range(len(grid)):\n    for c in range(len(grid[0])):\n        print(r, c, grid[r][c])', '0 0 1\n0 1 2\n1 0 3\n1 1 4')
py(G, 'visit the neighbours of a cell safely', '`for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:` and check `0 <= nr < rows and 0 <= nc < cols` before using the cell.', 'r = 0\nc = 0\nfor dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n    nr = r + dr\n    nc = c + dc\n    if 0 <= nr < 2 and 0 <= nc < 2:\n        print(nr, nc)', '1 0\n0 1')
py(G, 'go down one column of a grid', 'keep c fixed and loop `for r in range(len(grid)):` reading `grid[r][c]`.', 'grid = [[1, 2], [3, 4]]\nc = 1\nfor r in range(len(grid)):\n    print(grid[r][c])', '2\n4')

P = 'Strings and parsing'
py(P, 'squeeze extra spaces out of a line', '`" ".join(text.split())`.', 'print(" ".join("  a   b ".split()))', 'a b')
py(P, 'swap one piece of text for another', '`text.replace(old, new)`. It gives back new text.', 'print("a cat".replace("cat", "dog"))', 'a dog')
py(P, 'get the capital first letter of a word', '`word[0].upper()`.', 'print("ada"[0].upper())', 'A')
py(P, 'split a pair such as age=30 into its two parts', '`key, value = pair.split("=")`.', 'key, value = "age=30".split("=")\nprint(key, value)', 'age 30')
py(P, 'add up numbers written with commas', '`for part in text.split(","):` and `total += int(part)`.', 'total = 0\nfor part in "3,5,10".split(","):\n    total += int(part)\nprint(total)', '18')
py(P, 'read a count and then that many lines of text', '`n = int(input())` and then `lines = [input() for _ in range(n)]`.', 'n = int(input())\nlines = [input() for _ in range(n)]\nprint(lines)', "['ab', 'cd']", '2\nab\ncd\n')
py(P, 'test whether a character is a digit', '`ch.isdigit()`. There are also `isalpha()`, `isupper()` and `islower()`.', 'print("7".isdigit(), "a".isdigit())', 'True False')
py(P, 'find the place of a letter in the alphabet', '`ord(ch) - ord("a")`, which gives 0 for a and 25 for z.', 'print(ord("c") - ord("a"))', '2')
py(P, 'shift a letter and wrap round after z', '`(place + shift) % 26`, then turn it back with `chr(... + ord("a"))`.', 'print((24 + 3) % 26)', '1')
py(P, 'build new text one character at a time', '`result = ""` first, and `result += ch` inside the loop.', 'result = ""\nfor ch in "abc":\n    result += ch.upper()\nprint(result)', 'ABC')
py(P, 'test how a line begins', '`line.startswith("ERROR")`. Or split the line and compare its first word.', 'print("ERROR disk".startswith("ERROR"))', 'True')
py(P, 'print the items of a list on one line with spaces', '`print(*items)`. The star spreads the list into separate values.', 'items = [1, 2, 3]\nprint(*items)', '1 2 3')

O = 'Big O'
tx(O, 'describe one loop over n items', 'O(n), said as order n. The work grows in step with n.')
tx(O, 'describe a loop inside a loop over the same n items', 'O(n^2), said as order n squared. The work grows with n times n.')
py(O, 'check quickly whether a value has been seen before', '`x in seen` where `seen` is a dictionary or a set. That is O(1), while `x in a_list` is O(n).', 'seen = {3: True}\nprint(3 in seen)', 'True')
tx(O, 'describe the cost of sorting', 'O(n log n). Python sorted is this fast, so sorting first is usually fine.')
tx(O, 'describe a loop that halves the problem each round', 'O(log n). Halving is the sign of logarithmic growth.')

R = 'Prompt Engineering'
tx(R, 'make a model pull specific facts out of text', 'the task, the exact field names, a rule for missing values, and the output format. For example: Extract the name and order number. If either is missing, use null. Return only JSON.')
tx(R, 'show the model where my input starts and ends', 'the text between triple quotes or tags, and I say that it is the text to work on. This keeps my instructions apart from the data.')
tx(R, 'stop the model from inventing facts', 'a rule: Use only the information in the text. If something is not stated, say not stated.')
tx(R, 'get a clear answer when data is missing', 'a rule: If a value is not stated, use null. Do not guess. Missing is reported as missing.')
tx(R, 'get an answer that a program can parse', 'Return only a JSON object with exactly these keys, and write nothing before or after it. I name each key and its type.')
tx(R, 'check that a text has all the required parts', 'a numbered list of requirements, then: for each item write present or missing and quote the words that show it, then give one final decision.')
tx(R, 'make the model copy the style of answer I want', 'one or two short worked examples in the prompt, including one tricky case, so that the model can follow the pattern.')
tx(R, 'get a summary that suits its reader', 'who the reader is, how long the summary must be, what to keep, what to leave out, and a rule to use only the text.')

sq('list the names and salaries of one department, best paid first', 'SELECT the columns FROM the table WHERE the condition, then ORDER BY salary DESC.', "SELECT name, salary FROM employees WHERE department = 'Sales' ORDER BY salary DESC;")
sq('keep only rows that meet two conditions at once', 'WHERE the first condition AND the second condition.', "SELECT name FROM employees WHERE department = 'Engineering' AND salary < 80000 ORDER BY name;")
sq('match a column against a short list of values', 'WHERE column IN (value1, value2) instead of several ORs.', "SELECT id FROM orders WHERE product IN ('Mouse', 'Keyboard') ORDER BY id;")
sq('find text that ends with a given letter', 'WHERE column LIKE with a percent sign, which stands for any run of characters.', "SELECT name FROM customers WHERE name LIKE '%a' ORDER BY name;")
sq('find rows where a value is missing', 'WHERE column IS NULL. I never write = NULL.', "SELECT name FROM employees WHERE manager_id IS NULL ORDER BY name;")
sq('keep numbers from 100 to 300 including both ends', 'WHERE column BETWEEN 100 AND 300.', "SELECT id FROM orders WHERE amount BETWEEN 100 AND 300 ORDER BY id;")
sq('list each city once', 'SELECT DISTINCT column FROM the table. DISTINCT removes repeated rows.', "SELECT DISTINCT city FROM customers ORDER BY city;")
sq('get the three highest paid people', 'ORDER BY salary DESC and then LIMIT 3, with LIMIT last.', "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3;")
sq('show a calculated column with a name of my choice', 'the calculation followed by AS and the new name.', "SELECT name, salary * 105 / 100 AS new_salary FROM employees ORDER BY id LIMIT 2;")
sq('show each order next to the customer name', 'FROM orders JOIN customers ON orders.customer_id = customers.id, with short nicknames o and c.', "SELECT c.name, o.product FROM orders o JOIN customers c ON o.customer_id = c.id ORDER BY o.id LIMIT 3;")
sq('find customers who have never ordered', 'FROM customers LEFT JOIN orders ON the ids match, then WHERE the order id IS NULL.', "SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL ORDER BY c.name;")
sq('count the rows in each group', 'SELECT the group column and COUNT(*), then GROUP BY the group column.', "SELECT department, COUNT(*) AS headcount FROM employees GROUP BY department ORDER BY department;")
sq('keep only the groups with a big enough count', 'GROUP BY first, then HAVING COUNT(*) with the test. HAVING filters groups, WHERE filters rows.', "SELECT department, COUNT(*) AS headcount FROM employees GROUP BY department HAVING COUNT(*) > 3;")
sq('add up a column for each group, using only some of the rows', 'WHERE to choose rows first, then SUM(column) with GROUP BY.', "SELECT customer_id, SUM(amount) AS total FROM orders WHERE status = 'shipped' GROUP BY customer_id ORDER BY customer_id;")
sq('show each employee next to their manager', 'the employees table twice with two nicknames: FROM employees e JOIN employees m ON e.manager_id = m.id.', "SELECT e.name AS employee, m.name AS manager FROM employees e JOIN employees m ON e.manager_id = m.id ORDER BY e.id LIMIT 3;")
sq('get an average rounded to a whole number', 'ROUND(AVG(column)) with GROUP BY for one average per group.', "SELECT department, ROUND(AVG(salary)) AS average_pay FROM employees GROUP BY department ORDER BY department;")
sq('count every row of a table', 'SELECT COUNT(*) FROM the table.', "SELECT COUNT(*) FROM orders;")
sq('find the biggest value in a column', 'SELECT MAX(column) FROM the table.', "SELECT MAX(salary) FROM employees;")
