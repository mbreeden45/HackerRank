# Phase 2 problems, part 1: hashmaps, sorting, strings and parsing.
# Sample outputs are written by hand. Hidden outputs come from running the reference solution (build_content.py).
from c_kit import Kit
K = Kit()
PROBLEMS = K.PROBLEMS
fp = K.fp

# ---------------- hashmaps ----------------
fp("hashmaps", "hm_lookup", "Phone book", "Easy",
 ["Each line holds a name and a phone number separated by a space. Build a phone book, then look up the name `query`.", "Print the number for that name. If the name is not in the book, print `not found`. If a name appears twice, the later line wins."],
 [("lines", "lines"), ("query", "str")], "One line: the number, or `not found`.",
 [((["ana 555", "bo 777", "cy 123"], "bo"), "777", "The book is ana 555, bo 777, cy 123. Looking up bo gives 777.")],
 [(["ana 555", "bo 777"], "zed"), (["ana 1", "ana 2"], "ana"), (["x 9"], "x")],
 '    book = {}\n    for line in lines:\n        name, number = line.split()\n        book[name] = number\n    return book.get(query, "not found")\n',
 ["A dictionary lets you look up a value by name.", "Make an empty dictionary with `{}`. For each line, split it into a name and a number, and store the number under the name.", "Build the dictionary first. Then ask for `query`, using get with a fallback so a missing name does not crash.", "book = {}; for each line: name, number = line.split(); book[name] = number; return book.get(query, \"not found\")."])

fp("hashmaps", "hm_distinct", "How many different", "Easy",
 ["Count how many different numbers appear in the list. Repeats count once."],
 [("nums", "ints")], "One whole number.",
 [(([4, 4, 7, 1, 7],), "3", "The different numbers are 4, 7 and 1, so the answer is 3.")],
 [([5],), ([2, 2, 2, 2],), ([1, 2, 3, 4, 5, 6],), ([9, -9, 9, -9, 0],)],
 '    seen = {}\n    for x in nums:\n        seen[x] = True\n    return len(seen)\n',
 ["A dictionary cannot hold the same key twice.", "If you store every number as a key, repeats land on the same key. Then count the keys.", "Make an empty dictionary. Put each number in as a key. At the end, the number of keys is the answer.", "seen = {}; for x in nums: seen[x] = True; return len(seen)."])

fp("hashmaps", "hm_first_repeat", "First repeat", "Easy",
 ["Go through the list from left to right. Print the first number that you have already seen earlier in the list. If no number repeats, print `-1`."],
 [("nums", "ints")], "One whole number.",
 [(([3, 1, 4, 1, 3],), "1", "Going left to right, the second 1 is the first number we have seen before. The second 3 comes later.")],
 [([1, 2, 3],), ([5, 5],), ([7, 8, 9, 8, 7, 9],), ([2],)],
 '    seen = {}\n    for x in nums:\n        if x in seen:\n            return x\n        seen[x] = True\n    return -1\n',
 ["You need a memory of what you have already seen.", "A dictionary can be that memory. Before storing a number, ask whether it is already in the dictionary.", "Loop through the numbers. If the number is already a key, that is the answer. Otherwise store it and carry on. If the loop ends, answer -1.", "for x in nums: if x in seen: return x; seen[x] = True. After the loop: return -1."])

fp("hashmaps", "hm_most_common", "Most common word", "Medium",
 ["Print the word that appears most often. If two words appear the same number of times, print the one that comes first in alphabetical order."],
 [("words", "words")], "One word.",
 [((["red", "blue", "red", "green", "blue", "red"],), "red", "red appears 3 times, blue 2 times and green once."),
  ((["b", "a", "b", "a"],), "a", "a and b each appear twice, so the alphabetical first, a, wins.")],
 [(["x"],), (["z", "y", "z", "y", "x"],), (["pear", "apple", "pear", "fig", "apple", "fig"],), (["one", "two", "two", "three", "three", "three"],)],
 '    counts = {}\n    for w in words:\n        counts[w] = counts.get(w, 0) + 1\n    best = None\n    for w in sorted(counts):\n        if best is None or counts[w] > counts[best]:\n            best = w\n    return best\n',
 ["First count how often each word appears.", "Count with `counts[w] = counts.get(w, 0) + 1`. Then look for the biggest count. Visiting the words in alphabetical order helps with ties.", "Build the counts. Then go through the words in alphabetical order, and only replace your best word when a word has a strictly bigger count.", "counts = {}; for w in words: counts[w] = counts.get(w, 0) + 1; best = None; for w in sorted(counts): if best is None or counts[w] > counts[best]: best = w."])

# two numbers add up: make sure the answer is unique so any correct solution gives the same output
def _pairs(nums, t):
    return [(i, j) for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] + nums[j] == t]
for _n, _t in [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([3, 3], 6), ([-1, -2, -3, -4, -5], -8), ([1, 5, 9, 14, 20], 29), ([8, 1, 6, 3], 4)]:
    assert len(_pairs(_n, _t)) == 1, (_n, _t)

fp("hashmaps", "hm_two_sum", "Two numbers that add up", "Medium",
 ["Find the two positions `i` and `j` (with `i` smaller than `j`) where `nums[i] + nums[j]` equals `target`. Print `i` then `j`, separated by a space.", "Exactly one pair of positions works."],
 [("nums", "ints"), ("target", "int")], "Two whole numbers separated by a space: the smaller position first.",
 [(([2, 7, 11, 15], 9), "0 1", "nums[0] is 2 and nums[1] is 7, and 2 + 7 is 9.")],
 [([3, 2, 4], 6), ([3, 3], 6), ([-1, -2, -3, -4, -5], -8), ([1, 5, 9, 14, 20], 29), ([8, 1, 6, 3], 4)],
 '    seen = {}\n    for i in range(len(nums)):\n        need = target - nums[i]\n        if need in seen:\n            return [seen[need], i]\n        seen[nums[i]] = i\n    return []\n',
 ["For each number, there is exactly one other number that would complete the pair.", "If the current number is x, the partner you want is target - x. Keep a dictionary from number to position for the numbers already passed.", "Loop over positions. Work out the partner. If the partner is already in the dictionary, you have the answer. Otherwise store this number with its position.", "for i in range(len(nums)): need = target - nums[i]; if need in seen: return [seen[need], i]; seen[nums[i]] = i."],
 "2 to 1000 numbers.")

fp("hashmaps", "hm_anagram", "Same letters", "Medium",
 ["Two words are anagrams when they use exactly the same letters the same number of times, in any order. Print `True` if `a` and `b` are anagrams, otherwise print `False`."],
 [("a", "str"), ("b", "str")], "`True` or `False`.",
 [(("listen", "silent"), "True", "Both words have one each of e, i, l, n, s and t."),
  (("aab", "abb"), "False", "aab has two a and one b, but abb has one a and two b.")],
 [("abc", "abd"), ("aab", "aba"), ("a", "aa"), ("stressed", "desserts")],
 '    counts_a = {}\n    for ch in a:\n        counts_a[ch] = counts_a.get(ch, 0) + 1\n    counts_b = {}\n    for ch in b:\n        counts_b[ch] = counts_b.get(ch, 0) + 1\n    return counts_a == counts_b\n',
 ["Count the letters in each word.", "Make one dictionary of letter counts for each word. Two dictionaries with the same keys and values are equal when you compare them with `==`.", "Build counts for a, build counts for b, and answer whether the two dictionaries are equal.", "counts_a = {}; for ch in a: counts_a[ch] = counts_a.get(ch, 0) + 1; the same for b; return counts_a == counts_b."])

fp("hashmaps", "hm_group_sum", "Totals per person", "Medium",
 ["Each line holds a name and a whole number, separated by a space. Add up the numbers for each name.", "Print one item per name, in alphabetical order of the name, written as `name:total` and separated by spaces."],
 [("lines", "lines")], "One line of `name:total` items separated by spaces.",
 [((["bo 5", "ana 7", "ana 5"],), "ana:12 bo:5", "ana has 7 and 5, which makes 12. bo has 5. Alphabetical order puts ana first.")],
 [(["z 1"],), (["cy 4", "bo 4", "cy -1", "bo 2"],), (["x 10", "x 10", "x 10"],), (["b 1", "a 2", "c 3", "b 4"],)],
 '    totals = {}\n    for line in lines:\n        name, amount = line.split()\n        totals[name] = totals.get(name, 0) + int(amount)\n    result = []\n    for name in sorted(totals):\n        result.append(name + ":" + str(totals[name]))\n    return result\n',
 ["This is counting, but you add an amount instead of 1.", "Split each line, turn the amount into a number with int, and add it to the total stored under that name.", "Fill a dictionary of totals. Then go through the sorted names and build the text name:total for each.", "totals[name] = totals.get(name, 0) + int(amount); then for name in sorted(totals): result.append(name + \":\" + str(totals[name]))."])

fp("hashmaps", "hm_subarray_sum", "Blocks that add up", "Hard",
 ["A block is one or more neighbouring numbers. Count how many blocks have a total exactly equal to `k`."],
 [("nums", "ints"), ("k", "int")], "One whole number.",
 [(([1, 1, 1], 2), "2", "The blocks [1, 1] at positions 0 to 1 and at positions 1 to 2 both total 2."),
  (([1, 2, 3], 3), "2", "The blocks [1, 2] and [3] both total 3.")],
 [([5], 5), ([5], 4), ([1, -1, 1, -1], 0), ([3, 4, 7, 2, -3, 1, 4, 2], 7), ([0, 0, 0], 0)],
 '    counts = {0: 1}\n    running = 0\n    answer = 0\n    for x in nums:\n        running += x\n        answer += counts.get(running - k, 0)\n        counts[running] = counts.get(running, 0) + 1\n    return answer\n',
 ["Keep a running total as you go. The total of a block is the difference of two running totals.", "If the running total now is R, a block ending here has total k exactly when an earlier running total was R - k. Count how many times each running total has appeared.", "Start with counts of {0: 1}, meaning the empty start. For each number, update the running total, add how many earlier totals equal running - k, then record the running total.", "counts = {0: 1}; running = 0; answer = 0; for x in nums: running += x; answer += counts.get(running - k, 0); counts[running] = counts.get(running, 0) + 1."],
 "Numbers may be negative, so a loop inside a loop is too slow on big lists.")

# ---------------- sorting ----------------
fp("sorting", "sort_ascending", "Smallest to largest", "Easy",
 ["Print the numbers in order from smallest to largest, separated by spaces."],
 [("nums", "ints")], "The numbers in order, separated by spaces.",
 [(([5, 2, 9, 1],), "1 2 5 9", "Smallest is 1, then 2, then 5, then 9.")],
 [([3],), ([2, 2, 1],), ([-4, 8, 0, -9],), ([10, 9, 8, 7, 6],)],
 '    return sorted(nums)\n',
 ["Python has a tool that puts a list in order.", "sorted(nums) gives back a new list in order. Remember that solve must return it.", "Return the sorted version of nums.", "return sorted(nums)."])

fp("sorting", "sort_top3", "Top three", "Easy",
 ["Print the three biggest numbers, biggest first, separated by spaces. If there are fewer than three numbers, print all of them."],
 [("nums", "ints")], "Up to three numbers, biggest first.",
 [(([4, 9, 1, 7, 3],), "9 7 4", "In order from biggest the list is 9, 7, 4, 3, 1. The first three are 9, 7 and 4.")],
 [([1, 2],), ([5],), ([3, 3, 3, 3],), ([10, 40, 30, 20, 50, 60],)],
 '    ordered = sorted(nums, reverse=True)\n    return ordered[:3]\n',
 ["Sort so that the biggest are at the front.", "sorted(nums, reverse=True) puts biggest first. A slice with [:3] takes the first three items and does not crash on short lists.", "Sort from biggest to smallest, then keep only the first three items.", "ordered = sorted(nums, reverse=True); return ordered[:3]."])

fp("sorting", "sort_kth_largest", "The kth largest", "Easy",
 ["Print the `k`th largest number. The 1st largest is the biggest, the 2nd largest is the next one, and so on. The list always has at least `k` numbers. Equal numbers count separately."],
 [("nums", "ints"), ("k", "int")], "One whole number.",
 [(([3, 1, 5, 2, 4], 2), "4", "In order from biggest: 5, 4, 3, 2, 1. The 2nd one is 4.")],
 [([7], 1), ([5, 5, 3], 2), ([1, 2, 3, 4], 4), ([9, 8, 7, 6, 5], 3)],
 '    ordered = sorted(nums, reverse=True)\n    return ordered[k - 1]\n',
 ["Sorting makes the answer easy to find.", "After sorting from biggest to smallest, the 1st largest sits at position 0. So the kth sits at position k - 1.", "Sort biggest first, then return the item at position k - 1.", "return sorted(nums, reverse=True)[k - 1]."])

fp("sorting", "sort_median", "The middle value", "Medium",
 ["The middle value is the one in the middle after the numbers are put in order. When there are two middle values (an even count), use the lower one.", "Print the middle value."],
 [("nums", "ints")], "One whole number.",
 [(([9, 1, 5],), "5", "In order: 1, 5, 9. The middle one is 5."),
  (([4, 1, 3, 2],), "2", "In order: 1, 2, 3, 4. Two middle values, 2 and 3. The lower one is 2.")],
 [([7],), ([2, 1],), ([5, 5, 1, 9, 9, 3],), ([10, 20, 30, 40, 50],)],
 '    ordered = sorted(nums)\n    return ordered[(len(ordered) - 1) // 2]\n',
 ["Sort first, then pick by position.", "With 5 items the middle is position 2. With 4 items the lower middle is position 1. Try (len - 1) // 2, where // divides and drops the remainder.", "Sort. Work out the middle position as (number of items - 1) // 2. Return the item there.", "ordered = sorted(nums); return ordered[(len(ordered) - 1) // 2]."])

fp("sorting", "sort_by_length", "Shortest words first", "Medium",
 ["Sort the words by length, shortest first. Words with the same length go in alphabetical order. Print the words separated by spaces."],
 [("words", "words")], "The words in the new order, separated by spaces.",
 [((["pear", "fig", "apple", "kiwi"],), "fig kiwi pear apple", "fig has 3 letters. kiwi and pear have 4, and kiwi comes first alphabetically. apple has 5.")],
 [(["a"],), (["bb", "a", "cc", "b"],), (["zebra", "ox", "cat", "dog", "bee"],), (["same", "word", "mine"],)],
 '    return sorted(words, key=lambda w: (len(w), w))\n',
 ["A key can return a pair, so ties are broken by the second part.", "Use key=lambda w: (len(w), w). The pair is compared length first, then the word itself.", "Sort with a key that gives (length of the word, the word).", "return sorted(words, key=lambda w: (len(w), w))."])

fp("sorting", "sort_min_diff", "Closest two numbers", "Medium",
 ["Find the smallest difference between any two numbers in the list and print it. There are at least two numbers. The difference is the bigger number minus the smaller one."],
 [("nums", "ints")], "One whole number.",
 [(([8, 3, 15, 5],), "2", "In order: 3, 5, 8, 15. The differences between neighbours are 2, 3 and 7. The smallest is 2.")],
 [([1, 1],), ([10, 4],), ([1, 100, 50, 51],), ([-5, 0, 5, 4, -4],)],
 '    ordered = sorted(nums)\n    best = ordered[1] - ordered[0]\n    for i in range(1, len(ordered)):\n        gap = ordered[i] - ordered[i - 1]\n        if gap < best:\n            best = gap\n    return best\n',
 ["The two closest numbers must sit next to each other once the list is in order.", "Sort the list, then you only need to look at neighbours, not every pair.", "Sort. Start with the first gap as your best. Walk through the list comparing each item with the one before it.", "ordered = sorted(nums); best = ordered[1] - ordered[0]; for i in range(1, len(ordered)): gap = ordered[i] - ordered[i - 1]; keep the smallest."])

fp("sorting", "sort_by_score", "Leaderboard", "Medium",
 ["Each line holds a name and a score, separated by a space. Put the names in order from the highest score to the lowest. If two scores are equal, the name that comes first alphabetically goes first.", "Print the names separated by spaces."],
 [("lines", "lines")], "The names, best first, separated by spaces.",
 [((["ana 80", "bo 95", "cy 80"],), "bo ana cy", "bo has 95. ana and cy both have 80, and ana comes first alphabetically.")],
 [(["x 1"],), (["b 5", "a 5", "c 9"],), (["m 10", "n 20", "o 30", "p 20"],), (["z 0", "y 0", "x 0"],)],
 '    people = []\n    for line in lines:\n        name, score = line.split()\n        people.append((int(score), name))\n    people.sort(key=lambda p: (-p[0], p[1]))\n    names = []\n    for score, name in people:\n        names.append(name)\n    return names\n',
 ["Sort pairs, and flip the sign of the score so that big scores come first.", "Store (score, name) pairs with the score as a number. In the key, use -score for the high-first part and name for the tie-break.", "Parse each line into a pair. Sort with key=lambda p: (-p[0], p[1]). Collect the names in order.", "people.append((int(score), name)); people.sort(key=lambda p: (-p[0], p[1])); then take the name from each pair."])

fp("sorting", "sort_intervals", "Overlapping spans", "Hard",
 ["Each line holds the start and end of a span, as two whole numbers separated by a space. Two spans overlap when the second starts at or before the point where the first ends. Overlapping spans merge into one bigger span.", "Print how many spans are left after all overlapping spans are merged."],
 [("lines", "lines")], "One whole number.",
 [((["1 3", "2 6", "8 10", "15 18"],), "3", "1 to 3 and 2 to 6 overlap and merge into 1 to 6. The others stand alone, so 3 spans remain."),
  ((["1 4", "4 5"],), "1", "The first ends at 4 and the second starts at 4, so they touch and merge.")],
 [(["5 6"],), (["1 2", "3 4", "5 6"],), (["1 10", "2 3", "4 5"],), (["6 8", "1 9", "2 4", "4 7"],), (["10 12", "1 3", "2 11"],)],
 '    spans = []\n    for line in lines:\n        a, b = line.split()\n        spans.append([int(a), int(b)])\n    spans.sort()\n    groups = 0\n    current_end = None\n    for start, end in spans:\n        if current_end is None or start > current_end:\n            groups += 1\n            current_end = end\n        else:\n            current_end = max(current_end, end)\n    return groups\n',
 ["If the spans are in order of their start, you only need to compare each one with the group before it.", "Sort the spans by start. Keep track of where the current group ends. A new span either starts after that end (a new group) or reaches into it (it joins, and may push the end further).", "Sort. Walk through. If the span starts after current_end, count a new group and set current_end to its end. Otherwise set current_end to the bigger of the two ends.", "spans.sort(); for start, end in spans: if current_end is None or start > current_end: groups += 1; current_end = end; else: current_end = max(current_end, end)."])

# ---------------- strings: text tools ----------------
fp("strtools", "st_initials", "Initials", "Easy",
 ["Print the capital initials of the words in the name. For example `ada lovelace byron` gives `ALB`."],
 [("name", "str")], "The initials as one word of capital letters.",
 [(("ada lovelace byron",), "ALB", "The first letters are a, l and b. Made capital they are A, L and B.")],
 [("grace hopper",), ("x",), ("mary jane watson parker",), ("Alan Turing",)],
 '    words = name.split()\n    letters = ""\n    for w in words:\n        letters += w[0].upper()\n    return letters\n',
 ["Cut the name into words first.", "name.split() gives a list of words. w[0] is the first letter of w and w[0].upper() makes it capital.", "Split the name. Start with an empty text. For each word, glue its first letter, made capital, on the end.", "words = name.split(); letters = \"\"; for w in words: letters += w[0].upper(); return letters."])

fp("strtools", "st_clean_spaces", "Tidy the spaces", "Easy",
 ["The text may have extra spaces at the start, at the end, or several spaces in a row between words. Print the text with exactly one space between words and no spaces at the ends."],
 [("text", "str")], "The tidy text on one line.",
 [(("  hello    big   world ",), "hello big world", "Splitting on spaces drops the extras. Joining with one space gives hello big world.")],
 [("one",), ("a   b",), ("   spaced     out   text   ",), ("no extras here",)],
 '    return " ".join(text.split())\n',
 ["Two tools work together here.", "split() with nothing inside the brackets cuts on any run of spaces and ignores the ends. join glues the pieces back.", "Cut the text into words, then glue the words together with a single space.", "return \" \".join(text.split())."])

fp("strtools", "st_censor", "Hide a word", "Easy",
 ["Replace every appearance of the word `bad` in `text` with stars. Use one star for each letter of `bad`. Print the new text."],
 [("text", "str"), ("bad", "str")], "The new text on one line.",
 [(("the cat sat on the cat mat", "cat"), "the *** sat on the *** mat", "cat has 3 letters, so each cat becomes three stars.")],
 [("hello world", "lo"), ("aaa", "a"), ("no match here", "zzz"), ("abcabc", "bc")],
 '    stars = "*" * len(bad)\n    return text.replace(bad, stars)\n',
 ["replace swaps one piece of text for another.", "You can repeat text with a number: \"*\" * 3 gives \"***\". Use len(bad) for how many.", "Build the stars first. Then replace bad with the stars.", "stars = \"*\" * len(bad); return text.replace(bad, stars)."])

fp("strtools", "st_longest_word", "Longest word", "Medium",
 ["Print the longest word. If two words are equally long, print the one that comes first in the line."],
 [("words", "words")], "One word.",
 [((["a", "quick", "brown", "fox"],), "quick", "quick and brown both have 5 letters. quick comes first, so it wins.")],
 [(["x"],), (["aa", "b", "cc"],), (["tiny", "enormous", "big", "gigantic"],), (["hi", "hello", "world"],)],
 '    best = words[0]\n    for w in words:\n        if len(w) > len(best):\n            best = w\n    return best\n',
 ["Keep the best word you have seen so far.", "Start with the first word as your best. Only replace it when a word is strictly longer, not equal.", "Loop over the words. If the current word is longer than best, it becomes the new best.", "best = words[0]; for w in words: if len(w) > len(best): best = w; return best."])

# ---------------- parsing ----------------
fp("parsing", "pa_kv", "Find a setting", "Easy",
 ["A record is written as pairs like `name=Ana;age=30;city=Rome`. Pairs are separated by semicolons, and inside each pair the key and value are separated by an equals sign.", "Print the value for the key `key`. If the key is not in the record, print `missing`."],
 [("record", "str"), ("key", "str")], "The value, or `missing`.",
 [(("name=Ana;age=30;city=Rome", "age"), "30", "Cutting at semicolons gives three pairs. The pair age=30 has the key age and the value 30.")],
 [("a=1", "a"), ("a=1;b=2", "c"), ("x=10;y=20;z=30", "z"), ("k=v;kk=vv", "kk")],
 '    pairs = record.split(";")\n    for p in pairs:\n        k, v = p.split("=")\n        if k == key:\n            return v\n    return "missing"\n',
 ["Cut in two stages: first into pairs, then each pair into key and value.", "record.split(\";\") gives the pairs. Then p.split(\"=\") on one pair gives its two pieces, which you can name k and v.", "Split into pairs. For each pair, split at the equals sign. If the key matches, return the value. If nothing matched, return missing.", "for p in record.split(\";\"): k, v = p.split(\"=\"); if k == key: return v. After the loop: return \"missing\"."])

fp("parsing", "pa_csv_total", "Comma list total", "Easy",
 ["The text holds whole numbers separated by commas, such as `3,5,10`. Print their total."],
 [("text", "str")], "One whole number.",
 [(("3,5,10",), "18", "3 + 5 + 10 is 18.")],
 [("7",), ("1,1,1,1",), ("-5,5",), ("100,200,300,400",)],
 '    total = 0\n    for part in text.split(","):\n        total += int(part)\n    return total\n',
 ["The numbers arrive as text pieces.", "text.split(\",\") cuts at commas. Each piece is still text, so convert it with int before adding.", "Start a total at 0. For each piece, convert to a number and add it.", "total = 0; for part in text.split(\",\"): total += int(part); return total."])

fp("parsing", "pa_log_errors", "Count the errors", "Medium",
 ["Each line is a log message that starts with a level word, then the message, for example `ERROR disk full`. Count the lines whose level is exactly `ERROR`.", "Be careful: a line such as `ERRORS were fixed` has the first word `ERRORS`, which is not the same as `ERROR`."],
 [("lines", "lines")], "One whole number.",
 [((["INFO started", "ERROR disk full", "WARN slow", "ERROR timeout"],), "2", "Two lines start with the word ERROR.")],
 [(["INFO ok"],), (["ERROR a", "ERROR b", "ERROR c"],), (["ERRORS fixed", "ERROR real", "info ERROR"],), (["WARN x", "INFO y"],)],
 '    count = 0\n    for line in lines:\n        level = line.split()[0]\n        if level == "ERROR":\n            count += 1\n    return count\n',
 ["Look only at the first word of each line.", "line.split() gives the words. The first word is at position 0, so line.split()[0].", "Loop over the lines. Take the first word. If it equals ERROR, add 1 to a counter.", "count = 0; for line in lines: level = line.split()[0]; if level == \"ERROR\": count += 1; return count."])

fp("parsing", "pa_duration", "Minutes between times", "Medium",
 ["Two times are written as `HH:MM` using a 24 hour clock, such as `09:30`. Print how many minutes pass from `start` to `end`. The end is later on the same day."],
 [("start", "str"), ("end", "str")], "One whole number of minutes.",
 [(("09:30", "11:05"), "95", "09:30 is 570 minutes after midnight and 11:05 is 665. The difference is 95.")],
 [("00:00", "00:01"), ("12:00", "12:00"), ("08:15", "17:45"), ("00:00", "23:59")],
 '    sh, sm = start.split(":")\n    eh, em = end.split(":")\n    start_minutes = int(sh) * 60 + int(sm)\n    end_minutes = int(eh) * 60 + int(em)\n    return end_minutes - start_minutes\n',
 ["Turn each time into one number: minutes since midnight.", "Cut at the colon to get hours and minutes. Hours times 60 plus minutes gives minutes since midnight. int(\"09\") works and gives 9.", "Convert both times to minutes since midnight, then subtract.", "sh, sm = start.split(\":\"); start_minutes = int(sh) * 60 + int(sm); the same for end; return end_minutes - start_minutes."])

# ---------------- characters ----------------
fp("chars", "ch_digit_sum", "Add the digits", "Easy",
 ["The text mixes letters and digits, such as `a1b22c`. Add up the digits only, treating each digit character as its own number. Print the total."],
 [("text", "str")], "One whole number.",
 [(("a1b22c",), "5", "The digits are 1, 2 and 2. Together they make 5.")],
 [("abc",), ("9",), ("x9y9z9",), ("1234567890",)],
 '    total = 0\n    for ch in text:\n        if ch.isdigit():\n            total += int(ch)\n    return total\n',
 ["Check each character on its own.", "ch.isdigit() tells you if a character is a digit. int(ch) turns a digit character into a number.", "Loop over the characters. When a character is a digit, add int(ch) to a total.", "total = 0; for ch in text: if ch.isdigit(): total += int(ch); return total."])

fp("chars", "ch_caesar", "Shift the letters", "Medium",
 ["Shift every lowercase letter forward in the alphabet by `shift` places. After z, wrap round to a. Spaces stay as they are. Print the new text.", "The shift is between 0 and 25."],
 [("text", "str"), ("shift", "int")], "The shifted text on one line.",
 [(("abc xyz", 2), "cde zab", "a becomes c, b becomes d, c becomes e. x becomes z, y wraps to a and z wraps to b.")],
 [("a", 0), ("hello world", 13), ("zebra", 1), ("the quick brown fox", 25)],
 '    result = ""\n    for ch in text:\n        if ch == " ":\n            result += ch\n        else:\n            place = ord(ch) - ord("a")\n            result += chr((place + shift) % 26 + ord("a"))\n    return result\n',
 ["Turn each letter into its place in the alphabet, shift, and turn it back.", "ord(ch) - ord(\"a\") gives the place from 0 to 25. Add the shift, then use % 26 to wrap around. chr(place + ord(\"a\")) goes back to a letter.", "For each character: if it is a space, keep it. Otherwise work out the new place with (place + shift) % 26 and add the matching letter to the result.", "place = ord(ch) - ord(\"a\"); result += chr((place + shift) % 26 + ord(\"a\"))."])

fp("chars", "ch_compress", "Squash repeats", "Medium",
 ["Replace each run of the same letter with the letter followed by how long the run is. For example `aaabbc` becomes `a3b2c1`. The text is not empty."],
 [("s", "str")], "The squashed text.",
 [(("aaabbc",), "a3b2c1", "There are three a, then two b, then one c.")],
 [("a",), ("abc",), ("aaaa",), ("aabbaa",), ("zzzzzzzzzzy",)],
 '    result = ""\n    count = 1\n    for i in range(1, len(s)):\n        if s[i] == s[i - 1]:\n            count += 1\n        else:\n            result += s[i - 1] + str(count)\n            count = 1\n    result += s[-1] + str(count)\n    return result\n',
 ["Compare each character with the one before it.", "Keep a counter for the current run. When the letter changes, write the previous letter and its count, and restart the counter at 1.", "Loop from position 1. If s[i] equals s[i - 1], add 1 to count. Otherwise add the previous letter and the count to the result, and set count back to 1. When the loop ends, the last run is still waiting to be written.", "result += s[i - 1] + str(count) when the letter changes; after the loop, result += s[-1] + str(count)."])

fp("chars", "ch_password", "Check a password", "Medium",
 ["A password is `valid` when it has at least 8 characters, at least one digit and at least one capital letter. Print `valid` or `invalid`."],
 [("s", "str")], "`valid` or `invalid`.",
 [(("Passw0rdX",), "valid", "It has 9 characters, a digit 0 and a capital P."),
  (("password1",), "invalid", "It has a digit and 9 characters, but no capital letter.")],
 [("Ab1",), ("ABCDEFG1",), ("abcdefgh",), ("Abcdefg1",), ("12345678",)],
 '    has_digit = False\n    has_capital = False\n    for ch in s:\n        if ch.isdigit():\n            has_digit = True\n        if ch.isupper():\n            has_capital = True\n    if len(s) >= 8 and has_digit and has_capital:\n        return "valid"\n    return "invalid"\n',
 ["Check three separate rules.", "Use two True or False variables, one for digit and one for capital, both starting as False. Loop over the characters and switch them to True when you find one.", "Loop over the characters, setting has_digit and has_capital. After the loop, test all three rules together with and.", "if len(s) >= 8 and has_digit and has_capital: return \"valid\", otherwise return \"invalid\"."])
