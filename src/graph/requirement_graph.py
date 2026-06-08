from __future__ import annotations

from collections import deque
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

    def topological_sort(self) -> list[TaskNode]:
        """
        Retorna a ordem topológica das tasks usando algoritmo de Kahn.
        Tasks sem dependências vêm primeiro.
        Se houver ciclo, retorna lista vazia.
        Complexidade: O(n + m)

        Returns:
            list[TaskNode]: Lista de tasks em ordem topológica.
                           Lista vazia se ciclo for detectado.
        """
        # Calcula grau de entrada (quantas dependências cada task tem)
        indegrees = {node.id: 0 for node in self.all_nodes()}
        for node in self.all_nodes():
            for dep in node.depends_on:
                indegrees[node.id] += 1

        # Fila com tasks que não têm dependências
        zero_queue = deque()
        for task_id, count in indegrees.items():
            if count == 0:
                zero_queue.append(task_id)

        order_ids = []

        while zero_queue:
            task_id = zero_queue.popleft()
            order_ids.append(task_id)

            node = self.get_node(task_id)
            if node:
                # Remove as arestas saindo deste nó
                for dependent in node.required_by:
                    indegrees[dependent.id] -= 1
                    if indegrees[dependent.id] == 0:
                        zero_queue.append(dependent.id)

        # Se não processamos todos os nós, há ciclo
        if len(order_ids) != len(self):
            return []

        return [self.get_node(task_id) for task_id in order_ids]

    def get_topological_order_as_ids(self) -> list[int]:
        """Retorna a ordem topológica como lista de IDs."""
        return [node.id for node in self.topological_sort()]

    def get_topological_order_as_names(self) -> list[str]:
        """Retorna a ordem topológica como lista de nomes."""
        return [node.name for node in self.topological_sort()]

    def has_valid_topological_order(self) -> bool:
        """Verifica se é possível obter uma ordem topológica válida."""
        return len(self.topological_sort()) == len(self)

    def __len__(self) -> int:
        return len(self.nodes_by_id)
