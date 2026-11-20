import time
import pandas as pd

def prepare_data(df):
    out = df.copy()
    out["change"] = out["Close"].diff()
    return out

def brute_force(a):
    start = end = 0
    best = 0
    for i in range(len(a)):
        total = 0
        for j in range(i, len(a)):
            total += a[j]
            if total > best:
                best, start, end = total, i, j
    return {"profit":best,"start":start,"end":end}

def kadane(a):
    best = current = 0
    start = best_start = best_end = 0
    for i, value in enumerate(a):
        if current + value < 0:
            current = 0
            start = i + 1
        else:
            current += value
        if current > best:
            best, best_start, best_end = current, start, i
    return {"profit":best,"start":best_start,"end":best_end}

def divide_conquer(a):
    def solve(lo, hi):
        if lo == hi:
            return (max(0, a[lo]), lo, hi) if a[lo] > 0 else (0, lo, lo)
        mid = (lo + hi)//2
        left = solve(lo, mid)
        right = solve(mid+1, hi)
        total = 0; best_left = 0; best_left_i = mid
        for i in range(mid, lo-1, -1):
            total += a[i]
            if total > best_left:
                best_left, best_left_i = total, i
        total = 0; best_right = 0; best_right_i = mid+1
        for i in range(mid+1, hi+1):
            total += a[i]
            if total > best_right:
                best_right, best_right_i = total, i
        cross = (best_left+best_right, best_left_i, best_right_i)
        return max([left,right,cross], key=lambda x:x[0])
    if not a: return {"profit":0,"start":0,"end":0}
    p,s,e = solve(0,len(a)-1)
    return {"profit":p,"start":s,"end":e}

def compare_algorithms(a):
    specs = [
        ("Brute Force", brute_force, "O(n²)"),
        ("Divide and Conquer", divide_conquer, "O(n log n)"),
        ("Kadane", kadane, "O(n)")
    ]
    result = {}
    for name, fn, complexity in specs:
        start = time.perf_counter()
        answer = fn(a)
        elapsed = (time.perf_counter()-start)*1000
        answer.update({"complexity":complexity,"runtime_ms":elapsed})
        result[name] = answer
    return result

def max_profit_k(prices, k):
    n = len(prices)
    if n < 2 or k <= 0: return 0
    if k >= n//2:
        return sum(max(0, prices[i]-prices[i-1]) for i in range(1,n))
    dp = [[0]*n for _ in range(k+1)]
    for t in range(1,k+1):
        best = -prices[0]
        for day in range(1,n):
            dp[t][day] = max(dp[t][day-1], prices[day]+best)
            best = max(best, dp[t-1][day]-prices[day])
    return dp[k][-1]
