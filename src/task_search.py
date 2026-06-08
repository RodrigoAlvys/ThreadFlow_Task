TASK_NOT_FOUND = "task não encontrada"


class TaskSearcher:
    def __init__(self, tasks):
        self.tasks = list(tasks)
        self._tasks_by_id = {}

        for task in self.tasks:
            self._tasks_by_id[task["id"]] = task

    def find_by_id(self, task_id):
        return self._tasks_by_id.get(task_id, TASK_NOT_FOUND)

    def find_by_name(self, task_name):
        normalized_name = str(task_name).strip().casefold()

        for task in self.tasks:
            current_name = str(task.get("name", "")).strip().casefold()

            if current_name == normalized_name:
                return task

        return TASK_NOT_FOUND

    def find(self, term):
        if isinstance(term, int):
            return self.find_by_id(term)

        text_term = str(term).strip()

        if text_term.isdigit():
            return self.find_by_id(int(text_term))

        return self.find_by_name(text_term)


def search_task(tasks, term):
    return TaskSearcher(tasks).find(term)
