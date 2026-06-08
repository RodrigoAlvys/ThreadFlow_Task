def has_cycle(tasks):
    graph = {}

    for task in tasks:
        graph[task["id"]] = task["depends_on"]

    visited = set()
    recursion_stack = set()

    def dfs(task_id):
        if task_id in recursion_stack:
            return True

        if task_id in visited:
            return False

        visited.add(task_id)
        recursion_stack.add(task_id)

        for dependency in graph.get(task_id, []):
            if dfs(dependency):
                return True

        recursion_stack.remove(task_id)
        return False

    for task_id in graph:
        if dfs(task_id):
            return True

    return False