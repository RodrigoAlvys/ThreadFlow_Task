def get_tree_stats(tasks):
    total_tasks = len(tasks)

    total_dependencies = 0
    most_dependencies_task = None

    dependency_count = {}

    for task in tasks:
        dependencies = task["depends_on"]

        total_dependencies += len(dependencies)

        if (
            most_dependencies_task is None
            or len(dependencies) > len(most_dependencies_task["depends_on"])
        ):
            most_dependencies_task = task

        for dependency in dependencies:
            if dependency not in dependency_count:
                dependency_count[dependency] = 0

            dependency_count[dependency] += 1

    most_requested_task = None
    highest_count = -1

    for task in tasks:
        count = dependency_count.get(task["id"], 0)

        if count > highest_count:
            highest_count = count
            most_requested_task = task

    return {
        "total_tasks": total_tasks,
        "total_dependencies": total_dependencies,
        "most_dependencies_task": most_dependencies_task,
        "most_requested_task": most_requested_task
    }