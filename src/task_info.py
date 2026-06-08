from .task_search import TASK_NOT_FOUND, TaskSearcher


def _dependency_ids(task):
    return task.get("depends_on", task.get("dependencies", []))


def _task_label(task):
    return task.get("name", f"ID {task.get('id')}")


def _format_task_list(tasks):
    if not tasks:
        return "[]"

    return "[" + ", ".join(_task_label(task) for task in tasks) + "]"


def get_task_info(tasks, term):
    searcher = TaskSearcher(tasks)
    task = searcher.find(term)

    if task == TASK_NOT_FOUND:
        return TASK_NOT_FOUND

    task_id = task["id"]
    dependencies = []
    dependents = []

    for dependency_id in _dependency_ids(task):
        dependency = searcher.find_by_id(dependency_id)

        if dependency != TASK_NOT_FOUND:
            dependencies.append(dependency)

    for current_task in searcher.tasks:
        if task_id in _dependency_ids(current_task):
            dependents.append(current_task)

    return {
        "id": task_id,
        "name": task.get("name", ""),
        "depends_on": dependencies,
        "required_by": dependents,
    }


def format_task_info(tasks, term):
    info = get_task_info(tasks, term)

    if info == TASK_NOT_FOUND:
        return TASK_NOT_FOUND

    return "\n".join(
        [
            f"Task: {info['name']} (ID: {info['id']})",
            f"depende de: {_format_task_list(info['depends_on'])}",
            f"é requisitada por: {_format_task_list(info['required_by'])}",
        ]
    )
