# In Amazon, all the code is stored as packages. 
#Each package has its own list of dependencies (i.e., other packages that must be installed before it).
# Write a program that takes a list of packages and their dependencies and returns a valid installation order. 
#If no valid order exists (i.e., there is a cycle), return an error or empty list.

#input 
# packages = ["A", "B", "C", "D", "E", "F"]
# dependencies = [
#     ("B", "A"),  # B depends on A
#     ("C", "A"),
#     ("D", "B"),
#     ("E", "C"),
#     ("F", "E"),
# ]

# output
# ['A', 'B', 'C', 'D', 'E', 'F']


from collections import defaultdict, deque

class PackageInstaller:
    
    # ----------------- Brute Force (DFS) -----------------
    def get_install_order_dfs(self, packages, dependencies):
        graph = defaultdict(list)
        for u, v in dependencies:
            graph[v].append(u)

        visited = set()
        on_path = set()
        result = []

        def dfs(node):
            if node in on_path:
                return False
            if node in visited:
                return True

            on_path.add(node)
            for nei in graph[node]:
                if not dfs(nei):
                    return False
            on_path.remove(node)
            visited.add(node)
            result.append(node)
            return True

        for pkg in packages:
            if pkg not in visited:
                if not dfs(pkg):
                    return []  

        return result[::-1]

    # ----------------- Optimized (Kahn’s Algorithm) -----------------
    def get_install_order_bfs(self, packages, dependencies):
        graph = defaultdict(list)
        in_degree = {pkg: 0 for pkg in packages}

        for u, v in dependencies:
            graph[v].append(u)
            in_degree[u] += 1

        queue = deque([pkg for pkg in packages if in_degree[pkg] == 0])
        result = []

        while queue:
            curr = queue.popleft()
            result.append(curr)
            for neighbor in graph[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(packages):
            return []  
        return result

if __name__ == "__main__":
    packages = ["X", "Y", "Z", "W", "V", "U"]
    dependencies = [
    ("Y", "X"),  # Y depends on X
    ("Z", "X"),  # Z depends on X
    ("W", "Y"),  # W depends on Y
    ("W", "Z"),  # W depends on Z
    ("V", "W"),  # V depends on W
    ("U", "Y"),  # U depends on Y
    ]

    installer = PackageInstaller()

    print(" Brute Force (DFS) Order:")
    print(installer.get_install_order_dfs(packages, dependencies))

    print(" Optimized (BFS / Kahn's) Order:")
    print(installer.get_install_order_bfs(packages, dependencies))
