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
        """Usa o cycle_detector.py existente (Luiz Arthur)."""
        tasks_list = self.graph.to_task_list()
        if has_cycle(tasks_list):
            cycle_tasks = self._find_cycle_tasks()
            raise ValueError(f"Deadloop detectado: {' -> '.join(cycle_tasks)}")

    def _find_cycle_tasks(self) -> list[str]:
        """Identifica tasks envolvidas no ciclo."""
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
        print(f"DEBUG: Visitando node {node.id} - {node.name}")
        print(f"DEBUG:   depends_on: {[d.id for d in node.depends_on]}")
        print(f"DEBUG:   required_by: {[r.id for r in node.required_by]}")

        # Os filhos são as tasks que dependem deste nó
        for dependent in node.required_by:
            print(f"DEBUG:   Adicionando filho {dependent.id} - {dependent.name}")
            node.add_child(dependent)
            self._build_tree_recursive(dependent, visited)

    def build(self) -> list[TaskNode]:
        """Constrói e retorna as raízes da árvore de dependências."""
        if self._built:
            return self.roots

        self._validate_no_cycles()
        self._validate_all_dependencies_exist()

        print("\nDEBUG: Todos os nós do grafo:")
        for node in self.graph.all_nodes():
            print(f"  ID:{node.id} name:{node.name} depends_on:{[d.id for d in node.depends_on]}")

        visited: set[int] = set()
        self.roots = []

        # Encontra todos os nós raiz (não dependem de ninguém)
        for node in self.graph.all_nodes():
            if node.is_root():
                self.roots.append(node)

        print(f"\nDEBUG: Raizes encontradas: {[r.id for r in self.roots]}")

        if not self.roots and len(self.graph) > 0:
            raise ValueError("Ciclo detectado: nenhuma tarefa é independente")

        # Constrói a árvore a partir de cada raiz
        for root in sorted(self.roots, key=lambda x: x.id):
            print(f"\nDEBUG: Construindo a partir da raiz {root.id} - {root.name}")
            self._build_tree_recursive(root, visited)

        print(f"\nDEBUG: Nós visitados: {visited}")
        print(f"DEBUG: Total de nós: {len(self.graph)}")

        # Verifica se todos os nós foram visitados
        if len(visited) != len(self.graph):
            unvisited = set(self.graph.nodes_by_id.keys()) - visited
            unvisited_names = []
            for uid in unvisited:
                node = self.graph.get_node(uid)
                unvisited_names.append(f"{node.name}(ID:{uid})" if node else str(uid))
            raise ValueError(f"Nos nao conectados as raizes: {unvisited_names}")

        self._built = True
        return self.roots

    def get_roots(self) -> list[TaskNode]:
        if not self._built:
            self.build()
        return self.roots

    def get_tree_depth(self) -> int:
        if not self._built:
            self.build()
        max_depth = max((node.get_depth() for node in self.graph.all_nodes()), default=0)
        return max_depth

    def get_parent_of(self, task_id: int) -> TaskNode | None:
        if not self._built:
            self.build()
        node = self.graph.get_node(task_id)
        return node.parent if node else None

    def get_children_of(self, task_id: int) -> list[TaskNode]:
        if not self._built:
            self.build()
        node = self.graph.get_node(task_id)
        return node.children if node else []

    def has_cycle(self) -> bool:
        tasks_list = self.graph.to_task_list()
        return has_cycle(tasks_list)
