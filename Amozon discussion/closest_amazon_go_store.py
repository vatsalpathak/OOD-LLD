# --------------------- Problem Description ---------------------
# You are given a 2D matrix grid of city blocks:
# - 'G' represents an Amazon Go store
# - 'B' represents a building
#
# You need to return a matrix where each cell (that was originally a 'B')
# contains the minimum distance to the closest 'G' (Amazon Go store).
#
# Distance is measured in terms of number of moves (up, down, left, right).
#
# Example:
# Input:
# grid = [
#     ['B', 'B', 'B'],
#     ['B', 'B', 'B'],
#     ['G', 'B', 'B']
# ]
#
# Output:
# [
#     [2, 3, 4],
#     [1, 2, 3],
#     [0, 1, 2]
# ]

from collections import deque

class GoStoreDistance:

    def __init__(self) -> None:
        self.dirs = [[0,1],[0,-1],[1,0],[-1,0]]

    def compute_distance_brute_force(self,grid):
        m, n = len(grid), len(grid[0])
        result = [[0] * n for _ in range(m)]
        print(result)

        def bfs(r,c):
            visited = [[False]*n for _ in range(m)]
            q = deque([(r,c,0)])
            visited[r][c] = True
            while q:
                x,y,dist = q.popleft()
                if grid[x][y] == 'G':
                    return dist
                
                for dr in self.dirs:
                    nr, nc = x + dr[0], y + dr[1]
                    if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc]:
                        visited[nr][nc] = True
                        q.append((nr,nc,dist+1))
            return -1

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 'G':
                    result[r][c] =  0
                else:
                    result[r][c] = bfs(r,c)
        
        return result

    def compute_distance_optimized(self,grid):
        m, n = len(grid), len(grid[0])
        result = [[-1] * n for _ in range(m)]
        print(result)
        visited = [[False] * n for _ in range(m)]
        q = deque()

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 'G':
                    q.append((r,c,0))
                    visited[r][c] = True
                    result[r][c] =  0

        while q:
            x,y,dist = q.popleft()
            for dr in self.dirs:
                nr, nc = x + dr[0], y + dr[1]
                if 0<= nr < m and 0 <= nc < n and not visited[nr][nc]:
                    visited[nr][nc] = True
                    result[nr][nc] = dist + 1
                    q.append((nr,nc,dist+1))

        
        return result


if __name__ == "__main__":
    grid = [
        ['B', 'B', 'B'],
        ['B', 'B', 'B'],
        ['G', 'B', 'B']
    ]

    solver = GoStoreDistance()

    print("\n Brute Force Result:")
    for row in solver.compute_distance_brute_force(grid):
        print(row)

    print("\n Optimized Result:")
    for row in solver.compute_distance_optimized(grid):
        print(row)
