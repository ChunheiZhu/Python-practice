# ================================
# Hi Mr. Morozov,
# just press Run — a menu will appear.
# If you want to test the problems, simply choose from the menu.
# ================================
# USACO Bronze: Blocked Billboard
# Link: https://usaco.org/index.php?cpid=759&page=viewproblem2
# On the farm, there are two billboards A and B (rectangles aligned with the axes),
# and a truck T (also a rectangle).
# Each is represented by coordinates (x1, y1, x2, y2), the bottom-left and top-right points.
# The truck may cover part of the billboards.
# Compute the total visible area of both billboards A and B.
#
# Input format:
# Line 1: ax1 ay1 ax2 ay2 —— billboard A
# Line 2: bx1 by1 bx2 by2 —— billboard B
# Line 3: tx1 ty1 tx2 ty2 —— truck T
#
# Output format:
# A single integer: the total visible area of billboards A and B.
#
# Sample Input:
# 0 0 4 3
# 5 0 8 4
# 2 1 6 3
#
# Sample Output:
# 18
# ================================


def _area(rect):
   x1, y1, x2, y2 = rect
   w = max(0, x2 - x1)
   h = max(0, y2 - y1)
   return w * h


def _overlap(a, b):
   ax1, ay1, ax2, ay2 = a
   bx1, by1, bx2, by2 = b
   w = max(0, min(ax2, bx2) - max(ax1, bx1))
   h = max(0, min(ay2, by2) - max(ay1, by1))
   return w * h


def solve_blocked_billboard():
   print('Enter Test Data To 1.Blocked Billboard')
   ax1, ay1, ax2, ay2 = map(int, input().split())
   bx1, by1, bx2, by2 = map(int, input().split())
   tx1, ty1, tx2, ty2 = map(int, input().split())


   A = (ax1, ay1, ax2, ay2)
   B = (bx1, by1, bx2, by2)
   T = (tx1, ty1, tx2, ty2)


   visible_A = _area(A) - _overlap(A, T)
   visible_B = _area(B) - _overlap(B, T)


   print(visible_A + visible_B)




# solve_blocked_billboard()






# ================================
# USACO Bronze: Rectangle Pasture
# This problem is not from the official USACO archive.
# It is a simplified practice version created by ChatGPT.
"""
Here are some sample test data:


Input:
3
0 0
3 1
2 5
Expected Output:
15


Test 2
Input:
4
-1 -1
-1 2
3 -1
3 2
Expected Output:
12


Test 3
Input:
2
100 200
105 210
Expected Output:
50
"""


# Problem description:
# On the farm, there are N cows, each standing at an integer coordinate (x, y).
# You need to draw an axis-aligned rectangle that contains all the cows (boundary counts as inside).
# Output the minimum possible area of such a rectangle.
#
# Input format:
# First line: an integer N (1 <= N <= 100)
# Next N lines: two integers xi, yi (-1000 <= xi, yi <= 1000), the positions of the cows.
#
# Output format:
# One integer: the minimum rectangle area.
#
# Sample Input:
# 3
# 0 0
# 3 1
# 2 5
#
# Sample Output:
# 15
# ================================


def solve1():
   print('Enter Test Data To 2.Rectangle Pasture')
   n = int(input())
   allx = []
   ally = []
   for _ in range(n):
       x, y = map(int, input().split())
       allx.append(x)
       ally.append(y)
   minx = min(allx)
   maxx = max(allx)
   miny = min(ally)
   maxy = max(ally)
   area = (maxx - minx) * (maxy - miny)
   print(area)




# solve1()




# ================================
# USACO Bronze: Cow Gymnastics
# Link: https://usaco.org/index.php?cpid=963&page=viewproblem2
# Problem description:
# There are K gymnastics practice sessions. Each session lists the ranking of N cows.
# If cow A is ranked before cow B in all sessions, we say “A is always better than B.”
# Count how many pairs (A, B) satisfy this condition.
#
# Input format:
# First line: two integers K, N
# Next K lines: each contains N integers, the ranking in one session (from 1st to Nth).
#
# Output format:
# One integer: the number of pairs (A, B) such that A is always better than B.
#
# Sample Input:
# 3 4
# 4 1 2 3
# 4 1 3 2
# 4 2 1 3
#
# Sample Output:
# 4
#
# Explanation:
# - Session 1 order: 4 before 1, 1 before 2, 2 before 3
# - Session 2 order: 4 before 1, 1 before 3, 3 before 2
# - Session 3 order: 4 before 2, 2 before 1, 1 before 3
# Valid pairs: (4,1), (4,2), (4,3), (1,3)
# ================================


def always_before(i, j, pos, K):
   for r in range(K):
       if pos[r][i] >= pos[r][j]:
           return False
   return True


def solve2():
   print('Enter Test Data To 3.Cow Gymnastics')
   K, N = map(int, input().split())
   pos = []
   for _ in range(K):
       rank = list(map(int, input().split()))
       one_race_pos = {}
       for idx, cow in enumerate(rank):
           one_race_pos[cow] = idx
       pos.append(one_race_pos)
   ans = 0
   for i in range(1, N+1):
       for j in range(1, N+1):
           if i == j:
               continue
           if always_before(i, j, pos, K):
               ans += 1
   print(ans)




# solve2()


# ================================
# USACO Bronze: Mixing Milk
# Link: https://usaco.org/index.php?cpid=855&page=viewproblem2
# Problem description:
# There are three buckets with capacities c1, c2, c3,
# and initial amounts of milk m1, m2, m3.
# Farmer John performs 100 operations:
#   1st: pour bucket 1 into bucket 2,
#   2nd: pour bucket 2 into bucket 3,
#   3rd: pour bucket 3 into bucket 1,
#   4th: again from bucket 1 into bucket 2 … and so on in a cycle.
#
# Pouring rules:
# - If the target bucket isn’t full, pour as much as possible from the source.
# - If pouring would overflow, only pour until the target is full, leaving some milk in the source.
#
# Task: After 100 operations, output the final amount of milk in each bucket.
#
# Input format:
# c1 m1
# c2 m2
# c3 m3
#
# Output format:
# Three lines:
# amount in bucket 1
# amount in bucket 2
# amount in bucket 3
#
# Sample Input:
# 10 3
# 11 4
# 12 5
#
# Sample Output:
# 0
# 10
# 12
# ================================


def mixing_ops(a, ah, b, bh, c, ch):
   step = 0
   while step < 100:
       if bh + ah <= b:
           bh = bh + ah
           ah = 0
       else:
           ah = bh + ah - b
           bh = b
       step += 1
       if step == 100: break


       if ch + bh <= c:
           ch = ch + bh
           bh = 0
       else:
           bh = ch + bh - c
           ch = c
       step += 1
       if step == 100: break


       if ah + ch <= a:
           ah = ah + ch
           ch = 0
       else:
           ch = ah + ch - a
           ah = a
       step += 1


   print(ah)
   print(bh)
   print(ch)


def solve3():
   print('Enter Test Data To 4.Mixing Milk')
   a, ah = map(int, input().split())
   b, bh = map(int, input().split())
   c, ch = map(int, input().split())
   mixing_ops(a, ah, b, bh, c, ch)




# solve3()




# ================================
# USACO Bronze: Bucket Brigade
# Link: https://usaco.org/index.php?cpid=939&page=viewproblem2
# Problem description:
# The barn is on fire, and cows want to fetch water from the lake!
# The farm is represented by a 10x10 character grid:
#   - 'B' = Barn (on fire)
#   - 'L' = Lake (source of water)
#   - 'R' = Rock (cannot place cows)
#   - '.' = Empty space (cows can stand here)
#
# Cows must line up in a straight relay to pass water:
# - Water can only move up, down, left, or right
# - A cow must stand adjacent to the lake 'L' to fetch water
# - A cow must stand adjacent to the barn 'B' to put out the fire
# - Cows cannot stand on 'R'
#
# Task: Find the minimum number of cows (on '.' cells) required for the relay.
#
# Input format:
# 10 lines, each with 10 characters ('B', 'L', 'R', '.')
#
# Output format:
# One integer: the minimum number of cows needed.
#
# Sample Input:
# ..........
# ..........
# ..........
# ..B.......
# ..........
# .....R....
# ..........
# ..........
# .....L....
# ..........
#
# Sample Output:
# 7
#
# Explanation:
# - Barn at (4,3), lake at (9,6), rock at (6,6).
# - Shortest distance from lake to barn is 8 steps.
# - Only 7 cows are needed in between.
# ================================


def other(barn, lake):
   maxabsx = max(barn[0], lake[0])
   minabsx = min(barn[0], lake[0])
   maxabsy = max(barn[1], lake[1])
   minabsy = min(barn[1], lake[1])
   an = (maxabsx - minabsx) + (maxabsy - minabsy) - 1
   return an


def lakex_barnx_rockx(barn, lake, rock):
   if barn[0] == lake[0] and lake[0] == rock[0] and max(barn[1], lake[1]) > rock[1] > min(barn[1], lake[1]):
       maxan = max(barn[1], lake[1])
       minan = min(barn[1], lake[1])
       an = maxan - minan + 1
   else:
       maxan = max(barn[1], lake[1])
       minan = min(barn[1], lake[1])
       an = maxan - minan - 1
   return an


def lakey_barny_rocky(barn, lake, rock):
   if barn[1] == lake[1] and lake[1] == rock[1] and max(barn[0], lake[0]) > rock[0] > min(barn[0], lake[0]):
       maxan = max(barn[0], lake[0])
       minan = min(barn[0], lake[0])
       an = maxan - minan + 1
   else:
       maxan = max(barn[0], lake[0])
       minan = min(barn[0], lake[0])
       an = maxan - minan - 1
   return an


def solve4():
   print('Enter Test Data To 5.Bucket Brigade')
   grid = [input().strip() for _ in range(10)]
   rock = None
   for y in range(10):        
       for x in range(10):    
           if grid[y][x] == 'B':
               barn = (x, y)  
           if grid[y][x] == 'L':
               lake = (x, y)  
           if grid[y][x] == 'R':
               rock = (x, y) 


   if rock is not None and barn[0] == lake[0] and lake[0] == rock[0] and max(barn[1], lake[1]) > rock[1] > min(barn[1], lake[1]):
       print(lakex_barnx_rockx(barn, lake, rock))
   elif rock is not None and barn[1] == lake[1] and lake[1] == rock[1] and max(barn[0], lake[0]) > rock[0] > min(barn[0], lake[0]):
       print(lakey_barny_rocky(barn, lake, rock))
   else:
       print(other(barn, lake))


# solve4()


# ================================
# CCC 2018 S2 – Sunflowers
# Link: https://dmoj.ca/problem/ccc18s2
# Problem background:
# You are given an n × n grid of flower heights.
# The grid may have been rotated clockwise by 0°, 90°, 180°, or 270°.
# Your task is to restore it to the "correct orientation."
#
# Correct orientation definition:
#  - Each row is non-decreasing (left to right).
#  - Each column is non-decreasing (top to bottom).
#
# In other words:
# Looking left-to-right and top-to-bottom, the numbers must not decrease.
#
# Input format:
# First line: integer n (2 ≤ n ≤ 100), the size of the grid.
# Next n lines: each with n integers, the matrix rows.
#
# Output format:
# Output the rotated matrix (n rows), which is correctly oriented.
#
# Sample Input:
# 3
# 3 7 9
# 2 6 8
# 1 4 5
#
# Sample Output:
# 1 2 3
# 4 6 7
# 5 8 9
#
# Explanation:
# The given matrix was rotated counterclockwise.
# Rotating 90° clockwise produces the correct orientation.


def mat90(num,mat):
   n = num
   for _ in range(4):
       if check(n,mat):
           return mat
       nmat = []          
       for row in zip(*mat[::-1]):   
           nmat.append(list(row)) 
       mat = nmat
   return mat                  


def check(num,mat):
   n = num
   for i in range(n):
       for x in range(n-1):
           if mat[i][x] > mat[i][x+1]:
               return False
   for i in range(n):
       for x in range(n-1):
           if mat[x][i] > mat[x+1][i]:
               return False
   return True


def solve5():
   print('Enter Test Data To 6.Sunflowers')
   num = int(input().strip())
   mat = [list(map(int, input().split())) for _ in range(num)]
   ans = mat90(num,mat)
   for row in ans:
       print(*row)


#solve5()


# Codeforces 1133C – Balanced Team
# Link: https://codeforces.com/problemset/problem/1133/C
# A school has N students, each with an integer skill level.
# The coach wants to assign as many students as possible into "valid" teams.
#
# A valid team is defined as:
#  - Within the same team, the difference between the maximum and minimum skill
#    levels must be at most 5.
#
# Your Task:
#  - Determine the maximum number of students that can be assigned into valid teams
#    (maximize the number of students included).
#
# Input Format:
# The first line: an integer N (1 ≤ N ≤ 1000).
# The second line: N integers, representing the students' skill levels.
#
# Output Format:
# Output a single integer, the maximum number of students that can be included in teams.
#
# Sample Input:
# 6
# 1 10 17 12 15 2
#
# Sample Output:
# 3
#
# Explanation:
# After sorting the skill levels: [1, 2, 10, 12, 15, 17].
# We can select [10, 12, 15] as one team, since max - min = 15 - 10 = 5.
# Therefore, the maximum number of students in valid teams is 3.


def low_high_nums(num,nums):
   for a in range(num):
       for b in range(num-1):
           if nums[b] > nums[b+1]:
               nums[b],nums[b+1] = nums[b+1],nums[b]
   return nums
def found(num,nums):
   l = 0
   ans = 0
   newnums = low_high_nums(num,nums)
   for i in range(num):
       while newnums[i] - newnums[l] > 5:
               l += 1
       ans = max(ans,i - l + 1)
   return ans


def solve6():
   print('Enter Test Data To 7.Balanced Teams')
   num = int(input().strip())
   nums = list(map(int,input().split()))


   an = found(num,nums)
   print(an)


#solve6()


# ================================
# CCC 2017 J4 – Favourite Times (Practice)
# Link: https://dmoj.ca/problem/ccc17j4
#
# Problem Description:
#
# You have a 12-hour digital clock that shows times from 12:00 up to 11:59.
# Each minute, the time advances by one minute.
#
# A time on the clock is called a "favourite time" if, when the digits of the
# time are written without the colon, the digits form an arithmetic sequence.
# That is, the difference between each pair of consecutive digits is the same.
#
# Examples:
#  - 12:34 → digits 1,2,3,4 → differences are 1,1,1 → arithmetic sequence ✅
#  - 1:11  → digits 1,1,1 → differences are 0,0 → arithmetic sequence ✅
#  - 2:46  → digits 2,4,6 → differences are 2,2 → arithmetic sequence ✅
#  - 10:08 → digits 1,0,0,8 → differences are -1,0,8 → not arithmetic ❌
#
# Input format:
#  A single integer N (0 ≤ N ≤ 1,000,000), the number of minutes.
#
# Output format:
#  Output the number of favourite times that will occur in the N minutes after 12:00.
#
# Explanation:
#  - Start counting from 12:00, after one minute the time is 12:01,
#    after two minutes it is 12:02, etc.
#  - After N minutes, stop.
#  - Count how many of those times were "favourite times".
#
# Sample Input 1:
# 34
# Sample Output 1:
# 1
#
# Sample Input 2:
# 180
# Sample Output 2:
# 11
#
# Sample Input 3:
# 1440
# Sample Output 3:
# 62
# ================================


def solve7():
   print('Enter Test Data To 8.Favourite Time')
   num = int(input().strip())
   hour = 12
   minute = 0
   a = 0
   for i in range(num):
       minute += 1
       if minute > 59:
           minute = 0
           hour += 1
           if hour > 12:
               hour = 1
       h1 = hour // 10    
       h2 = hour % 10  
       m1 = minute // 10 
       m2 = minute % 10
       if hour < 10:
           clock = [h2, m1, m2]
           if clock[1] - clock[0] == clock[2] - clock[1]:
               a += 1
       else:
           clock = [h1, h2, m1, m2]
           if clock[1] - clock[0] == clock[2] - clock[1] == clock[3] - clock[2]:
               a += 1
   print(a)
  
#solve7()


while True:
   print('')
   print('Test: 1.Blocked Billboard | 2.Rectangle Pasture | 3.Cow Gymnastics')
   print('4.Mixing Milk | 5.Bucket Brigade | 6.Sunflowers | 7.Balanced Teams')
   print('8.Favourite Time')
   an = input('>>> ').strip()
   if an == "1" or an.lower() == "blocked billboard" or an.lower() == "1.blocked billboard":
       solve_blocked_billboard()
   elif an == "2" or an.lower() == "rectangle pasture" or an.lower() == "2.rectangle pasture":
       solve1()
   elif an == "3" or an.lower() == "cow gymnastics" or an.lower() == "3.cow gymnastics":
       solve2()
   elif an == "4" or an.lower() == "mixing milk" or an.lower() == "4.mixing milk":
       solve3()
   elif an == "5" or an.lower() == "bucket brigade" or an.lower() == "5.bucket brigade":
       solve4()
   elif an == "6" or an.lower() == "sunflowers" or an.lower() == "6.sunflowers":
       solve5()
   elif an == "7" or an.lower() == "balanced teams" or an.lower() == "7.balanced teams":
       solve6()
   elif an == "8" or an.lower() == "favourite timess" or an.lower() == "8.favourite times":
       solve7()

