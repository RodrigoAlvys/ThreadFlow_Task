from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from file_reader import load_file
from graph.tree_builder import TreeBuilder
from tree_stats import get_tree_stats
from tree_ascii import print_requirements_tree


def main():
    input_file = None
    output_file = None

    for argument in sys.argv[1:]:
        if argument.startswith("--if="):
            input_file = argument[5:]
        elif argument.startswith("--of="):
            output_file = argument[5:]

    if input_file is None:
        print("Uso: threadflow --if=<arquivo_entrada> --of=<arquivo_saida>")
        print("Exemplo: threadflow --if=tasks.txt --of=saida.json")
        print("\nFormatos suportados: .txt e .json")
        return 1

    if not os.path.exists(input_file):
        print(f"ERRO: Arquivo '{input_file}' nao encontrado")
        return 1

    try:
        graph = load_file(input_file)
        builder = TreeBuilder(graph)
        roots = builder.build()

        tasks_list = graph.to_task_list()
        stats = get_tree_stats(tasks_list)

        print("\n" + "="*50)
        print("RF-03: ARVORE DE REQUISITOS")
        print("="*50)
        print(f"Numero de tasks: {stats['total_tasks']}")
        print(f"Numero de dependencias: {stats['total_dependencies']}")
        print(f"Task com mais dependencias: {stats['most_dependencies_task']['name']}")
        print(f"Task mais requisitada: {stats['most_requested_task']['name']}")
        print(f"Profundidade maxima da arvore: {builder.get_tree_depth()}")

        print("\n" + "="*50)
        print("VISUALIZACAO ASCII (RF-07)")
        print("="*50)
        print_requirements_tree(tasks_list)

        if output_file:
            print(f"\nExportando para '{output_file}'...")
            if output_file.endswith('.txt'):
                with open(output_file, 'w', encoding='utf-8') as f:
                    for task in tasks_list:
                        f.write(f"{task['id']};{task['name']};{','.join(map(str, task['depends_on']))}\n")
                print(f"Exportado para {output_file}")
            elif output_file.endswith('.json'):
                import json
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({"tasks": tasks_list}, f, indent=2, ensure_ascii=False)
                print(f"Exportado para {output_file}")
            else:
                print(f"Formato nao suportado: {output_file}")

        print("\n" + "="*50)
        print("Arvore construida com sucesso")
        print("="*50)

    except ValueError as e:
        print(f"\nERRO: {e}")
        return 1
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
