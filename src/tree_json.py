import json
from collections import deque


def _dependency_ids(task):
    return task.get("depends_on", task.get("dependencies", []))


def _task_summary(task):
    return {
        "id": task["id"],
        "name": task.get("name", ""),
    }


def _build_graph(tasks):
    task_by_id = {task["id"]: task for task in tasks}
    children_by_id = {task_id: [] for task_id in task_by_id}
    dependency_count = {task_id: 0 for task_id in task_by_id}

    for task in tasks:
        task_id = task["id"]

        for dependency_id in _dependency_ids(task):
            if dependency_id not in task_by_id:
                continue

            children_by_id[dependency_id].append(task_id)
            dependency_count[task_id] += 1

    return task_by_id, children_by_id, dependency_count


def _topological_order(tasks, children_by_id, dependency_count):
    pending = deque(
        task_id
        for task_id, count in (
            (task["id"], dependency_count[task["id"]])
            for task in tasks
        )
        if count == 0
    )
    order = []

    while pending:
        task_id = pending.popleft()
        order.append(task_id)

        for child_id in children_by_id[task_id]:
            dependency_count[child_id] -= 1

            if dependency_count[child_id] == 0:
                pending.append(child_id)

    return order


def _build_tree_node(task_id, task_by_id, children_by_id):
    task = task_by_id[task_id]

    return {
        **_task_summary(task),
        "children": [
            _build_tree_node(child_id, task_by_id, children_by_id)
            for child_id in children_by_id[task_id]
        ],
    }


def requirements_tree_to_json(tasks):
    tasks = list(tasks)
    task_by_id, children_by_id, dependency_count = _build_graph(tasks)
    order_ids = _topological_order(
        tasks,
        children_by_id,
        dependency_count.copy(),
    )

    if len(order_ids) != len(tasks):
        data = {
            "ordem_topologica": [],
            "arvore": [],
            "erro": "deadloop detectado",
        }
        return json.dumps(data, ensure_ascii=False)

    roots = [
        task["id"]
        for task in tasks
        if not any(
            dependency_id in task_by_id
            for dependency_id in _dependency_ids(task)
        )
    ]
    data = {
        "ordem_topologica": [
            _task_summary(task_by_id[task_id])
            for task_id in order_ids
        ],
        "arvore": [
            _build_tree_node(root_id, task_by_id, children_by_id)
            for root_id in roots
        ],
        "erro": None,
    }

    return json.dumps(data, ensure_ascii=False)
