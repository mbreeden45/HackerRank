# Phase 2 problems, part 2: two pointers, sliding window, 2D grids.
from c_kit import Kit
K = Kit()
PROBLEMS = K.PROBLEMS
fp = K.fp

# ---------------- two pointers ----------------
fp("twopointers", "tp_reverse", "Reverse a word", "Easy",
 ["Print the word `s` backwards. Use two pointers: swap the first and last letters, then move inward."],
 [("s", "str")], "The reversed word.",
 [(("hello",), "olleh", "Swapping the ends h and o, then e and l, leaves the middle l alone.")],
 [("a",), ("ab",), ("racecar",), ("python",), ("abcde",)],
 '    chars = list(s)\n    left = 0\n    right = len(chars) - 1\n    while left < right:\n        temp = chars[left]\n        chars[left] = chars[right]\n        chars[right] = temp\n        left += 1\n        right -= 1\n    return "".join(chars)\n',
 ["Text cannot be changed in place, but a list can.", "list(s) turns the word into a list of letters. Put left at 0 and right at the last position, and swap while left is before right.", "Make a list of letters. Swap the two ends, move both pointers inward, and repeat. Glue the letters back with join.", "chars = list(s); left = 0; right = len(chars) - 1; while left < right: swap chars[left] and chars[right]; left += 1; right -= 1; return \"\".join(chars)."])

fp("twopointers", "tp_mirror", "Mirrored pairs", "Easy",
 ["Pair up the first number with the last, the second with the second to last, and so on. Count how many pairs hold two equal numbers. A middle number with no partner is not counted."],
 [("nums", "ints")], "One whole number.",
 [(([1, 2, 3, 2, 1],), "2", "The pairs are 1 and 1, then 2 and 2. The 3 in the middle has no partner. Both pairs match, so the answer is 2.")],
 [([5],), ([1, 2],), ([4, 4],), ([1, 2, 3, 4, 5, 6],), ([7, 1, 8, 1, 7, 9],)],
 '    left = 0\n    right = len(nums) - 1\n    count = 0\n    while left < right:\n        if nums[left] == nums[right]:\n            count += 1\n        left += 1\n        right -= 1\n    return count\n',
 ["One pointer starts at each end.", "Compare nums[left] and nums[right], then move both inward. Stop when left is no longer before right.", "Set left to 0 and right to the last position. While left < right, add 1 to a counter if the numbers match, then move both pointers.", "while left < right: if nums[left] == nums[right]: count += 1; left += 1; right -= 1."])

fp("twopointers", "tp_pair_sum_sorted", "Pair with a target", "Easy",
 ["The numbers are already in order from smallest to largest. Is there a pair of numbers at two different positions that add up to `target`? Print `True` or `False`."],
 [("nums", "ints"), ("target", "int")], "`True` or `False`.",
 [(([1, 3, 4, 6, 9], 13), "True", "4 + 9 is 13."),
  (([1, 3, 4, 6, 9], 2), "False", "The smallest possible total is 1 + 3 = 4, so 2 is not reachable.")],
 [([1, 2], 3), ([1, 2], 4), ([-3, -1, 0, 2, 5], 1), ([2, 2, 2], 4), ([1, 5, 8, 20], 28)],
 '    left = 0\n    right = len(nums) - 1\n    while left < right:\n        total = nums[left] + nums[right]\n        if total == target:\n            return True\n        elif total < target:\n            left += 1\n        else:\n            right -= 1\n    return False\n',
 ["Because the list is in order, a total that is too big tells you something.", "Start with the smallest and the biggest. If the total is too small, only moving left up can make it bigger. If it is too big, only moving right down can make it smaller.", "Put left at the start and right at the end. Add the two numbers. Equal to target means True. Too small means left += 1. Too big means right -= 1. If the pointers meet, answer False.", "while left < right: total = nums[left] + nums[right]; if total == target: return True; elif total < target: left += 1; else: right -= 1. After the loop: return False."])

fp("twopointers", "tp_merge_sorted", "Merge two ordered lists", "Medium",
 ["Both lists are already in order, smallest first. Print all the numbers from both lists together, in order, separated by spaces."],
 [("first", "ints"), ("second", "ints")], "All the numbers in order, separated by spaces.",
 [(([1, 4, 7], [2, 3, 9]), "1 2 3 4 7 9", "Take the smaller front number each time: 1, then 2, then 3, then 4, then 7, then 9.")],
 [([5], [1]), ([1, 2, 3], [4, 5]), ([2, 2], [2]), ([-5, 0, 10], [-6, 1, 11, 12])],
 '    i = 0\n    j = 0\n    result = []\n    while i < len(first) and j < len(second):\n        if first[i] <= second[j]:\n            result.append(first[i])\n            i += 1\n        else:\n            result.append(second[j])\n            j += 1\n    result += first[i:]\n    result += second[j:]\n    return result\n',
 ["Use one pointer for each list.", "Compare the numbers the two pointers point at. Take the smaller one and move only that pointer. When one list runs out, the rest of the other list can be added in one go.", "Start i and j at 0. While both lists have items left, add the smaller front item to the result and move its pointer. Then add whatever is left over from each list.", "while i < len(first) and j < len(second): if first[i] <= second[j]: append first[i]; i += 1 else: append second[j]; j += 1. Then result += first[i:] and result += second[j:]."])

fp("twopointers", "tp_palindrome_clean", "Palindrome in a sentence", "Medium",
 ["A palindrome reads the same forwards and backwards. For sentences, ignore capital letters and ignore everything that is not a letter or a digit. Print `True` if the text is a palindrome under those rules, otherwise `False`."],
 [("s", "str")], "`True` or `False`.",
 [(("A man, a plan, a canal: Panama",), "True", "Ignoring spaces, commas and capitals this reads amanaplanacanalpanama, the same both ways."),
  (("race a car",), "False", "It becomes raceacar, which backwards is racaecar.")],
 [("a",), ("ab",), ("No lemon, no melon",), ("..",), ("0P",)],
 '    left = 0\n    right = len(s) - 1\n    while left < right:\n        if not s[left].isalnum():\n            left += 1\n        elif not s[right].isalnum():\n            right -= 1\n        elif s[left].lower() != s[right].lower():\n            return False\n        else:\n            left += 1\n            right -= 1\n    return True\n',
 ["Skip over characters that do not count.", "s[left].isalnum() is True for a letter or a digit. If the left character does not count, move left. If the right one does not count, move right. Otherwise compare them in lower case.", "Pointers at both ends. If left is junk, left += 1. Else if right is junk, right -= 1. Else compare the two in lower case: different means False, same means move both.", "while left < right: if not s[left].isalnum(): left += 1; elif not s[right].isalnum(): right -= 1; elif s[left].lower() != s[right].lower(): return False; else: move both. Then return True."])

fp("twopointers", "tp_remove_dups", "Remove repeats", "Medium",
 ["The numbers are in order, so equal numbers sit side by side. Print the numbers with every repeat removed, keeping the order."],
 [("nums", "ints")], "The different numbers in order, separated by spaces.",
 [(([1, 1, 2, 3, 3, 3],), "1 2 3", "Each different number is kept once.")],
 [([4],), ([2, 2, 2],), ([1, 2, 3],), ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4],)],
 '    slow = 0\n    for fast in range(1, len(nums)):\n        if nums[fast] != nums[slow]:\n            slow += 1\n            nums[slow] = nums[fast]\n    return nums[:slow + 1]\n',
 ["Use a slow pointer for where the next new number goes and a fast pointer that scans ahead.", "Both start at the left. When the fast pointer finds a number that differs from the one at slow, move slow up one and copy the number there.", "Set slow to 0. For fast from 1 to the end: if nums[fast] differs from nums[slow], add 1 to slow and copy nums[fast] into nums[slow]. At the end the good numbers are positions 0 to slow.", "slow = 0; for fast in range(1, len(nums)): if nums[fast] != nums[slow]: slow += 1; nums[slow] = nums[fast]; return nums[:slow + 1]."],
 "At least one number.")

fp("twopointers", "tp_container", "Most water", "Medium",
 ["The numbers are the heights of vertical walls placed one unit apart. Pick two walls. The water between them is as wide as the gap between their positions and as tall as the shorter wall. Print the biggest amount of water that any pair of walls can hold.", "For walls at positions `left` and `right`, the amount is `min(height at left, height at right) * (right - left)`."],
 [("heights", "ints")], "One whole number.",
 [(([1, 8, 6, 2, 5, 4, 8, 3, 7],), "49", "The walls of height 8 (position 1) and 7 (position 8) are 7 apart. The shorter is 7, and 7 times 7 is 49.")],
 [([1, 1],), ([4, 3, 2, 1, 4],), ([1, 2, 1],), ([5, 5, 5, 5],), ([2, 3, 4, 5, 18, 17, 6],)],
 '    left = 0\n    right = len(heights) - 1\n    best = 0\n    while left < right:\n        width = right - left\n        height = min(heights[left], heights[right])\n        if width * height > best:\n            best = width * height\n        if heights[left] < heights[right]:\n            left += 1\n        else:\n            right -= 1\n    return best\n',
 ["Start as wide as possible, and think about which wall to give up.", "The shorter wall limits the water. Moving the taller wall inward can only make the gap smaller without any chance of a taller limit, so move the shorter one.", "Start with the widest pair. Work out the amount and keep the best. Then move the pointer at the shorter wall inward, and repeat.", "while left < right: amount = min(heights[left], heights[right]) * (right - left); keep the best; if heights[left] < heights[right]: left += 1 else: right -= 1."])

fp("twopointers", "tp_three_sum", "Three that cancel out", "Hard",
 ["Count the different sets of three numbers, taken from three different positions, whose total is 0. Two sets are the same if they hold the same three numbers, whatever positions they came from."],
 [("nums", "ints")], "One whole number.",
 [(([-1, 0, 1, 2, -1, -4],), "2", "The sets are (-1, -1, 2) and (-1, 0, 1). That is 2 different sets.")],
 [([0, 0, 0],), ([1, 2, 3],), ([0, 0, 0, 0],), ([-2, 0, 1, 1, 2],), ([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],)],
 '    nums = sorted(nums)\n    count = 0\n    for i in range(len(nums) - 2):\n        if i > 0 and nums[i] == nums[i - 1]:\n            continue\n        left = i + 1\n        right = len(nums) - 1\n        while left < right:\n            total = nums[i] + nums[left] + nums[right]\n            if total == 0:\n                count += 1\n                left += 1\n                while left < right and nums[left] == nums[left - 1]:\n                    left += 1\n            elif total < 0:\n                left += 1\n            else:\n                right -= 1\n    return count\n',
 ["Sort first. Then fix one number and look for a pair that cancels it, like the pair-with-a-target problem.", "For each position i, the other two must add up to -nums[i]. Use left = i + 1 and right at the end, moving them as in the pair problem. To avoid counting a set twice, skip a number equal to the one before it. The word continue skips to the next round of the loop.", "Sort. For each i, skip it if it equals the previous number. Then run left and right inward. Total zero: count it and move left past any equal numbers. Total too small: left up. Too big: right down.", "for i in range(len(nums) - 2): if i > 0 and nums[i] == nums[i - 1]: continue; then the left and right loop; on total 0 do count += 1, left += 1, and skip equal numbers."],
 "Do not try every set of three: that is too slow for big lists.")

# ---------------- sliding window ----------------
fp("slidingwindow", "sw_max_sum_k", "Best block of k", "Easy",
 ["Find the biggest total of `k` neighbouring numbers and print it. The list always has at least `k` numbers."],
 [("nums", "ints"), ("k", "int")], "One whole number.",
 [(([2, 1, 5, 1, 3, 2], 3), "9", "The blocks of 3 total 8, 7, 9 and 6. The biggest is 9, from 5, 1, 3.")],
 [([4], 1), ([1, 2, 3, 4], 4), ([5, -1, -2, 6, 1], 2), ([1, 1, 1, 1, 1, 9], 3), ([-3, -2, -1], 2)],
 '    window = 0\n    for i in range(k):\n        window += nums[i]\n    best = window\n    for right in range(k, len(nums)):\n        window = window + nums[right] - nums[right - k]\n        if window > best:\n            best = window\n    return best\n',
 ["Do not add up every block from scratch.", "Add up the first k numbers. Then slide one step: add the number that enters and take away the number that leaves.", "Total the first k numbers and call that best. For each later position right, window becomes window + nums[right] - nums[right - k]. Keep the biggest.", "for right in range(k, len(nums)): window = window + nums[right] - nums[right - k]; if window > best: best = window."])

fp("slidingwindow", "sw_vowels_k", "Most vowels in k letters", "Easy",
 ["Look at every block of `k` neighbouring letters in the word. Print the biggest number of vowels (a, e, i, o, u) in any one block. The word has at least `k` letters."],
 [("s", "str"), ("k", "int")], "One whole number.",
 [(("abciiidef", 3), "3", "The block iii has three vowels.")],
 [("a", 1), ("bcd", 2), ("aeiou", 5), ("leetcode", 3), ("rhythms", 3)],
 '    vowels = "aeiou"\n    window = 0\n    for i in range(k):\n        if s[i] in vowels:\n            window += 1\n    best = window\n    for right in range(k, len(s)):\n        if s[right] in vowels:\n            window += 1\n        if s[right - k] in vowels:\n            window -= 1\n        if window > best:\n            best = window\n    return best\n',
 ["Keep a count of vowels in the current block as it slides.", "When the block moves, check the letter that enters. If it is a vowel add 1. Check the letter that leaves. If it is a vowel take away 1.", "Count the vowels in the first k letters. Then for each later position, update the count for the entering and leaving letters, and keep the biggest.", "if s[right] in vowels: window += 1; if s[right - k] in vowels: window -= 1; if window > best: best = window."])

fp("slidingwindow", "sw_count_windows", "Blocks that are big enough", "Easy",
 ["Count the blocks of `k` neighbouring numbers whose total is at least `t`."],
 [("nums", "ints"), ("k", "int"), ("t", "int")], "One whole number.",
 [(([2, 1, 5, 1, 3, 2], 3, 8), "2", "The blocks of 3 total 8, 7, 9 and 6. Two of them, 8 and 9, are at least 8.")],
 [([5], 1, 5), ([1, 2, 3], 2, 100), ([4, 4, 4, 4], 2, 8), ([1, -1, 1, -1, 1], 2, 0), ([10, 1, 10, 1, 10], 3, 21)],
 '    window = 0\n    for i in range(k):\n        window += nums[i]\n    count = 0\n    if window >= t:\n        count += 1\n    for right in range(k, len(nums)):\n        window = window + nums[right] - nums[right - k]\n        if window >= t:\n            count += 1\n    return count\n',
 ["This is the best-block problem again, but you count instead of keeping the biggest.", "Do not forget the very first block, which is made before the sliding starts.", "Total the first block and count it if it is big enough. Then slide, and count each new block that is big enough.", "if window >= t: count += 1, once for the first block and once inside the loop for each slide."])

fp("slidingwindow", "sw_min_len_sum", "Shortest big enough block", "Medium",
 ["All the numbers are positive. Find the length of the shortest block of neighbouring numbers whose total is at least `target`. If no block is big enough, print `0`."],
 [("nums", "ints"), ("target", "int")], "One whole number.",
 [(([2, 3, 1, 2, 4, 3], 7), "2", "The block 4, 3 totals 7 and has length 2. No single number reaches 7.")],
 [([1, 1, 1], 10), ([5], 5), ([1, 2, 3, 4, 5], 11), ([1, 4, 4], 4), ([2, 3, 1, 2, 4, 3], 15)],
 '    left = 0\n    total = 0\n    best = 0\n    for right in range(len(nums)):\n        total += nums[right]\n        while total >= target:\n            size = right - left + 1\n            if best == 0 or size < best:\n                best = size\n            total -= nums[left]\n            left += 1\n    return best\n',
 ["Grow the window on the right, and shrink it from the left as long as it is still big enough.", "Since all numbers are positive, taking one off the left only makes the total smaller. Keep shrinking while total >= target, and record the size each time.", "For each right, add nums[right] to total. While total >= target, record right - left + 1 if it is the smallest so far, then take nums[left] away and move left up.", "total += nums[right]; while total >= target: size = right - left + 1; update best (0 means none yet); total -= nums[left]; left += 1."])

fp("slidingwindow", "sw_longest_unique", "Longest without repeats", "Medium",
 ["Find the length of the longest block of neighbouring letters in which no letter appears twice. Print its length."],
 [("s", "str")], "One whole number.",
 [(("abcabcbb",), "3", "The block abc has no repeats and has length 3. No longer block avoids repeats.")],
 [("a",), ("bbbbb",), ("pwwkew",), ("abba",), ("dvdf",), ("abcdefg",)],
 '    last = {}\n    left = 0\n    best = 0\n    for right in range(len(s)):\n        ch = s[right]\n        if ch in last and last[ch] >= left:\n            left = last[ch] + 1\n        last[ch] = right\n        size = right - left + 1\n        if size > best:\n            best = size\n    return best\n',
 ["Remember where each letter was last seen.", "Use a dictionary from letter to its latest position. When the new letter was seen inside the current window, move left to just after that earlier position.", "For each right: if its letter was last seen at a position that is at or after left, set left to that position plus 1. Store the new position. Record the size.", "if ch in last and last[ch] >= left: left = last[ch] + 1; last[ch] = right; best = max of best and right - left + 1."])

fp("slidingwindow", "sw_ones_flip", "Flip some zeros", "Medium",
 ["The list holds only 0 and 1. You may change at most `k` of the zeros into ones. Print the length of the longest block of neighbouring ones you can make."],
 [("nums", "ints"), ("k", "int")], "One whole number.",
 [(([1, 1, 0, 0, 1, 1, 1, 0, 1], 1), "5", "Change the last zero to a one, and positions 4 to 8 become five ones in a row.")],
 [([0], 0), ([0], 1), ([1, 1, 1], 0), ([0, 0, 0, 0], 2), ([1, 0, 1, 0, 1, 0, 1], 2)],
 '    left = 0\n    zeros = 0\n    best = 0\n    for right in range(len(nums)):\n        if nums[right] == 0:\n            zeros += 1\n        while zeros > k:\n            if nums[left] == 0:\n                zeros -= 1\n            left += 1\n        size = right - left + 1\n        if size > best:\n            best = size\n    return best\n',
 ["Find the longest block that holds at most k zeros.", "Count the zeros inside the window. If the count goes over k, shrink from the left until it is back to k or fewer.", "For each right, add 1 to zeros if it is a zero. While zeros > k, if nums[left] is a zero take 1 off zeros, then move left up. Record the size.", "if nums[right] == 0: zeros += 1; while zeros > k: if nums[left] == 0: zeros -= 1; left += 1; best = max(best, right - left + 1)."])

fp("slidingwindow", "sw_distinct_in_window", "Most variety in a block", "Medium",
 ["Look at every block of `k` neighbouring numbers. Print the biggest number of different values found in any single block. The list has at least `k` numbers."],
 [("nums", "ints"), ("k", "int")], "One whole number.",
 [(([1, 2, 1, 3, 4, 2, 3], 4), "4", "The block 2, 1, 3, 4 holds four different values.")],
 [([5], 1), ([1, 1, 1, 1], 2), ([1, 2, 3, 4], 4), ([1, 2, 1, 2, 1, 2], 3), ([7, 7, 8, 9, 9, 8], 3)],
 '    counts = {}\n    best = 0\n    for right in range(len(nums)):\n        counts[nums[right]] = counts.get(nums[right], 0) + 1\n        if right >= k:\n            old = nums[right - k]\n            counts[old] -= 1\n            if counts[old] == 0:\n                del counts[old]\n        if len(counts) > best:\n            best = len(counts)\n    return best\n',
 ["Keep a dictionary of how many times each value is inside the window.", "When a value leaves, take 1 off its count. If the count reaches 0, remove the key so that len(counts) only counts values that are still inside. del counts[key] removes a key.", "Add the entering number. If the window now has more than k items, reduce the count of the leaving number and delete it at 0. After that, len(counts) is the variety.", "counts[nums[right]] = counts.get(nums[right], 0) + 1; if right >= k: remove nums[right - k]; best = max(best, len(counts))."])

fp("slidingwindow", "sw_at_most_k_distinct", "Longest with few kinds", "Hard",
 ["Find the length of the longest block of neighbouring letters that uses at most `k` different letters. Print its length."],
 [("s", "str"), ("k", "int")], "One whole number.",
 [(("eceba", 2), "3", "The block ece uses only the letters e and c, and has length 3.")],
 [("a", 1), ("aaaa", 1), ("abcabc", 2), ("aabacbebebe", 3), ("abaccc", 2)],
 '    counts = {}\n    left = 0\n    best = 0\n    for right in range(len(s)):\n        counts[s[right]] = counts.get(s[right], 0) + 1\n        while len(counts) > k:\n            counts[s[left]] -= 1\n            if counts[s[left]] == 0:\n                del counts[s[left]]\n            left += 1\n        size = right - left + 1\n        if size > best:\n            best = size\n    return best\n',
 ["Grow on the right and shrink on the left when the block has too many kinds of letter.", "Keep a dictionary of letter counts inside the window. When len(counts) is bigger than k, shrink from the left. A count that hits 0 must be deleted so it stops counting as a kind.", "For each right, add its letter. While len(counts) > k, take 1 off the leftmost letter's count, delete it at 0, and move left up. Then record the size.", "while len(counts) > k: counts[s[left]] -= 1; if counts[s[left]] == 0: del counts[s[left]]; left += 1; best = max(best, right - left + 1)."])

# ---------------- 2D grids ----------------
fp("grids", "gr_sum", "Add up the grid", "Easy",
 ["Print the total of all the numbers in the grid."],
 [("grid", "grid")], "One whole number.",
 [(([[1, 2, 3], [4, 5, 6]],), "21", "1 + 2 + 3 + 4 + 5 + 6 is 21.")],
 [([[7]],), ([[1, 1], [1, 1]],), ([[-1, 2], [3, -4], [5, 6]],), ([[0, 0, 0]],)],
 '    total = 0\n    for r in range(len(grid)):\n        for c in range(len(grid[0])):\n            total += grid[r][c]\n    return total\n',
 ["Visit every cell with a loop inside a loop.", "The outer loop picks a row with range(len(grid)). The inner loop walks across with range(len(grid[0])).", "Start a total at 0. For each row r and each column c, add grid[r][c].", "for r in range(len(grid)): for c in range(len(grid[0])): total += grid[r][c]."])

fp("grids", "gr_row_sums", "Total of each row", "Easy",
 ["Print the total of each row, from the top row to the bottom row, separated by spaces."],
 [("grid", "grid")], "One number for each row, separated by spaces.",
 [(([[1, 2, 3], [4, 5, 6]],), "6 15", "The first row totals 6 and the second row totals 15.")],
 [([[5]],), ([[1, 2], [3, 4], [5, 6]],), ([[0, 0, 0], [1, 1, 1]],), ([[-1, -1]],)],
 '    sums = []\n    for r in range(len(grid)):\n        row_total = 0\n        for c in range(len(grid[0])):\n            row_total += grid[r][c]\n        sums.append(row_total)\n    return sums\n',
 ["Restart the total at the beginning of each row.", "Make a new row_total of 0 inside the outer loop, before the inner loop. After the inner loop, save it in a list.", "For each row: set row_total to 0, add every cell of that row, then append row_total to the answer list.", "for r: row_total = 0; for c: row_total += grid[r][c]; sums.append(row_total)."])

fp("grids", "gr_col_max", "Biggest in each column", "Medium",
 ["Print the biggest number in each column, from left to right, separated by spaces."],
 [("grid", "grid")], "One number for each column, separated by spaces.",
 [(([[1, 9, 3], [4, 5, 6]],), "4 9 6", "Column 0 holds 1 and 4, column 1 holds 9 and 5, column 2 holds 3 and 6.")],
 [([[5]],), ([[1, 2], [3, 4], [5, 0]],), ([[-5, -6, -7]],), ([[1], [9], [4]],)],
 '    best = []\n    for c in range(len(grid[0])):\n        biggest = grid[0][c]\n        for r in range(len(grid)):\n            if grid[r][c] > biggest:\n                biggest = grid[r][c]\n        best.append(biggest)\n    return best\n',
 ["This time the outer loop goes over columns.", "To read down one column, keep c fixed and let r change. The first number in the column is a good starting value for the biggest.", "For each column c: start biggest at grid[0][c], loop over all rows r, and update biggest if grid[r][c] is larger. Append biggest to the answer.", "for c in range(len(grid[0])): biggest = grid[0][c]; for r in range(len(grid)): compare grid[r][c]; best.append(biggest)."])

fp("grids", "gr_diagonal", "Both diagonals", "Easy",
 ["The grid is square, meaning it has as many rows as columns. Print two numbers: the total of the main diagonal (top left to bottom right) and the total of the other diagonal (top right to bottom left)."],
 [("grid", "grid")], "Two whole numbers separated by a space.",
 [(([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), "15 15", "Main diagonal: 1 + 5 + 9. Other diagonal: 3 + 5 + 7. Both are 15."),
  (([[1, 2], [3, 4]],), "5 5", "Main: 1 + 4. Other: 2 + 3.")],
 [([[5]],), ([[1, 0], [0, 1]],), ([[2, 9, 1], [4, 6, 8], [3, 7, 5]],), ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 1, 2, 3], [4, 5, 6, 7]],)],
 '    n = len(grid)\n    main = 0\n    other = 0\n    for i in range(n):\n        main += grid[i][i]\n        other += grid[i][n - 1 - i]\n    return [main, other]\n',
 ["You only need one loop, not two.", "On the main diagonal the row and column are the same: grid[i][i]. On the other diagonal the column counts down from the right: grid[i][n - 1 - i].", "Loop i from 0 to n - 1. Add grid[i][i] to one total and grid[i][n - 1 - i] to the other.", "for i in range(n): main += grid[i][i]; other += grid[i][n - 1 - i]; return [main, other]."])

fp("grids", "gr_find", "Where is it", "Medium",
 ["Search the grid row by row, from the top row down, and left to right inside each row. Print the row and column of the first cell equal to `target`, separated by a space. If it is not there, print `-1 -1`."],
 [("grid", "grid"), ("target", "int")], "Two whole numbers: row then column.",
 [(([[1, 2, 3], [4, 5, 6]], 5), "1 1", "5 is in row 1, column 1."),
  (([[1, 2], [3, 4]], 9), "-1 -1", "9 is not in the grid.")],
 [([[7]], 7), ([[7]], 8), ([[1, 2, 2], [2, 2, 2]], 2), ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9), ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 4)],
 '    for r in range(len(grid)):\n        for c in range(len(grid[0])):\n            if grid[r][c] == target:\n                return [r, c]\n    return [-1, -1]\n',
 ["Check every cell in reading order, and stop at the first match.", "return inside the loops ends the whole function straight away, which is what you want for the first match.", "Loop over rows, then columns. If grid[r][c] equals target, return the pair r and c. If both loops finish, return -1 and -1.", "for r in range(len(grid)): for c in range(len(grid[0])): if grid[r][c] == target: return [r, c]. After the loops: return [-1, -1]."])

fp("grids", "gr_transpose", "Flip rows and columns", "Medium",
 ["Print the grid turned on its side, so that each column becomes a row. Print one line per new row, with the numbers separated by spaces."],
 [("grid", "grid")], "One line per new row.",
 [(([[1, 2, 3], [4, 5, 6]],), "1 4\n2 5\n3 6", "The first column 1, 4 becomes the first row. The second column 2, 5 becomes the second row, and so on.")],
 [([[5]],), ([[1, 2, 3]],), ([[1], [2], [3]],), ([[1, 2], [3, 4], [5, 6]],)],
 '    result = []\n    for c in range(len(grid[0])):\n        new_row = []\n        for r in range(len(grid)):\n            new_row.append(grid[r][c])\n        result.append(new_row)\n    return result\n',
 ["The new grid has as many rows as the old one has columns.", "Loop over the old columns on the outside. For each one, collect its cells from top to bottom into a new row.", "For each column c: make an empty new_row, add grid[r][c] for every r, then add new_row to the result.", "for c in range(len(grid[0])): new_row = []; for r in range(len(grid)): new_row.append(grid[r][c]); result.append(new_row)."])

fp("grids", "gr_neighbors", "Cells with a friend", "Medium",
 ["The grid holds only 0 and 1. Count the cells holding 1 that have at least one neighbour holding 1. Neighbours are the cells directly above, below, left and right. Diagonals do not count."],
 [("grid", "grid")], "One whole number.",
 [(([[1, 0, 1], [1, 0, 0], [0, 0, 1]],), "2", "Only the two ones in the first column touch each other. The other ones are alone.")],
 [([[1]],), ([[0, 0], [0, 0]],), ([[1, 1], [1, 1]],), ([[1, 0], [0, 1]],), ([[1, 1, 0], [0, 1, 0], [1, 0, 1]],)],
 '    rows = len(grid)\n    cols = len(grid[0])\n    count = 0\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] != 1:\n                continue\n            has_friend = False\n            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n                nr = r + dr\n                nc = c + dc\n                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:\n                    has_friend = True\n            if has_friend:\n                count += 1\n    return count\n',
 ["Use the four neighbour changes from the lesson, and check that each neighbour is on the grid.", "For each cell that holds a 1, look in four directions. A flag called has_friend starts False and turns True when any neighbour is a 1.", "Loop over cells. Skip cells that are not 1 (continue skips to the next round). For a 1, try the four directions with a bounds check. Add 1 to the count if has_friend is True.", "for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: nr = r + dr; nc = c + dc; if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1: has_friend = True."])

fp("grids", "gr_islands", "Count the islands", "Hard",
 ["The grid holds 0 (water) and 1 (land). An island is a group of land cells joined through their neighbours above, below, left or right. Diagonals do not join cells. Print how many islands there are."],
 [("grid", "grid")], "One whole number.",
 [(([[1, 1, 0, 0], [1, 0, 0, 1], [0, 0, 1, 1]],), "2", "The top left group of three cells is one island. The group of three at the right and bottom is another.")],
 [([[0]],), ([[1]],), ([[1, 0, 1], [0, 1, 0], [1, 0, 1]],), ([[1, 1, 1], [1, 1, 1]],), ([[1, 0, 1, 1], [1, 0, 0, 1], [0, 1, 0, 0], [1, 1, 0, 1]],)],
 '    rows = len(grid)\n    cols = len(grid[0])\n    seen = []\n    for r in range(rows):\n        seen.append([False] * cols)\n    islands = 0\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == 1 and not seen[r][c]:\n                islands += 1\n                stack = [(r, c)]\n                seen[r][c] = True\n                while stack:\n                    cr, cc = stack.pop()\n                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:\n                        nr = cr + dr\n                        nc = cc + dc\n                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and not seen[nr][nc]:\n                            seen[nr][nc] = True\n                            stack.append((nr, nc))\n    return islands\n',
 ["When you find a land cell you have not visited, you have found a new island. Then you must mark the whole island as visited so you do not count it again.", "Keep a second grid called seen, with True for visited cells. To visit a whole island, keep a to-do list called a stack. Take a cell off it, and add its unvisited land neighbours.", "Loop over cells. At a land cell that is not seen: add 1 to islands, mark it seen, and put it on the stack. While the stack has cells, take one off with pop(), check its four neighbours, and mark and add any land neighbour not yet seen.", "seen = a grid of False; for each cell: if grid[r][c] == 1 and not seen[r][c]: islands += 1; stack = [(r, c)]; while stack: cr, cc = stack.pop(); for each direction: if on the grid, land and not seen: seen[nr][nc] = True; stack.append((nr, nc))."])
