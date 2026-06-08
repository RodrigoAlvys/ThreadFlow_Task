from __future__ import annotations


class TaskNode:
    """Nó personalizado para a árvore de requisitos (RF-03)."""

    def __init__(self, task_id: int, name: str):
        self.id = task_id
        self.name = name
        self.depends_on: list[TaskNode] = []   # tarefas que este nó depende
        self.required_by: list[TaskNode] = []  # tarefas que dependem deste nó

    def add_dependency(self, node: TaskNode):
        """Adiciona uma dependência (self depende de node)."""
        if node not in self.depends_on:
            self.depends_on.append(node)
            node.required_by.append(self)

    def to_dict(self) -> dict:
        """Converte para dicionário (compatível com formato antigo)."""
        return {
            "id": self.id,
            "name": self.name,
            "depends_on": [dep.id for dep in self.depends_on]
        }

    def __repr__(self):
        return f"TaskNode(id={self.id}, name={self.name})"

