# Problem Description
# You're given an array n where n[i] is the number of diamonds in the i-th rock.
# You cannot dig two adjacent rocks.

# Goal:
# Return the maximum number of diamonds that can be dug without digging two adjacent rocks.

# Example
# Input: n = [1, 3, 5, 1]
# Output: 6
# Explanation: Pick rocks at index 0 and 2 → 1 + 5 = 6


class DiamondMiner:

    def max_diamonds_brute_force(self, n):
        def dfs(i):
            if i >= len(n):
                return 0
            take = n[i] + dfs(i + 2)
            skip = dfs(i + 1)
            return max(take, skip)

        return dfs(0)

    def max_diamonds_dp(self, n):
        if not n:
            return 0
        l = len(n)
        dp = [0] * (l + 2) 

        for i in range(l - 1, -1, -1):
            dp[i] = max(n[i] + dp[i + 2], dp[i + 1])

        return dp[0]

    def max_diamonds_optimized(self, n):
        if not n:
            return 0
        if len(n) == 1:
            return n[0]

        prev2 = 0
        prev1 = 0
        for i in range(len(n) - 1, -1, -1):
            current = max(n[i] + (prev2 if i + 2 <= len(n) - 1 else 0), prev1)
            prev2 = prev1
            prev1 = current
        return prev1

if __name__ == "__main__":
    n = [2, 7, 9, 3, 1]

    miner = DiamondMiner()

    print("Brute Force Result:", miner.max_diamonds_brute_force(n))
    print("DP Result:", miner.max_diamonds_dp(n))  
    print("Optimized DP Result:", miner.max_diamonds_optimized(n))
