import unittest
from contextlib import redirect_stdout
from io import StringIO

from src.tree_ascii import print_requirements_tree, requirements_tree_to_ascii


class TreeAsciiTest(unittest.TestCase):
    def test_return_ascii_tree_with_dependency_hierarchy(self):
        tasks = [
            {"id": 1, "name": "Ler arquivo", "depends_on": []},
            {"id": 2, "name": "Construir arvore", "depends_on": [1]},
            {"id": 3, "name": "Exportar resultado", "depends_on": [2]},
        ]

        result = requirements_tree_to_ascii(tasks)

        self.assertEqual(
            result,
            "\n".join(
                [
                    "`-- [1] Ler arquivo",
                    "    `-- [2] Construir arvore",
                    "        `-- [3] Exportar resultado",
                ]
            ),
        )

    def test_return_ascii_tree_with_more_than_one_root(self):
        tasks = [
            {"id": 1, "name": "Ler txt", "depends_on": []},
            {"id": 2, "name": "Ler json", "depends_on": []},
            {"id": 3, "name": "Montar arvore", "depends_on": [1, 2]},
        ]

        result = requirements_tree_to_ascii(tasks)

        self.assertIn("|-- [1] Ler txt", result)
        self.assertIn("`-- [2] Ler json", result)
        self.assertIn("`-- [3] Montar arvore", result)

    def test_truncate_long_task_name(self):
        tasks = [
            {
                "id": 1,
                "name": "Nome de task muito grande para caber no terminal",
                "depends_on": [],
            },
        ]

        result = requirements_tree_to_ascii(tasks, max_name_length=12)

        self.assertEqual(result, "`-- [1] Nome de t...")

    def test_show_error_when_tree_has_deadloop(self):
        tasks = [
            {"id": 1, "name": "Task A", "depends_on": [2]},
            {"id": 2, "name": "Task B", "depends_on": [1]},
        ]

        result = requirements_tree_to_ascii(tasks)

        self.assertEqual(result, "erro: deadloop detectado")

    def test_print_requirements_tree_returns_printed_text(self):
        tasks = [
            {"id": 1, "name": "Ler arquivo", "depends_on": []},
        ]
        output = StringIO()

        with redirect_stdout(output):
            result = print_requirements_tree(tasks)

        self.assertEqual(result, "`-- [1] Ler arquivo")
        self.assertEqual(output.getvalue(), "`-- [1] Ler arquivo\n")


if __name__ == "__main__":
    unittest.main()
