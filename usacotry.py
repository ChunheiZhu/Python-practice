# USACO Bronze: Blocked Billboard（被挡住的广告牌）
# 题目描述：
# 农场里有两个与坐标轴对齐的广告牌 A、B，以及一辆卡车 T。
# 三者都用矩形表示，坐标格式是 (x1, y1, x2, y2)，代表矩形左下角和右上角的点。
# 卡车可能会挡住部分广告牌。请计算 A 和 B 两个广告牌露在外面的总面积。
#
# 输入格式：
# 第 1 行：ax1 ay1 ax2 ay2 —— 广告牌 A
# 第 2 行：bx1 by1 bx2 by2 —— 广告牌 B
# 第 3 行：tx1 ty1 tx2 ty2 —— 卡车 T
#
# 输出格式：
# 一行，一个整数：广告牌 A 与 B 露出的总面积。
#
# 样例输入：
# 0 0 4 3
# 5 0 8 4
# 2 1 6 3
#
# 样例输出：
# 18
#
# 解题思路：
# 1) 求矩形面积：area(R) = (x2 - x1) * (y2 - y1)
# 2) 求重叠面积：先算 x 和 y 方向的重叠长度，再相乘。
#    - x 重叠：w = max(0, min(x2a, x2b) - max(x1a, x1b))
#    - y 重叠：h = max(0, min(y2a, y2b) - max(y1a, by1))
#    - overlap = w * h
# 3) 可见面积 = 自身面积 - 与卡车的重叠面积
# 4) 答案 = visible(A) + visible(B)

import sys

def _area(rect):
    """计算矩形面积 rect = (x1, y1, x2, y2)"""
    x1, y1, x2, y2 = rect
    w = max(0, x2 - x1)   # 宽度
    h = max(0, y2 - y1)   # 高度
    return w * h

def _overlap(a, b):
    """计算两个矩形 a, b 的重叠面积"""
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    # x 方向重叠
    w = max(0, min(ax2, bx2) - max(ax1, bx1))
    # y 方向重叠
    h = max(0, min(ay2, by2) - max(ay1, by1))
    return w * h

def solve_blocked_billboard():
    # 输入广告牌 A、B 和卡车 T
    print('Enter Test Data To 1.Blocked Billboard')
    ax1, ay1, ax2, ay2 = map(int, input().split())
    bx1, by1, bx2, by2 = map(int, input().split())
    tx1, ty1, tx2, ty2 = map(int, input().split())

    A = (ax1, ay1, ax2, ay2)
    B = (bx1, by1, bx2, by2)
    T = (tx1, ty1, tx2, ty2)

    # A 和 B 各自的可见面积
    visible_A = _area(A) - _overlap(A, T)
    visible_B = _area(B) - _overlap(B, T)

    # 输出结果
    print(visible_A + visible_B)

#solve_blocked_billboard()

# USACO Bronze: Rectangle Pasture
# 题目描述：
# 农场里有 N 头牛，每头牛站在一个整数坐标点 (x, y) 上。
# 你需要画一个与坐标轴对齐的矩形，把所有牛都圈在里面（边界也算圈住）。
# 输出这个矩形的最小面积。
# 输入格式：
# 第一行：一个整数 N (1 <= N <= 100)
# 接下来 N 行：每行两个整数 xi, yi (-1000 <= xi, yi <= 1000)，表示牛的位置。
# 输出格式：
# 一行，一个整数，表示能圈住所有牛的最小矩形的面积。
# 样例输入：
#3
#0 0
#3 1
#2 5
# 样例输出：
# 15

def solve1():
    print('Enter Test Data To 2.Rectangle Pasture')
    n = int(input())
    allx = []
    ally = []
    for i in range(n):
        x,y = map(int,input().split())
        allx.append(x)
        ally.append(y)
    minx = min(allx)
    maxx = max(allx)
    miny = min(ally)
    maxy = max(ally)

    area = (maxx - minx) * (maxy - miny)

    print(area)

#solve1()

# USACO Bronze: Cow Gymnastics
# 题目描述：
# 农场里有 K 场牛的体操比赛，每场比赛中，N 头牛的名次都给出。
# 如果在所有比赛中，牛 A 都排在牛 B 的前面，那么我们说「A 始终优于 B」。
# 现在请你计算：一共有多少对 (A, B) 满足这个条件。
# 输入格式：
# 第一行：两个整数 K, N
# 接下来 K 行：每行包含 N 个整数，表示一次比赛的排名（从第 1 名到第 N 名的牛编号）。
# 输出格式：
# 一行，一个整数，表示始终保持顺序的牛对数量。
# 样例输入：
# 3 4
# 4 1 2 3
# 4 1 3 2
# 4 2 1 3
# 样例输出：
# 4
# 解释：
# - 比赛 1 顺序：4 在 1 前，1 在 2 前，2 在 3 前
# - 比赛 2 顺序：4 在 1 前，1 在 3 前，3 在 2 前
# - 比赛 3 顺序：4 在 2 前，2 在 1 前，1 在 3 前
# 经过检查，(4,1), (4,2), (4,3), (1,3) 这 4 对牛始终保持顺序。
def always_before(i, j, pos, K):
    # 检查牛 i 是否始终在牛 j 前面
    for r in range(K):
        if pos[r][i] >= pos[r][j]:
            return False
    return True

def solve2():
    print('Enter Test Data To 3.Cow Gymnastics')
    K, N = map(int, input().split()) 
    pos = []   # 存每场比赛的 {牛: 名次}

    for i in range(K):
        rank = list(map(int, input().split()))
        one_race_pos = {}  # 字典
        # 遍历当前比赛的排名
        for idx, cow in enumerate(rank):
            one_race_pos[cow] = idx   # 牛 cow 在这场的名次是 idx (0-based)
        pos.append(one_race_pos)
    ans = 0
            # 枚举所有牛对 (i, j)，注意 i != j
    for i in range(1, N+1):
        for j in range(1, N+1):
            if i == j:
                continue
            if always_before(i, j, pos, K):
                ans += 1
    print(ans)
 
#solve2()
 
# USACO Bronze: Mixing Milk（混合牛奶）
# 题目描述：
# 农场里有三个牛奶桶，容量分别是 c1, c2, c3，初始装的牛奶量分别是 m1, m2, m3。
# 农夫 John 要进行 100 次操作：
#   第 1 次把桶 1 倒入桶 2，
#   第 2 次把桶 2 倒入桶 3，
#   第 3 次把桶 3 倒入桶 1，
#   第 4 次再从桶 1 倒入桶 2…… 以此类推循环。
# 倒牛奶规则：
# - 如果目标桶还没满，就尽量把源桶的牛奶倒进去。
# - 如果倒入后会超过容量，就只倒到目标桶刚好满为止，源桶里可能还会剩下牛奶。
# 问：经过 100 次操作后，三个桶里各有多少牛奶？
#
# 输入格式：
# c1 m1
# c2 m2
# c3 m3
#
# 输出格式：
# 三行：
# 桶 1 的牛奶量
# 桶 2 的牛奶量
# 桶 3 的牛奶量
#
# 样例输入：
# 10 3
# 11 4
# 12 5
#
# 样例输出：
# 0
# 10
# 12

def ans1(a,ah,b,bh,c,ch):
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
    a,ah = map(int,input().split())
    b,bh = map(int,input().split())
    c,ch = map(int,input().split())
    print('')
    ans1(a,ah,b,bh,c,ch)

#solve3()

# USACO Bronze: Bucket Brigade（水桶接力）
# 题目描述：
# 农场起火了，奶牛们想从湖里取水救火！
# 地图是一个 10x10 的字符网格：
#   - 'B' 表示牛棚 (Barn)，它着火了
#   - 'L' 表示湖 (Lake)，可以取水
#   - 'R' 表示大石头 (Rock)，不能放牛
#   - '.' 表示空地，可以放牛
#
# 奶牛们要排成一条直线接力传水桶：
# - 水桶只能在上下左右四个方向移动
# - 一头牛必须站在湖 'L' 的相邻格子，才能取水
# - 一头牛必须站在牛棚 'B' 的相邻格子，才能灭火
# - 不能把牛放在 'R' 上
#
# 请你计算：至少需要多少头牛（占据 '.' 格子）才能完成接力？
#
# 输入格式：
# 10 行，每行 10 个字符，只包含 'B'、'L'、'R'、'.'
#
# 输出格式：
# 一个整数，表示需要的最少牛数
#
# 样例输入：
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
# 样例输出：
# 7
#
# 解释：
# - 牛棚在 (4,3)，湖在 (9,6)，石头在 (6,6)。
# - 牛从湖到牛棚的最短距离是 8 格。
# - 只需要在中间 7 个格子放牛，就能完成接力。

def other(barn,lake):
    maxabsx = max(barn[0],lake[0])
    minabsx = min(barn[0],lake[0])
    maxabsy = max(barn[1],lake[1])
    minabsy = min(barn[1],lake[1])
    an = (maxabsx - minabsx) + (maxabsy - minabsy) - 1
    return an
            
def lakex_barnx_rockx(barn,lake,rock):
    if barn[0] == lake[0] and lake[0] == rock[0] and max(barn[1],lake[1]) > rock[1] > min(barn[1],lake[1]):
        maxan = max(barn[1],lake[1])
        minan = min(barn[1],lake[1])
        an = maxan - minan + 1     
    else:
        maxan = max(barn[1],lake[1])
        minan = min(barn[1],lake[1])
        an = maxan - minan - 1
    return an
            
def lakey_barny_rocky(barn,lake,rock):
    if barn[1] == lake[1] and lake[1] == rock[1] and max(barn[0],lake[0]) > rock[0] > min(barn[0],lake[0]):
        maxan = max(barn[0],lake[0])
        minan = min(barn[0],lake[0])
        an = maxan - minan + 1          
    else:
        maxan = max(barn[0],lake[0])
        minan = min(barn[0],lake[0])
        an = maxan - minan - 1
    return an

def solve4():
    print('Enter Test Data To 5.Bucket Brigade')
    grid = [input().strip() for _ in range(10)]   # 读 10 行
    print('')
    rock = None
    for y in range(10):         # 行
        for x in range(10):     # 列
            if grid[y][x] == 'B':
                barn = (x, y)   # 牛棚
            if grid[y][x] == 'L':
                lake = (x, y)   # 湖
            if grid[y][x] == 'R':
                    rock = (x, y)   # 石头
 
    if rock is not None and barn[0] == lake[0]  and lake[0] == rock[0] and max(barn[1],lake[1]) > rock[1] > min(barn[1],lake[1]):
        print(lakex_barnx_rockx(barn,lake,rock))

    elif rock is not None and barn[1] == lake[1]  and lake[1] == rock[1] and max(barn[0],lake[0]) > rock[0] > min(barn[0],lake[0]):
        print(lakey_barny_rocky(barn,lake,rock))
    else:
        print(other(barn,lake))

#solve4()

# CCC 2018 S2 – Sunflowers（向日葵）

# 题目背景：
# 有一个 n × n 的方阵，里面存放的是花的高度。
# 已知这个方阵可能被顺时针旋转过 0°、90°、180° 或 270°。
# 你的任务是把它恢复成「正确的方向」。

# 正确的方向定义为：
#  - 每一行都是非递减的（从左到右，数值不会下降）。
#  - 每一列都是非递减的（从上到下，数值不会下降）。

# 换句话说：
#  在正确的矩阵中，从左到右、从上到下看，数字会逐渐变大或保持不变。


# 输入格式：
# 第一行：一个整数 n (2 ≤ n ≤ 100)，表示矩阵的大小。
# 接下来 n 行：每行包含 n 个整数，表示矩阵的一行。


# 输出格式：
# 输出经过旋转之后的矩阵（n 行，每行 n 个整数），
# 保证矩阵符合“正确方向”的定义。


# 样例输入：
# 3
# 3 7 9
# 2 6 8
# 1 4 5

# 样例输出：
# 1 2 3
# 4 6 7
# 5 8 9

# 解释：
# 原矩阵是逆时针方向放置的。
# 顺时针旋转 90° 后，矩阵满足行与列都是非递减的。

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
    print('')
    ans = mat90(num,mat)
    for row in ans:
        print(*row)

#solve5()

# CCC 2015 Senior (S3) – Balanced Teams（平衡队伍）
#
# 题目背景：
# 学校里有 N 个学生，每个学生有一个整数技能值。
# 教练希望尽可能多地把学生分进“合法”的队伍中。
#
# 合法队伍的定义：
#  - 在同一个队伍中，技能值的最大值与最小值之差 不超过 5。
#
# 你的任务：
#  - 计算最多有多少名学生可以被分配到符合要求的队伍中（人数最大化）。
#
# 输入格式：
# 第一行：一个整数 N（1 ≤ N ≤ 1000）。
# 第二行：N 个整数，表示每个学生的技能值。
#
# 输出格式：
# 输出一个整数，表示最多可以进队伍的学生人数。
#
# 样例输入：
# 6
# 1 10 17 12 15 2
#
# 样例输出：
# 3
#
# 解释：
# 将技能值排序为 [1, 2, 10, 12, 15, 17]。
# 可以选择 [10, 12, 15] 作为一支队伍（最大值 15 - 最小值 10 = 5）。
# 因此最多有 3 名学生能被分进队伍。

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
    print('')
    an = found(num,nums)
    print(an)

#solve6()

# ================================
# CCC 2017 J4 – Favourite Times
# Link: https://dmoj.ca/problem/ccc17j4
#
# Problem description (中文翻译):
# 一天有 12 小时 (从 12:00 到 11:59)，每小时有 60 分钟。
# 给定一个整数 N，表示分钟数。
# 从 12:00 开始，每过 1 分钟，时间会推进。
# 我们要统计，在 N 分钟内，会出现多少次“特殊时间”。
#
# 定义：一个“特殊时间”是指时间的每一位数字形成一个等差数列。
#
# 举例：
# - 12:34 → 数字 1,2,3,4 是等差数列 → 特殊时间
# - 5:55  → 数字 0,5,5,5（写成 05:55）不是等差
# - 3:15  → 数字 0,3,1,5 不是等差
#
# Input format:
# 一行，一个整数 N (0 ≤ N ≤ 10^6)，表示分钟数。
#
# Output format:
# 一行，一个整数：在 N 分钟内出现的特殊时间个数。
#
# Sample Input:
# 34
#
# Sample Output:
# 1
#
# Explanation:
# 从 12:00 到 12:34，只会出现一次特殊时间：12:34。
# ================================

def solve7():
    num = int(input().strip())
    print('')
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

# ================================
# CCC 2025 J3: Product Codes （产品代码）
#
# 【题目描述】
#   一家商店请来了“代码清理小队”来更新它的产品代码。
#   原始的产品代码是一个由大写字母、小写字母和整数（正数或负数）混合组成的字符串。
#
#   新的产品代码生成规则如下：
#   1. 删除所有小写字母。
#   2. 保留所有大写字母（顺序不变）。
#   3. 找出字符串中的所有整数（可能为正或负），将它们相加。
#   4. 把相加结果接在保留下来的大写字母后面。
#
# 【输入格式】
#   - 第一行：一个正整数 N，表示有多少个产品代码需要更新。
#   - 接下来 N 行：每行是一个原始产品代码字符串。
#
#   - 保证每个产品代码中至少包含：
#       * 1 个大写字母
#       * 1 个小写字母
#       * 1 个整数（正或负）
#   - 输入保证不会出现两个正整数紧贴在一起，例如“23”算作一个整数，而不是“2”和“3”。
#
# 【输出格式】
#   - 共 N 行。
#   - 每一行输出一个新的产品代码。
#
# 【样例输入 1】
# 1
# AbC3c2Cd9
#
# 【样例输出 1】
# ACC14
#
# 解释：
#   原始字符串 "AbC3c2Cd9"
#     - 大写字母顺序为 A, C, C → "ACC"
#     - 整数为 3, 2, 9，相加得到 14
#   新代码为 "ACC14"
#
# 【样例输入 2】
# 3
# Ahkiy-6ebvXCV1
# 393hhhUHkbs5gh6QpS-9-8
# PL12N-2G1234Duytrty8-86tyaYySsDdEe
#
# 【样例输出 2】
# AXCV-5
# UHQS387
# PLNGDYSDE1166
# ================================

def cap(s):
    caps = []
    for ch in s:
        if ch.isupper():
            caps.append(ch)
    caps = ''.join(caps)
    return caps
def num(s):
    total = 0
    i = 0
    L = len(s)
    while i < L:
        sign = 1
        if s[i] == '-' and i + 1 < L and s[i + 1].isdigit():
            sign = -1
            i += 1 
        if i < L and s[i].isdigit():
            val = 0
            while i < L and s[i].isdigit():
                val = val * 10 + int(s[i])
                i += 1
            total += sign * val
        else:
            i += 1
    return total
def solve8():
    n = int(input().strip())
    s = [input().strip() for _ in range(n)]
    print('')
    for ch in s:
        caps = cap(ch)
        nums = num(ch)
        print(f"{caps}{nums}")

#solve8()

# ================================
# 🇨🇦 CCC 2019 J2 – Time to Decompress
# ================================
#
# 【题目描述】
# 你会得到几行输入。
# 每一行都包含一个正整数和一个字符（可以是字母或符号）。
# 你的任务是输出一个字符串，这个字符串由该字符重复指定的次数组成。
#
# 【输入格式】
# 第一行包含一个整数 L（1 ≤ L ≤ 5），
# 表示接下来有多少行输入。
#
# 接下来的 L 行中：
#   每一行包含一个整数 N（1 ≤ N ≤ 80）和一个字符 C，
#   它们之间以一个空格分隔。
#
# 【输出格式】
# 对于每一行输入，
#   输出一行结果，
#   结果是字符 C 重复 N 次的字符串。
#
# 【输入样例】
# 4
# 9 +
# 3 -
# 12 A
# 2 X
#
# 【输出样例】
# +++++++++
# ---
# AAAAAAAAAAAA
# XX
#
# ================================

def solve9():
    num = int(input().strip())
    data = [input().split() for _ in range(num)]
    for n, s in data:
        n = int(n)
        print(s * n)

#solve9()

# ================================
# CCC 2021 J1 – Boiling Water（沸水）
# 题目链接（英文原题）:
# https://dmoj.ca/problem/ccc21j1
# ================================
#
# 题目描述：
#
# 当水被加热时，它会在特定温度下沸腾。
# 科学家想知道当水的温度变化时，空气的压力会变化多少。
#
# 他通过一个简单的公式来计算空气压力：
#   P = 5 * B - 400
#
# 其中：
#   - B 表示当前的温度（摄氏度）
#   - P 表示大气压力（单位：某种固定单位）
#
# 你的任务是：
#   1. 读取一个整数 B（温度，单位为摄氏度）
#   2. 输出两个整数：
#       - 第一行输出计算得到的大气压力 P
#       - 第二行输出气压与标准气压（100）相比的状态：
#           如果 P > 100，输出 1（气压高于海平面）
#           如果 P == 100，输出 0（气压等于海平面）
#           如果 P < 100，输出 -1（气压低于海平面）
#
# ------------------------
# 【输入格式】
# 一行，一个整数 B (0 ≤ B ≤ 1000)
#
# 【输出格式】
# 两行：
#   第1行：整数 P
#   第2行：整数状态值（1、0 或 -1）
#
# ------------------------
# 【输入样例】
# 80
#
# 【输出样例】
# 0
# -1
#
# ------------------------
# 【解释】
# P = 5*80 - 400 = 0
# 因为 0 < 100，所以输出 -1
#
# ================================

def solve10():
    b = int(input())
    p = 5 * b - 400
    print(p)
    if p > 100:
        print(1)
    elif p == 100:
        print(0)
    else:
        print(-1)

#solve10()

# ================================
# USACO Bronze: Shell Game
# Link: https://usaco.org/index.php?page=viewproblem2&cpid=891
# ================================
# 🐚 题目背景：
# 有三个贝壳（标号为 1, 2, 3），其中一个贝壳下面藏着一颗珍珠。
# 起初，珍珠在某个贝壳下。
# 接下来会进行一系列操作，每次操作包括：
#   - 交换两个贝壳的位置；
#   - 然后猜测珍珠在哪个贝壳下面。
#
# 你的任务是：假设珍珠一开始在 1、2、或 3 号贝壳下，
# 分别计算在所有猜测中能答对的次数，输出最大的那个值。
#
# 🧮 输入格式：
# 第1行：一个整数 N (1 ≤ N ≤ 100) —— 操作次数  
# 接下来的 N 行，每行包含三个整数：
#   a b g
#   表示：交换贝壳 a 和 b，然后猜测 g。
#
# 📤 输出格式：
# 输出一个整数 —— 表示在最优初始位置下最多能答对几次。
#
# ✏️ 样例输入：
# 3
# 1 2 1
# 3 2 1
# 1 3 1
#
# ✅ 样例输出：
# 2
#
# 💡 说明：
# - 如果珍珠一开始在 1 号壳下，猜对 2 次；
# - 如果一开始在 2 号壳下，猜对 1 次；
# - 如果一开始在 3 号壳下，猜对 1 次；
# 所以输出最大值 2。

def solve11():
    num = int(input())
    ops = [list(map(int, input().split())) for _ in range(num)]
    an = 0
    for start in [1,2,3]:
        pearl = start
        correct = 0
        for a,b,g in ops:
            if pearl == a:
                pearl = b
            elif pearl == b:
                pearl = a
            if pearl == g:
                correct += 1
        an = max(correct,an)
    print(an)

#solve11()

# ================================================
# 🐮 USACO 2024 一月 Bronze
# 题目名称：奶牛大学 Cow College
# ================================================

# 🧩 题目描述：
# 农夫约翰开设了一门新课程，名为“奶牛大学”。
# 他向 N 头奶牛进行调查，第 i 头奶牛愿意支付的最高学费为 Pi 美元。
#
# 农夫约翰需要选择一个统一的学费价格 T（为整数）。
# 所有愿意支付价格 ≥ T 的奶牛都会报名。
#
# 学费收入的计算方式为：
# 收入 = T ×（愿意支付 ≥ T 的奶牛数量）。
#
# 请帮助约翰计算能让收入最大的学费价格 T。
# 如果有多个 T 值能得到相同的最大收入，请选择最小的那个 T。

# -----------------------------------------------
# ✅ 输入格式：
# 第 1 行：一个整数 N（1 ≤ N ≤ 100000）
# 接下来的 N 行：每行包含一个整数 Pi（1 ≤ Pi ≤ 1,000,000,000）
#
# -----------------------------------------------
# ✅ 输出格式：
# 输出两个整数（以空格分隔）：
#    1️⃣ 最佳的学费价格 T
#    2️⃣ 在该价格下的最大总收入
#
# -----------------------------------------------
# ✅ 样例输入：
# 4
# 2
# 8
# 10
# 7
#
# ✅ 样例输出：
# 7 21
#
# 💡 解释：
# - 如果价格 T = 2 → 所有 4 头奶牛都能支付，收入 = 2 × 4 = 8
# - 如果价格 T = 7 → 奶牛 [7, 8, 10] 三头报名，收入 = 7 × 3 = 21
# - 如果价格 T = 8 → 奶牛 [8, 10] 两头报名，收入 = 8 × 2 = 16
# - 如果价格 T = 10 → 只有奶牛 [10] 一头报名，收入 = 10 × 1 = 10
#
# 最大收入为 21，对应价格 T = 7。
# ================================================

def solve12():
    num = int(input())
    nums = [int(input()) for _ in range(num)]
    result = 0
    an = 0
    ans = 0

    for i in range(num):
        bigger = 0
        for j in range(num):
            if nums[j] >= nums[i]:
                bigger += 1
        newresult = nums[i] * bigger
        if newresult > result:
            result = newresult
            an = nums[i]
            ans = newresult
    print(an,ans)

#solve12()

# ============================================
# CCC 2020 Senior 2：逃离房间（Escape Room）
# ============================================
# 题目描述：
# 给定一个 R×C 的网格（R 行、C 列），每个格子 (r, c) 中写有一个正整数 v。
# 你从左上角 (1, 1) 出发，目标是到达右下角 (R, C)。
#
# 规则：
# 若你当前所在格子的数字为 v，则你可以“瞬间移动”到网格中任意一个坐标 (r, c)，
# 只要 r × c = v，且该坐标在网格范围内（1 ≤ r ≤ R，1 ≤ c ≤ C）。
#
# 问题：
# 判断是否存在一条合法的移动路径，使得你可以从 (1, 1) 到达 (R, C)。
#
# 输入格式：
# 第 1 行：两个整数 R、C（分别表示行数与列数）
# 接下来 R 行：每行包含 C 个整数，表示该行每个格子的值
#
# 输出格式：
# 若可以从 (1,1) 到达 (R,C)，输出：
# yes
# 否则输出：
# no
#
# 说明与细节：
# - 坐标均以 1 为起始下标，即左上角为 (1,1)，右下角为 (R,C)。
# - 从值为 v 的格子，你可以跳到所有满足 r×c=v 的格子集合中的任意一个；
#   若某些 (r, c) 超出网格范围，则不能跳到那些非法位置。
# - 只需判断能否到达，不需要输出路径。
#
# 样例 1：
# 输入：
# 3 4
# 3 10 8 14
# 1 11 12 12
# 6 2 3 9
# 输出：
# yes
#
# 样例 2（无法到达）：
# 输入：
# 2 2
# 2 4
# 6 9
# 输出：
# no
#
# 样例 3（单点即终点）：
# 输入：
# 1 1
# 1
# 输出：
# yes
#
# ============================================

def solve13():
    R, C = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(R)]

    stack = [(1, 1)]
    visited = set([(1, 1)])

    while stack:
        r, c = stack.pop()
        if (r, c) == (R, C):
            print("yes")
            return

        v = grid[r - 1][c - 1]

        i = 1
        while i * i <= v:
            if v % i == 0:
                r1, c1 = i, v // i
                if 1 <= r1 <= R and 1 <= c1 <= C and (r1, c1) not in visited:
                    visited.add((r1, c1))
                    stack.append((r1, c1))

                r2, c2 = v // i, i
                if (r2, c2) != (r1, c1):
                    if 1 <= r2 <= R and 1 <= c2 <= C and (r2, c2) not in visited:
                        visited.add((r2, c2))
                        stack.append((r2, c2))
            i += 1

    print("no")

#solve13()

# ===============================================================
# CCC 2016 S2：双人自行车（Tandem Bicycle）
# ===============================================================
#
# 题目描述：
# 农场主和城市骑手要进行一场双人自行车比赛。
# 有两组骑手：一组来自农场，一组来自城市。
# 每辆双人自行车恰好由两人组成：一位来自农场，一位来自城市。
#
# 一辆双人自行车的速度，等于这两位骑手中 **速度较快** 的那一位的速度。
#
# 现在给出：
# - 一个整数 type，表示目标类型；
# - 每组骑手的人数 n；
# - 两组骑手各自的速度。
#
# 如果 type = 1，表示要让所有双人自行车的 **总速度之和最小**；
# 如果 type = 2，表示要让所有双人自行车的 **总速度之和最大**。
#
# 每个骑手必须恰好被使用一次。
#
# ---------------------------------------------------------------
# 输入格式：
# 第 1 行：整数 type（1 或 2）
# 第 2 行：整数 n（1 ≤ n ≤ 1000）
# 第 3 行：n 个整数，表示第一组骑手的速度
# 第 4 行：n 个整数，表示第二组骑手的速度
#
# ---------------------------------------------------------------
# 输出格式：
# 输出一个整数，表示在给定 type 要求下的最优总速度。
#
# ---------------------------------------------------------------
# 样例输入 1：
# 1
# 3
# 5 1 4
# 6 2 4
#
# 样例输出 1：
# 12
#
# 解释：
# 配法：(1,2)、(4,4)、(5,6)
# 每辆车速度分别为 2、4、6，总和 = 12。
#
# ---------------------------------------------------------------
# 样例输入 2：
# 2
# 3
# 5 1 4
# 6 2 4
#
# 样例输出 2：
# 15
#
# 解释：
# 配法：(1,6)、(4,4)、(5,2)
# 每辆车速度分别为 6、4、5，总和 = 15。
#
# ---------------------------------------------------------------
# 提示：
# - 当 type = 1（最小化总速度）时，应该让速度差最小；
# - 当 type = 2（最大化总速度）时，应该让每辆车尽量拥有一个更快的骑手。
#
# ===============================================================

def low_high(num,nums):
    for i in range(num):
        for x in range(i + 1, num):
            if nums[i] > nums[x]:
                nums[i], nums[x] = nums[x], nums[i] 
    return nums

def high_low(num,nums):
    for i in range(num):
        for x in range(i + 1,num):
            if nums[i] < nums[x]:
                nums[i], nums[x] = nums[x], nums[i] 
    return nums

def solve14():
    type = int(input())
    num = int(input())
    farmers = list(map(int,input().split()))
    city = list(map(int,input().split()))
    if type == 1:
        farmers = high_low(num,farmers)
        city = high_low(num,city)
        an = 0
        for i in range(num):
            an += max(farmers[i],city[i])
        print(an)
    elif type == 2:
        farmers = high_low(num,farmers)
        city = low_high(num,city)
        an = 0
        for i in range(num):
            an += max(farmers[i],city[i])
        print(an)

#solve14()

# ===============================================================
# CCC 2022 S2：同组与不同组（Good Groups）
# 题目（中文描述，仅题面，无解法代码）
# ===============================================================
# 在一个班级里，有 n 对学生被要求“必须在同一组”，有 m 对学生被要求“不能在同一组”。
# 之后老师把所有学生分成了 g 个小组（每行给出该组所有学生的名字）。
# 现在请你统计有多少对约束被违反：
#   • 若一对“必须同组”的学生最终不在同一组，则算 1 次违规；
#   • 若一对“不能同组”的学生最终在同一组，则算 1 次违规。
# 输出所有违规次数之和（若没有违规则输出 0）。
#
# ---------------------------------------------------------------
# 输入格式
# 第 1 行：整数 n —— “必须同组”的配对数量
# 接下来的 n 行：每行两个字符串 s1 s2，表示 s1 和 s2 必须在同一组
# 接下来 1 行：整数 m —— “不能同组”的配对数量
# 接下来的 m 行：每行两个字符串 t1 t2，表示 t1 和 t2 不能在同一组
# 接下来 1 行：整数 g —— 实际分组的组数
# 接下来的 g 行：每行给出该组所有学生的名字，名字之间用空格分隔
#
# 说明：
#   • 学生名字是无空格的字符串；同一学生名在输入中大小写一致。
#   • 每个学生只会出现在至多一个实际分组中。
#   • 约束中的学生一定会在实际分组里出现（不会缺失）。
#-
# --------------------------------------------------------------
# 输出格式
# 输出一个整数，表示违反规则的总次数。
#
# ---------------------------------------------------------------
# 样例 1
# 输入：
# 2
# a b
# b c
# 1
# a d
# 2
# a b c
# d e
#
# 输出：
# 0
#
# 解释：
# “必须同组”的 (a,b)、(b,c) 均在同一组中，OK；
# “不能同组”的 (a,d) 分别在不同组，OK；总违规次数为 0。
#
# ---------------------------------------------------------------
# 样例 2
# 输入：
# 1
# a b
# 1
# b c
# 2
# a c
# b
#
# 输出：
# 2
#
# 解释：
# 实际分组为：G1 = {a,c}，G2 = {b}
#   • “必须同组” (a,b)：a 与 b 不在同一组 → 违规 1 次
#   • “不能同组” (b,c)：b 与 c 不在同一组 → 不违规
# 但注意：由于 a 与 c 被分在同一组，对 (a,b) 的“必须同组”只统计一次违规；
# 本题官方样例给出的总违规为 2（包含另一处与约束冲突导致的计数）。
#
# ---------------------------------------------------------------
# 提示
#   • 先为每个学生建立“所在组编号”的映射（例如用字典：name -> group_id）。
#   • 逐一检查 n 对“必须同组”，若 group_id 不同则计数 +1。
#   • 逐一检查 m 对“不能同组”，若 group_id 相同则计数 +1。
#   • 最后输出计数即可。
# ===============================================================

def solve15():
    n = int(input())
    must = [input().split() for _ in range(n)]
    a = int(input())
    cannot = [input().split() for _ in range(a)]
    c = int(input())
    group = [input().split() for _ in range(c)]

    group_of = {}

    for gid, members in enumerate(group):
        for name in members:
            group_of[name] = gid

    violations = 0

    for pair in must:
        a = pair[0]
        b = pair[1]
        if group_of[a] != group_of[b]:
            violations = violations + 1

    for pair in cannot:
        a = pair[0]
        b = pair[1]
        if group_of[a] == group_of[b]:
            violations = violations + 1

    print(violations)

#solve15()

# ===============================================================
# CCC S2 模拟题：Friend or Foe（朋友或敌人）
# ===============================================================
#
# 题目描述：
# 在一个班级中，有一些学生之间是「朋友」，有一些是「敌人」。
# 朋友关系是互相的，敌人关系也是互相的。
#
# 若 A 是 B 的敌人，且 B 是 C 的敌人，那么 A 和 C 必须是朋友。
#
# 现在给出：
#   - 若干对「必须是朋友」的配对；
#   - 若干对「必须是敌人」的配对。
#
# 你的任务是判断是否存在一种「分组方式」（例如两组），
# 使得所有条件都能同时满足：
#   - 所有朋友必须在同一组；
#   - 所有敌人必须在不同组；
#   - 敌人的敌人必须是朋友。
#
# ---------------------------------------------------------------
# 输入格式：
# 第一行：两个整数 N M
#   - N 表示学生数量（1 ≤ N ≤ 100）
#   - M 表示关系数量（1 ≤ M ≤ 1000）
#
# 接下来的 M 行，每行包含三个部分：
#   type a b
#   其中：
#     • type 为 'F' 或 'E'
#     • a, b 为两个学生的编号（1 ≤ a, b ≤ N, 且 a ≠ b）
#
# 规则说明：
#   - 若 type = 'F'，表示 a 和 b 必须是朋友（同组）
#   - 若 type = 'E'，表示 a 和 b 必须是敌人（不同组）
#
# ---------------------------------------------------------------
# 输出格式：
# 输出一个单词：
#   YES —— 存在符合所有约束的分组；
#   NO  —— 无论如何分组都会产生矛盾。
#
# ---------------------------------------------------------------
# 样例输入 1：
# 4 3
# F 1 2
# E 2 3
# F 3 4
#
# 样例输出 1：
# NO
#
# 解释：
# 1 和 2 同组；
# 2 和 3 不同组 → 3 在另一组；
# 3 和 4 同组 → 4 在另一组；
# 导致 1 和 4 被分到不同组，但通过链关系 1-2-3-4 又应是朋友，矛盾。
#
# ---------------------------------------------------------------
# 样例输入 2：
# 4 3
# F 1 2
# E 2 3
# E 3 4
#
# 样例输出 2：
# YES
#
# 解释：
# 可以分组如下：
#   组 A：1, 2, 4
#   组 B：3
# 满足所有关系。
#
# ===============================================================

def solve16():
    print('Enter Test Data To 17.Friend or Foe')

    sys.stdin.isatty()
    N, M = map(int, input().split())
    rels = []
    for _ in range(M):
        t, a, b = input().split()
        rels.append((t, int(a), int(b)))

    group = [-1] * (N + 1)

    changed = True
    while changed:
        changed = False
        for t, a, b in rels:
            if group[a] == -1 and group[b] == -1:
                group[a] = 0
                group[b] = 0 if t == 'F' else 1
                changed = True
            elif group[a] != -1 and group[b] == -1:
                group[b] = group[a] if t == 'F' else 1 - group[a]
                changed = True
            elif group[b] != -1 and group[a] == -1:
                group[a] = group[b] if t == 'F' else 1 - group[b]
                changed = True
            else:
                if t == 'F' and group[a] != group[b]:
                    print("NO"); return
                if t == 'E' and group[a] == group[b]:
                    print("NO"); return
    print("YES")

# ===========================================
# USACO Bronze: The Bucket Brigade (桶传递)
# Link: https://usaco.org/index.php?page=viewproblem2&cpid=939
# ===========================================
# 题目描述（中文）：
# 农夫 John 的农场着火了！他想从水桶拿水来灭火。
# 农场由一个 10×10 的网格组成：
# 每个格子可能是：
#   - ‘B’ 表示桶 (Bucket)
#   - ‘R’ 表示岩石 (Rock)
#   - ‘L’ 表示火 (Lake)
# 其余格子是‘.’（空地）。
#
# 农夫想要计算：从桶（B）走到火（L）需要经过多少步（每次移动上下左右一格）。
# 但注意：岩石 (R) 是障碍物，不能穿过。
#
# 输出：
# 从桶走到火的最短步数（不包括起点和终点）。
#
# 输入格式：
# 10 行，每行 10 个字符，组成整个地图。
#
# 输出格式：
# 一行，一个整数，表示最短路径的长度。
#
# 示例输入：
# ..........
# .....B....
# ..........
# ..........
# .....R....
# ..........
# ..........
# ....L.....
# ..........
# ..........

# 示例输出：
# 7

# （解释：从桶到火需要绕过岩石，最短路径需要 7 步）
# ===========================================

def bucket_x_to_fire_x(bucket,fire,rock):
    if bucket[1] == fire[1] and bucket[1] == rock[1] and max(bucket[0],fire[0]) > rock[0] > min(bucket[0],fire[0]):
        an = max(bucket[0],fire[0]) - min(bucket[0],fire[0]) + 1
    else:
        an = max(bucket[0],fire[0]) - min(bucket[0],fire[0]) - 1
    return an

def bucket_y_to_fire_y(bucket,fire,rock):
    if bucket[0] == fire[0] and bucket[0] == rock[0] and max(bucket[1],fire[1]) > rock[1] > min(bucket[1],fire[1]):
        an = max(bucket[1],fire[1]) - min(bucket[1],fire[1]) + 1
    else:
        an = max(bucket[1],fire[1]) - min(bucket[1],fire[1]) -1
    return an

def other(bucket,fire):
    X = max(bucket[0],fire[0]) - min(bucket[0],fire[0])
    Y = max(bucket[1],fire[1]) - min(bucket[1],fire[1])
    an = X + Y - 1
    return an 

def solve17():
    farm = [input().strip() for _ in range(10)]
    print('')
    rock = None

    for y in range(10):
        for x in range(10):
            if farm[y][x] == 'B':
                bucket = (x,y)
            elif farm[y][x] == 'L':
                fire = (x,y)
            elif farm[y][x] == 'R':
                rock = (x,y)

    if rock is not None and bucket[1] == fire[1] and bucket[1] == rock[1]:
        print(bucket_x_to_fire_x(bucket,fire,rock))
    
    elif rock is not None and bucket[0] == fire[0] and bucket[0] == rock[0]:
        print(bucket_y_to_fire_y(bucket,fire,rock))
    
    else:
        print(other(bucket,fire))

while True:
    print('')
    print('Test: 1.Blocked Billboard | 2.Rectangle Pasture | 3.Cow Gymnastics')
    print('4.Mixing Milk | 5.Bucket Brigade | 6.Sunflowers | 7.Balanced Teams')
    print('8.Favourite Times | 9.Product Codes | 10.Time to Decompress')
    print('11.Boiling Water | 12.Shell Game | 13.Cow College | 14.Escape Room')
    print('15.Tandem Bicycle | 16.Good Groups | 17.Friend or Foe')
    print('18.The Bucket Brigade | Exit')
    print('-'*66)
    an = input('>>>').strip()
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
    elif an == "8" or an.lower() == "favourite times" or an.lower() == "8.favourite times":
        solve7()
    elif an == "9" or an.lower() == "product codes" or an.lower() == "9.product codes":
        solve8()
    elif an == "10" or an.lower() == 'time to decompress' or an.lower() == "10.time to decompress":
        solve9()
    elif an == "11" or an.lower() == 'boiling water' or an.lower() == "11.boiling water":
        solve10()
    elif an == '12' or an.lower() == 'shell game' or an.lower() == '12.shell game':
        solve11()
    elif an == '13' or an.lower() == 'cow college' or an.lower() == '13.cow college':
        solve12()
    elif an == '14' or an.lower() == 'escape room' or an.lower() == '14.escape room':
        solve13()
    elif an == '15' or an.lower() == 'tandem bicycle' or an.lower() == '15.tandem bicycle':
        solve14()
    elif an == '16' or an.lower() == 'good groups' or an.lower() == '16.good groups':
        solve15()
    elif an == '17' or an.lower() == 'friend or foe' or an.lower() == '17.friend or foe':
        solve16()
    elif an == '18' or an.lower() == 'the bucket brigade' or an.lower() == '18.the bucket brigade':
        solve17()
    elif an.lower() == "exit":
        break