import unittest

from src.task_search import TASK_NOT_FOUND, TaskSearcher, search_task


class TaskSearchTest(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            {"id": 1, "name": "Ler arquivo", "depends_on": []},
            {"id": 2, "name": "Construir arvore", "depends_on": [1]},
            {"id": 3, "name": "Testar API", "depends_on": [1, 2]},
        ]

    def test_find_existing_task_by_id(self):
        searcher = TaskSearcher(self.tasks)

        task = searcher.find(2)

        self.assertEqual(task["name"], "Construir arvore")

    def test_find_existing_task_by_string_id(self):
        task = search_task(self.tasks, "3")

        self.assertEqual(task["name"], "Testar API")

    def test_find_existing_task_by_name_case_insensitive(self):
        searcher = TaskSearcher(self.tasks)

        task = searcher.find("testar api")

        self.assertEqual(task["id"], 3)

    def test_return_message_when_task_is_not_found(self):
        searcher = TaskSearcher(self.tasks)

        result = searcher.find("task inexistente")

        self.assertEqual(result, TASK_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
