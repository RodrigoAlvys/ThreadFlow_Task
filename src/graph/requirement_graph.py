from __future__ import annotations

from .task_node import TaskNode


class RequirementGraph:
    """Grafo de dependências personalizado para RF-03."""

    def __init__(self):
        self.nodes_by_id: dict[int, TaskNode] = {}
        self.nodes_by_name: dict[str, TaskNode] = {}

    def add_task(self, task_id: int, name: str) -> TaskNode:
        """Adiciona ou retorna um nó existente."""
        if task_id in self.nodes_by_id:
            return self.nodes_by_id[task_id]

        node = TaskNode(task_id, name)
        self.nodes_by_id[task_id] = node
        self.nodes_by_name[name.lower()] = node
        return node

    def add_dependency(self, task_id: int, depends_on_id: int):
        """Cria relação: task_id depende de depends_on_id."""
        task_node = self.nodes_by_id.get(task_id)
        dep_node = self.nodes_by_id.get(depends_on_id)

        if task_node is None or dep_node is None:
            raise ValueError(f"Task ou dependência não encontrada: {task_id} -> {depends_on_id}")

        task_node.add_dependency(dep_node)

    def get_node(self, task_id: int) -> TaskNode | None:
        return self.nodes_by_id.get(task_id)

    def get_node_by_name(self, name: str) -> TaskNode | None:
        return self.nodes_by_name.get(name.lower())

    def all_nodes(self) -> list[TaskNode]:
        return list(self.nodes_by_id.values())

    def to_task_list(self) -> list[dict]:
        """Converte o grafo para lista de dicionários."""
        tasks = []
        for node in self.all_nodes():
            tasks.append({
                "id": node.id,
                "name": node.name,
                "depends_on": [dep.id for dep in node.depends_on]
            })
        return tasks

    def __len__(self) -> int:
        return len(self.nodes_by_id)
