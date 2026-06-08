from __future__ import annotations


class TaskNode:
    """Nó personalizado para a árvore de requisitos (RF-03)."""

    def __init__(self, task_id: int, name: str):
        self.id = task_id
        self.name = name
        self.depends_on: list[TaskNode] = []   # tarefas que este nó depende
        self.required_by: list[TaskNode] = []  # tarefas que dependem deste nó
        self.children: list[TaskNode] = []     # filhos na arvore (dependencias diretas)
        self.parent: TaskNode | None = None    # pai na arvore

    def add_dependency(self, node: TaskNode):
        """Adiciona uma dependencia (self depende de node)."""
        if node not in self.depends_on:
            self.depends_on.append(node)
            node.required_by.append(self)

    def add_child(self, node: TaskNode):
        """Adiciona um filho na arvore (node depende de self)."""
        if node not in self.children and node != self:
            self.children.append(node)
            node.parent = self

    def is_root(self) -> bool:
        """Verifica se é um nó raiz (nao depende de ninguem)."""
        return len(self.depends_on) == 0

    def is_leaf(self) -> bool:
        """Verifica se é uma folha (ninguem depende dela)."""
        return len(self.required_by) == 0

    def get_depth(self) -> int:
        """Retorna a profundidade do nó na arvore."""
        depth = 0
        current = self
        while current.parent:
            depth += 1
            current = current.parent
        return depth

    def to_dict(self) -> dict:
        """Converte para dicionario (compativel com formato antigo)."""
        return {
            "id": self.id,
            "name": self.name,
            "depends_on": [dep.id for dep in self.depends_on]
        }

    def __repr__(self):
        return f"TaskNode(id={self.id}, name={self.name})"
