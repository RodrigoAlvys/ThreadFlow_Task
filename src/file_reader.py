from __future__ import annotations

import json
from src.graph import RequirementGraph


def read_txt(file_path: str) -> RequirementGraph:
    """Le arquivo .txt e retorna um RequirementGraph."""
    graph = RequirementGraph()

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split(";")

            task_id = int(parts[0])
            task_name = parts[1]

            graph.add_task(task_id, task_name)

            if len(parts) > 2 and parts[2]:
                dependencies = [int(dep) for dep in parts[2].split(",")]
                for dep_id in dependencies:
                    # Garante que o no da dependencia existe com nome temporario
                    # O nome sera atualizado se a task aparecer depois
                    graph.add_task(dep_id, f"temp_{dep_id}")
                    graph.add_dependency(task_id, dep_id)

    return graph


def read_json(file_path: str) -> RequirementGraph:
    """Le arquivo .json e retorna um RequirementGraph."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    graph = RequirementGraph()

    for task in data["tasks"]:
        task_id = task["id"]
        task_name = task["name"]
        dependencies = task.get("depends_on", [])

        graph.add_task(task_id, task_name)

        for dep_id in dependencies:
            graph.add_task(dep_id, f"temp_{dep_id}")
            graph.add_dependency(task_id, dep_id)

    return graph


def load_file(file_path: str) -> RequirementGraph:
    """Carrega arquivo .txt ou .json e retorna um RequirementGraph."""
    if file_path.endswith(".txt"):
        return read_txt(file_path)

    if file_path.endswith(".json"):
        return read_json(file_path)

    raise ValueError("Formato invalido. Utilize .txt ou .json")
