from __future__ import annotations

import sys
from file_reader import load_file
from cycle_detector import has_cycle
from tree_stats import get_tree_stats


def main():
    input_file = None
    output_file = None

    for argument in sys.argv[1:]:
        if argument.startswith("--if="):
            input_file = argument[5:]
        elif argument.startswith("--of="):
            output_file = argument[5:]

    if input_file is None:
        print("Erro: arquivo de entrada não informado.")
        return

    graph = load_file(input_file)

    # Converte para lista de dicionários para compatibilidade com código existente
    tasks_list = graph.to_task_list()

    if has_cycle(tasks_list):
        print("Erro: dependência circular detectada.")
        return

    stats = get_tree_stats(tasks_list)

    print("Número de tasks:", stats["total_tasks"])
    print("Número de dependências:", stats["total_dependencies"])
    print("Task com mais dependências:", stats["most_dependencies_task"]["name"])
    print("Task mais requisitada:", stats["most_requested_task"]["name"])

    if output_file is not None:
        print(f"Exportação para '{output_file}' ainda não implementada.")


if __name__ == "__main__":
    main()
