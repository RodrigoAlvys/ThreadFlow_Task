from __future__ import annotations

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from file_reader import load_file
from graph.tree_builder import TreeBuilder
from tree_stats import get_tree_stats
from tree_ascii import print_requirements_tree


class CLIMenu:
    """Menu interativo via linha de comando (RF-05)."""

    def __init__(self):
        self.current_graph = None
        self.current_builder = None
        self.current_file = None
        self.running = True

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("\n" + "="*60)
        print("  THREADFLOW_TASK - Gerenciador de Dependências")
        print("  Organização topológica de tasks")
        print("="*60)

    def print_menu(self):
        print("\n--- MENU PRINCIPAL ---")
        print("1. Carregar arquivo (.txt ou .json)")
        print("2. Exibir árvore de dependências (ASCII)")
        print("3. Exibir ordem topológica")
        print("4. Exibir estatísticas da árvore")
        print("5. Buscar task por ID ou nome")
        print("6. Exportar resultado")
        print("7. Sair")
        print("-"*40)

        if self.current_file:
            print(f"Arquivo carregado: {self.current_file}")
            print(f"Total de tasks: {self.current_graph.total_tasks() if self.current_graph else 0}")
        else:
            print("Nenhum arquivo carregado")
        print("-"*40)

    def check_file_loaded(self) -> bool:
        if self.current_graph is None:
            print("\nERRO: Nenhum arquivo carregado. Carregue um arquivo primeiro (opção 1)")
            return False
        return True

    def load_file_option(self):
        print("\n--- CARREGAR ARQUIVO ---")
        file_path = input("Caminho do arquivo: ").strip()

        if not os.path.exists(file_path):
            print(f"ERRO: Arquivo '{file_path}' não encontrado")
            return

        try:
            graph = load_file(file_path)
            builder = TreeBuilder(graph)
            roots = builder.build()

            self.current_graph = graph
            self.current_builder = builder
            self.current_file = file_path

            print(f"\nSUCESSO: Arquivo '{file_path}' carregado")
            print(f"Total de tasks: {graph.total_tasks()}")
            print(f"Tasks raiz: {len(builder.get_roots())}")

        except ValueError as e:
            print(f"\nERRO: {e}")
        except Exception as e:
            print(f"\nErro inesperado: {e}")

    def display_tree_option(self):
        if not self.check_file_loaded():
            return

        print("\n--- ÁRVORE DE DEPENDÊNCIAS (ASCII) ---")
        tasks_list = self.current_graph.to_task_list()
        print("\n")
        print_requirements_tree(tasks_list)
        print("\n")

    def display_topological_order_option(self):
        if not self.check_file_loaded():
            return

        print("\n--- ORDEM TOPOLÓGICA ---")

        topological_order = self.current_builder.get_topological_order()
        has_cycle = len(topological_order) != self.current_graph.total_tasks()

        if has_cycle:
            print("\nERRO: Deadloop detectado - não é possível gerar ordem topológica")
            try:
                self.current_builder.build()
            except ValueError as e:
                print(f"Detalhe: {e}")
        else:
            print("\nOrdem de execução (da primeira para a última task):")
            print("-" * 40)
            for idx, task in enumerate(topological_order, 1):
                deps = [d.name for d in task.depends_on]
                if deps:
                    print(f"{idx:2d}. [{task.id}] {task.name}")
                    print(f"     Depende de: {', '.join(deps)}")
                else:
                    print(f"{idx:2d}. [{task.id}] {task.name} (sem dependências)")
            print("-" * 40)

    def display_stats_option(self):
        if not self.check_file_loaded():
            return

        print("\n--- ESTATÍSTICAS DA ÁRVORE ---")
        tasks_list = self.current_graph.to_task_list()
        stats = get_tree_stats(tasks_list)

        print(f"\nTotal de tasks: {stats['total_tasks']}")
        print(f"Total de dependências: {stats['total_dependencies']}")
        print(f"Task com mais dependências: {stats['most_dependencies_task']['name']} (ID: {stats['most_dependencies_task']['id']})")
        print(f"Task mais requisitada: {stats['most_requested_task']['name']} (ID: {stats['most_requested_task']['id']})")
        print(f"Profundidade máxima da árvore: {self.current_builder.get_tree_depth()}")
        print(f"Tasks raiz: {len(self.current_builder.get_roots())}")

    def search_task_option(self):
        if not self.check_file_loaded():
            return

        print("\n--- BUSCAR TASK ---")
        term = input("Digite o ID ou nome da task: ").strip()

        if not term:
            print("ERRO: Termo de busca vazio")
            return

        try:
            task_id = int(term)
            task = self.current_graph.get_node(task_id)
        except ValueError:
            task = self.current_graph.get_node_by_name(term)

        if task is None:
            print(f"\nERRO: Task '{term}' não encontrada")
            return

        print(f"\n--- INFORMAÇÕES DA TASK ---")
        print(f"ID: {task.id}")
        print(f"Nome: {task.name}")
        
        if task.depends_on:
            deps = [f"{dep.name} (ID:{dep.id})" for dep in task.depends_on]
            print(f"Depende de: {', '.join(deps)}")
        else:
            print("Depende de: (nenhuma)")
        
        if task.required_by:
            reqs = [f"{req.name} (ID:{req.id})" for req in task.required_by]
            print(f"É requisitada por: {', '.join(reqs)}")
        else:
            print("É requisitada por: (nenhuma)")
        
        if task.parent:
            print(f"Pai na árvore: {task.parent.name} (ID:{task.parent.id})")
        else:
            print("Pai na árvore: (raiz)")
        
        if task.children:
            children_names = [f"{c.name} (ID:{c.id})" for c in task.children]
            print(f"Filhos na árvore: {', '.join(children_names)}")
        else:
            print("Filhos na árvore: (nenhum)")
        
        print(f"Profundidade: {task.get_depth()}")

    def export_option(self):
        if not self.check_file_loaded():
            return

        print("\n--- EXPORTAR RESULTADO ---")
        print("Formatos disponíveis: txt, json")
        output_file = input("Caminho do arquivo de saída (ex: saida.txt ou saida.json): ").strip()

        if not output_file:
            print("ERRO: Caminho do arquivo não informado")
            return

        tasks_list = self.current_graph.to_task_list()
        stats = get_tree_stats(tasks_list)
        topological_order = self.current_builder.get_topological_order()
        has_cycle = len(topological_order) != self.current_graph.total_tasks()

        try:
            if output_file.endswith('.txt'):
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("# THREADFLOW_TASK - RESULTADO\n")
                    f.write(f"# Arquivo original: {self.current_file}\n\n")
                    
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
                    
                    f.write("\n# ESTATISTICAS\n")
                    f.write(f"Total de tasks: {stats['total_tasks']}\n")
                    f.write(f"Total de dependencias: {stats['total_dependencies']}\n")
                    f.write(f"Profundidade maxima: {self.current_builder.get_tree_depth()}\n")
                
                print(f"\nSUCESSO: Exportado para {output_file}")
                
            elif output_file.endswith('.json'):
                export_data = {
                    "arquivo_original": self.current_file,
                    "ordem_topologica": [],
                    "arvore": tasks_list,
                    "estatisticas": {
                        "total_tasks": stats['total_tasks'],
                        "total_dependencies": stats['total_dependencies'],
                        "most_dependencies_task": {
                            "id": stats['most_dependencies_task']['id'],
                            "name": stats['most_dependencies_task']['name']
                        },
                        "most_requested_task": {
                            "id": stats['most_requested_task']['id'],
                            "name": stats['most_requested_task']['name']
                        }
                    },
                    "profundidade_maxima": self.current_builder.get_tree_depth(),
                    "tem_ciclo": has_cycle
                }
                
                if not has_cycle:
                    export_data["ordem_topologica"] = [
                        {"id": task.id, "name": task.name} for task in topological_order
                    ]
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                print(f"\nSUCESSO: Exportado para {output_file}")
            else:
                print("ERRO: Formato não suportado. Use .txt ou .json")
                
        except Exception as e:
            print(f"\nERRO ao exportar: {e}")

    def exit_option(self):
        print("\nEncerrando o programa...")
        self.running = False

    def run(self):
        while self.running:
            self.print_header()
            self.print_menu()

            option = input("\nEscolha uma opção: ").strip()

            if option == "1":
                self.load_file_option()
            elif option == "2":
                self.display_tree_option()
            elif option == "3":
                self.display_topological_order_option()
            elif option == "4":
                self.display_stats_option()
            elif option == "5":
                self.search_task_option()
            elif option == "6":
                self.export_option()
            elif option == "7":
                self.exit_option()
            else:
                print("\nOpção inválida. Escolha um número de 1 a 7")

            if self.running and option not in ["2"]:
                input("\nPressione Enter para continuar...")
                self.clear_screen()


def main():
    menu = CLIMenu()
    menu.run()


if __name__ == "__main__":
    main()
