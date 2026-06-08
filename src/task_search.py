from __future__ import annotations

TASK_NOT_FOUND = "task não encontrada"


class TaskSearcher:
    """Buscador de tasks por ID ou nome (RF-10)."""

    def __init__(self, tasks):
        self.tasks = list(tasks)
        self._tasks_by_id = {}
        self._tasks_by_name = {}

        for task in self.tasks:
            self._tasks_by_id[task["id"]] = task
            # Indexa por nome (case-insensitive)
            name_lower = task.get("name", "").strip().lower()
            if name_lower:
                self._tasks_by_name[name_lower] = task

    def find_by_id(self, task_id: int):
        """Busca task por ID. Complexidade O(1)."""
        return self._tasks_by_id.get(task_id, TASK_NOT_FOUND)

    def find_by_name(self, task_name: str):
        """Busca task por nome (case-insensitive). Complexidade O(1) com dicionário."""
        normalized_name = str(task_name).strip().lower()
        return self._tasks_by_name.get(normalized_name, TASK_NOT_FOUND)

    def find(self, term):
        """
        Busca task por ID ou nome.
        Se term for número, busca por ID.
        Se term for texto, busca por nome (case-insensitive).
        """
        if isinstance(term, int):
            return self.find_by_id(term)

        text_term = str(term).strip()

        # Tenta interpretar como número
        if text_term.isdigit():
            return self.find_by_id(int(text_term))

        # Busca por nome
        return self.find_by_name(text_term)


def search_task(tasks, term):
    """Função auxiliar para buscar task."""
    return TaskSearcher(tasks).find(term)
