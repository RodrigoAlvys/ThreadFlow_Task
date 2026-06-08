from __future__ import annotations

from cycle_detector import has_cycle
from .requirement_graph import RequirementGraph
from .task_node import TaskNode


class TreeBuilder:
    """Constrói a árvore de dependências a partir do grafo (RF-03)."""

    def __init__(self, graph: RequirementGraph):
        self.graph = graph
        self.roots: list[TaskNode] = []
        self._built = False

    def _validate_no_cycles(self):
        """Valida que não há dependências circulares usando cycle_detector."""
        tasks_list = self.graph.to_task_list()
        if has_cycle(tasks_list):
            cycle_tasks = self._find_cycle_tasks()
            raise ValueError(f"Deadloop detectado: {' -> '.join(cycle_tasks)}")

    def _find_cycle_tasks(self) -> list[str]:
        """Identifica as tasks envolvidas no primeiro ciclo encontrado."""
        visited = set()
        stack = []

        def dfs(task_id: int) -> list[int] | None:
            if task_id in stack:
                cycle_start = stack.index(task_id)
                return stack[cycle_start:] + [task_id]

            if task_id in visited:
                return None

            visited.add(task_id)
            stack.append(task_id)

            node = self.graph.get_node(task_id)
            if node:
                for dep in node.depends_on:
                    result = dfs(dep.id)
                    if result:
                        return result

            stack.pop()
            return None

        for node in self.graph.all_nodes():
            result = dfs(node.id)
            if result:
                task_names = []
                for tid in result:
                    n = self.graph.get_node(tid)
                    if n:
                        task_names.append(f"{n.name}(ID:{tid})")
                return task_names

        return ["ciclo detectado"]

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

    def _build_tree_recursive(self, node: TaskNode, visited: set[int]):
        """Constrói a árvore recursivamente a partir de um nó."""
        if node.id in visited:
            return

        visited.add(node.id)

        for dependent in node.required_by:
            node.add_child(dependent)
            self._build_tree_recursive(dependent, visited)

    def build(self) -> list[TaskNode]:
        """
        Constrói e retorna as raízes da árvore de dependências.
        Complexidade: O(n + m) para detecção de ciclo + O(n log n) para ordenação.
        """
        if self._built:
            return self.roots

        self._validate_no_cycles()
        self._validate_all_dependencies_exist()

        visited: set[int] = set()
        self.roots = []

        for node in self.graph.all_nodes():
            if node.is_root():
                self.roots.append(node)

        if not self.roots and len(self.graph) > 0:
            raise ValueError("Ciclo detectado: nenhuma tarefa é independente")

        for root in sorted(self.roots, key=lambda x: x.id):
            self._build_tree_recursive(root, visited)

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

    def has_cycle(self) -> bool:
        """Verifica se o grafo contém ciclo."""
        tasks_list = self.graph.to_task_list()
        return has_cycle(tasks_list)

    def print_tree_summary(self) -> str:
        """Retorna um resumo da árvore para exibição."""
        if not self._built:
            self.build()

        lines = []
        lines.append(f"Total de tasks: {len(self.graph)}")
        lines.append(f"Tasks raiz: {len(self.roots)}")
        lines.append(f"Profundidade maxima: {self.get_tree_depth()}")

        if self.roots:
            lines.append("\nRaizes:")
            for root in self.roots:
                lines.append(f"  - [{root.id}] {root.name}")

        return "\n".join(lines)

    def get_topological_order(self) -> list[TaskNode]:
        """
        Retorna a ordem topológica das tasks usando o método do grafo.
        Se houver ciclo, retorna lista vazia e não constrói a árvore.
        """
        return self.graph.topological_sort()

    def get_topological_order_as_names(self) -> list[str]:
        """Retorna a ordem topológica como lista de nomes."""
        return [node.name for node in self.get_topological_order()]

    def get_topological_order_as_ids(self) -> list[int]:
        """Retorna a ordem topológica como lista de IDs."""
        return [node.id for node in self.get_topological_order()]
