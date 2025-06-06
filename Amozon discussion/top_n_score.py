# You are given an unsorted list of scores (integers).
# Write an algorithm to return the average of the top N scores.

# Input:
# A list of scores (e.g., [55, 92, 86, 70, 65])

# An integer N (e.g., 3)

# Output:
# A single float/int value — the average of the top N scores (e.g., 82.67)

import heapq
class TopNAverager:
    def average_top_n_brute(self, scores, n):
        if n <= 0 or n > len(scores):
            return 0
        top_scores = sorted(scores, reverse=True)[:n]
        return sum(top_scores) / n

    def average_top_n_heap(self, scores, n):
        if n <= 0 or n > len(scores):
            return 0

        min_heap = []
        for score in scores:
            heapq.heappush(min_heap, score)
            if len(min_heap) > n:
                heapq.heappop(min_heap)

        return sum(min_heap) / n

if __name__ == "__main__":
    scores = [55, 92, 86, 70, 65]
    top_n = 3

    averager = TopNAverager()
    print("Brute Force:", averager.average_top_n_brute(scores, top_n)) 
    print("Optimized Heap:", averager.average_top_n_heap(scores, top_n))
