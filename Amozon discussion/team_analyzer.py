# --------------------- Problem Description ---------------------
# In a gaming league, players form teams via connections.
# Each player has a score.
#
# Input:
# - N: Number of connections
# - M: Number of players
# - K: Top K scores to return per team
# - M player names (space-separated)
# - N pairs of player names (indicating a connection)
# - M scores in same order as names
#
# Output:
# - For each connected team, return top K scores (in descending order)
# 
# Example:
# Input:
# 6 8 2
# Alex Bob Charlie David Eva Frank George Henry
# Alex Bob
# Bob Charlie
# David Eva
# Eva Frank
# George Henry
# Frank George
# 85 92 78 95 88 73 89 91
#
# Output: [[92, 85], [95, 91]]
# (3 teams with their top 2 scores)


from collections import defaultdict, deque
import heapq

class TeamAnalyzer:

    def get_top_k_brute_force(self, K, names, connections, scores):
        name_to_index =  {name: i for i,name in enumerate(names)}
        graph = defaultdict(list)
        
        for u,v in connections:
            graph[u].append(v)
            graph[v].append(u)

        visited = set()

        result = []

        def bfs(start):
            team = []
            queue = deque([start])
            visited.add(start)

            while queue:
                player = queue.popleft()
                team.append(player)
                for neighbor in graph[player]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            return team
        
        for name in names:
            if name not in visited:
                team = bfs(name)
                
                #score for the team 
                team_score = [scores[name_to_index[player]] for player in team]
                top_k = sorted(team_score,reverse=True)[:K]
                result.append(top_k)
        return result

    def get_top_k_optimized(self, K, names, connections, scores):
        name_to_index = {name:i for i,name in enumerate(names)}
        graph = defaultdict(list)

        for u,v in connections:
            graph[u].append(v)
            graph[v].append(u)

        visited = set()

        result = []

        def bfs(start):
            team = []
            queue = deque([start])
            visited.add(start)

            while queue:
                player = queue.popleft()
                team.append(player)
                for neighbor in graph[player]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            return team

        for name in names:
            if name not in visited:
                team = bfs(name)
                
                #score
                min_heap = []
                for player in team:
                    score = scores[name_to_index[player]]
                    heapq.heappush(min_heap,score)
                    if len(min_heap) > K:
                        heapq.heappop(min_heap)
                result.append(sorted(min_heap, reverse=True))
        return result




# --------------------- Test the Code ---------------------
if __name__ == "__main__":
    N, M, K = 6, 8, 2
    names = ["Alex", "Bob", "Charlie", "David", "Eva", "Frank", "George", "Henry"]
    connections = [
        ("Alex", "Bob"),
        ("Bob", "Charlie"),
        ("David", "Eva"),
        ("Eva", "Frank"),
        ("George", "Henry"),
        ("Frank", "George"),
    ]
    scores = [85, 92, 78, 95, 88, 73, 89, 91]

    analyzer = TeamAnalyzer()

    print("\nBrute Force Results:")
    print(analyzer.get_top_k_brute_force(K, names, connections, scores))  

    print("\nOptimized (Heap) Results:")
    print(analyzer.get_top_k_optimized(K, names, connections, scores))   
