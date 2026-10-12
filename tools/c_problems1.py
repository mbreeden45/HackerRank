# Basics problems (lessons 1 to 14). Expected outputs for SAMPLES are written by hand.
# Hidden test outputs are produced by running the reference solution (see build_content.py).
#
# Two kinds of problem:
#   preset  (lessons 1 to 11): no def, no return, no input. The starting data is a few locked lines such as
#           nums = [7, 8, 9]. The learner writes print(...) lines. Each test case swaps in its own starting data.
#   stdin   (lessons 12 and later): starter code with def solve(...) and a locked bottom part that reads the
#           typed input. Taught in the "Reading the starter code" part of the functions lesson.
# The open section of every stub holds only "# Write your code here".
PROBLEMS = []
STUB = "    # Write your code here\n"
NO_DATA = "Nothing to type. The starting data (if any) is already set in the grey lines at the top of the editor."

def add(lesson, id, title, diff, statement, infmt, outfmt, samples, hidden, prefix, body, suffix, solution, hints, constraints=None, mode="stdin"):
    assert len(hints) == 4, id
    PROBLEMS.append(dict(id=id, lesson=lesson, title=title, difficulty=diff, statement=statement, input_fmt=infmt, mode=mode,
        output_fmt=outfmt, constraints=constraints, samples=[dict(input=a, output=b, explanation=c) for a, b, c in samples],
        hidden_inputs=hidden, prefix=prefix, body=body, suffix=suffix, solution=solution, hints=hints))

def pre(lesson, id, title, diff, statement, outfmt, samples, hidden, solution, hints):
    """Preset problem. samples: (starting data, output, explanation). hidden: list of starting data strings."""
    assert samples[0][0] == samples[0][0]
    add(lesson, id, title, diff, statement, NO_DATA, outfmt, samples, hidden, samples[0][0], "# Write your code here\n", "", solution, hints, mode="preset")

# ---------- 1 print ----------
pre("print", "print_two_lines", "Two lines", "Easy",
 ["Print the word `Hello` on the first line, and the number `42` on the second line."],
 "Two lines: `Hello`, then `42`.",
 [("", "Hello\n42", "The first print shows the word Hello. The second print shows 42, with no quote marks because it is a number.")], [""],
 'print("Hello")\nprint(42)\n',
 ["Each print makes its own line.", "You need two print lines. Words need quote marks, numbers do not.", "Line 1 shows the text Hello. Line 2 shows the number 42.", "1. Use `print(\"Hello\")`. 2. Use `print(42)`."])
pre("print", "print_greeting", "A greeting", "Easy",
 ["Print `Hi,` and then `Ana` on one line, with a space between them. Use a single print with two things inside the brackets."],
 "One line: `Hi, Ana`.",
 [("", "Hi, Ana", "The text Hi, and the text Ana are printed with one space between them. The comma inside print adds that space.")], [""],
 'print("Hi,", "Ana")\n',
 ["print can show two things at once.", "Put a comma between two things inside the print brackets. The comma adds the space for you.", "Both things are text, so each needs quote marks.", "1. Write `print(` then the text `\"Hi,\"`, then a comma, then the text `\"Ana\"`, then `)`."])
pre("print", "print_count", "Count to three", "Easy",
 ["Print the numbers 1, 2 and 3, each on its own line. Then print them once more on a single line with spaces between them: `1 2 3`."],
 "Four lines: `1`, `2`, `3`, then `1 2 3`.",
 [("", "1\n2\n3\n1 2 3", "Three prints give three lines. One print with three things in it gives the last line.")], [""],
 'print(1)\nprint(2)\nprint(3)\nprint(1, 2, 3)\n',
 ["Four lines of output need four prints.", "The first three prints hold one number each. The last print holds all three numbers.", "Separate the three numbers in the last print with commas.", "1. `print(1)`. 2. `print(2)`. 3. `print(3)`. 4. `print(1, 2, 3)`."])

# ---------- 2 variables ----------
pre("variables", "var_add", "Add two numbers", "Easy",
 ["The grey lines at the top store two whole numbers in `a` and `b`. Print their sum, meaning `a` plus `b`."],
 "One number: the sum.",
 [("a = 2\nb = 5\n", "7", "2 plus 5 is 7.")], ["a = -3\nb = 3\n", "a = 100\nb = 250\n", "a = 0\nb = 9\n"],
 'print(a + b)\n',
 ["The + sign adds numbers.", "You can do the adding inside the print brackets.", "Print the answer of a plus b.", "1. Write `print(` then `a + b` then `)`."])
pre("variables", "var_rectangle", "Area and perimeter", "Easy",
 ["The grey lines store the `width` and `height` of a rectangle. The area is width times height. The perimeter is the total length around the outside: 2 times (width plus height).", "Print the area on the first line and the perimeter on the second line. The symbol `*` means times."],
 "Two lines: the area, then the perimeter.",
 [("width = 3\nheight = 4\n", "12\n14", "Area is 3 * 4 = 12. Perimeter is 2 * (3 + 4) = 14.")], ["width = 1\nheight = 1\n", "width = 10\nheight = 2\n", "width = 7\nheight = 9\n"],
 'area = width * height\nperimeter = 2 * (width + height)\nprint(area)\nprint(perimeter)\n',
 ["Work out each answer and store it in a name first.", "Make a name called area, and a name called perimeter. Then print each.", "area is width times height. perimeter is 2 times the sum of width and height.", "1. `area = width * height`. 2. `perimeter = 2 * (width + height)`. 3. `print(area)`. 4. `print(perimeter)`."])
pre("variables", "var_swap", "Swap two values", "Medium",
 ["The names `a` and `b` hold two numbers. Make `a` hold what `b` held, and `b` hold what `a` held. Then print `a` on the first line and `b` on the second.", "Warning: if you write `a = b` first, the old value of `a` is lost. A third name can hold it safely for a moment."],
 "Two lines: the new a, then the new b.",
 [("a = 3\nb = 8\n", "8\n3", "After the swap, a holds 8 and b holds 3.")], ["a = 1\nb = 2\n", "a = -5\nb = 5\n", "a = 7\nb = 7\n"],
 'temp = a\na = b\nb = temp\nprint(a)\nprint(b)\n',
 ["Think of two cups of juice that you want to swap. You need a third empty cup.", "Store the old a in a new name before you change a.", "Save a in a new name called temp. Then put b into a. Then put temp into b.", "1. `temp = a`. 2. `a = b`. 3. `b = temp`. 4. `print(a)`. 5. `print(b)`."])

# ---------- 3 equals ----------
pre("equals", "eq_same", "Are they equal", "Easy",
 ["The grey lines store two numbers in `a` and `b`. Print `True` if they are equal, otherwise print `False`.", "Hint on symbols: `==` asks whether two things are equal and gives back `True` or `False`."],
 "`True` or `False`.",
 [("a = 4\nb = 4\n", "True", "4 is equal to 4."), ("a = 4\nb = 9\n", "False", "4 is not equal to 9.")], ["a = 0\nb = 0\n", "a = -1\nb = 1\n", "a = 50\nb = 50\n"],
 'print(a == b)\n',
 ["The answer to print is already a True or False answer.", "Ask the question a == b inside the print.", "Print the answer to the question: is a equal to b.", "1. Write `print(` then `a == b` then `)`."])
pre("equals", "eq_three", "Three questions", "Easy",
 ["The grey lines store two numbers in `a` and `b`. Print three lines, each the answer to one question:", "Line 1: is `a` equal to `b`. Line 2: is `a` less than `b`. Line 3: is `a` greater than `b`.", "The symbols are `==`, `<` and `>`."],
 "Three lines, each `True` or `False`.",
 [("a = 2\nb = 5\n", "False\nTrue\nFalse", "2 is not equal to 5. 2 is less than 5. 2 is not greater than 5.")], ["a = 5\nb = 5\n", "a = 9\nb = 1\n", "a = -2\nb = -3\n"],
 'print(a == b)\nprint(a < b)\nprint(a > b)\n',
 ["Each line is its own print.", "Three print lines. Each holds one question.", "The questions use ==, < and > in that order.", "1. `print(a == b)`. 2. `print(a < b)`. 3. `print(a > b)`."])
pre("equals", "eq_password", "Password check", "Medium",
 ["The grey line stores a word in `word`. Print `True` if it is exactly `builder` (all small letters), otherwise `False`.", "Capital letters count as different letters. `Builder` is not the same as `builder`."],
 "`True` or `False`.",
 [("word = \"builder\"\n", "True", "Exactly the same."), ("word = \"Builder\"\n", "False", "The capital B makes it different.")], ["word = \"build\"\n", "word = \"BUILDER\"\n", "word = \"builder\"\n"],
 'print(word == "builder")\n',
 ["The word you compare against needs quote marks.", "Compare the name word with the text \"builder\" using two equals signs.", "Print the answer to: is word equal to the text builder.", "1. Write `print(` then `word == \"builder\"` then `)`."])

# ---------- 4 remainder ----------
pre("remainder", "mod_even", "Is it even", "Easy",
 ["The grey line stores a whole number in `n`. Print `True` if it is even and `False` if it is odd.", "An even number has remainder 0 when divided by 2. The symbol `%` gives the remainder."],
 "`True` or `False`.",
 [("n = 10\n", "True", "10 % 2 is 0."), ("n = 7\n", "False", "7 % 2 is 1.")], ["n = 0\n", "n = 1\n", "n = -4\n", "n = 99\n"],
 'print(n % 2 == 0)\n',
 ["Use % with the number 2.", "Ask whether the remainder after dividing by 2 equals 0.", "Print the answer to: is n % 2 equal to 0.", "1. Write `print(` then `n % 2 == 0` then `)`."])
pre("remainder", "mod_digits", "Split off the last digit", "Easy",
 ["The grey line stores a non-negative whole number in `n`. Print its last digit on the first line. On the second line print the number with its last digit removed (that is `0` if nothing is left).", "Hint: `n % 10` is the last digit. `n // 10` divides by 10 and drops the decimal part."],
 "Two lines: the last digit, then the number without it.",
 [("n = 472\n", "2\n47", "472 % 10 is 2. 472 // 10 is 47.")], ["n = 5\n", "n = 100\n", "n = 90817\n"],
 'print(n % 10)\nprint(n // 10)\n',
 ["Dividing by 10 and looking at the remainder isolates the last digit.", "Use % 10 for the first line and // 10 for the second.", "Two prints: one for the remainder, one for the division that drops the decimal part.", "1. `print(n % 10)`. 2. `print(n // 10)`."])
pre("remainder", "mod_weeks", "Days to weeks", "Medium",
 ["The grey line stores a number of days in `days`. Print the number of whole weeks on the first line and the days left over on the second line. A week has 7 days."],
 "Two lines: whole weeks, then leftover days.",
 [("days = 17\n", "2\n3", "17 days is 2 whole weeks (14 days) and 3 days left over.")], ["days = 7\n", "days = 6\n", "days = 0\n", "days = 100\n"],
 'print(days // 7)\nprint(days % 7)\n',
 ["Whole weeks is a division with the decimal part dropped. Leftover days is a remainder.", "Use // 7 for weeks and % 7 for leftover days.", "Two prints, one for each answer.", "1. `print(days // 7)`. 2. `print(days % 7)`."])

# ---------- 5 if/else ----------
pre("ifelse", "if_evenodd", "Even or odd", "Easy",
 ["The grey line stores a whole number in `n`. Print the word `even` if it is even, otherwise print `odd`."],
 "`even` or `odd`.",
 [("n = 8\n", "even", "8 % 2 is 0."), ("n = 5\n", "odd", "5 % 2 is 1.")], ["n = 0\n", "n = 1\n", "n = 22\n", "n = -3\n"],
 'if n % 2 == 0:\n    print("even")\nelse:\n    print("odd")\n',
 ["You need a choice with two outcomes.", "Use if with the question n % 2 == 0, and else for the other outcome.", "If the remainder after dividing by 2 is 0, show even. Otherwise show odd.", "1. `if n % 2 == 0:` then an indented `print(\"even\")`. 2. `else:` then an indented `print(\"odd\")`."])
pre("ifelse", "if_sign", "Positive, negative or zero", "Easy",
 ["The grey line stores a whole number in `n`. Print `positive` if it is above zero, `negative` if it is below zero, and `zero` if it is zero."],
 "`positive`, `negative` or `zero`.",
 [("n = 5\n", "positive", "5 is above zero."), ("n = -2\n", "negative", "-2 is below zero.")], ["n = 0\n", "n = 1\n", "n = -100\n"],
 'if n > 0:\n    print("positive")\nelif n < 0:\n    print("negative")\nelse:\n    print("zero")\n',
 ["There are three outcomes, so you need more than if and else.", "Use if, then elif, then else.", "If n is above 0 show positive. Else if n is below 0 show negative. Otherwise show zero.", "1. `if n > 0:` then an indented print. 2. `elif n < 0:` then an indented print. 3. `else:` then an indented print."])
pre("ifelse", "if_fizz", "Fizz and Buzz", "Medium",
 ["The grey line stores a whole number in `n`. Print:", "`FizzBuzz` if n divides exactly by both 3 and 5; `Fizz` if it divides exactly by 3 only; `Buzz` if it divides exactly by 5 only; otherwise the number itself.", "Hint: divides exactly by 3 means `n % 3 == 0`. The word `and` is True only when both sides are True."],
 "One line.",
 [("n = 15\n", "FizzBuzz", "15 divides by 3 and by 5."), ("n = 9\n", "Fizz", "9 divides by 3 only."), ("n = 7\n", "7", "7 divides by neither.")], ["n = 10\n", "n = 30\n", "n = 1\n", "n = 2\n", "n = 27\n"],
 'if n % 3 == 0 and n % 5 == 0:\n    print("FizzBuzz")\nelif n % 3 == 0:\n    print("Fizz")\nelif n % 5 == 0:\n    print("Buzz")\nelse:\n    print(n)\n',
 ["The order of your questions matters. Which question should be asked first.", "Ask the both-3-and-5 question first. If you ask about 3 first, 15 would show Fizz.", "Ask in this order: both 3 and 5, then 3, then 5, then everything else.", "1. `if n % 3 == 0 and n % 5 == 0:` then FizzBuzz. 2. `elif n % 3 == 0:` then Fizz. 3. `elif n % 5 == 0:` then Buzz. 4. `else:` then `print(n)`."])

# ---------- 6 lists ----------
pre("lists", "list_build", "Build a list", "Easy",
 ["The grey lines store three numbers in `a`, `b` and `c`. Make a list holding them in that order, add the number `100` to the end, then print the list.", "A list prints with square brackets, for example `[1, 2, 3, 100]`."],
 "One line: the list.",
 [("a = 1\nb = 2\nc = 3\n", "[1, 2, 3, 100]", "The list starts as [1, 2, 3] and 100 is added at the end.")], ["a = 0\nb = 0\nc = 0\n", "a = -1\nb = 5\nc = 9\n"],
 'items = [a, b, c]\nitems.append(100)\nprint(items)\n',
 ["First make the list, then add to it.", "Write square brackets with a, b and c inside, store it in a name, then use .append.", "Make a list called items from a, b and c. Append 100 to it. Print it.", "1. `items = [a, b, c]`. 2. `items.append(100)`. 3. `print(items)`."])
pre("lists", "list_grow", "Add two more", "Easy",
 ["The grey lines store a list in `nums` and a whole number in `x`. Add `x` to the end of the list two times, then print the list."],
 "One line: the list.",
 [("nums = [4, 5]\nx = 9\n", "[4, 5, 9, 9]", "9 is added twice at the end.")], ["nums = [1]\nx = 2\n", "nums = [1, 2, 3, 4]\nx = 0\n", "nums = [-1, -2]\nx = -3\n"],
 'nums.append(x)\nnums.append(x)\nprint(nums)\n',
 [".append adds one item at a time.", "You need two append lines.", "Append x. Append x again. Then show nums with `print(nums)`.", "1. `nums.append(x)`. 2. `nums.append(x)`. 3. `print(nums)`."])
pre("lists", "list_stats", "Sum, biggest, smallest", "Medium",
 ["The grey line stores a list in `nums`. Three tools help here: `sum(nums)` adds up all the numbers, `max(nums)` gives the biggest number, and `min(nums)` gives the smallest.", "Print the sum, then the biggest, then the smallest, each on its own line."],
 "Three lines.",
 [("nums = [3, 9, 2]\n", "14\n9\n2", "3 + 9 + 2 is 14. The biggest is 9. The smallest is 2.")], ["nums = [5]\n", "nums = [-1, -5, -3]\n", "nums = [10, 20, 30, 40]\n"],
 'print(sum(nums))\nprint(max(nums))\nprint(min(nums))\n',
 ["The three tools are described in the statement.", "Three prints, one for each tool.", "Each print holds one tool applied to nums.", "1. `print(sum(nums))`. 2. `print(max(nums))`. 3. `print(min(nums))`."])

# ---------- 7 indexing ----------
pre("indexing", "idx_first", "First item", "Easy",
 ["The grey line stores a list in `nums`. Print the first item of the list."],
 "One number.",
 [("nums = [7, 8, 9]\n", "7", "The first item sits at position 0.")], ["nums = [5]\n", "nums = [-2, 0, 9, 4]\n", "nums = [100, 1]\n"],
 'print(nums[0])\n',
 ["Positions start at 0.", "Use square brackets after the name of the list.", "Print the item at position 0.", "1. Write `print(` then `nums[0]` then `)`."])
pre("indexing", "idx_last", "Last item", "Easy",
 ["The grey line stores a list in `nums`. Print the last item of the list. Negative positions count from the end."],
 "One number.",
 [("nums = [7, 8, 9]\n", "9", "Position -1 is the last item.")], ["nums = [5]\n", "nums = [-2, 0, 9, 4]\n", "nums = [100, 1]\n"],
 'print(nums[-1])\n',
 ["There is a position that always means the last item.", "It is a negative number.", "Print the item at position -1.", "1. Write `print(` then `nums[-1]` then `)`."])
pre("indexing", "idx_second", "Second and second from the end", "Medium",
 ["The grey line stores a list in `nums`. It always has at least 4 items. Print the second item plus the second item from the end, added together."],
 "One number.",
 [("nums = [1, 2, 3, 4]\n", "5", "The second item is 2 (position 1). The second from the end is 3 (position -2). 2 + 3 is 5.")], ["nums = [10, 20, 30, 40]\n", "nums = [1, 100, 3, 200, 5]\n", "nums = [-1, -2, -3, -4, -5, -6]\n"],
 'print(nums[1] + nums[-2])\n',
 ["Second item means position 1, because counting starts at 0.", "Second from the end is position -2.", "Add the item at position 1 to the item at position -2, and print the total.", "1. Write `print(` then `nums[1] + nums[-2]` then `)`."])

# ---------- 8 slicing ----------
pre("slicing", "slice_first3", "First three", "Easy",
 ["The grey line stores a list in `nums`. It always has at least 3 items. Print a list holding the first 3 items."],
 "One line: the list.",
 [("nums = [1, 2, 3, 4, 5]\n", "[1, 2, 3]", "The slice from position 0 up to but not including position 3.")], ["nums = [9, 8, 7]\n", "nums = [0, 0, 0, 1]\n"],
 'print(nums[:3])\n',
 ["A slice copies a piece of a list.", "A slice that starts at the beginning can leave the first number empty.", "Use [:3], which means from the start up to but not including position 3.", "1. Write `print(` then `nums[:3]` then `)`."])
pre("slicing", "slice_middle", "Drop the ends", "Medium",
 ["The grey line stores a list in `nums` with at least 2 items. Print a list holding everything except the first and the last item. The answer can be an empty list `[]`."],
 "One line: the list.",
 [("nums = [1, 2, 3, 4, 5]\n", "[2, 3, 4]", "Start at position 1 and stop before the last position."), ("nums = [7, 8]\n", "[]", "Nothing is left once both ends are dropped.")], ["nums = [4, 5, 6]\n", "nums = [1, 1, 1, 1]\n", "nums = [9, 8, 7, 6, 5, 4]\n"],
 'print(nums[1:-1])\n',
 ["Start at position 1. For the end, think about negative positions.", "The end of a slice is not included, so stopping at -1 leaves out the last item.", "Print the slice that starts at 1 and ends at -1.", "1. Write `print(` then `nums[1:-1]` then `)`."])
pre("slicing", "slice_reverse", "Reverse the list", "Easy",
 ["The grey line stores a list in `nums`. Print a copy of it in reverse order."],
 "One line: the list.",
 [("nums = [1, 2, 3, 4]\n", "[4, 3, 2, 1]", "The last item comes first.")], ["nums = [5]\n", "nums = [3, 1, 2]\n"],
 'print(nums[::-1])\n',
 ["There is a slice shape that walks backwards.", "A step of -1 walks backwards through the whole list.", "Use the slice with both ends empty and a step of -1.", "1. Write `print(` then `nums[::-1]` then `)`."])

# ---------- 9 len ----------
pre("len", "len_count", "How many items", "Easy",
 ["The grey line stores a list in `nums`. Print how many items it holds."],
 "One number.",
 [("nums = [7, 8, 9]\n", "3", "There are 3 items.")], ["nums = [5]\n", "nums = [1, 2, 3, 4, 5]\n"],
 'print(len(nums))\n',
 ["There is a built-in tool for counting.", "It is called len.", "Print len of nums.", "1. Write `print(` then `len(nums)` then `)`."])
pre("len", "len_lastpos", "The last position", "Easy",
 ["The grey line stores a list in `nums`. Print the number of the last position in it. For a list of 4 items the answer is 3, because positions start at 0."],
 "One number.",
 [("nums = [9, 9, 9, 9]\n", "3", "Positions are 0, 1, 2, 3, so the last is 3.")], ["nums = [5]\n", "nums = [1, 2, 3, 4, 5, 6]\n", "nums = [0, 0]\n"],
 'print(len(nums) - 1)\n',
 ["The last position is one less than how many items there are.", "Take the length and subtract 1.", "Print len(nums) minus 1.", "1. Write `print(` then `len(nums) - 1` then `)`."])
pre("len", "len_middle", "The middle item", "Medium",
 ["The grey line stores a list in `nums`. It always has an odd number of items. Print the item in the exact middle. For 5 items the middle is at position 2.", "Use `//` to divide and drop the decimal part."],
 "One number.",
 [("nums = [1, 2, 3, 4, 5]\n", "3", "5 // 2 is 2, and position 2 holds 3.")], ["nums = [8]\n", "nums = [10, 20, 30]\n", "nums = [1, 2, 3, 4, 5, 6, 7]\n"],
 'print(nums[len(nums) // 2])\n',
 ["The middle position depends on the length.", "Divide the length by 2 and drop the decimal part to get the position.", "Work out len(nums) // 2 and use it as the position.", "1. Write `print(` then `nums[len(nums) // 2]` then `)`."])

# ---------- 10 range ----------
pre("range", "range_n", "Zero up to n", "Easy",
 ["The grey line stores a whole number (at least 1) in `n`. Print a list of the whole numbers from 0 up to `n - 1`. Use `range` and wrap it in `list( )` so the numbers can be printed."],
 "One line: the list.",
 [("n = 4\n", "[0, 1, 2, 3]", "range(4) gives 0, 1, 2, 3.")], ["n = 1\n", "n = 2\n", "n = 8\n"],
 'print(list(range(n)))\n',
 ["range(n) stops just before n.", "Wrap range(n) in list so it can be shown.", "Print list of range of n.", "1. Write `print(list(range(n)))`."])
pre("range", "range_ab", "From a up to b", "Easy",
 ["The grey lines store two whole numbers in `a` and `b`, with `a` smaller than `b`. Print a list of the whole numbers starting at `a` and stopping just before `b`."],
 "One line: the list.",
 [("a = 2\nb = 6\n", "[2, 3, 4, 5]", "Starts at 2 and stops before 6.")], ["a = 0\nb = 1\n", "a = -2\nb = 2\n", "a = 10\nb = 13\n"],
 'print(list(range(a, b)))\n',
 ["range can take two numbers.", "range(a, b) starts at a and stops just before b.", "Print list(range(a, b)).", "1. Write `print(list(range(a, b)))`."])
pre("range", "range_step", "Every third number", "Medium",
 ["The grey line stores a whole number (at least 1) in `n`. Print a list of the numbers 0, 3, 6, 9 and so on that are smaller than `n`.", "A third number inside `range` sets the size of each jump."],
 "One line: the list.",
 [("n = 10\n", "[0, 3, 6, 9]", "Jumps of 3 starting at 0, stopping before 10.")], ["n = 1\n", "n = 3\n", "n = 4\n", "n = 30\n"],
 'print(list(range(0, n, 3)))\n',
 ["range can take three numbers: start, stop, jump.", "Start at 0, stop before n, jump by 3.", "Print list(range(0, n, 3)).", "1. Write `print(list(range(0, n, 3)))`."])

# ---------- 11 for loops ----------
pre("forloops", "for_total", "Add them up", "Easy",
 ["The grey line stores a list in `nums`. Print the total of all the numbers. Do not use `sum`. Use a `for` loop over the values and a name called `total` that starts at 0."],
 "One number.",
 [("nums = [5, 8, 3]\n", "16", "5 + 8 + 3 is 16.")], ["nums = [7]\n", "nums = [-1, 1, -1, 1]\n", "nums = [10, 20, 30, 40, 50]\n"],
 'total = 0\nfor x in nums:\n    total = total + x\nprint(total)\n',
 ["Start with a total of 0 and add each item to it.", "for x in nums gives you each item. Inside the loop, add x to total. Print after the loop, not inside it.", "Set total to 0. Loop over nums. Add each x to total. After the loop, show total with `print(total)`.", "1. `total = 0`. 2. `for x in nums:` then an indented `total = total + x`. 3. `print(total)` with no indent."])
pre("forloops", "for_countbig", "Count the big ones", "Easy",
 ["The grey line stores a list in `nums`. Print how many numbers in it are greater than 10. Use a `for` loop over the values and a counter that starts at 0."],
 "One number.",
 [("nums = [3, 12, 15, 10, 40]\n", "3", "12, 15 and 40 are greater than 10. The 10 is not greater than 10.")], ["nums = [11]\n", "nums = [1, 2, 3]\n", "nums = [10, 10, 10, 11]\n"],
 'count = 0\nfor x in nums:\n    if x > 10:\n        count = count + 1\nprint(count)\n',
 ["A counter goes up by 1 each time you find a match.", "Inside the loop, use an if to check x > 10.", "Set count to 0. Loop over nums. If x is above 10, add 1 to count. After the loop, show count with `print(count)`.", "1. `count = 0`. 2. `for x in nums:`. 3. Indented: `if x > 10:`. 4. Indented twice: `count = count + 1`. 5. `print(count)` with no indent."])
pre("forloops", "for_evenpos", "Add the even positions", "Medium",
 ["The grey line stores a list in `nums`. Print the total of the items at positions 0, 2, 4 and so on (the even positions). Use `for i in range(len(nums))` so that `i` is the position.", "For `[10, 20, 30, 40, 50]` the answer is 10 + 30 + 50 = 90."],
 "One number.",
 [("nums = [10, 20, 30, 40, 50]\n", "90", "Positions 0, 2 and 4 hold 10, 30 and 50.")], ["nums = [7]\n", "nums = [5, 100]\n", "nums = [1, 2, 3, 4]\n"],
 'total = 0\nfor i in range(len(nums)):\n    if i % 2 == 0:\n        total = total + nums[i]\nprint(total)\n',
 ["You need the position, not only the value.", "Loop over positions with range(len(nums)). Check whether i is even using i % 2 == 0.", "Set total to 0. For each position i, if i is even, add nums[i] to total. After the loop, show total with `print(total)`.", "1. `total = 0`. 2. `for i in range(len(nums)):`. 3. Indented: `if i % 2 == 0:`. 4. Indented twice: `total = total + nums[i]`. 5. `print(total)` with no indent."])
pre("forloops", "for_rises", "Count the rises", "Hard",
 ["The grey line stores a list in `nums`. Print how many times an item is smaller than the item right after it. For `[1, 3, 2, 5]` the pairs are (1, 3), (3, 2) and (2, 5), and two of them rise, so the answer is 2.", "Take care at the end. The last item has no neighbour after it, so asking for `nums[i + 1]` there causes an IndexError. Loop over the positions `0` to `len(nums) - 2`."],
 "One number.",
 [("nums = [1, 3, 2, 5]\n", "2", "1 is smaller than 3 and 2 is smaller than 5."), ("nums = [9]\n", "0", "A single item has no pairs.")], ["nums = [1, 2, 3, 4, 5]\n", "nums = [3, 2, 1]\n", "nums = [5, 5, 5, 5]\n", "nums = [1, 0, 1, 0, 1, 0]\n"],
 'count = 0\nfor i in range(len(nums) - 1):\n    if nums[i] < nums[i + 1]:\n        count = count + 1\nprint(count)\n',
 ["Each round compares an item with its neighbour on the right.", "Use range(len(nums) - 1) so that i + 1 is always a real position.", "Set count to 0. For each position i from 0 to len(nums) - 2, compare nums[i] with nums[i + 1]. Add 1 when it rises. Print count at the end.", "1. `count = 0`. 2. `for i in range(len(nums) - 1):`. 3. Indented: `if nums[i] < nums[i + 1]:`. 4. Indented twice: `count = count + 1`. 5. `print(count)` with no indent."])

# ---------- 12 functions (starter code with def, return and a locked main) ----------
def intfn(lesson, id, title, diff, statement, sample, hidden, solution, hints, sig="def solve(n):\n", reads="    n = int(input())\n", call="solve(n)", infmt="One line holding a whole number."):
    add(lesson, id, title, diff, statement, infmt, "One line.", [sample], hidden, sig, STUB, '\nif __name__ == "__main__":\n' + reads + '    print(' + call + ')\n', solution, hints)
intfn("functions", "fn_square", "Square it", "Easy", ["The function `solve` receives a number `n`. Return `n` multiplied by itself. The locked lines at the bottom read the number and print whatever your function returns."],
 ("5\n", "25", "5 times 5 is 25."), ["0\n", "1\n", "-3\n", "12\n"], '    return n * n\n',
 ["The answer must be handed back with return. Do not use print inside the function.", "Multiply n by n.", "Return n times n.", "1. Write `return` then `n * n`, indented by 4 spaces."])
intfn("functions", "fn_larger", "The larger of two", "Easy", ["The function `solve` receives two numbers `a` and `b`. Return the larger one. If they are equal, return either."],
 ("3\n9\n", "9", "9 is larger than 3."), ["5\n5\n", "-1\n-7\n", "100\n99\n"],
 '    if a > b:\n        return a\n    return b\n',
 ["You need a choice.", "If a is greater than b return a. Otherwise return b.", "Check a > b. Return a when it is True. After the check, return b.", "1. `if a > b:` then an indented `return a`. 2. Then `return b` at the same indent as the `if`."],
 sig="def solve(a, b):\n", reads="    a = int(input())\n    b = int(input())\n", call="solve(a, b)", infmt="Two lines: the number a, then the number b.")
add("functions", "fn_countevens", "Count the even numbers", "Medium",
 ["The function `solve` receives the list `nums`. Return how many of its numbers are even. Remember: `x % 2 == 0` asks whether `x` is even."],
 "A line with how many numbers there are, then a line with the whole numbers for `nums`, separated by spaces.", "One number.",
 [("5\n1 2 3 4 6\n", "3", "2, 4 and 6 are even.")], ["1\n7\n", "3\n2 4 6\n", "4\n0 -2 5 9\n"],
 "def solve(nums):\n", STUB, '\nif __name__ == "__main__":\n    count = int(input())\n    nums = list(map(int, input().split()))\n    print(solve(nums))\n',
 '    count = 0\n    for x in nums:\n        if x % 2 == 0:\n            count = count + 1\n    return count\n',
 ["Combine a loop, a check and a counter.", "For each x, if x % 2 == 0, add 1 to count.", "Set count to 0. Loop over nums. If x is even, add 1. Return count after the loop.", "1. `count = 0`. 2. `for x in nums:`. 3. Indented: `if x % 2 == 0:`. 4. Indented twice: `count = count + 1`. 5. `return count`, indented 4 spaces."])

# ---------- 13 input (the learner writes the reading lines) ----------
def script(lesson, id, title, diff, statement, infmt, outfmt, samples, hidden, solution, hints):
    add(lesson, id, title, diff, statement, infmt, outfmt, samples, hidden, "", "# Write your code here\n", "", solution, hints)
script("input", "in_sumline", "Sum of one line", "Easy",
 ["You read the input yourself this time. One line holds some whole numbers separated by spaces. Print their sum.", "To read it: `nums = list(map(int, input().split()))`. Then `sum(nums)` adds them."],
 "One line of whole numbers separated by spaces.", "One number.",
 [("4 5 6\n", "15", "4 + 5 + 6 is 15.")], ["10\n", "-1 1\n", "1 2 3 4 5 6 7 8 9 10\n"],
 'nums = list(map(int, input().split()))\nprint(sum(nums))\n',
 ["The reading line is shown in the statement.", "Read the line into nums, then print sum(nums).", "First read the line and turn each piece into a number. Then print the sum.", "1. `nums = list(map(int, input().split()))`. 2. `print(sum(nums))`."])
script("input", "in_biggest", "Biggest number", "Easy",
 ["Line 1 holds `n`, how many numbers follow. Line 2 holds those `n` numbers separated by spaces. Print the biggest one.", "You can read `n` with `n = int(input())`, even though you will not need it afterwards."],
 "Line 1: n. Line 2: n whole numbers.", "One number.",
 [("3\n4 9 2\n", "9", "9 is the biggest.")], ["1\n5\n", "4\n-3 -1 -7 -2\n", "5\n1 1 1 1 1\n"],
 'n = int(input())\nnums = list(map(int, input().split()))\nprint(max(nums))\n',
 ["Two input lines means two reads.", "Read the first line and ignore it, or store it. Read the second line as a list.", "Read n. Read the list. Print the biggest.", "1. `n = int(input())`. 2. `nums = list(map(int, input().split()))`. 3. `print(max(nums))`."])
script("input", "in_average", "Whole-number average", "Medium",
 ["Line 1 holds `n`. Line 2 holds `n` whole numbers. Print the average, dropping the decimal part. The average is the total divided by how many numbers there are.", "Use `//` for division that drops the decimal part."],
 "Line 1: n. Line 2: n whole numbers.", "One whole number.",
 [("4\n1 2 3 5\n", "2", "The total is 11. 11 // 4 is 2.")], ["1\n9\n", "3\n10 20 30\n", "2\n0 1\n"],
 'n = int(input())\nnums = list(map(int, input().split()))\nprint(sum(nums) // n)\n',
 ["You need the total and the count.", "The total comes from sum. The count is n.", "Read n and the list. Then print the total divided by n, dropping the decimal part.", "1. `n = int(input())`. 2. `nums = list(map(int, input().split()))`. 3. `print(sum(nums) // n)`."])

# ---------- 14 strings ----------
def wordfn(lesson, id, title, diff, statement, outfmt, sample, hidden, solution, hints):
    add(lesson, id, title, diff, statement, "One line holding a word of small letters, with no spaces.", outfmt, [sample], hidden, "def solve(word):\n", STUB, '\nif __name__ == "__main__":\n    word = input()\n    print(solve(word))\n', solution, hints)
wordfn("strings", "str_ends", "First and last letter", "Easy", ["Return the first letter and the last letter of `word` joined together. The symbol `+` joins two pieces of text. The word has at least 2 letters."],
 "One line: two letters.", ("planet\n", "pt", "The first letter is p and the last is t."), ["ab\n", "level\n", "builder\n"],
 '    return word[0] + word[-1]\n',
 ["Text has positions like a list.", "The first letter is at position 0 and the last at position -1.", "Return word[0] joined with word[-1] using +.", "1. Write `return` then `word[0] + word[-1]`, indented by 4 spaces."])
wordfn("strings", "str_reverse", "Reverse a word", "Easy", ["Return `word` written backwards."], "One line: the reversed word.",
 ("stone\n", "enots", "The letters in the opposite order."), ["a\n", "ab\n", "racecar\n"],
 '    return word[::-1]\n',
 ["Slices work on text too.", "The backwards slice is the same one as for lists.", "Return word with the step -1 slice.", "1. Write `return` then `word[::-1]`, indented by 4 spaces."])
wordfn("strings", "str_palindrome", "Same backwards", "Medium", ["A palindrome reads the same forwards and backwards. Return `True` if `word` is one, otherwise `False`."], "`True` or `False`.",
 ("level\n", "True", "level backwards is level."), ["abc\n", "a\n", "noon\n", "ab\n"],
 '    return word == word[::-1]\n',
 ["Compare the word with its reverse.", "A reversed copy is word[::-1]. Ask whether it equals the word.", "Return the answer to: is word equal to word reversed.", "1. Write `return` then `word == word[::-1]`, indented by 4 spaces."])
wordfn("strings", "str_vowels", "Count the vowels", "Medium", ["Return how many letters in `word` are vowels. The vowels are `a`, `e`, `i`, `o` and `u`.", "The word `in` asks whether something is found inside something else. For example `'a' in 'aeiou'` is True."], "One number.",
 ("education\n", "5", "e, u, a, i, o are vowels."), ["xyz\n", "aeiou\n", "builder\n"],
 '    count = 0\n    for letter in word:\n        if letter in "aeiou":\n            count = count + 1\n    return count\n',
 ["A for loop can go through the letters of a word.", "Loop over word. For each letter, check whether it is inside the text aeiou.", "Set count to 0. For each letter in word, if the letter is in \"aeiou\", add 1 to count. Return count.", "1. `count = 0`. 2. `for letter in word:`. 3. Indented: `if letter in \"aeiou\":`. 4. Indented twice: `count = count + 1`. 5. `return count`, indented 4 spaces."])
