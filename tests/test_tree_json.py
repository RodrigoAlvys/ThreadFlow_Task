import json
import unittest

from src.tree_json import requirements_tree_to_json


class TreeJsonTest(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            {"id": 1, "name": "Ler arquivo", "depends_on": []},
            {"id": 2, "name": "Construir arvore", "depends_on": [1]},
            {"id": 3, "name": "Exportar resultado", "depends_on": [2]},
        ]

    def test_return_valid_json_string(self):
        result = requirements_tree_to_json(self.tasks)
        data = json.loads(result)

        self.assertIsInstance(result, str)
        self.assertIn("ordem_topologica", data)
        self.assertIn("arvore", data)

    def test_success_json_contains_topological_order(self):
        data = json.loads(requirements_tree_to_json(self.tasks))
        order_names = [task["name"] for task in data["ordem_topologica"]]

        self.assertEqual(
            order_names,
            ["Ler arquivo", "Construir arvore", "Exportar resultado"],
        )

    def test_success_json_contains_dependency_tree(self):
        data = json.loads(requirements_tree_to_json(self.tasks))
        root = data["arvore"][0]

        self.assertEqual(root["name"], "Ler arquivo")
        self.assertEqual(root["children"][0]["name"], "Construir arvore")
        self.assertEqual(root["children"][0]["children"][0]["name"], "Exportar resultado")

    def test_deadloop_returns_empty_order_and_error(self):
        tasks = [
            {"id": 1, "name": "Task A", "depends_on": [2]},
            {"id": 2, "name": "Task B", "depends_on": [1]},
        ]

        data = json.loads(requirements_tree_to_json(tasks))

        self.assertEqual(data["ordem_topologica"], [])
        self.assertEqual(data["arvore"], [])
        self.assertEqual(data["erro"], "deadloop detectado")

    def test_keep_special_characters_readable(self):
        tasks = [
            {"id": 1, "name": "Revisão final", "depends_on": []},
        ]

        result = requirements_tree_to_json(tasks)

        self.assertIn("Revisão final", result)


if __name__ == "__main__":
    unittest.main()
