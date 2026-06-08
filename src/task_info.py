from __future__ import annotations

from task_search import TASK_NOT_FOUND, TaskSearcher


def _dependency_ids(task):
    """Extrai IDs das dependências da task."""
    return task.get("depends_on", task.get("dependencies", []))


def _task_label(task):
    """Retorna o nome da task ou fallback."""
    return task.get("name", f"ID {task.get('id')}")


def _format_task_list(tasks):
    """Formata lista de tasks para exibição."""
    if not tasks:
        return "[]"

    return "[" + ", ".join(_task_label(task) for task in tasks) + "]"


def get_task_info(tasks, term):
    """
    Retorna informações detalhadas de uma task (RF-09).
    
    Returns:
        dict: Com chaves: id, name, depends_on, required_by
        ou TASK_NOT_FOUND se não encontrar
    """
    searcher = TaskSearcher(tasks)
    task = searcher.find(term)

    if task == TASK_NOT_FOUND:
        return TASK_NOT_FOUND

    task_id = task["id"]
    dependencies = []
    dependents = []

    # Busca as tasks das quais esta depende
    for dependency_id in _dependency_ids(task):
        dependency = searcher.find_by_id(dependency_id)
        if dependency != TASK_NOT_FOUND:
            dependencies.append(dependency)

    # Busca as tasks que dependem desta
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
    """
    Formata as informações da task para exibição no terminal.
    
    Returns:
        str: Texto formatado ou TASK_NOT_FOUND
    """
    info = get_task_info(tasks, term)

    if info == TASK_NOT_FOUND:
        return TASK_NOT_FOUND

    lines = [
        f"Task: {info['name']} (ID: {info['id']})",
        f"depende de: {_format_task_list(info['depends_on'])}",
        f"é requisitada por: {_format_task_list(info['required_by'])}",
    ]
    
    return "\n".join(lines)   )
