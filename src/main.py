from __future__ import annotations

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))


def run_cli_mode():
    from cli.menu import main as menu_main
    menu_main()


def run_file_mode(input_file: str, output_file: str = None):
    from file_reader import load_file
    from graph.tree_builder import TreeBuilder
    from tree_stats import get_tree_stats
    from tree_ascii import print_requirements_tree

    if not os.path.exists(input_file):
        print(f"ERRO: Arquivo '{input_file}' nao encontrado")
        return 1

    try:
        graph = load_file(input_file)
        builder = TreeBuilder(graph)
        roots = builder.build()

        tasks_list = graph.to_task_list()
        stats = get_tree_stats(tasks_list)

        topological_order = builder.get_topological_order()
        has_cycle = len(topological_order) != graph.total_tasks()

        print("\n" + "="*50)
        print("RF-03: ARVORE DE REQUISITOS")
        print("="*50)
        print(f"Numero de tasks: {stats['total_tasks']}")
        print(f"Numero de dependencias: {stats['total_dependencies']}")
        print(f"Task com mais dependencias: {stats['most_dependencies_task']['name']}")
        print(f"Task mais requisitada: {stats['most_requested_task']['name']}")
        print(f"Profundidade maxima da arvore: {builder.get_tree_depth()}")

        print("\n" + "="*50)
        print("RF-12: ORDEM TOPOLOGICA")
        print("="*50)
        if has_cycle:
            print("ERRO: Deadloop detectado - nao e possivel gerar ordem topologica")
        else:
            print("Ordem de execucao (da primeira para a ultima task):")
            for idx, task in enumerate(topological_order, 1):
                print(f"  {idx}. [{task.id}] {task.name}")

        print("\n" + "="*50)
        print("RF-07: VISUALIZACAO ASCII")
        print("="*50)
        print_requirements_tree(tasks_list)

        if output_file:
            print(f"\nExportando para '{output_file}'...")
            
            if output_file.endswith('.txt'):
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("# ORDEM TOPOLOGICA\n")
                    if has_cycle:
                        f.write("ERRO: Deadloop detectado\n")
                    else:
                        for task in topological_order:
                            f.write(f"{task.id};{task.name}\n")
                    
                    f.write("\n# ESTRUTURA COMPLETA\n")
                    for task in tasks_list:
                        deps = ','.join(map(str, task['depends_on'])) if task['depends_on'] else ''
                        f.write(f"{task['id']};{task['name']};{deps}\n")
                print(f"Exportado para {output_file}")
                
            elif output_file.endswith('.json'):
                export_data = {
                    "ordem_topologica": [],
                    "arvore": tasks_list,
                    "estatisticas": stats,
                    "profundidade_maxima": builder.get_tree_depth(),
                    "tem_ciclo": has_cycle
                }
                
                if not has_cycle:
                    export_data["ordem_topologica"] = [
                        {"id": task.id, "name": task.name} for task in topological_order
                    ]
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                print(f"Exportado para {output_file}")
            else:
                print(f"Formato nao suportado: {output_file}")

        print("\n" + "="*50)
        if has_cycle:
            print("ERRO: Deadloop detectado na estrutura")
        else:
            print("Arvore construida com sucesso")
        print("="*50)

    except ValueError as e:
        print(f"\nERRO: {e}")
        return 1
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        return 1

    return 0


def main():
    input_file = None
    output_file = None

    for argument in sys.argv[1:]:
        if argument.startswith("--if="):
            input_file = argument[5:]
        elif argument.startswith("--of="):
            output_file = argument[5:]

    if input_file is None and len(sys.argv) == 1:
        run_cli_mode()
        return 0

    if input_file:
        return run_file_mode(input_file, output_file)

    print("Uso: threadflow --if=<arquivo_entrada> --of=<arquivo_saida>")
    print("Ou: threadflow (sem argumentos para modo interativo)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
