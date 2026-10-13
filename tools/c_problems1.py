# Phase 1 practice problems. Expected outputs for SAMPLES are written by hand.
# Hidden test outputs are produced by running the reference solution (see build_content.py).
PROBLEMS = []
STUB = "    # Write your code here\n    pass\n"
LIST_FMT = "The first line holds `n`, the number of items. The second line holds `n` whole numbers separated by spaces."

def add(lesson, id, title, diff, statement, infmt, outfmt, samples, hidden, prefix, body, suffix, solution, hints, constraints=None):
    assert len(hints) == 4, id
    PROBLEMS.append(dict(id=id, lesson=lesson, title=title, difficulty=diff, statement=statement, input_fmt=infmt,
        output_fmt=outfmt, constraints=constraints, samples=[dict(input=a, output=b, explanation=c) for a, b, c in samples],
        hidden_inputs=hidden, prefix=prefix, body=body, suffix=suffix, solution=solution, hints=hints))

def script(lesson, id, title, diff, statement, infmt, outfmt, reads, samples, hidden, solution, hints, constraints=None):
    add(lesson, id, title, diff, statement, infmt, outfmt, samples, hidden, reads, "# Write your code here\n", "", solution, hints, constraints)

LIST_SUFFIX = '\nif __name__ == "__main__":\n    n = int(input())\n    nums = list(map(int, input().split()))\n    print(solve(nums))\n'
def listfn(lesson, id, title, diff, statement, outfmt, samples, hidden, solution, hints, constraints=None, extra=None):
    add(lesson, id, title, diff, statement, LIST_FMT, outfmt, samples, hidden, "def solve(nums):\n", STUB, LIST_SUFFIX, solution, hints, constraints)

# ---------- 1 print ----------
script("print", "print_two_lines", "Two lines", "Easy",
 ["Print the word `Hello` on the first line, and the number `42` on the second line."],
 "There is no input.", "Two lines: `Hello`, then `42`.", "",
 [("", "Hello\n42", "The first print shows the word Hello. The second print shows 42, with no quote marks because it is a number.")], [""],
 'print("Hello")\nprint(42)\n',
 ["Each print makes its own line.", "You need two print lines. Words need quote marks, numbers do not.", "Line one: print the text Hello. Line two: print the number 42.", "print(\"Hello\") on one line, then print(42) on the next."])
script("print", "print_greeting", "A greeting", "Easy",
 ["The name has already been read for you and stored in a variable called `name`. A variable is a name that holds a value.", "Print `Hi,` followed by a space and then the name, all on one line."],
 "One line holding a name.", "One line: `Hi,` then a space, then the name.", "name = input()\n",
 [("Ana\n", "Hi, Ana", "The text Hi, and the name Ana are printed with one space between them.")], ["Bo\n", "Maria\n", "Sam Lee\n"],
 'print("Hi,", name)\n',
 ["print can show two things at once.", "Put a comma between two things inside the print brackets. The comma adds the space for you.", "Print the text \"Hi,\" and the variable name together.", "print(\"Hi,\", name)."])
script("print", "print_pair", "Two numbers on one line", "Easy",
 ["Two whole numbers have been read for you, stored in `a` and `b`. Print them on one line with a space between."],
 "Two lines, each holding one whole number.", "One line with the two numbers separated by a space.", "a = int(input())\nb = int(input())\n",
 [("3\n8\n", "3 8", "a is 3 and b is 8, so the line shows 3 8.")], ["10\n-4\n", "0\n0\n", "123\n456\n"],
 'print(a, b)\n',
 ["You can give print more than one thing.", "Write both names inside one print, separated by a comma.", "One print line that holds a and b.", "print(a, b)."])

# ---------- 2 variables ----------
script("variables", "var_add", "Add two numbers", "Easy",
 ["Two whole numbers are stored in `a` and `b`. Print their sum, meaning `a` plus `b`."],
 "Two lines, each one whole number.", "One number: the sum.", "a = int(input())\nb = int(input())\n",
 [("2\n5\n", "7", "2 plus 5 is 7.")], ["-3\n3\n", "100\n250\n", "0\n9\n"],
 'print(a + b)\n',
 ["The + sign adds numbers.", "You can do the adding inside the print brackets.", "Print the answer of a plus b.", "print(a + b)."])
script("variables", "var_rectangle", "Area and perimeter", "Easy",
 ["The `width` and `height` of a rectangle are stored for you. The area is width times height. The perimeter is the total length around the outside: 2 times (width plus height).", "Print the area on the first line and the perimeter on the second line. The symbol `*` means times."],
 "Two lines: the width, then the height. Both are whole numbers.", "Two lines: the area, then the perimeter.", "width = int(input())\nheight = int(input())\n",
 [("3\n4\n", "12\n14", "Area is 3 * 4 = 12. Perimeter is 2 * (3 + 4) = 14.")], ["1\n1\n", "10\n2\n", "7\n9\n"],
 'area = width * height\nperimeter = 2 * (width + height)\nprint(area)\nprint(perimeter)\n',
 ["Work out each answer and store it in a name first.", "Make a name called area, and a name called perimeter. Then print each.", "area is width times height. perimeter is 2 times the sum of width and height. Print area, then print perimeter.", "area = width * height; perimeter = 2 * (width + height); print(area); print(perimeter)."])
script("variables", "var_swap", "Swap two values", "Medium",
 ["The names `a` and `b` hold two numbers. Make `a` hold what `b` held, and `b` hold what `a` held. Then print `a` on the first line and `b` on the second.", "Warning: if you write `a = b` first, the old value of `a` is lost. A third name can hold it safely for a moment."],
 "Two lines, each one whole number.", "Two lines: the new a, then the new b.", "a = int(input())\nb = int(input())\n",
 [("3\n8\n", "8\n3", "After the swap, a holds 8 and b holds 3.")], ["1\n2\n", "-5\n5\n", "7\n7\n"],
 'temp = a\na = b\nb = temp\nprint(a)\nprint(b)\n',
 ["Think of two cups of juice that you want to swap. You need a third empty cup.", "Store the old a in a new name before you change a.", "1. Save a in a new name called temp. 2. Put b into a. 3. Put temp into b. 4. Print a and b.", "temp = a; a = b; b = temp; print(a); print(b)."])

# ---------- 3 equals ----------
script("equals", "eq_same", "Are they equal", "Easy",
 ["Two numbers are stored in `a` and `b`. Print `True` if they are equal, otherwise print `False`.", "Hint on symbols: `==` asks whether two things are equal and gives back `True` or `False`."],
 "Two lines, each one whole number.", "`True` or `False`.", "a = int(input())\nb = int(input())\n",
 [("4\n4\n", "True", "4 is equal to 4."), ("4\n9\n", "False", "4 is not equal to 9.")], ["0\n0\n", "-1\n1\n", "50\n50\n"],
 'print(a == b)\n',
 ["The answer to print is already a True or False answer.", "Ask the question a == b inside the print.", "Print the answer to the question: is a equal to b.", "print(a == b)."])
script("equals", "eq_three", "Three questions", "Easy",
 ["Two numbers are stored in `a` and `b`. Print three lines, each the answer to one question:", "Line 1: is `a` equal to `b`. Line 2: is `a` less than `b`. Line 3: is `a` greater than `b`.", "The symbols are `==`, `<` and `>`."],
 "Two lines, each one whole number.", "Three lines, each `True` or `False`.", "a = int(input())\nb = int(input())\n",
 [("2\n5\n", "False\nTrue\nFalse", "2 is not equal to 5. 2 is less than 5. 2 is not greater than 5.")], ["5\n5\n", "9\n1\n", "-2\n-3\n"],
 'print(a == b)\nprint(a < b)\nprint(a > b)\n',
 ["Each line is its own print.", "Three print lines. Each holds one question.", "Print a == b. Print a < b. Print a > b.", "print(a == b); print(a < b); print(a > b)."])
script("equals", "eq_password", "Password check", "Medium",
 ["A word is stored in `word`. Print `True` if it is exactly `builder` (all small letters), otherwise `False`.", "Capital letters count as different letters. `Builder` is not the same as `builder`."],
 "One line holding a word.", "`True` or `False`.", "word = input()\n",
 [("builder\n", "True", "Exactly the same."), ("Builder\n", "False", "The capital B makes it different.")], ["build\n", "BUILDER\n", "builder\n"],
 'print(word == "builder")\n',
 ["The word you compare against needs quote marks.", "Compare the variable word with the text \"builder\" using two equals signs.", "Print the answer to: is word equal to the text builder.", "print(word == \"builder\")."])

# ---------- 4 remainder ----------
script("remainder", "mod_even", "Is it even", "Easy",
 ["A whole number is stored in `n`. Print `True` if it is even and `False` if it is odd.", "An even number has remainder 0 when divided by 2. The symbol `%` gives the remainder."],
 "One line holding a whole number.", "`True` or `False`.", "n = int(input())\n",
 [("10\n", "True", "10 % 2 is 0."), ("7\n", "False", "7 % 2 is 1.")], ["0\n", "1\n", "-4\n", "99\n"],
 'print(n % 2 == 0)\n',
 ["Use % with the number 2.", "Ask whether the remainder after dividing by 2 equals 0.", "Print the answer to: is n % 2 equal to 0.", "print(n % 2 == 0)."])
script("remainder", "mod_digits", "Split off the last digit", "Easy",
 ["A non-negative whole number is stored in `n`. Print its last digit on the first line. On the second line print the number with its last digit removed (print `0` if nothing is left).", "Hint: `n % 10` is the last digit. `n // 10` divides by 10 and drops the decimal part."],
 "One line holding a whole number.", "Two lines: the last digit, then the number without it.", "n = int(input())\n",
 [("472\n", "2\n47", "472 % 10 is 2. 472 // 10 is 47.")], ["5\n", "100\n", "90817\n"],
 'print(n % 10)\nprint(n // 10)\n',
 ["Dividing by 10 and looking at the remainder isolates the last digit.", "Use % 10 for the first line and // 10 for the second.", "Print n % 10. Then print n // 10.", "print(n % 10); print(n // 10)."])
script("remainder", "mod_weeks", "Days to weeks", "Medium",
 ["The number of days is stored in `days`. Print the number of whole weeks on the first line and the days left over on the second line. A week has 7 days."],
 "One line holding a whole number of days.", "Two lines: whole weeks, then leftover days.", "days = int(input())\n",
 [("17\n", "2\n3", "17 days is 2 whole weeks (14 days) and 3 days left over.")], ["7\n", "6\n", "0\n", "100\n"],
 'print(days // 7)\nprint(days % 7)\n',
 ["Whole weeks is a division with the decimal part dropped. Leftover days is a remainder.", "Use // 7 for weeks and % 7 for leftover days.", "Print days // 7. Then print days % 7.", "print(days // 7); print(days % 7)."])

# ---------- 5 if/else ----------
script("ifelse", "if_evenodd", "Even or odd", "Easy",
 ["A whole number is stored in `n`. Print the word `even` if it is even, otherwise print `odd`."],
 "One line holding a whole number.", "`even` or `odd`.", "n = int(input())\n",
 [("8\n", "even", "8 % 2 is 0."), ("5\n", "odd", "5 % 2 is 1.")], ["0\n", "1\n", "22\n", "-3\n"],
 'if n % 2 == 0:\n    print("even")\nelse:\n    print("odd")\n',
 ["You need a choice with two outcomes.", "Use if with the question n % 2 == 0, and else for the other outcome.", "If the remainder after dividing by 2 is 0, print even. Otherwise print odd.", "if n % 2 == 0: print(\"even\"); else: print(\"odd\"). Remember the colons and the indents."])
script("ifelse", "if_sign", "Positive, negative or zero", "Easy",
 ["A whole number is stored in `n`. Print `positive` if it is above zero, `negative` if it is below zero, and `zero` if it is zero."],
 "One line holding a whole number.", "`positive`, `negative` or `zero`.", "n = int(input())\n",
 [("5\n", "positive", "5 is above zero."), ("-2\n", "negative", "-2 is below zero.")], ["0\n", "1\n", "-100\n"],
 'if n > 0:\n    print("positive")\nelif n < 0:\n    print("negative")\nelse:\n    print("zero")\n',
 ["There are three outcomes, so you need more than if and else.", "Use if, then elif, then else.", "If n is above 0 print positive. Else if n is below 0 print negative. Otherwise print zero.", "if n > 0: ...; elif n < 0: ...; else: ..."])
script("ifelse", "if_fizz", "Fizz and Buzz", "Medium",
 ["A whole number is stored in `n`. Print:", "`FizzBuzz` if n divides exactly by both 3 and 5; `Fizz` if it divides exactly by 3 only; `Buzz` if it divides exactly by 5 only; otherwise the number itself.", "Hint: divides exactly by 3 means `n % 3 == 0`. The word `and` is True only when both sides are True."],
 "One line holding a whole number.", "One line.", "n = int(input())\n",
 [("15\n", "FizzBuzz", "15 divides by 3 and by 5."), ("9\n", "Fizz", "9 divides by 3 only."), ("7\n", "7", "7 divides by neither.")], ["10\n", "30\n", "1\n", "2\n", "27\n"],
 'if n % 3 == 0 and n % 5 == 0:\n    print("FizzBuzz")\nelif n % 3 == 0:\n    print("Fizz")\nelif n % 5 == 0:\n    print("Buzz")\nelse:\n    print(n)\n',
 ["The order of your questions matters. Which question should be asked first.", "Ask the both-3-and-5 question first. If you ask about 3 first, 15 would print Fizz.", "1. If divisible by 3 and 5, print FizzBuzz. 2. Else if divisible by 3, print Fizz. 3. Else if divisible by 5, print Buzz. 4. Else print n.", "if n % 3 == 0 and n % 5 == 0 ... elif n % 3 == 0 ... elif n % 5 == 0 ... else print(n)."])

# ---------- 6 lists ----------
script("lists", "list_build", "Build a list", "Easy",
 ["Three numbers are stored in `a`, `b` and `c`. Make a list holding them in that order, add the number `100` to the end, then print the list.", "A list prints with square brackets, for example `[1, 2, 3, 100]`."],
 "Three lines, each one whole number.", "One line: the list.", "a = int(input())\nb = int(input())\nc = int(input())\n",
 [("1\n2\n3\n", "[1, 2, 3, 100]", "The list starts as [1, 2, 3] and 100 is added at the end.")], ["0\n0\n0\n", "-1\n5\n9\n"],
 'items = [a, b, c]\nitems.append(100)\nprint(items)\n',
 ["First make the list, then add to it.", "Write square brackets with a, b and c inside, store it in a name, then use .append.", "1. Make a list called items from a, b, c. 2. Append 100. 3. Print items.", "items = [a, b, c]; items.append(100); print(items)."])
script("lists", "list_grow", "Add two more", "Easy",
 ["A list is stored in `nums`, and a whole number is stored in `x`. Add `x` to the end of the list two times, then print the list."],
 "Line 1: the numbers of the list, separated by spaces. Line 2: the number x.", "One line: the list.",
 "nums = list(map(int, input().split()))\nx = int(input())\n",
 [("4 5\n9\n", "[4, 5, 9, 9]", "9 is added twice at the end.")], ["1\n2\n", "1 2 3 4\n0\n", "-1 -2\n-3\n"],
 'nums.append(x)\nnums.append(x)\nprint(nums)\n',
 [".append adds one item at a time.", "You need two append lines.", "Append x. Append x again. Print nums.", "nums.append(x); nums.append(x); print(nums)."])
script("lists", "list_stats", "Sum, biggest, smallest", "Medium",
 ["A list is stored in `nums`. Three tools help here: `sum(nums)` adds up all the numbers, `max(nums)` gives the biggest number, and `min(nums)` gives the smallest.", "Print the sum, then the biggest, then the smallest, each on its own line."],
 "One line holding the numbers of the list, separated by spaces.", "Three lines.", "nums = list(map(int, input().split()))\n",
 [("3 9 2\n", "14\n9\n2", "3 + 9 + 2 is 14. The biggest is 9. The smallest is 2.")], ["5\n", "-1 -5 -3\n", "10 20 30 40\n"],
 'print(sum(nums))\nprint(max(nums))\nprint(min(nums))\n',
 ["The three tools are given to you in the statement.", "Three prints, one for each tool.", "Print sum of nums. Print max of nums. Print min of nums.", "print(sum(nums)); print(max(nums)); print(min(nums))."])

# ---------- 6b functions (comes before indexing, the first lesson whose problems need return) ----------
def intfn(lesson, id, title, diff, statement, sample, hidden, solution, hints, sig="def solve(n):\n", reads="    n = int(input())\n", call="solve(n)", infmt="One line holding a whole number."):
    add(lesson, id, title, diff, statement, infmt, "One line.", [sample], hidden, sig, STUB, '\nif __name__ == "__main__":\n' + reads + '    print(' + call + ')\n', solution, hints)
intfn("functions", "fn_square", "Square it", "Easy", ["The function `solve` receives a number `n`. Return `n` multiplied by itself."],
 ("5\n", "25", "5 times 5 is 25."), ["0\n", "1\n", "-3\n", "12\n"], '    return n * n\n',
 ["The answer must be handed back with return.", "Multiply n by n.", "Return n times n.", "return n * n"])
intfn("functions", "fn_larger", "The larger of two", "Easy", ["The function `solve` receives two numbers `a` and `b`. Return the larger one. If they are equal, return either."],
 ("3\n9\n", "9", "9 is larger than 3."), ["5\n5\n", "-1\n-7\n", "100\n99\n"],
 '    if a > b:\n        return a\n    return b\n',
 ["You need a choice.", "If a is greater than b return a. Otherwise return b.", "if a > b: return a. Then outside the if, return b.", "if a > b: return a; return b."],
 sig="def solve(a, b):\n", reads="    a = int(input())\n    b = int(input())\n", call="solve(a, b)", infmt="Two lines: the number a, then the number b.")
add("functions", "fn_fix_print", "Return, do not print", "Easy",
 ["The starter code prints its answer instead of returning it. Run it as it is first: you will see the right number, then a line saying `None`, and the test fails.", "Fix `solve` so it returns `n + 10` instead of printing it."],
 "One line holding a whole number.", "One line.", [("5\n", "15", "5 plus 10 is 15. Only 15 should appear, with no None line.")], ["0\n", "-10\n", "990\n"],
 "def solve(n):\n", "    # Write your code here\n    # This line prints instead of returning. Fix it.\n    print(n + 10)\n", '\nif __name__ == "__main__":\n    n = int(input())\n    print(solve(n))\n', "    return n + 10\n",
 ["Print shows a value. Return hands it back to the line that called solve.", "That line already prints whatever solve hands back, so solve itself should not print.", "Change the word print to return, and drop the brackets.", "return n + 10"])
PROBLEMS[-1]["fixme"] = True

# ---------- 7 indexing ----------
listfn("indexing", "idx_first", "First item", "Easy",
 ["The function `solve` receives a list called `nums`. Return the first item of the list."], "One number.",
 [("3\n7 8 9\n", "7", "The first item sits at position 0.")], ["1\n5\n", "4\n-2 0 9 4\n", "2\n100 1\n"],
 '    return nums[0]\n',
 ["Positions start at 0.", "Use square brackets after the name of the list.", "Return the item at position 0.", "return nums[0]"])
listfn("indexing", "idx_last", "Last item", "Easy",
 ["Return the last item of the list `nums`. Negative positions count from the end."], "One number.",
 [("3\n7 8 9\n", "9", "Position -1 is the last item.")], ["1\n5\n", "4\n-2 0 9 4\n", "2\n100 1\n"],
 '    return nums[-1]\n',
 ["There is a position that always means the last item.", "It is a negative number.", "Return the item at position -1.", "return nums[-1]"])
listfn("indexing", "idx_second", "Second and second from the end", "Medium",
 ["The list `nums` always has at least 4 items. Return the second item plus the second item from the end, added together."], "One number.",
 [("4\n1 2 3 4\n", "5", "The second item is 2 (position 1). The second from the end is 3 (position -2). 2 + 3 is 5.")], ["4\n10 20 30 40\n", "5\n1 100 3 200 5\n", "6\n-1 -2 -3 -4 -5 -6\n"],
 '    return nums[1] + nums[-2]\n',
 ["Second item means position 1, because counting starts at 0.", "Second from the end is position -2.", "Add the item at position 1 to the item at position -2, and return the total.", "return nums[1] + nums[-2]"])

# ---------- 8 slicing ----------
listfn("slicing", "slice_first3", "First three", "Easy",
 ["Return a list holding the first 3 items of `nums`. The list always has at least 3 items."], "One line: the list.",
 [("5\n1 2 3 4 5\n", "[1, 2, 3]", "The slice from position 0 up to but not including position 3.")], ["3\n9 8 7\n", "4\n0 0 0 1\n"],
 '    return nums[:3]\n',
 ["A slice copies a piece of a list.", "A slice that starts at the beginning can leave the first number empty.", "Use [:3], which means from the start up to but not including position 3.", "return nums[:3]"])
listfn("slicing", "slice_middle", "Drop the ends", "Medium",
 ["Return a list holding everything except the first and the last item of `nums`. The list has at least 2 items, and the answer can be an empty list `[]`."], "One line: the list.",
 [("5\n1 2 3 4 5\n", "[2, 3, 4]", "Start at position 1 and stop before the last position."), ("2\n7 8\n", "[]", "Nothing is left once both ends are dropped.")], ["3\n4 5 6\n", "4\n1 1 1 1\n", "6\n9 8 7 6 5 4\n"],
 '    return nums[1:-1]\n',
 ["Start at position 1. For the end, think about negative positions.", "The end of a slice is not included, so stopping at -1 leaves out the last item.", "Return the slice that starts at 1 and ends at -1.", "return nums[1:-1]"])
listfn("slicing", "slice_reverse", "Reverse the list", "Easy",
 ["Return a copy of `nums` in reverse order."], "One line: the list.",
 [("4\n1 2 3 4\n", "[4, 3, 2, 1]", "The last item comes first.")], ["1\n5\n", "3\n3 1 2\n"],
 '    return nums[::-1]\n',
 ["There is a slice shape that walks backwards.", "A step of -1 walks backwards through the whole list.", "Use the slice with both ends empty and a step of -1.", "return nums[::-1]"])

# ---------- 9 len ----------
listfn("len", "len_count", "How many items", "Easy",
 ["Return how many items `nums` holds."], "One number.",
 [("3\n7 8 9\n", "3", "There are 3 items.")], ["1\n5\n", "5\n1 2 3 4 5\n"],
 '    return len(nums)\n',
 ["There is a built-in tool for counting.", "It is called len.", "Return len of nums.", "return len(nums)"])
listfn("len", "len_lastpos", "The last position", "Easy",
 ["Return the number of the last position in `nums`. For a list of 4 items the answer is 3, because positions start at 0."], "One number.",
 [("4\n9 9 9 9\n", "3", "Positions are 0, 1, 2, 3, so the last is 3.")], ["1\n5\n", "6\n1 2 3 4 5 6\n", "2\n0 0\n"],
 '    return len(nums) - 1\n',
 ["The last position is one less than how many items there are.", "Take the length and subtract 1.", "Return len(nums) minus 1.", "return len(nums) - 1"])
listfn("len", "len_middle", "The middle item", "Medium",
 ["The list `nums` always has an odd number of items. Return the item in the exact middle. For 5 items the middle is at position 2.", "Use `//` to divide and drop the decimal part."], "One number.",
 [("5\n1 2 3 4 5\n", "3", "5 // 2 is 2, and position 2 holds 3.")], ["1\n8\n", "3\n10 20 30\n", "7\n1 2 3 4 5 6 7\n"],
 '    return nums[len(nums) // 2]\n',
 ["The middle position depends on the length.", "Divide the length by 2 and drop the decimal part to get the position.", "Work out len(nums) // 2 and use it as the position.", "return nums[len(nums) // 2]"])

# ---------- 10 range ----------
script("range", "range_n", "Zero up to n", "Easy",
 ["A whole number `n` is stored for you. Print a list of the whole numbers from 0 up to `n - 1`. Use `range` and wrap it in `list( )` so the numbers can be printed."],
 "One line holding a whole number n (at least 1).", "One line: the list.", "n = int(input())\n",
 [("4\n", "[0, 1, 2, 3]", "range(4) gives 0, 1, 2, 3.")], ["1\n", "2\n", "8\n"],
 'print(list(range(n)))\n',
 ["range(n) stops just before n.", "Wrap range(n) in list so it can be shown.", "Print list of range of n.", "print(list(range(n)))"])
script("range", "range_ab", "From a up to b", "Easy",
 ["Two whole numbers `a` and `b` are stored for you, with `a` smaller than `b`. Print a list of the whole numbers starting at `a` and stopping just before `b`."],
 "Two lines: a, then b.", "One line: the list.", "a = int(input())\nb = int(input())\n",
 [("2\n6\n", "[2, 3, 4, 5]", "Starts at 2 and stops before 6.")], ["0\n1\n", "-2\n2\n", "10\n13\n"],
 'print(list(range(a, b)))\n',
 ["range can take two numbers.", "range(a, b) starts at a and stops just before b.", "Print list(range(a, b)).", "print(list(range(a, b)))"])
script("range", "range_step", "Every third number", "Medium",
 ["A whole number `n` is stored for you. Print a list of the numbers 0, 3, 6, 9 and so on that are smaller than `n`.", "A third number inside `range` sets the size of each jump."],
 "One line holding a whole number n (at least 1).", "One line: the list.", "n = int(input())\n",
 [("10\n", "[0, 3, 6, 9]", "Jumps of 3 starting at 0, stopping before 10.")], ["1\n", "3\n", "4\n", "30\n"],
 'print(list(range(0, n, 3)))\n',
 ["range can take three numbers: start, stop, jump.", "Start at 0, stop before n, jump by 3.", "Print list(range(0, n, 3)).", "print(list(range(0, n, 3)))"])

# ---------- 11 for loops ----------
listfn("forloops", "for_total", "Add them up", "Easy",
 ["Return the total of all the numbers in `nums`. Do not use `sum`. Use a `for` loop over the values and a name called `total` that starts at 0."], "One number.",
 [("3\n5 8 3\n", "16", "5 + 8 + 3 is 16.")], ["1\n7\n", "4\n-1 1 -1 1\n", "5\n10 20 30 40 50\n"],
 '    total = 0\n    for x in nums:\n        total = total + x\n    return total\n',
 ["Start with a total of 0 and add each item to it.", "for x in nums gives you each item. Inside the loop, add x to total.", "1. total = 0. 2. For each x in nums, total = total + x. 3. Return total.", "total = 0; for x in nums: total = total + x; return total. Remember the colon and the indent."])
listfn("forloops", "for_countbig", "Count the big ones", "Easy",
 ["Return how many numbers in `nums` are greater than 10. Use a `for` loop over the values and a counter that starts at 0."], "One number.",
 [("5\n3 12 15 10 40\n", "3", "12, 15 and 40 are greater than 10. The 10 is not greater than 10.")], ["1\n11\n", "3\n1 2 3\n", "4\n10 10 10 11\n"],
 '    count = 0\n    for x in nums:\n        if x > 10:\n            count = count + 1\n    return count\n',
 ["A counter goes up by 1 each time you find a match.", "Inside the loop, use an if to check x > 10.", "1. count = 0. 2. For each x, if x > 10 then add 1 to count. 3. Return count.", "count = 0; for x in nums: if x > 10: count = count + 1; return count."])
listfn("forloops", "for_evenpos", "Add the even positions", "Medium",
 ["Return the total of the items at positions 0, 2, 4 and so on (the even positions). Use `for i in range(len(nums))` so that `i` is the position.", "For `[10, 20, 30, 40, 50]` the answer is 10 + 30 + 50 = 90."], "One number.",
 [("5\n10 20 30 40 50\n", "90", "Positions 0, 2 and 4 hold 10, 30 and 50.")], ["1\n7\n", "2\n5 100\n", "4\n1 2 3 4\n"],
 '    total = 0\n    for i in range(len(nums)):\n        if i % 2 == 0:\n            total = total + nums[i]\n    return total\n',
 ["You need the position, not only the value.", "Loop over positions with range(len(nums)). Check whether i is even using i % 2 == 0.", "1. total = 0. 2. For each position i, if i % 2 == 0, add nums[i] to total. 3. Return total.", "total = 0; for i in range(len(nums)): if i % 2 == 0: total = total + nums[i]; return total."])
listfn("forloops", "for_rises", "Count the rises", "Hard",
 ["Count how many times an item is smaller than the item right after it. For `[1, 3, 2, 5]` the pairs are (1, 3), (3, 2) and (2, 5), and two of them rise, so the answer is 2.", "Take care at the end. The last item has no neighbour after it, so asking for `nums[i + 1]` there causes an IndexError. Loop over the positions `0` to `len(nums) - 2`."], "One number.",
 [("4\n1 3 2 5\n", "2", "1 is smaller than 3 and 2 is smaller than 5."), ("1\n9\n", "0", "A single item has no pairs.")], ["5\n1 2 3 4 5\n", "3\n3 2 1\n", "4\n5 5 5 5\n", "6\n1 0 1 0 1 0\n"],
 '    count = 0\n    for i in range(len(nums) - 1):\n        if nums[i] < nums[i + 1]:\n            count = count + 1\n    return count\n',
 ["Each round compares an item with its neighbour on the right.", "Use range(len(nums) - 1) so that i + 1 is always a real position.", "1. count = 0. 2. For each position i from 0 to len(nums) - 2: if nums[i] < nums[i + 1], add 1 to count. 3. Return count.", "count = 0; for i in range(len(nums) - 1): if nums[i] < nums[i + 1]: count = count + 1; return count."])

listfn("forloops", "fn_countevens", "Count the even numbers", "Medium",
 ["The function `solve` receives the list `nums`. Return how many of its numbers are even. Remember: `x % 2 == 0` asks whether `x` is even."], "One number.",
 [("5\n1 2 3 4 6\n", "3", "2, 4 and 6 are even.")], ["1\n7\n", "3\n2 4 6\n", "4\n0 -2 5 9\n"],
 '    count = 0\n    for x in nums:\n        if x % 2 == 0:\n            count = count + 1\n    return count\n',
 ["Combine a loop, a check and a counter.", "For each x, if x % 2 == 0, add 1 to count.", "1. count = 0. 2. Loop over nums. 3. If x is even, add 1. 4. Return count.", "count = 0; for x in nums: if x % 2 == 0: count = count + 1; return count."])

# ---------- 13 input ----------
script("input", "in_sumline", "Sum of one line", "Easy",
 ["You read the input yourself this time. One line holds some whole numbers separated by spaces. Print their sum.", "To read it: `nums = list(map(int, input().split()))`. Then `sum(nums)` adds them."],
 "One line of whole numbers separated by spaces.", "One number.", "",
 [("4 5 6\n", "15", "4 + 5 + 6 is 15.")], ["10\n", "-1 1\n", "1 2 3 4 5 6 7 8 9 10\n"],
 'nums = list(map(int, input().split()))\nprint(sum(nums))\n',
 ["The lesson showed the exact line for reading numbers.", "Read the line into nums, then print sum(nums).", "1. Read the line and turn each piece into a number. 2. Print the sum.", "nums = list(map(int, input().split())); print(sum(nums))."])
script("input", "in_biggest", "Biggest number", "Easy",
 ["Line 1 holds `n`, how many numbers follow. Line 2 holds those `n` numbers separated by spaces. Print the biggest one.", "You can read `n` with `n = int(input())`, even though you will not need it afterwards."],
 "Line 1: n. Line 2: n whole numbers.", "One number.", "",
 [("3\n4 9 2\n", "9", "9 is the biggest.")], ["1\n5\n", "4\n-3 -1 -7 -2\n", "5\n1 1 1 1 1\n"],
 'n = int(input())\nnums = list(map(int, input().split()))\nprint(max(nums))\n',
 ["Two input lines means two reads.", "Read the first line and ignore it, or store it. Read the second line as a list.", "1. Read n. 2. Read the list. 3. Print max of the list.", "n = int(input()); nums = list(map(...)); print(max(nums))."])
script("input", "in_average", "Whole-number average", "Medium",
 ["Line 1 holds `n`. Line 2 holds `n` whole numbers. Print the average, dropping the decimal part. The average is the total divided by how many numbers there are.", "Use `//` for division that drops the decimal part."],
 "Line 1: n. Line 2: n whole numbers.", "One whole number.", "",
 [("4\n1 2 3 5\n", "2", "The total is 11. 11 // 4 is 2.")], ["1\n9\n", "3\n10 20 30\n", "2\n0 1\n"],
 'n = int(input())\nnums = list(map(int, input().split()))\nprint(sum(nums) // n)\n',
 ["You need the total and the count.", "The total comes from sum. The count is n.", "1. Read n and the list. 2. Print sum(nums) // n.", "print(sum(nums) // n)"])

# ---------- 14 strings ----------
def wordfn(lesson, id, title, diff, statement, outfmt, sample, hidden, solution, hints):
    add(lesson, id, title, diff, statement, "One line holding a word of small letters, with no spaces.", outfmt, [sample], hidden, "def solve(word):\n", STUB, '\nif __name__ == "__main__":\n    word = input()\n    print(solve(word))\n', solution, hints)
wordfn("strings", "str_ends", "First and last letter", "Easy", ["Return the first letter and the last letter of `word` joined together. The symbol `+` joins two pieces of text. The word has at least 2 letters."],
 "One line: two letters.", ("planet\n", "pt", "The first letter is p and the last is t."), ["ab\n", "level\n", "builder\n"],
 '    return word[0] + word[-1]\n',
 ["Text has positions like a list.", "The first letter is at position 0 and the last at position -1.", "Return word[0] joined with word[-1] using +.", "return word[0] + word[-1]"])
wordfn("strings", "str_reverse", "Reverse a word", "Easy", ["Return `word` written backwards."], "One line: the reversed word.",
 ("stone\n", "enots", "The letters in the opposite order."), ["a\n", "ab\n", "racecar\n"],
 '    return word[::-1]\n',
 ["Slices work on text too.", "The backwards slice is the same one as for lists.", "Return word with the step -1 slice.", "return word[::-1]"])
wordfn("strings", "str_palindrome", "Same backwards", "Medium", ["A palindrome reads the same forwards and backwards. Return `True` if `word` is one, otherwise `False`."], "`True` or `False`.",
 ("level\n", "True", "level backwards is level."), ["abc\n", "a\n", "noon\n", "ab\n"],
 '    return word == word[::-1]\n',
 ["Compare the word with its reverse.", "A reversed copy is word[::-1]. Ask whether it equals the word.", "Return the answer to: is word equal to word reversed.", "return word == word[::-1]"])
wordfn("strings", "str_vowels", "Count the vowels", "Medium", ["Return how many letters in `word` are vowels. The vowels are `a`, `e`, `i`, `o` and `u`.", "The word `in` asks whether something is found inside something else. For example `'a' in 'aeiou'` is True."], "One number.",
 ("education\n", "5", "e, u, a, i, o are vowels."), ["xyz\n", "aeiou\n", "builder\n"],
 '    count = 0\n    for letter in word:\n        if letter in "aeiou":\n            count = count + 1\n    return count\n',
 ["A for loop can go through the letters of a word.", "Loop over word. For each letter, check whether it is inside the text aeiou.", "1. count = 0. 2. For each letter in word, if letter in \"aeiou\", add 1 to count. 3. Return count.", "count = 0; for letter in word: if letter in \"aeiou\": count = count + 1; return count."])
