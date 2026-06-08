import unittest

from src.task_info import format_task_info, get_task_info
from src.task_search import TASK_NOT_FOUND


class TaskInfoTest(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            {"id": 1, "name": "Ler arquivo", "depends_on": []},
            {"id": 2, "name": "Construir arvore", "depends_on": [1]},
            {"id": 3, "name": "Testar API", "depends_on": [1, 2]},
        ]

    def test_get_task_info_returns_dependencies(self):
        info = get_task_info(self.tasks, 2)

        self.assertEqual(info["depends_on"][0]["name"], "Ler arquivo")

    def test_get_task_info_returns_dependents(self):
        info = get_task_info(self.tasks, "Construir arvore")

        self.assertEqual(info["required_by"][0]["name"], "Testar API")

    def test_format_task_info_shows_dependency_list(self):
        text = format_task_info(self.tasks, 2)

        self.assertIn("depende de: [Ler arquivo]", text)

    def test_format_task_info_shows_dependents_list(self):
        text = format_task_info(self.tasks, 2)

        self.assertIn("é requisitada por: [Testar API]", text)

    def test_return_error_when_task_does_not_exist(self):
        text = format_task_info(self.tasks, "Sem task")

        self.assertEqual(text, TASK_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
