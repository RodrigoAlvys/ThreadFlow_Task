from __future__ import annotations

from .requirement_graph import RequirementGraph
from .task_node import TaskNode


class TreeBuilder:
    """Constrói a árvore de dependências a partir do grafo (RF-03)."""

    def __init__(self, graph: RequirementGraph):
        self.graph = graph
        self.roots: list[TaskNode] = []
        self._built = False

    def _validate_all_dependencies_exist(self):
        """Valida se todas as dependências referenciadas existem no grafo."""
        missing_deps = []

        for node in self.graph.all_nodes():
            for dep in node.depends_on:
                if dep.id not in self.graph.nodes_by_id:
                    missing_deps.append((node.id, dep.id))

        if missing_deps:
            error_msg = "Dependencias faltantes encontradas:\n"
            for task_id, dep_id in missing_deps:
                error_msg += f"  Task {task_id} depende de {dep_id}, mas {dep_id} nao existe\n"
            raise ValueError(error_msg)

    def _build_tree_recursive(self, node: TaskNode, visited: set[int]) -> TaskNode:
        """Constrói a árvore recursivamente a partir de um nó."""
        if node.id in visited:
            return node

        visited.add(node.id)

        # Para cada dependência, ela se torna pai do nó atual
        for dep in node.depends_on:
            dep.add_child(node)
            self._build_tree_recursive(dep, visited)

        return node

    def build(self) -> list[TaskNode]:
        """
        Constrói e retorna as raízes da árvore de dependências.
        Complexidade: O(n log n) devido à ordenação.
        """
        if self._built:
            return self.roots

        # Valida se todas as dependências existem
        self._validate_all_dependencies_exist()

        visited: set[int] = set()
        self.roots = []

        # Encontra todos os nós raiz (não dependem de ninguém)
        for node in self.graph.all_nodes():
            if node.is_root():
                self.roots.append(node)

        # Se não houver raízes e houver nós, é um ciclo completo
        if not self.roots and len(self.graph) > 0:
            raise ValueError("Ciclo detectado: nenhuma tarefa é independente")

        # Constrói a árvore a partir de cada raiz
        for root in sorted(self.roots, key=lambda x: x.id):
            self._build_tree_recursive(root, visited)

        # Verifica se todos os nós foram visitados
        if len(visited) != len(self.graph):
            unvisited = set(self.graph.nodes_by_id.keys()) - visited
            raise ValueError(f"Nos nao conectados as raizes: {unvisited}")

        self._built = True
        return self.roots

    def get_roots(self) -> list[TaskNode]:
        """Retorna as raízes da árvore."""
        if not self._built:
            self.build()
        return self.roots

    def get_tree_depth(self) -> int:
        """Retorna a profundidade máxima da árvore."""
        if not self._built:
            self.build()
        max_depth = max((node.get_depth() for node in self.graph.all_nodes()), default=0)
        return max_depth

    def get_parent_of(self, task_id: int) -> TaskNode | None:
        """Retorna o pai de uma task na árvore."""
        if not self._built:
            self.build()
        node = self.graph.get_node(task_id)
        return node.parent if node else None

    def get_children_of(self, task_id: int) -> list[TaskNode]:
        """Retorna os filhos de uma task na árvore."""
        if not self._built:
            self.build()
        node = self.graph.get_node(task_id)
        return node.children if node else []
