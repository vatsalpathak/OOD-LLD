# --------------------- Problem Description ---------------------
# You are given a list of employee-manager relationships as CSV pairs.
# You must implement a permission assignment system.
#
# Input:
# - List of (employee, manager) pairs (e.g., E1, M1)
# - A target employee
#
# Output:
# - Return a list of all employees who should be granted permission
#   (the target and everyone under them in the org chart)
#
# Example:
# Input:
#   pairs = [("E1", "M1"), ("E2", "M1"), ("M1", "M2")]
#   target = "M1"
#
# Output:
#   ['M1', 'E1', 'E2']   # M1 and all under them
#
# Notes:
# The org chart is a tree. You can use DFS/BFS to collect all subordinates.

from collections import defaultdict

class PermissionAssigner:

    def assign_permissions_brute_force(self, pairs, target):
        tree = defaultdict(list)
        for emp, mgr in pairs:
            tree[mgr].append(emp)

        result = []

        def dfs(emp):
            result.append(emp)
            for sub in tree[emp]:
                print("sub : ",sub)
                dfs(sub)

        dfs(target)
        return result

    def assign_permissions_optimized(self, pairs, target):
        tree = defaultdict(list)
        for emp, mgr in pairs:
            tree[mgr].append(emp)


        memo = {}

        def dfs(emp):
            if emp in memo:
                return memo[emp]
            result = [emp]
            for sub in tree[emp]:
                result.extend(dfs(sub))
            memo[emp] = result
            return result

        return dfs(target)


# --------------------- Test the Code ---------------------
if __name__ == "__main__":
    pairs = [("E1", "M1"), ("E2", "M1"), ("M1", "M2")]
    target = "E2"

    assigner = PermissionAssigner()

    print("\n Brute Force Result:")
    print(assigner.assign_permissions_brute_force(pairs, target))

    print("\n Optimized Result:")
    print(assigner.assign_permissions_optimized(pairs, target))
